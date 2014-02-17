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
#include "iksemel.h"
#include "script.h"
#include "log.h"
#include "utils.h"

#include <dirent.h>
#include <unistd.h>
#include <sys/file.h>
#include <sys/stat.h>

#include <dbus/dbus.h>

//! Validates model file
int
db_validate_model(iks *xml, char *filename)
{
    /*!
     * Validates model file.
     *
     * @xml Iksemel document
     * @return 0 on success, -1 on error
     *
     */

    iks *iface, *met, *arg;

    DBusError bus_error;
    dbus_error_init(&bus_error);

    // Check root tag
    if (iks_strcmp(iks_name(xml), "comarModel") != 0) {
        log_error("Not a valid model XML: %s\n", filename);
        return -1;
    }

    for (iface = iks_first_tag(xml); iface; iface = iks_next_tag(iface)) {
        // Only "interface" tag is allowed
        if (iks_strcmp(iks_name(iface), "interface") != 0) {
            log_error("Unknown tag '%s' in XML: %s\n", iks_name(iface), filename);
            return -1;
        }
        // Interfaces must have a "name" attribute
        if (!iks_strlen(iks_find_attrib(iface, "name"))) {
            log_error("Model with no name in XML: %s\n", filename);
            return -1;
        }

        for (met = iks_first_tag(iface); met; met = iks_next_tag(met)) {
            // Only "method" and "signal" tags are allowed
            if (iks_strcmp(iks_name(met), "method") == 0 || iks_strcmp(iks_name(met), "signal") == 0) {
                // Tags must have a "name" attribute
                if (!iks_strlen(iks_find_attrib(met, "name"))) {
                    log_error("Method/Signal tag without name under '%s' in XML: %s\n", iks_find_attrib(iface, "name"), filename);
                    return -1;
                }
                for (arg = iks_first_tag(met); arg; arg = iks_next_tag(arg)) {
                    if (iks_strcmp(iks_name(arg), "arg") == 0) {
                        // Arguments must have a "name" attribute
                        if (!iks_strlen(iks_find_attrib(arg, "name"))) {
                            log_error("Argument tag with no name under '%s/%s' in XML: %s\n", iks_find_attrib(iface, "name"), iks_find_attrib(met, "name"), filename);
                            return -1;
                        }
                        // Arguments must have a "type" attribute
                        if (!iks_strlen(iks_find_attrib(arg, "type"))) {
                            log_error("Argument tag without type under '%s/%s' in XML: %s\n", iks_find_attrib(iface, "name"), iks_find_attrib(met, "name"), filename);
                            return -1;
                        }
                        // Types must be a valid DBus signature
                        if (!dbus_signature_validate(iks_find_attrib(arg, "type"), &bus_error)) {
                            dbus_error_free(&bus_error);
                            log_error("Argument tag with invalid type (%s/%s/%s) in XML: %s\n", iks_find_attrib(iface, "name"), iks_find_attrib(met, "name"), iks_find_attrib(arg, "name"), filename);
                            return -1;
                        }
                        // Types must be single type object
                        if (!dbus_signature_validate_single(iks_find_attrib(arg, "type"), &bus_error)) {
                            dbus_error_free(&bus_error);
                            log_error("Argument tag with a non-single element type (%s/%s/%s) in XML: %s\n", iks_find_attrib(iface, "name"), iks_find_attrib(met, "name"), iks_find_attrib(arg, "name"), filename);
                            return -1;
                        }
                    }
                    else if (iks_strcmp(iks_name(arg), "annotation") == 0) {
                        // Attributes must have a "name" attribute
                        if (!iks_strlen(iks_find_attrib(arg, "name"))) {
                            log_error("Annotation tag without name under '%s' in XML: %s\n", iks_find_attrib(iface, "name"), iks_find_attrib(met, "name"), filename);
                            return -1;
                        }
                    }
                    else {
                        log_error("Unknown tag '%s' under '%s/%s' in XML: %s\n", iks_name(arg), iks_find_attrib(iface, "name"), iks_find_attrib(met, "name"), filename);
                        return -1;
                    }
                }
            }
            else {
                log_error("Unknown tag '%s' under '%s' in XML: %s\n", iks_name(met), iks_find_attrib(iface, "name"), filename);
                return -1;
            }
        }
    }

    return 0;
}

//! Gets PolicyKit action ID of a method
char *
db_action_id(char *iface_name, iks *met)
{
    // If necerssary, get PolicyKit action ID from XML
    char *action_id = iks_find_attrib(met, "action_id");
    if (action_id) {
        return action_id;
    }
    else {
        // Else, make action ID from alias attribute
        char *alias = iks_find_attrib(met, "alias");
        if (!alias) {
            // or, from access_label attribute
            alias = iks_find_attrib(met, "access_label");
        }
        if (!alias) {
            // or, from method name
            alias = iks_find_attrib(met, "name");
        }

        // Append alias to interface name
        int size = strlen(config_interface) + 1 + strlen(iface_name) + 1 + strlen(alias) + 1;
        action_id = malloc(size);
        if (!action_id) oom();
        snprintf(action_id, size, "%s.%s.%s", config_interface, iface_name, alias);
        action_id[size - 1] = '\0';

        // All chars must be lowercase
        char *t;
        for (t = action_id; *t != '\0'; t++) {
            *t = tolower(*t);
        }

        return action_id;
    }
}

