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

#include "pydbus.h"
#include "utils.h"
#include "script.h"

//! Returns DBus object type of a Python object
char *
get_obj_sign(PyObject *obj)
{
    /*!
     * Returns DBus object type of a Python object.
     *
     * @obj Python object
     * @return DBus object type, "?" if unknown
     *
     */

    if (PyString_Check(obj) || PyUnicode_Check(obj)) {
        return "s";
    }
    else if (PyBool_Check(obj)) {
        return "b";
    }
    else if (PyInt_Check(obj)) {
        return "i";
    }
    else if (PyLong_Check(obj)) {
        return "x";
    }
    else if (PyFloat_Check(obj)) {
        return "d";
    }
    else if (PyList_Check(obj)) {
        return "a";
    }
    else if (PyTuple_Check(obj)) {
        return "r";
    }
    else if (PyDict_Check(obj)) {
        return "D";
    }
    else if (obj == Py_None) {
        return "N";
    }
    return "?";
}

//! Appends a Python tuple to a DBus message iterator
int
pydbus_export(DBusMessageIter *iter, PyObject *obj, char *signature)
{
    /*!
     * Appends a Python tuple to a DBus message iterator.
     *
     * @iter DBus message iterator
     * @obj Python tuple
     * @signature Object signature
     * @return 0 on success, -1 on error (also raises an exception)
     *
     */

    if (!PyTuple_Check(obj)) {
        PyErr_SetString(PyExc_COMAR_Internal, "DBus export method accepts Python tuple only.");
        return -1;
    }

    // Check signature and tuple size
    PyObject *py_list = script_signature_each(signature);
    if (py_list == NULL) {
        PyErr_SetString(PyExc_COMAR_Invalid, "Method signature is invalid.");
        return -1;
    }
    else if (PyList_Size(py_list) != PyTuple_Size(obj)) {
        PyErr_SetString(PyExc_COMAR_Invalid, "Method signature does not match with object.");
        return -1;
    }

    // Append tuple's items to DBus message
    int i;
    for (i = 0; i < PyTuple_Size(obj); i++) {
        PyObject *py_sign = PyList_GetItem(py_list, i);
        PyObject *py_item = PyTuple_GetItem(obj, i);
        if (pydbus_export_item(iter, py_item, PyString_AsString(py_sign)) != 0) {
            return -1;
        }
    }

    return 0;
}

