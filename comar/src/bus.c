/*
 *
 * Copyright (c) 2005-2010, TUBITAK/UEKAE
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 *
 */

#include "config.h"
#include "log.h"
#include "process.h"
#include "pydbus.h"
#include "script.h"
#include "utils.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/poll.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <dirent.h>



//! DBus connection
DBusConnection *bus_conn;

//! Sends a DBus message
void
bus_send(DBusMessage *bus_msg)
{
    /*!
     * Sends a DBus message and flushes connection.
     *
     * @bus_msg DBus message
     *
     */

    dbus_uint32_t serial = 0;

    dbus_connection_send(bus_conn, bus_msg, &serial);
    dbus_connection_flush(bus_conn);
}

//! Replies to a DBus message with an error message
void
bus_reply_error(DBusMessage *bus_msg, const char *name, const char *msg)
{
    // DBus error = interface + name
    int size = strlen(config_interface) + 1 + strlen(name) + 1;
    char *exception = malloc(size);
    snprintf(exception, size, "%s.%s", config_interface, name);
    exception[size - 1] = '\0';

    DBusMessage *error = dbus_message_new_error(bus_msg, exception, msg);
    free(exception);
    bus_send(error);
    dbus_message_unref(error);
}

//! Replies to a DBus message with a Python object
void
bus_reply_object(DBusMessage *bus_msg, PyObject *py_obj, char *signature)
{
    DBusMessage *reply;
    DBusMessageIter iter;
    char *eStr, *vStr;

    reply = dbus_message_new_method_return(bus_msg);
    dbus_message_iter_init_append(reply, &iter);

    // If signature is not null, append Python object to message
    if (strcmp(signature, "") != 0) {
        PyObject *py_tuple;
        if (!PyTuple_Check(py_obj)) {
            py_tuple = PyTuple_New(1);
            PyTuple_SetItem(py_tuple, 0, py_obj);
        }
        else {
            py_tuple = py_obj;
        }
        if (pydbus_export(&iter, py_tuple, signature) != 0) {
            py_catch(&eStr, &vStr, 1);
            bus_reply_error(bus_msg, eStr, vStr);
            return;
        }
    }

    bus_send(reply);
    dbus_message_unref(reply);
}

//! Replies to a DBus message with a "UnknownMethod" error
void
bus_reply_unknown_method(DBusMessage *bus_msg)
{
    DBusMessage *error = dbus_message_new_error_printf(bus_msg, "org.freedesktop.DBus.Error.UnknownMethod",
                                                                "Method \"%s\" with signature \"%s\" on interface \"%s\" doesn't exist",
                                                                dbus_message_get_member(bus_msg),
                                                                dbus_message_get_signature(bus_msg),
                                                                dbus_message_get_interface(bus_msg));
    bus_send(error);
    dbus_message_unref(error);
}

//! Emits a DBus signal with a Python object
int
bus_signal(const char *path, const char *interface, const char *member, PyObject *obj, char *signature)
{
    DBusMessage *msg;
    DBusMessageIter iter;

    msg = dbus_message_new_signal(path, interface, member);
    dbus_message_iter_init_append(msg, &iter);

    // If signature is not null, append Python object to message
    if (obj && obj != Py_None && strcmp(signature, "") != 0) {
        PyObject *py_tuple;
        if (!PyTuple_Check(obj)) {
            py_tuple = PyTuple_New(1);
            PyTuple_SetItem(py_tuple, 0, obj);
        }
        else {
            py_tuple = obj;
        }
        if (pydbus_export(&iter, py_tuple, signature) != 0) {
            return -1;
        }
    }

    bus_send(msg);

    return 0;
}

