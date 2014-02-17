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
#include "process.h"

#include <stdarg.h>
#include <stdio.h>
#include <time.h>


//! Puts time into file
void
timestamp(FILE *f)
{
    static char buf[128];
    time_t t;
    struct tm *bt;

    time(&t);
    bt = localtime(&t);
    strftime(buf, 127, "%F %T ", bt);
    fputs(buf, f);
}

//! Prints comar version info and process id to stdout
void
pidstamp(FILE *f)
{
    if (my_proc.bus_msg) {
        const char *sender = dbus_message_get_sender(my_proc.bus_msg);
        fprintf(f, "(%d) [bus%s] ", getpid(), sender);
    }
    else {
        fprintf(f, "(%d) ", getpid());
    }
}

//! Logs a message
void
log_print(const char *fmt, va_list ap, int error)
{
    FILE *f;

    if (config_runlevel != 0) {
        f = fopen(config_file_log_traceback, "a");
    }
    else {
        f = stdout;
    }

    timestamp(f);
    pidstamp(f);

    if (error) {
        fprintf(f, "ERROR: ");
    }

    vfprintf(f, fmt, ap);

    if (config_runlevel != 0) {
        fclose(f);
    }
}

//! Logs an error message
void log_error(const char *fmt, ...)
{
    va_list ap;

    va_start(ap, fmt);
    log_print(fmt, ap, 1);
    va_end(ap);
}

//! Logs an information message
void log_info(const char *fmt, ...)
{
    va_list ap;

    va_start(ap, fmt);
    log_print(fmt, ap, 0);
    va_end(ap);
}

//! Logs a debug message
void log_debug(const char *fmt, ...)
{
    if (!config_debug) {
        return;
    }

    va_list ap;

    va_start(ap, fmt);
    log_print(fmt, ap, 0);
    va_end(ap);
}