//! Appends a Python object to a DBus message iterator
int
pydbus_export_item(DBusMessageIter *iter, PyObject *obj, char *signature)
{
    /*!
     * Appends a Python object to a DBus message iterator
     *
     * @iter DBus message iterator
     * @obj Python object
     * @signature Object signature
     * @return 0 on success, -1 on error (also raises an exception)
     *
     */

    DBusMessageIter sub, sub_dict;
    char *sign_content = NULL;
    char *sign_subcontent = NULL;
    char *sign_key = NULL;
    char *sign_value = NULL;
    PyObject *item = NULL;
    PyObject *key = NULL;
    PyObject *value = NULL;

    int e = 0;
    int i = 0;
    Py_ssize_t pos = 0;

    union {
        const char *s;
        dbus_bool_t b;
        dbus_int16_t i16;
        dbus_uint16_t u16;
        dbus_int32_t i32;
        dbus_uint32_t u32;
        dbus_int64_t i64;
        double d;
    } p;

    switch (signature[0]) {
        case 'a':
            // A list or dictionary object found

            // Find signature of content
            sign_subcontent = strsub(signature, 1, strlen(signature));
            if (!sign_subcontent) {
                e = 0;
                break;
            }

            // Open a container
            e = dbus_message_iter_open_container(iter, DBUS_TYPE_ARRAY, sign_subcontent, &sub);
            if (!e) break;

            // Oh, this is not a list, a dictionary instead.
            // a{??} means dictionary, not list of dictionaries
            if (sign_subcontent[0] == '{') {
                // Get key and value signatures
                sign_key = strsub(signature, 2, 3);
                sign_value = strsub(signature, 3, strlen(signature) - 1);
                pos = 0; // Go to first index
                while (PyDict_Next(obj, &pos, &key, &value)) {
                    e = dbus_message_iter_open_container(&sub, DBUS_TYPE_DICT_ENTRY, NULL, &sub_dict);
                    if (pydbus_export_item(&sub_dict, key, sign_key) != 0 || pydbus_export_item(&sub_dict, value, sign_value) != 0) {
                        return -1;
                    }
                    dbus_message_iter_close_container(&sub, &sub_dict);
                }
            }
            else {
                // This is a list. Append items to message
                for (i = 0; i < PyList_Size(obj); i++) {
                    item = PyList_GetItem(obj, i);
                    if (pydbus_export_item(&sub, item, sign_subcontent) != 0) {
                        return -1;
                    }
                }
            }
            dbus_message_iter_close_container(iter, &sub);
            free(sign_subcontent);
            break;
        case '(':
            // A tuple found

            // Find signature of content
            sign_content = strsub(signature, 1, strlen(signature) - 1);
            if (!sign_content) {
                e = 0;
                break;
            }

            // Open a container
            e = dbus_message_iter_open_container(iter, DBUS_TYPE_STRUCT, NULL, &sub);
            if (!e) break;

            // Append items to message
            if (pydbus_export(&sub, obj, sign_content) != 0) {
                free(sign_content);
                return -1;
            }
            free(sign_content);
            dbus_message_iter_close_container(iter, &sub);
            break;
        case 'b':
            if (PyBool_Check(obj)) {
                p.b = (obj == Py_True) ? 1 :0;
            }
            else {
                // TODO: Raise error
                p.b = 0;
            }
            e = dbus_message_iter_append_basic(iter, DBUS_TYPE_BOOLEAN, &p.b);
            break;
        case 'n':
            if (PyInt_Check(obj)) {
                p.i16 = (short) PyInt_AsLong(obj);
            }
            else {
                // TODO: Raise error
                p.i16 = (short) 0;
            }
            e = dbus_message_iter_append_basic(iter, DBUS_TYPE_INT16, &p.i16);
            break;
        case 'q':
            if (PyInt_Check(obj)) {
                p.u16 = (unsigned short) PyInt_AsLong(obj);
            }
            else {
                // TODO: Raise error
                p.u16 = (unsigned short) 0;
            }
            e = dbus_message_iter_append_basic(iter, DBUS_TYPE_UINT16, &p.u16);
            break;
        case 'i':
            if (PyInt_Check(obj)) {
                p.i32 = (int) PyInt_AsLong(obj);
            }
            else {
                // TODO: Raise error
                p.i32 = 0;
            }
            e = dbus_message_iter_append_basic(iter, DBUS_TYPE_INT32, &p.i32);
            break;
        case 'u':
            if (PyInt_Check(obj)) {
                p.u32 = (long) PyInt_AsLong(obj);
            }
            else {
                // TODO: Raise error
                p.u32 = 0;
            }
            e = dbus_message_iter_append_basic(iter, DBUS_TYPE_UINT32, &p.u32);
            break;
        case 'x':
            if (PyLong_Check(obj)) {
                p.i64 = (long) PyLong_AsLong(obj);
            }
            else {
                // TODO: Raise error
                p.i64 = 0;
            }
            e = dbus_message_iter_append_basic(iter, DBUS_TYPE_INT64, &p.i64);
            break;
        case 't':
            // TODO: Long long support
            break;
        case 'd':
            if (PyFloat_Check(obj)) {
                p.d = PyFloat_AsDouble(obj);
            }
            else {
                // TODO: Raise error
                p.d = 0.0;
            }
            e = dbus_message_iter_append_basic(iter, DBUS_TYPE_DOUBLE, &p.d);
            break;
        case 's':
            if (PyString_Check(obj)) {
                p.s = PyString_AsString(obj);
            }
            else {
                // TODO: Raise error
                p.s = "";
            }
            e = dbus_message_iter_append_basic(iter, DBUS_TYPE_STRING, &p.s);
            break;
        case 'o':
            // TODO: Object path
            break;
        case 'g':
            // TODO: Type signature
            break;
        case 'v':
            sign_content = get_obj_sign(obj);
            if (strstr(TYPES_BASIC, sign_content) == NULL) {
                PyErr_SetString(PyExc_COMAR_Invalid, "Aboo Variant content must be single typed.");
                return -1;
            }
            e = dbus_message_iter_open_container(iter, DBUS_TYPE_VARIANT, sign_content, &sub);
            if (pydbus_export_item(&sub, obj, sign_content) != 0) {
                return -1;
            }
            dbus_message_iter_close_container(iter, &sub);
            break;
        case 'N':
            // TODO: Remove
            p.s = "";
            e = dbus_message_iter_append_basic(iter, DBUS_TYPE_STRING, &p.s);
            break;
    }

    if (!e) {
        // Out of memory, panic!
        oom();
    }

    return 0;
}

// IMPORT