//! Loads model to database
void
db_load_model(iks *xml, PyObject **py_models)
{
    /*!
     * Loads models to database
     *
     * @xml Iksemel document
     * @py_models Pointer to models dictionary
     *
     */

    iks *iface, *met, *arg;

    for (iface = iks_first_tag(xml); iface; iface = iks_next_tag(iface)) {
        PyObject *py_methods = PyDict_New();

        char *iface_name = iks_find_attrib(iface, "name");

        for (met = iks_first_tag(iface); met; met = iks_next_tag(met)) {
            PyObject *py_tuple = PyTuple_New(4);

            // First argument is type. 0 for methods, 1 for signals
            if (iks_strcmp(iks_name(met), "method") == 0) {
                PyTuple_SetItem(py_tuple, 0, PyInt_FromLong((long) 0));
            }
            else {
                PyTuple_SetItem(py_tuple, 0, PyInt_FromLong((long) 1));
            }

            // Second argument is PolicyKit action ID
            char *action_id = db_action_id(iface_name, met);
            PyTuple_SetItem(py_tuple, 1, PyString_FromString(action_id));

            // Build argument lists
            PyObject *py_args_in = PyList_New(0);
            PyObject *py_args_out = PyList_New(0);
            int noreply = 0;
            for (arg = iks_first_tag(met); arg; arg = iks_next_tag(arg)) {
                if (iks_strcmp(iks_name(arg), "attribute") == 0) {
                    if (iks_strcmp(iks_find_attrib(arg, "name"), "org.freedesktop.DBus.Method.NoReply") == 0) {
                        if (iks_strcmp(iks_find_attrib(arg, "value"), "true") == 0) {
                            noreply = 1;
                        }
                    }
                }
                else if (iks_strcmp(iks_name(arg), "arg") == 0) {
                    if (iks_strcmp(iks_name(met), "method") == 0) {
                        if (iks_strcmp(iks_find_attrib(arg, "direction"), "out") == 0) {
                            PyList_Append(py_args_out, PyString_FromString(iks_find_attrib(arg, "type")));
                        }
                        else {
                            PyList_Append(py_args_in, PyString_FromString(iks_find_attrib(arg, "type")));
                        }
                    }
                    else if (iks_strcmp(iks_name(met), "signal") == 0) {
                        PyList_Append(py_args_out, PyString_FromString(iks_find_attrib(arg, "type")));
                    }
                }
            }

            if (noreply) {
                py_args_out = PyList_New(0);
            }

            // Third argument is input arguments
            PyTuple_SetItem(py_tuple, 2, py_args_in);
            // Fourth argument is output arguments
            PyTuple_SetItem(py_tuple, 3, py_args_out);

            PyDict_SetItemString(py_methods, iks_find_attrib(met, "name"), py_tuple);
        }

        PyDict_SetItemString(*py_models, iface_name, py_methods);
    }
}

//! Returns a dictionar of models: methods
int
db_load_models(PyObject **py_models)
{
    /*!
     * Returns a dictionary of models and their methods.
     *
     * @py_models Pointer to dictionary
     * @return 0 on success, -1 on error
     *
     */

    struct dirent *dp;
    DIR *dir = opendir(config_dir_models);
    iks *xml;

    *py_models = PyDict_New();

    // Iterate over all files under models directory
    while ((dp = readdir(dir)) != NULL) {
        if (dp->d_name[0] == '.') {
            continue;
        }

        // Load XML
        int size = strlen(config_dir_models) + 1 + strlen(dp->d_name) + 1;
        char *fn_xml = malloc(size);
        if (fn_xml == NULL) oom();
        snprintf(fn_xml, size, "%s/%s", config_dir_models, dp->d_name);
        fn_xml[size - 1] = 0;

        switch (iks_load(fn_xml, &xml)) {
            case IKS_NOMEM:
                free(fn_xml);
                oom();
            case IKS_FILE_RWERR:
            case IKS_FILE_NOACCESS:
                log_error("Unable to open XML: %s\n", fn_xml);
                closedir(dir);
                free(fn_xml);
                return -1;
        }

        // Validate XML
        if (db_validate_model(xml, fn_xml) != 0) {
            closedir(dir);
            iks_delete(xml);
            free(fn_xml);
            return -1;
        }

        // Load model
        db_load_model(xml, py_models);

    }
    closedir(dir);

    return 0;
}