//! Calls a method and returns reply.
PyObject *
bus_execute(DBusConnection *conn, const char *path, const char *interface, const char *member, PyObject *obj, int timeout, char *signature)
{
    DBusMessage *msg, *reply;
    DBusMessageIter iter;
    DBusError err;

    msg = dbus_message_new_method_call(config_service_name, path, interface, member);
    dbus_message_iter_init_append(msg, &iter);

    // If signature is not null, append Python object to message
    if (strcmp(signature, "") != 0) {
        PyObject *py_tuple;
        if (!PyTuple_Check(obj)) {
            py_tuple = PyTuple_New(1);
            PyTuple_SetItem(py_tuple, 0, obj);
        }
        else {
            py_tuple = obj;
        }
        if (pydbus_export(&iter, py_tuple, signature) != 0) {
            return NULL;
        }
    }

    // -1 means "use DBus default timeout
    // Else, multiply it with 1000, because DBus wants time in microseconds.
    if (timeout != -1) {
        timeout *= 1000;
    }

    dbus_error_init(&err);
    reply = dbus_connection_send_with_reply_and_block(conn, msg, timeout, &err);
    dbus_message_unref(msg);

    // Unable to call method, raise an exception
    if (dbus_error_is_set(&err)) {
        PyErr_Format(PyExc_DBus, "Unable to call method: %s", err.message);
        dbus_error_free(&err);
        return NULL;
    }

    PyObject *ret;

    switch (dbus_message_get_type(reply)) {
        case DBUS_MESSAGE_TYPE_METHOD_RETURN:
            // Method returned a reply
            ret = pydbus_import(reply);
            if (ret && PyTuple_Size(ret) == 1) {
                ret = PyTuple_GetItem(ret, 0);
            }
            dbus_message_unref(reply);
            return ret;
        case DBUS_MESSAGE_TYPE_ERROR:
            // Method retuned an error, raise an exception
            PyErr_SetString(PyExc_DBus, dbus_message_get_error_name(reply));
            dbus_message_unref(reply);
            return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

//! Calls a method and returns reply.
PyObject *
bus_execute2(DBusConnection *conn, const char *destination, const char *path, const char *interface, const char *member, PyObject *obj, int timeout, char *signature)
{
    DBusMessage *msg, *reply;
    DBusMessageIter iter;
    DBusError err;

    msg = dbus_message_new_method_call(destination, path, interface, member);
    dbus_message_iter_init_append(msg, &iter);

    // If signature is not null, append Python object to message
    if (strcmp(signature, "") != 0) {
        PyObject *py_tuple;
        if (!PyTuple_Check(obj)) {
            py_tuple = PyTuple_New(1);
            PyTuple_SetItem(py_tuple, 0, obj);
        }
        else {
            py_tuple = obj;
        }
        if (pydbus_export(&iter, py_tuple, signature) != 0) {
            return NULL;
        }
    }

    // -1 means "use DBus default timeout
    // Else, multiply it with 1000, because DBus wants time in microseconds.
    if (timeout != -1) {
        timeout *= 1000;
    }

    dbus_error_init(&err);
    reply = dbus_connection_send_with_reply_and_block(conn, msg, timeout, &err);
    dbus_message_unref(msg);

    // Unable to call method, raise an exception
    if (dbus_error_is_set(&err)) {
        PyErr_Format(PyExc_DBus, "Unable to call method: %s", err.message);
        dbus_error_free(&err);
        return NULL;
    }

    PyObject *ret;

    switch (dbus_message_get_type(reply)) {
        case DBUS_MESSAGE_TYPE_METHOD_RETURN:
            // Method returned a reply
            ret = pydbus_import(reply);
            if (ret && PyTuple_Size(ret) == 1) {
                ret = PyTuple_GetItem(ret, 0);
            }
            dbus_message_unref(reply);
            return ret;
        case DBUS_MESSAGE_TYPE_ERROR:
            // Method retuned an error, raise an exception
            PyErr_SetString(PyExc_DBus, dbus_message_get_error_name(reply));
            dbus_message_unref(reply);
            return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

//! Opens a connection, sets locale and calls interface.member()
PyObject *
bus_call(const char *path, const char *interface, const char *member, PyObject *obj, int timeout, const char *lang, char *signature)
{
    DBusConnection *conn;
    DBusError err;

    // Open a new connection
    dbus_error_init(&err);
    conn = dbus_bus_get_private(DBUS_BUS_SYSTEM, &err);
    if (dbus_error_is_set(&err)) {
        PyErr_SetString(PyExc_DBus, "Unable to open bus connection for call() method.");
        dbus_error_free(&err);
        return NULL;
    }

    // setLocale first
    PyObject *args = PyTuple_New(1);
    PyTuple_SetItem(args, 0, PyString_FromString(lang));

    PyObject *ret = bus_execute(conn, "/", config_interface, "setLocale", args, 25, "s");
    if (!ret) {
        dbus_connection_close(conn);
        dbus_connection_unref(conn);
        return ret;
    }

    // Execute method
    ret = bus_execute(conn, path, interface, member, obj, timeout, signature);

    dbus_connection_close(conn);
    dbus_connection_unref(conn);

    return ret;
}
