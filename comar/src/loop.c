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

#include "bus.h"
#include "config.h"
#include "log.h"
#include "process.h"
#include "policy.h"
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

#define MAX_FDS 1024
#define MAX_PROC 500
#define MAX_WATCHES 10

static struct pollfd bus_fds[MAX_WATCHES];
static DBusWatch *bus_watches[MAX_WATCHES];
static int bus_nr_watches = 0;

//! Executes registered Python code of app/model
void
message_execute(DBusMessage *msg, const char *app, const char *model, const char *method)
{
    PyObject *py_ret;
    PyObject *py_args = pydbus_import(msg);
    char *eStr, *vStr;

    // Validate model and method
    if (validate_model_member(model, method, 0) != 0) {
        bus_reply_unknown_method(msg);
        return;
    }

    // Check policy

    PyObject *model_def = PyDict_GetItemString(PyDict_GetItemString(py_core, "models"), model);
    PyObject *method_def = PyDict_GetItemString(model_def, method);
    char *signature = script_signature(model, method, 1);

    if (PyDict_GetItemString(model_def, method) != Py_None) {
        const char *action_id = PyString_AsString(PyTuple_GetItem(method_def, 1));
        const char *sender = dbus_message_get_sender(my_proc.bus_msg);

        if (strcmp(action_id, "") != 0) {
            int result;
            if (policy_check(sender, action_id, &result) == 0) {
                if (result != POLICY_YES) {
                    bus_reply_error(msg, "Comar.PolicyKit", action_id);
                    return;
                }
            }
            else {
                bus_reply_error(msg, "Comar.PolicyKit", "error");
                return;
            }
        }
    }

    // Execute method
    switch (py_execute(app, model, method, py_args, &py_ret)) {
        case 0:
            // Success
            bus_reply_object(msg, py_ret, signature);
            break;
        case -1:
        case -2:
            // Python exception raised
            py_catch(&eStr, &vStr, 1);
            bus_reply_error(msg, eStr, vStr);
            break;
        case -3:
        case -4:
            // PolicyKit exception raised
            py_catch(&eStr, &vStr, 0);
            bus_reply_error(msg, eStr, vStr);
            break;
    }
}

//! Handles a DBus message and executes related script
void
handle_message(DBusMessage *msg)
{
    Py_Initialize();

    const char *method = dbus_message_get_member(msg);
    const char *iface = dbus_message_get_interface(msg);
    const char *path = dbus_message_get_path(msg);

    if (method == NULL || path == NULL || method == NULL) {
        bus_reply_unknown_method(msg);
    }
    else if (strcmp("org.freedesktop.DBus.Introspectable", iface) == 0 && strcmp("Introspect", method) == 0) {
        // Introspection method
        message_execute(msg, NULL, "Core", "introspect");
    }
    else if (strcmp(config_interface, iface) == 0) {
        // Core methods
        message_execute(msg, NULL, "Core", method);
    }
    else if (strncmp(config_interface, iface, strlen(config_interface)) == 0 && iface[strlen(config_interface)] == '.') {
        // Model.method
        char *model = strsub(iface, strlen(config_interface) + 1, strlen(iface));
        char *app = strsub(path, strlen("/package/"), strlen(path));

        message_execute(msg, app, model, method);

        free(model);
        free(app);
    }
    else {
        bus_reply_unknown_method(msg);
    }

    Py_Finalize();
}

void
handle_core_message(DBusMessage *bus_msg, const char *path, const char *iface, const char *method, const char *sender, PyObject *py_args)
{
    if (strcmp(method, "setLocale") == 0) {
        PyDict_SetItemString(PyDict_GetItemString(py_core, "locales"), sender, PyTuple_GetItem(py_args, 0));
        bus_reply_object(bus_msg, Py_True, "b");
    }
    else if (strcmp(method, "cancel") == 0) {
        log_debug("Cancel requested.\n");
        int i;
        int total = 0;
        // Iterate over all child processes
        for (i = 0; i < my_proc.nr_children; i++) {
            struct ProcChild *child = &my_proc.children[i];
            if (dbus_message_has_sender(child->bus_msg, sender)) {
                kill(child->pid, SIGINT);
                total++;
            }
        }
        log_debug("Killed %d processes.\n", total);
        bus_reply_object(bus_msg, PyInt_FromLong((long) total), "i");
    }
    else if (strcmp(method, "listRunning") == 0) {
        int i;
        PyObject *py_list = PyList_New(0);
        // Iterate over all child processes
        for (i = 0; i < my_proc.nr_children; i++) {
            struct ProcChild *child = &my_proc.children[i];
            if (PyTuple_GetItem(py_args, 0) == Py_True || dbus_message_has_sender(child->bus_msg, sender)) {
                PyList_Append(py_list, PyString_FromFormat("%s.%s", dbus_message_get_interface(child->bus_msg), dbus_message_get_member(child->bus_msg)));
            }
        }
        bus_reply_object(bus_msg, py_list, "as");
    }
}

