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
#include "db.h"
#include "log.h"
#include "script.h"
#include "policy.h"
#include "process.h"
#include "utils.h"

#include <string.h>

//! Core dictionary
PyObject *py_core;

//! Exceptions
PyObject *PyExc_COMAR_Internal;
PyObject *PyExc_COMAR_Invalid;
PyObject *PyExc_COMAR_Script;
PyObject *PyExc_COMAR_Missing;
PyObject *PyExc_DBus;
PyObject *PyExc_PolicyKit;

//! Initializes Python VM
int
script_init()
{
    Py_InitializeEx(0);

    // Initialize exceptions
    PyExc_COMAR_Internal = PyErr_NewException("Comar.Internal", NULL, NULL);
    PyExc_COMAR_Invalid = PyErr_NewException("Comar.Invalid", NULL, NULL);
    PyExc_COMAR_Script = PyErr_NewException("Comar.Script", NULL, NULL);
    PyExc_COMAR_Missing = PyErr_NewException("Comar.Missing", NULL, NULL);
    PyExc_DBus = PyErr_NewException("Comar.DBus", NULL, NULL);
    PyExc_PolicyKit = PyErr_NewException("Comar.PolicyKit", NULL, NULL);

    // Load model definitions
    PyObject *py_models;
    if (db_load_models(&py_models) != 0) {
        return -1;
    }

    if (PyDict_Size(py_models) == 0) {
        log_error("No models present in data/models directory.\n");
        return -1;
    }

    // Build core dictionary
    py_core = PyDict_New();
    PyDict_SetItemString(py_core, "models", py_models);
    PyDict_SetItemString(py_core, "locales", PyDict_New());

    log_debug("Models defined             : %d\n", PyDict_Size(py_models));
    log_debug("\n");

    return 0;
}

//! Finalizes Python VM
void
script_finalize()
{
    Py_Finalize();
}

//! Returns method's signature
char *
script_signature(const char *model, const char *member, int direction)
{
    /*!
     * Returns method's signature
     *
     * @model Model name
     * @member Member nam
     * @direction 0 for input, 1 for output
     * @return Signature
     *
     */

    PyObject *py_models = PyDict_GetItemString(py_core, "models");
    PyObject *py_model = PyDict_GetItemString(py_models, model);
    PyObject *py_method = PyDict_GetItemString(py_model, member);
    PyObject *py_str = PyString_FromString("");
    PyObject *py_list;

    if (direction == 0) {
        py_list = PyTuple_GetItem(py_method, 2);
    }
    else {
        py_list = PyTuple_GetItem(py_method, 3);
    }

    int i;
    for (i = 0; i < PyList_Size(py_list); i++) {
        PyString_Concat(&py_str, PyList_GetItem(py_list, i));
    }

    return PyString_AsString(py_str);
}

//! Splits signature into atomic DBus object signatures
PyObject *
script_signature_each(const char *signature)
{
    PyObject *py_list = PyList_New(0);

    DBusError error;
    DBusSignatureIter iter;

    dbus_signature_iter_init(&iter, signature);
    while (dbus_signature_iter_get_current_type(&iter) != DBUS_TYPE_INVALID) {
        char *sign = dbus_signature_iter_get_signature(&iter);

        dbus_error_init(&error);
        dbus_signature_validate(sign, &error);
        if (dbus_error_is_set(&error)) {
            dbus_error_free(&error);
            return NULL;
        }
        else {
            PyList_Append(py_list, PyString_FromString(sign));
        }

        dbus_free(sign);
        dbus_signature_iter_next(&iter);
    }

    return py_list;
}

