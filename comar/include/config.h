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

#ifndef CONFIG_H
#define CONFIG_H

#ifndef VERSION
#define VERSION "3.0.3"
#endif

#ifndef DBUS_SERVER_ADDRESS
#define DBUS_SERVER_ADDRESS "unix:path=/var/run/dbus/system_bus_socket"
#endif

#ifndef DBUS_SERVICE_NAME
#define DBUS_SERVICE_NAME "tr.org.pardus.comar"
#endif

#ifndef DBUS_INTERFACE_PREFIX
#define DBUS_INTERFACE_PREFIX "tr.org.pardus.comar"
#endif

#ifndef IDLE_TIMEOUT
#define IDLE_TIMEOUT 60
#endif

#ifndef DIR_DATA
#define DIR_DATA "/var/db/comar3"
#endif

#ifndef DIR_LOG
#define DIR_LOG "/var/log/comar3"
#endif

#ifndef FILE_PID
#define FILE_PID "/var/run/comar3.pid"
#endif

#ifndef WWW_BUGS
#define WWW_BUGS "http://bugs.pardus.org.tr"
#endif

extern char *config_server_address;
extern const char *config_unique_address;
extern char *config_service_name;
extern char *config_interface;
extern char *config_dir_data;
extern char *config_dir_log;
extern char *config_file_pid;

extern int config_timeout;
extern int config_debug;
extern int config_print;
extern int config_runlevel;
extern int config_ignore_missing;

extern char *config_dir_models;
extern char *config_dir_modules;
extern char *config_dir_scripts;
extern char *config_dir_apps;
extern char *config_file_log_access;
extern char *config_file_log_traceback;

void config_init(int argc, char *argv[]);
#endif /* CONFIG_H */