static DBusHandlerResult
filter_func(DBusConnection *conn, DBusMessage *bus_msg, void *data)
{
    const char *method = dbus_message_get_member(bus_msg);
    const char *iface = dbus_message_get_interface(bus_msg);
    const char *sender = dbus_message_get_sender(bus_msg);
    const char *path = dbus_message_get_path(bus_msg);

    PyObject *py_args = pydbus_import(bus_msg);

    if (!dbus_message_has_destination(bus_msg, config_unique_address)
        && strncmp(dbus_message_get_destination(bus_msg), DBUS_SERVICE_NAME, strlen(DBUS_SERVICE_NAME))) {
        return DBUS_HANDLER_RESULT_HANDLED;
    }

    switch (dbus_message_get_type(bus_msg)) {
        case DBUS_MESSAGE_TYPE_METHOD_CALL:
            if (my_proc.nr_children > MAX_PROC) {
                // Busy
                return DBUS_HANDLER_RESULT_NOT_YET_HANDLED;
            }
            else {
                log_debug("Got message '%s.%s' from '%s'\n", iface, method, sender);
                if (strcmp(config_interface, iface) == 0 && strcmp(path, "/") == 0) {
                    // "setLocale" and "cancel" methods are handled in main process
                    if (strcmp(method, "setLocale") == 0 || strcmp(method, "cancel") == 0 || strcmp(method, "listRunning") == 0) {
                        handle_core_message(bus_msg, path, iface, method, sender, py_args);
                    }
                    else {
                        // Else, handle in child process
                        proc_fork(handle_message, bus_msg);
                    }
                }
                else {
                    // Else, handle in child process
                    proc_fork(handle_message, bus_msg);
                }
                break;
            }
        case DBUS_MESSAGE_TYPE_SIGNAL:
            log_debug("Got signal '%s.%s' from '%s'\n", iface, method, sender);
            break;
    }
    return DBUS_HANDLER_RESULT_HANDLED;
}

static dbus_bool_t add_watch(DBusWatch *watch, void *data)
{
    short cond = POLLHUP | POLLERR;
    int fd = dbus_watch_get_unix_fd(watch);
    unsigned int flags = dbus_watch_get_flags(watch);

    if (flags & DBUS_WATCH_READABLE)
        cond |= POLLIN;
    if (flags & DBUS_WATCH_WRITABLE)
        cond |= POLLOUT;

    bus_fds[bus_nr_watches].fd = fd;
    bus_fds[bus_nr_watches].events = cond;
    bus_watches[bus_nr_watches] = watch;
    bus_nr_watches++;

    return 1;
}

static void remove_watch(DBusWatch *watch, void *data)
{
    int i, found = 0;

    for (i = 0; i < bus_nr_watches; ++i) {
        if (bus_watches[i] == watch) {
            found = 1;
            break;
        }
    }
    if (!found) {
        log_error("Missing DBus watch: %p\n", (void *) watch);
        return;
    }

    memset(&bus_fds[i], 0, sizeof(bus_fds[i]));
    bus_watches[i] = NULL;

    if (i == bus_nr_watches && bus_nr_watches > 0) --bus_nr_watches;
}

static void fd_handler(short events, DBusWatch *watch)
{
    unsigned int flags = 0;

    if (events & POLLIN)
        flags |= DBUS_WATCH_READABLE;
    if (events & POLLOUT)
        flags |= DBUS_WATCH_WRITABLE;
    if (events & POLLHUP)
        flags |= DBUS_WATCH_HANGUP;
    if (events & POLLERR)
        flags |= DBUS_WATCH_ERROR;

    while (!dbus_watch_handle(watch, flags)) {
        log_error("DBus watch handler needs more memory, sleeping...\n");
        sleep(1);
    }

    dbus_connection_ref(bus_conn);
    while (dbus_connection_dispatch(bus_conn) == DBUS_DISPATCH_DATA_REMAINS);
    dbus_connection_unref(bus_conn);
}

