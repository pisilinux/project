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
#include "log.h"
#include "loop.h"
#include "process.h"
#include "script.h"
#include "utils.h"

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int
main(int argc, char *argv[])
{
    // Configuration
    config_init(argc, argv);

    // Got root?
    if (getuid() != 0) {
        log_error("System service should be started as root.\n");
        exit(1);
    }

    // Check directories
    if (check_dir(config_dir_data) != 0 || check_dir(config_dir_models) != 0 || check_dir(config_dir_modules) != 0) {
        exit(1);
    }

    // Create directories
    if (create_dir(config_dir_scripts) != 0 || create_dir(config_dir_apps) != 0 || create_dir(config_dir_log) != 0) {
        exit(1);
    }

    // If "--print" is not used, log to file from this moment
    if (config_print == 0) {
        config_runlevel = 1;
    }

    log_debug("Initializing...\n");
    log_debug("\n");

    log_debug("Modules directory          : %s\n", config_dir_modules);
    log_debug("Models directory           : %s\n", config_dir_models);
    log_debug("Scripts directory          : %s\n", config_dir_scripts);
    log_debug("Access log                 : %s\n", config_file_log_access);
    log_debug("Trace log                  : %s\n", config_file_log_traceback);
    log_debug("\n");

    // Initialize Python VM
    if (script_init() != 0) {
        exit(1);
    }

    // Initialize parent process
    proc_init();

    // Enter main loop
    loop_exec();

    // Finalize Python VM
    script_finalize();

    return 0;
}
