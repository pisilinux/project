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

#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>
#include <sys/stat.h>
#include <errno.h>
#include <dirent.h>
#include <unistd.h>

#include "log.h"

//! Out of memory, panic!
void
oom()
{
    /*!
     * Logs "out of memory" message and exits.
     *
     */

    log_error("Out of memory\n");
    exit(1);
}

//! Return content of a file
char *
load_file(const char *fname, int *sizeptr)
{
    /*!
     * Returns content of a file. Memory required obtained with malloc() 
     * and needs to be freed.
     *
     * @fname File name
     * @sizeptr Size pointer of file content
     * @return File content, NULL on error
     *
     */

    FILE *f;
    struct stat fs;
    size_t size;
    char *data;

    if (stat(fname, &fs) != 0) return NULL;
    size = fs.st_size;
    if (sizeptr) *sizeptr = size;

    data = malloc(size + 1);
    if (!data) oom();
    memset(data, 0, size + 1);

    f = fopen(fname, "rb");
    if (!f) {
        free(data);
        return NULL;
    }
    if (fread(data, size, 1, f) < 1) {
        free(data);
        return NULL;
    }
    fclose(f);

    return data;
}

//! Checks directory
int
check_dir(char *dir)
{
    /*!
     * Checks existance of a directory, and logs an error message
     * if necessary.
     *
     * @dir Path
     * @return 0 on success, -1 on error
     *
     */

    struct stat fs;

    if (stat(dir, &fs) != 0) {
        log_error("Missing directory: '%s'\n", dir);
        return -1;
    } else {
        if (0 != access(dir, W_OK)) {
            log_error("Cannot write directory: '%s'\n", dir);
            return -1;
        }
        else if (0 != access(dir, R_OK)) {
            log_error("Cannot read directory: '%s'\n", dir);
            return -1;
        }
    }

    return 0;
}

//! Creates directory
int
create_dir(char *dir)
{
    /*!
     * Checks existance of a directory, creates if missing. Also
     * logs an error message if necessary.
     *
     * @dir Path
     * @return 0 on success, -1 on error
     *
     */

    struct stat fs;

    if (stat(dir, &fs) != 0) {
        if (0 != mkdir(dir, S_IRWXU)) {
            log_error("Cannot create directory: '%s'\n", dir);
            return -1;
        }
    } else {
        if (0 != access(dir, W_OK)) {
            log_error("Cannot write directory: '%s'\n", dir);
            return -1;
        }
    }

    return 0;
}

//! Returns a part of a string.
char *
strsub(const char *str, int start, int end)
{
    /*!
     * Returns a part of a string.
     *
     * @str String
     * @start Where to start
     * @end Where to end
     * @return Requested part
     */
    char *new_src, *t;

    /*
    if (start < 0) {
        start = strlen(str) + start;
    }
    if (start > strlen(str)) {
        start = 0;
    }
    if (end == 0) {
        end = strlen(str);
    }
    else if (end < 0) {
        end = strlen(str) + end;
    }
    if (end > strlen(str)) {
        end = strlen(str);
    }
    */

    new_src = malloc(end - start + 2);
    for (t = (char *) str + start; t < str + end; t++) {
        new_src[t - (str + start)] = *t;
    }
    new_src[t - (str + start)] = '\0';
    return new_src;
}