//! Catches raised Python exceptions
void
py_catch(char **eStr, char **vStr, int log)
{
    /*!
     * Catches a Python exception.
     *
     * @eStr Pointer to error type string
     * @vStr Pointer to error message string
     * @log 0 disables, 1 enables logging
     *
     */

    PyObject *py_type, *py_value, *py_trace;
    PyObject *py_frame, *py_code;

    *vStr = "";

    PyErr_Fetch(&py_type, &py_value, &py_trace);
    if (!py_type) {
        // Even though logging is disabled, this error should be logged.
        log_error("py_exception() called when there isn't an exception");
        return;
    }

    *eStr = PyString_AsString(PyObject_GetAttrString(py_type, "__name__"));

    if (py_value) {
        *vStr = PyString_AsString(PyObject_Str(py_value));
    }

    if (log == 0) {
        return;
    }

    log_error("Exception: %s - %s\n", *eStr, *vStr);

    // Also log error traceback
    while (py_trace != NULL && py_trace != Py_None) {
        py_frame = PyObject_GetAttrString(py_trace, "tb_frame");
        py_code = PyObject_GetAttrString(py_frame, "f_code");
        log_error("    File %s, line %d, in %s()\n", PyString_AsString(PyObject_GetAttrString(py_code, "co_filename")),
                                                   (int) PyInt_AsLong(PyObject_GetAttrString(py_trace, "tb_lineno")),
                                                   PyString_AsString(PyObject_GetAttrString(py_code, "co_name")));
        py_trace = PyObject_GetAttrString(py_trace, "tb_next");
    }
}

//! Returns sender's locale
const char *
sender_language()
{
    /*!
     * Returns sender's locale.
     *
     * @return Language code
     *
     */

    const char *sender = dbus_message_get_sender(my_proc.bus_msg);
    PyObject *py_locales = PyDict_GetItemString(py_core, "locales");
    const char *lang;

    if (PyDict_Contains(py_locales, PyString_FromString(sender))) {
        lang = PyString_AsString(PyDict_GetItemString(py_locales, sender));
    }
    else {
        lang = "en";
    }

    return lang;
}

//! Tells if model.member is defined in model database
int
validate_model_member(const char *model, const char *member, int type)
{
    /*!
     * Tells if model.member is defined in model database.
     *
     * @model Model name
     * @member Member (method or signal name)
     * @type 0 if member is a method, 1 if member is a signal
     * @return 0 if valid, -1 if invalid
     *
     */

    if (PyDict_Contains(PyDict_GetItemString(py_core, "models"), PyString_FromString(model))) {
        PyObject *py_dict_model = PyDict_GetItemString(PyDict_GetItemString(py_core, "models"), model);
        if (PyDict_Contains(py_dict_model, PyString_FromString(member))) {
            PyObject *py_tuple = PyDict_GetItemString(py_dict_model, member);
            if (PyInt_AsLong(PyTuple_GetItem(py_tuple, 0)) == (long) type) {
                return 0;
            }
        }
    }
    return -1;
}

//! Returns DBus message path, used in scripts
static PyObject *
c_bus_path(PyObject *self, PyObject *args)
{
    const char *path = dbus_message_get_path(my_proc.bus_msg);
    PyObject *py_str = PyString_FromString(path);
    Py_INCREF(py_str);
    return py_str;
}

//! Returns DBus message interface, used in scripts
static PyObject *
c_bus_interface(PyObject *self, PyObject *args)
{
    const char *iface = dbus_message_get_interface(my_proc.bus_msg);
    PyObject *py_str = PyString_FromString(iface);
    Py_INCREF(py_str);
    return py_str;
}

//! Returns DBus message member, used in scripts
static PyObject *
c_bus_member(PyObject *self, PyObject *args)
{
    const char *member = dbus_message_get_member(my_proc.bus_msg);
    PyObject *py_str = PyString_FromString(member);
    Py_INCREF(py_str);
    return py_str;
}

//! Returns DBus message sender, used in scripts
static PyObject *
c_bus_sender(PyObject *self, PyObject *args)
{
    const char *sender = dbus_message_get_sender(my_proc.bus_msg);
    PyObject *py_str = PyString_FromString(sender);
    Py_INCREF(py_str);
    return py_str;
}

