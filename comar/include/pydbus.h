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

#ifndef PYDBUS_H
#define PYDBUS_H

#define TYPES_BASIC "sbixd"
#define TYPES_CONTAINER "arD"

#include <Python.h>
#include <dbus/dbus.h>

char *get_obj_sign(PyObject *obj);

int pydbus_export_item(DBusMessageIter *iter, PyObject *obj, char *signature);
int pydbus_export(DBusMessageIter *iter, PyObject *obj, char *signature);

PyObject *py_get_item(DBusMessageIter* iter);
PyObject *py_get_dict(DBusMessageIter *iter);
PyObject *py_get_tuple(DBusMessageIter *iter);
PyObject *py_get_list(DBusMessageIter *iter);
PyObject *pydbus_import(DBusMessage *msg);

#endif /* PYDBUS_H */
