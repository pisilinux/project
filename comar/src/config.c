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

#include <unistd.h>
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/file.h>
#include <sys/stat.h>

#include "config.h"
#include "utils.h"

//! D-Bus socket file
char *config_server_address = DBUS_SERVER_ADDRESS;

//! D-Bus unique address
const char *config_unique_address;

//! D-Bus service name
char *config_service_name = DBUS_SERVICE_NAME;

//! D-Bus service interface prefix
char *config_interface = DBUS_INTERFACE_PREFIX;

//! Idle timeout in seconds
int config_timeout = IDLE_TIMEOUT;

//! Data directory
char *config_dir_data = DIR_DATA;

//! Model directory
char *config_dir_models;

//! Modules directory
char *config_dir_modules;;

//! Scripts directory
char *config_dir_scripts;

//! Application scripts directory
char *config_dir_apps;

//! Log dir
char *config_dir_log = DIR_LOG;

//! Access log file
char *config_file_log_access;

//! Traceback log file
char *config_file_log_traceback;

//! Pid file
char *config_file_pid = FILE_PID;

//! Debug mode
int config_debug = 0;

//! Print to console
int config_print = 0;

//! Runlevel (1 after logging enabled)
int config_runlevel = 0;

//! Ignore missing functions
int config_ignore_missing = 0;

//! Command line options
static struct option longopts[] = {
    { "busname", required_argument, NULL, 'b' },
    { "datadir", required_argument, NULL, 'd' },
    { "debug", 0, NULL, 'g' },
    { "ignore-missing", 0, NULL, 'i' },
    { "logdir", required_argument, NULL, 'l' },
    { "print", 0, NULL, 'p' },
    { "socket", required_argument, NULL, 's' },
    { "timeout", required_argument, NULL, 't' },
    { "help", 0, NULL, 'h' },
    { "version", 0, NULL, 'v' },
    { NULL, 0, NULL, 0 }
};

//! Short options
static char *shortopts = "b:d:gil:ps:t:phv";

//! Print help message
static void
print_usage(const char *name)
{
    /*!
     * Prints help message.
     *
     * @name Application name
     */

    printf(
        "Usage: %s [OPTIONS]\n"
        "\n"
        "  -b, --busname  [NAME] Bus address.\n"
        "                        (default is %s)\n"
        "  -d, --datadir   [DIR] Data storage directory.\n"
        "                        (default is %s)\n"
        "  -g, --debug           Enable debug mode.\n"
        "  -i, --ignore-missing  Ignore 'missing function' errors.\n"
        "  -l, --logdir    [DIR] Log storage directory.\n"
        "                        (default is %s)\n"
        "  -p, --print           Print to console.\n"
        "                        Also disables idle timeout.\n"
        "  -s, --socket   [SOCK] DBus socket address.\n"
        "                        (Default is %s)\n"
        "  -t, --timeout  [SECS] Shutdown after [SECS] seconds with no action.\n"
        "                        (Default is %d, 0 disables timeout)\n"
        "  -h, --help            Print this text and exit.\n"
        "  -v, --version         Print version and exit.\n"
        "\n"
        "Report bugs to %s\n",
        name,
        config_service_name,
        config_dir_data,
        config_dir_log,
        config_server_address,
        config_timeout,
        WWW_BUGS
    );
}

//! Print version
static void
print_version(void)
{
    /*!
     * Prints application version.
     *
     */

    printf("COMAR %s\n", VERSION);
}

//! Parse command line options
void
config_init(int argc, char *argv[])
{
    /*!
     * Parses command line options..
     *
     * @argc Number of arguments
     * @argc Array of arguments
     */

    int c, i;
    int size;

    while ((c = getopt_long(argc, argv, shortopts, longopts, &i)) != -1) {
        switch (c) {
            case 'b':
                config_service_name = strdup(optarg);
                if (!config_service_name) oom();
                break;
            case 'd':
                config_dir_data = strdup(optarg);
                if (!config_dir_data) oom();
                break;
            case 'g':
                config_debug = 1;
                break;
            case 'i':
                config_ignore_missing = 1;
                break;
            case 'l':
                config_dir_log = strdup(optarg);
                if (!config_dir_log) oom();
                break;
            case 'p':
                config_print = 1;
                config_timeout = 0;
                break;
            case 's':
                config_server_address = strdup(optarg);
                if (!config_server_address) oom();
                break;
            case 't':
                config_timeout = strtol(optarg, NULL, 0);
                break;
            case 'h':
                print_usage(argv[0]);
                exit(0);
            case 'v':
                print_version();
                exit(0);
            default:
                exit(1);
        }
    }

    // Build modules path
    size = strlen(config_dir_data) + 1 + strlen("modules") + 1;
    config_dir_modules = malloc(size);
    if (!config_dir_modules) oom();
    snprintf(config_dir_modules, size, "%s/modules", config_dir_data);
    config_dir_modules[size - 1] = '\0';

    // Build models path
    size = strlen(config_dir_data) + 1 + strlen("models") + 1;
    config_dir_models = malloc(size);
    if (!config_dir_models) oom();
    snprintf(config_dir_models, size, "%s/models", config_dir_data);
    config_dir_models[size - 1] = '\0';

    // Build scripts path
    size = strlen(config_dir_data) + 1 + strlen("scripts") + 1;
    config_dir_scripts = malloc(size);
    if (!config_dir_scripts) oom();
    snprintf(config_dir_scripts, size, "%s/scripts", config_dir_data);
    config_dir_scripts[size - 1] = '\0';

    // Build application dir
    size = strlen(config_dir_data) + 1 + strlen("apps") + 1;
    config_dir_apps = malloc(size);
    if (!config_dir_apps) oom();
    snprintf(config_dir_apps, size, "%s/apps", config_dir_data);
    config_dir_apps[size - 1] = '\0';

    // Build access.log path
    size = strlen(config_dir_log) + 1 + strlen("access.log") + 1;
    config_file_log_access = malloc(size);
    if (!config_file_log_access) oom();
    snprintf(config_file_log_access, size, "%s/access.log", config_dir_log);
    config_file_log_access[size - 1] = '\0';

    // Build trace.log path
    size = strlen(config_dir_log) + 1 + strlen("trace.log") + 1;
    config_file_log_traceback = malloc(size);
    if (!config_file_log_traceback) oom();
    snprintf(config_file_log_traceback, size, "%s/trace.log", config_dir_log);
    config_file_log_traceback[size - 1] = '\0';
}
