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

#ifndef SCRIPT_H
#define SCRIPT_H

#include <Python.h>

extern PyObject *py_core;

extern PyObject *PyExc_COMAR_Internal;
extern PyObject *PyExc_COMAR_Invalid;
extern PyObject *PyExc_COMAR_Script;
extern PyObject *PyExc_COMAR_Missing;
extern PyObject *PyExc_DBus;
extern PyObject *PyExc_PolicyKit;

int script_init();
void script_finalize();

void py_catch(char **eStr, char **vStr, int log);
int py_execute(const char *str_application, const char *str_model, const char *str_method, PyObject *py_args, PyObject **py_ret);

int validate_model_member(const char *model, const char *method, int type);

char *script_signature(const char *model, const char *member, int direction);
PyObject *script_signature_each(const char *signature);

#endif // SCRIPT_H
