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


#ifndef BUS_H
#define BUS_H

#include <Python.h>
#include <dbus/dbus.h>

extern DBusConnection *bus_conn;

void bus_send(DBusMessage *bus_msg);
void bus_reply_error(DBusMessage *bus_msg, const char *name, const char *msg);
void bus_reply_object(DBusMessage *bus_msg, PyObject *py_obj, char *signature);
void bus_reply_unknown_method(DBusMessage *bus_msg);
int bus_signal(const char *path, const char *interface, const char *member, PyObject *obj, char *signature);
PyObject *bus_call(const char *path, const char *interface, const char *member, PyObject *obj, int timeout, const char *lang, char *signature);
PyObject * bus_execute(DBusConnection *conn, const char *path, const char *interface, const char *member, PyObject *obj, int timeout, char *signature);
PyObject *bus_execute2(DBusConnection *conn, const char *destination, const char *path, const char *interface, const char *member, PyObject *obj, int timeout, char *signature);

#endif /* BUS_H */