PyObject *
py_get_item(DBusMessageIter* iter)
{
    /*!
     * Extracts Python object from a D-Bus message iterator.
     *
     * @iter D-Bus iterator
     * @return Python object
     *
     */

    union {
        const char *s;
        unsigned char y;
        dbus_bool_t b;
        double d;
        dbus_uint16_t u16;
        dbus_int16_t i16;
        dbus_uint32_t u32;
        dbus_int32_t i32;
        dbus_uint64_t u64;
        dbus_int64_t i64;
    } obj;

    PyObject *ret = NULL;
    DBusMessageIter sub;
    int type = 0;

    type = dbus_message_iter_get_arg_type(iter);

    switch (type) {
        case DBUS_TYPE_BYTE:
            dbus_message_iter_get_basic(iter, &obj.y);
            ret = Py_BuildValue("i", (int)obj.y);
            break;
        case DBUS_TYPE_STRING:
        case DBUS_TYPE_OBJECT_PATH:
        case DBUS_TYPE_SIGNATURE:
            dbus_message_iter_get_basic(iter, &obj.s);
            ret = Py_BuildValue("s", obj.s);
            // ret = Py_BuildValue("N", PyUnicode_DecodeUTF8(obj.s, strlen(obj.s), NULL));
            break;
        case DBUS_TYPE_DOUBLE:
            dbus_message_iter_get_basic(iter, &obj.d);
            ret = Py_BuildValue("f", obj.d);
            break;
        case DBUS_TYPE_INT16:
            dbus_message_iter_get_basic(iter, &obj.i16);
            ret = Py_BuildValue("i", (int)obj.i16);
            break;
        case DBUS_TYPE_UINT16:
            dbus_message_iter_get_basic(iter, &obj.u16);
            ret = Py_BuildValue("i", (int)obj.u16);
            break;
        case DBUS_TYPE_INT32:
            dbus_message_iter_get_basic(iter, &obj.i32);
            ret = Py_BuildValue("l", (long)obj.i32);
            break;
        case DBUS_TYPE_UINT32:
            dbus_message_iter_get_basic(iter, &obj.u32);
            ret = Py_BuildValue("k", (unsigned long)obj.u32);
            break;
        case DBUS_TYPE_INT64:
            dbus_message_iter_get_basic(iter, &obj.i64);
            ret = Py_BuildValue("L", (PY_LONG_LONG)obj.i64);
            break;
        case DBUS_TYPE_UINT64:
            dbus_message_iter_get_basic(iter, &obj.u64);
            ret = Py_BuildValue("K", (PY_LONG_LONG)obj.u64);
            break;
        case DBUS_TYPE_BOOLEAN:
            dbus_message_iter_get_basic(iter, &obj.b);
            ret = (long)obj.b == 1 ? PyBool_FromLong(1) : PyBool_FromLong(0);
            break;
        case DBUS_TYPE_DICT_ENTRY:
            break;
        case DBUS_TYPE_ARRAY:
            type = dbus_message_iter_get_element_type(iter);
            if (type == DBUS_TYPE_DICT_ENTRY) {
                dbus_message_iter_recurse(iter, &sub);
                ret = py_get_dict(&sub);
            }
            else {
                dbus_message_iter_recurse(iter, &sub);
                ret = py_get_list(&sub);
            }
            break;
        case DBUS_TYPE_STRUCT:
            dbus_message_iter_recurse(iter, &sub);
            ret = PyList_AsTuple(py_get_list(&sub));
            break;
        case DBUS_TYPE_VARIANT:
            dbus_message_iter_recurse(iter, &sub);
            type = dbus_message_iter_get_arg_type(&sub);
            ret = py_get_item(&sub);
            break;
    }
    return ret;
}

PyObject *
py_get_dict(DBusMessageIter *iter)
{
    /*!
     * Extracts Python dict object from a D-Bus message iterator.
     *
     * @iter D-Bus iterator
     * @return Python object
     *
     */

    PyObject *dict = NULL;
    PyObject *key = NULL;
    PyObject *value = NULL;

    dict = PyDict_New();

    while (dbus_message_iter_get_arg_type(iter) == DBUS_TYPE_DICT_ENTRY) {
        DBusMessageIter kv;

        dbus_message_iter_recurse(iter, &kv);

        key = py_get_item(&kv);
        if (!key) {
            Py_DECREF(dict);
            return NULL;
        }
        dbus_message_iter_next(&kv);

        value = py_get_item(&kv);
        if (!value) {
            Py_DECREF(dict);
            Py_DECREF(key);
            return NULL;
        }

        PyDict_SetItem(dict, key, value);
        Py_DECREF(key);
        Py_DECREF(value);

        dbus_message_iter_next(iter);
    }
    return dict;
}

PyObject *
py_get_tuple(DBusMessageIter *iter)
{
    /*!
     * Extracts Python tuple object from a D-Bus message iterator.
     *
     * @iter D-Bus iterator
     * @return Python object
     *
     */

    int type = 0;
    PyObject *list = NULL;

    list = PyList_New(0);

    while ((type = dbus_message_iter_get_arg_type(iter)) != DBUS_TYPE_INVALID) {
        PyList_Append(list, py_get_item(iter));
        dbus_message_iter_next(iter);
    }
    return PyList_AsTuple(list);
}

PyObject *
py_get_list(DBusMessageIter *iter)
{
    /*!
     * Extracts Python list object from a D-Bus message iterator.
     *
     * @iter D-Bus iterator
     * @return Python object
     *
     */

    int type = 0;
    PyObject *list = NULL;

    list = PyList_New(0);

    while ((type = dbus_message_iter_get_arg_type(iter)) != DBUS_TYPE_INVALID) {
        PyList_Append(list, py_get_item(iter));
        dbus_message_iter_next(iter);
    }
    return list;
}

PyObject *
pydbus_import(DBusMessage *msg)
{
    /*!
     * Extracts Python object from D-Bus message.
     *
     * @msg D-Bus message
     * @return Python object
     *
     */

    DBusMessageIter iter;
    dbus_message_iter_init(msg, &iter);
    return py_get_tuple(&iter);
}
