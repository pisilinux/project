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

#include "log.h"
#include "bus.h"
#include "script.h"
#include "policy.h"

//! Check if sender is allowed to call method
int
policy_check(const char *sender, const char *action, int *result)
{
    /*!
     *
     * @sender Bus name of the sender
     * @result PK result
     * @return 0 on success, 1 on error
     */

    DBusConnection *conn;
    DBusError err;
    int uid = -1;

    *result = POLICY_NO;

    dbus_error_init(&err);

    conn = dbus_bus_get_private(DBUS_BUS_SYSTEM, &err);
    if (dbus_error_is_set(&err)) {
        log_error("Unable to open DBus connection to query PolicyKit: %s\n", err.message);
        dbus_error_free(&err);
        return -1;
    }

    // If UID is 0, don't query PolicyKit
    uid = dbus_bus_get_unix_user(conn, sender, &err);
    if (dbus_error_is_set(&err)) {
        log_error("Unable to get caller UID: %s\n", err.message);
        dbus_error_free(&err);
        return -1;
    }
    if (uid == 0) {
        *result = POLICY_YES;
        return 0;
    }

    PyObject *subject = PyTuple_New(2);
    PyTuple_SetItem(subject, 0, PyString_FromString("system-bus-name"));
    PyObject *details = PyDict_New();
    PyDict_SetItemString(details, "name", PyString_FromString(sender));
    PyTuple_SetItem(subject, 1, details);

    PyObject *details2 = PyDict_New();

    PyObject *obj = PyTuple_New(5);
    PyTuple_SetItem(obj, 0, subject);
    PyTuple_SetItem(obj, 1, PyString_FromString(action));
    PyTuple_SetItem(obj, 2, details2);
    PyTuple_SetItem(obj, 3, PyInt_FromLong((long) 1));
    PyTuple_SetItem(obj, 4, PyString_FromString("abc"));

    PyObject *ret = bus_execute2(conn, "org.freedesktop.PolicyKit1", "/org/freedesktop/PolicyKit1/Authority", "org.freedesktop.PolicyKit1.Authority", "CheckAuthorization", obj, -1, "(sa{sv})sa{ss}us");

    if (!ret) {
        char *eStr, *vStr;
        py_catch(&eStr, &vStr, 1);
        *result = POLICY_NO;
        return 0;
    }

    if (PyTuple_GetItem(ret, 0) == Py_True) {
        *result = POLICY_YES;
    }

    return 0;
}