//! Returns package name, used in scripts
static PyObject *
c_package(PyObject *self, PyObject *args)
{
    const char *path = dbus_message_get_path(my_proc.bus_msg);

    if (strncmp(path, "/package/", strlen("/package/")) == 0) {
        const char *app = strsub(path, strlen("/package/"), strlen(path));
        if (strlen(app) > 0) {
            return PyString_FromString(app);
        }
    }

    Py_INCREF(Py_None);
    return Py_None;
}

//! Returns model name, used in scripts
static PyObject *
c_model(PyObject *self, PyObject *args)
{
    const char *iface = dbus_message_get_interface(my_proc.bus_msg);

    if (strncmp(iface, config_interface, strlen(config_interface)) == 0) {
        const char *model = strsub(iface, strlen(config_interface) + 1, strlen(iface));
        if (strlen(model) > 0) {
            return PyString_FromString(model);
        }
    }

    Py_INCREF(Py_None);
    return Py_None;
}

//! i18n method, used in scripts
static PyObject *
c_i18n(PyObject *self, PyObject *args)
{
    PyObject *py_dict;

    if (!PyArg_ParseTuple(args, "O!", &PyDict_Type, &py_dict)) {
        return NULL;
    }

    PyObject *py_lang = PyString_FromString(sender_language());
    if (!PyDict_Contains(py_dict, py_lang)) {
        py_lang = PyString_FromString("en");
    }

    if (PyDict_Contains(py_dict, py_lang)) {
        return PyDict_GetItem(py_dict, py_lang);
    }
    else {
        PyErr_Format(PyExc_COMAR_Script, "Script is lack of default ('en') locale string.");
        return NULL;
    }
}

//! Signal emitter method, used in scripts
static PyObject *
c_notify(PyObject *self, PyObject *args)
{
    const char *model, *signal;
    PyObject *py_tuple = NULL;

    if (!PyArg_ParseTuple(args, "ss|O", &model, &signal, &py_tuple)) {
        return NULL;
    }

    if (validate_model_member(model, signal, 1) != 0) {
        PyErr_Format(PyExc_COMAR_Invalid, "Signal '%s' is not defined in '%s' model", signal, model);
        return NULL;
    }

    const char *path = dbus_message_get_path(my_proc.bus_msg);

    int size = strlen(config_interface) + 1 + strlen(model) + 1;
    char *interface = malloc(size);
    snprintf(interface, size, "%s.%s", config_interface, model);
    interface[size - 1] = '\0';

    char *signature = script_signature(model, signal, 1);

    if (bus_signal(path, interface, signal, py_tuple, signature) != 0) {
        free(interface);
        return NULL;
    }

    free(interface);

    Py_INCREF(Py_None);
    return Py_None;
}

//! Internal method call method, used in scripts
static PyObject *
c_call(PyObject *self, PyObject *args, PyObject *keywds)
{
    const char *app, *model, *method;
    PyObject *py_tuple = NULL;
    int timeout = -1;
    static char *kwlist[] = {"app", "model", "method", "args", "timeout", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "sss|Oi", kwlist, &app, &model, &method, &py_tuple, &timeout)) {
        return NULL;
    }

    if (validate_model_member(model, method, 0) != 0) {
        PyErr_Format(PyExc_COMAR_Invalid, "Method '%s' is not defined in '%s' model", method, model);
        return NULL;
    }

    if (py_tuple == NULL) {
        py_tuple = PyTuple_New(0);
    }

    // Build DBus interface from model name
    int size = strlen(config_interface) + 1 + strlen(model) + 1;
    char *interface = malloc(size);
    snprintf(interface, size, "%s.%s", config_interface, model);
    interface[size - 1] = '\0';

    // Build DBus path from application name
    size = strlen("/package/") + strlen(app) + 1;
    char *path = malloc(size);
    snprintf(path, size, "/package/%s", app);
    path[size - 1] = '\0';

    log_debug("Internal call: %s.%s %s\n", interface, method, path);

    // Get language
    const char *lang = sender_language();

    // Get signature
    char *signature = script_signature(model, method, 0);

    // Call method
    PyObject *ret = bus_call(path, interface, method, py_tuple, timeout, lang, signature);

    free(path);
    free(interface);

    return ret;
}