//! Main loop
int
loop_exec()
{
    /*!
     * This is the main loop function.
     *
     * Based on code written by Kimmo.Hamalainen at nokia.com
     * http://lists.freedesktop.org/archives/dbus/2007-October/008859.html
     *
     * @return 0 on success, -1 on error
     */

    DBusError bus_error;
    dbus_error_init(&bus_error);

    // Connect to D-Bus
    bus_conn = dbus_connection_open_private(config_server_address, &bus_error);
    if (dbus_error_is_set(&bus_error)) {
        log_error("Error while connecting to the bus: %s\n", bus_error.message);
        dbus_error_free(&bus_error);
        return -1;
    }

    if (!dbus_bus_register(bus_conn, &bus_error)) {
        log_error("Error while registering to the bus: %s\n", bus_error.message);
        dbus_error_free(&bus_error);
        return -1;
    }

    config_unique_address = dbus_bus_get_unique_name(bus_conn);
    log_debug("Connected to D-Bus, unique id is %s\n", dbus_bus_get_unique_name(bus_conn));

    // Request a name (example: com.server.test)
    dbus_bus_request_name(bus_conn, config_service_name, DBUS_NAME_FLAG_REPLACE_EXISTING, &bus_error);
    if (dbus_error_is_set(&bus_error)) {
        log_error("Name Error (%s)\n", bus_error.message);
        dbus_error_free(&bus_error);
        return -1;
    }

    log_debug("Registered name '%s'\n", config_service_name);

    // Register watch callback functions
    if (!dbus_connection_set_watch_functions(bus_conn, add_watch, remove_watch, NULL, NULL, NULL)) {
        log_error("dbus_connection_set_watch_functions failed\n");
        return -1;
    }

    // Register function that handles D-Bus events (calls, signals, ...)
    if (!dbus_connection_add_filter(bus_conn, filter_func, NULL, NULL)) {
        log_error("Failed to register signal handler callback\n");
        return -1;
    }

    // Catch all method calls
    dbus_bus_add_match(bus_conn, "type='method_call'", NULL);

    log_info("Listening for connections...\n");

    /* This clears any pending messages avoiding weird timeouts on some systems
     * with dbus >= 1.2.22
     */
    while (dbus_connection_dispatch(bus_conn) == DBUS_DISPATCH_DATA_REMAINS);

    while (1) {
        struct pollfd fds[MAX_FDS];
        DBusWatch *watches[MAX_WATCHES];
        int i, j;
        int nr_fds = 0;
        int nr_watches = 0;
        int poll_result;

        // Add D-Bus watch descriptors to the list
        nr_fds = 0;
        for (i = 0; i < bus_nr_watches; i++) {
            if (bus_fds[i].fd == 0 || !dbus_watch_get_enabled(bus_watches[i])) {
                continue;
            }

            fds[nr_fds].fd = bus_fds[i].fd;
            fds[nr_fds].events = bus_fds[i].events;
            fds[nr_fds].revents = 0;
            watches[nr_fds] = bus_watches[i];
            nr_fds++;
            if (i > MAX_WATCHES) {
                log_error("ERR: %d watches reached\n", MAX_WATCHES);
                break;
            }
        }
        nr_watches = nr_fds;

        // Add subprocess descriptors to the list
        for (i = 0; i < my_proc.nr_children; i++) {
            fds[nr_fds].fd = my_proc.children[i].from;
            fds[nr_fds].events = 0;
            fds[nr_fds].revents = 0;
            nr_fds++;
        }

        // Poll descriptors
        poll_result = 0;

        if (config_timeout == 0) {
            // If no timeout defined, wait forever.
            poll_result = poll(fds, nr_fds, -1);
        }
        else {
            // wait <timeout> seconds
            poll_result = poll(fds, nr_fds, config_timeout * 1000);
        }

        if (poll_result == 0) {
            if (config_timeout != 0 && my_proc.nr_children == 0) {
                log_info("Service was idle for more than %d second(s), closing daemon...\n", config_timeout);
                break;
            }
            continue;
        }
        else if (poll_result < 0) {
            perror("poll");
            return -1;
        }

        // Iterate over all descriptors
        for (i = 0; i < nr_fds; i++) {
            if (i < nr_watches) {
                // D-Bus watch event
                if (fds[i].revents) {
                    // Handle D-Bus watch event
                    fd_handler(fds[i].revents, watches[i]);
                }
            } else {
                // Subprocess event
                for (j = 0; j < my_proc.nr_children; j++) {
                    if (my_proc.children[j].from == fds[i].fd) {
                        if (fds[i].revents) {
                            // Subprocess exited, remove it
                            rem_child(j);
                        }
                        break;
                    }
                }
            }
        }
    }

    return 0;
}