//! Abort method, used in scripts
static PyObject *
c_fail(PyObject *self, PyObject *args)
{
    const char *strerr;

    if (!PyArg_ParseTuple(args, "s", &strerr)) {
        return NULL;
    }

    PyErr_SetString(PyExc_Exception, strerr);
    return NULL;
}

//! Returns data path, used in scripts
static PyObject *
c_cfg_datapath(PyObject *self, PyObject *args)
{
    PyObject *py_str = PyString_FromString(config_dir_data);
    Py_INCREF(py_str);
    return py_str;
}

//! Returns model database, used in scripts
static PyObject *
c_cfg_modelbase(PyObject *self, PyObject *args)
{
    PyObject *py_dict = PyDict_GetItemString(py_core, "models");
    Py_INCREF(py_dict);
    return py_dict;
}

//! Returns default interface
static PyObject *
c_cfg_interface(PyObject *self, PyObject *args)
{
    PyObject *py_str = PyString_FromString(config_interface);
    Py_INCREF(py_str);
    return py_str;
}

//! Methods usable in scripts
static PyMethodDef methods[] = {
    { "model", c_model, METH_NOARGS, "Return model name" },
    { "package", c_package, METH_NOARGS, "Return package name" },
    { "script", c_package, METH_NOARGS, "Alias to package()" },
    { "_", c_i18n, METH_VARARGS, "i18n" },
    { "notify", c_notify, METH_VARARGS, "Emit signal" },
    { "call", (PyCFunction) c_call, METH_VARARGS|METH_KEYWORDS, "Call COMAR method" },
    { "fail", c_fail, METH_VARARGS, "Abort script" },
    // Configuration
    { "config_datapath", c_cfg_datapath, METH_NOARGS, "Return data path" },
    { "config_interface", c_cfg_interface, METH_NOARGS, "Returns default interface" },
    { "config_modelbase", c_cfg_modelbase, METH_NOARGS, "Return model database" },
    // DBus message
    { "bus_path", c_bus_path, METH_NOARGS, "Return DBus message path" },
    { "bus_interface", c_bus_interface, METH_NOARGS, "Return DBus message interface" },
    { "bus_member", c_bus_member, METH_NOARGS, "Return DBus message member" },
    { "bus_sender", c_bus_sender, METH_NOARGS, "Return DBus message sender" },
    { NULL, NULL, 0, NULL }
};

//! Executes given method of app/model
int
py_execute(const char *app, const char *model, const char *method, PyObject *py_args, PyObject **py_ret)
{
    /*!
     * Loads app/model.py and calls method with given arguments. If app or module is null, this
     * function will execute specified method on CORE module.
     *
     * @app Application
     * @model Model
     * @method Method
     * @py_args Arguments
     * @py_ret Pointer to returned value
     * @return 0 on success, -1 on missing file, -2 on Python error, -3 on access denied, -4 on PolicyKit error
     *
     */

    PyObject *py_mod_script, *py_mod_builtin;
    PyObject *py_dict_script, *py_dict_builtin;
    PyObject *py_code, *py_method_code, *py_kwargs, *py_func = NULL;
    PyMethodDef *py_method;

    PyObject *py_module, *py_dict, *py_list;
    PyObject *py_dict_core;
    PyObject *py_mod_core;

    // Add core module directory to sys.path
    py_module = PyImport_ImportModule("sys");
    py_dict = PyModule_GetDict(py_module);
    py_list = PyDict_GetItemString(py_dict, "path");
    PyList_Insert(py_list, 0, PyString_FromString(config_dir_modules));

    // Put CSL methods into __builtin__
    py_mod_builtin = PyImport_AddModule("__builtin__");
    py_dict_builtin = PyModule_GetDict(py_mod_builtin);
    for (py_method = methods; py_method->ml_name; py_method++) {
        py_method_code = PyCFunction_New(py_method, NULL);
        PyDict_SetItemString(py_dict_builtin, py_method->ml_name, py_method_code);
    }

    // If model and application name given, try to execute method on registered script
    if (model != NULL && app != NULL) {
        // Import script
        int size = strlen(config_dir_scripts) + 1 + strlen(model) + 1 + strlen(app) + 3 + 1;
        char *fn_script = malloc(size);
        if (fn_script == NULL) oom();
        snprintf(fn_script, size, "%s/%s/%s.py", config_dir_scripts, model, app);
        fn_script[size - 1] = 0;

        // Check script existance
        if (access(fn_script, R_OK) != 0) {
            log_error("Unable to find script: %s\n", fn_script);
            PyErr_Format(PyExc_COMAR_Internal, "Unable to find '%s'", fn_script);
            free(fn_script);
            return -1;
        }

        // Load script file
        char *code = load_file(fn_script, NULL);
        if (!code) {
            log_error("Unable to read script: %s\n", fn_script);
            PyErr_Format(PyExc_COMAR_Internal, "Unable to read '%s'", fn_script);
            free(fn_script);
            return -1;
        }

        // Compile script
        py_code = Py_CompileString(code, fn_script, Py_file_input);
        free(code);
        if (!py_code) {
            log_error("Unable to compile script: %s\n", fn_script);
            free(fn_script);
            return -2;
        }

        // Import script as "csl" module
        py_mod_script = PyImport_ExecCodeModule("csl", py_code);
        if (!py_mod_script) {
            log_error("Unable to exec code module script: %s\n", fn_script);
            free(fn_script);
            return -2;
        }

        free(fn_script);

        // Look for 'method()' in script
        py_dict_script = PyModule_GetDict(py_mod_script);
        py_func = PyDict_GetItemString(py_dict_script, method);
    }
    // Else, execute method on core module
    else {
        // Import core module
        py_mod_core = PyImport_ImportModule("core");
        if (!py_mod_core) {
            log_error("Unable to import core module.\n");
            return -2;
        }

        // Look for 'method()' in script
        py_dict_core = PyModule_GetDict(py_mod_core);
        py_func = PyDict_GetItemString(py_dict_core, method);
    }

    // Finally, run method
    if (!py_func) {
        if (config_ignore_missing) {
            Py_INCREF(Py_None);
            *py_ret = Py_None;
        }
        else {
            PyErr_Format(PyExc_COMAR_Missing, "Method '%s' is not defined in script", method);
            return -2;
        }
    }
    else if (!PyCallable_Check(py_func)) {
        PyErr_Format(PyExc_COMAR_Script, "Method '%s' is not callable in script", method);
        return -2;
    }
    else {
        // Check if PolicyKit action defined at runtime
        if (PyObject_HasAttrString(py_func, "policy_action_id")) {
            const char *action_id = PyString_AsString(PyObject_GetAttrString(py_func, "policy_action_id"));
            const char *sender = dbus_message_get_sender(my_proc.bus_msg);

            int result;
            if (policy_check(sender, action_id, &result) == 0) {
                if (result != POLICY_YES) {
                    PyErr_Format(PyExc_PolicyKit, action_id);
                    return -3;
                }
            }
            else {
                PyErr_Format(PyExc_PolicyKit, "error");
                return -4;
            }
        }

        py_kwargs = PyDict_New();
        *py_ret = PyObject_Call(py_func, py_args, py_kwargs);
        if (!*py_ret) {
            return -2;
        }
    }

    return 0;
}
