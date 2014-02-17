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

#include "process.h"
#include "log.h"
#include "utils.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/poll.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

struct Proc my_proc;

struct ProcChild *
add_child(pid_t pid, int from, DBusMessage *bus_msg)
{
    int i;

    i = my_proc.nr_children;
    if (i >= my_proc.max_children) {
        if (i == 0) {
            my_proc.max_children = 4;
        } else {
            my_proc.max_children *= 2;
        }
        my_proc.children = realloc(my_proc.children, my_proc.max_children * sizeof(struct ProcChild));
        if (!my_proc.children) oom();
    }

    memset(&my_proc.children[i], 0, sizeof(struct ProcChild));
    my_proc.children[i].from = from;
    my_proc.children[i].pid = pid;
    my_proc.children[i].bus_msg = bus_msg;
    ++my_proc.nr_children;
    return &my_proc.children[i];
}

void
rem_child(int nr)
{
    int status;
    waitpid(my_proc.children[nr].pid, &status, 0);
    close(my_proc.children[nr].from);
    --my_proc.nr_children;
    if (0 == my_proc.nr_children) return;
    (my_proc.children)[nr] = (my_proc.children)[my_proc.nr_children];
}

int
proc_init()
{
    memset(&my_proc, 0, sizeof(struct Proc));
    my_proc.parent.from = -1;
    my_proc.max_children = 8;
    my_proc.bus_msg = NULL;
    my_proc.children = calloc(8, sizeof(struct ProcChild));
    if (!my_proc.children) oom();
    return 0;
}

void
stop_children(void)
{
}

void
proc_finish(void)
{
    if (my_proc.nr_children) stop_children();
    exit(0);
}

static void
handle_sigterm(int signum)
{
}

void
handle_signals(void)
{
    struct sigaction act;
    struct sigaction ign;
    struct sigaction dfl;

    act.sa_handler = handle_sigterm;
    /*! initialize and empty a signal set. Signals are to be blocked while executing handle_sigterm */
    sigemptyset(&act.sa_mask);
    act.sa_flags = 0; /*!< special flags */

    ign.sa_handler = SIG_IGN;
    sigemptyset(&ign.sa_mask);
    ign.sa_flags = 0;

    dfl.sa_handler = SIG_DFL;
    sigemptyset(&dfl.sa_mask);
    dfl.sa_flags = 0;

    sigaction(SIGTERM, &act, NULL);
    sigaction(SIGPIPE, &ign, NULL);
    sigaction(SIGINT, &dfl, NULL);
}

struct ProcChild *
proc_fork(void (*child_func)(DBusMessage *msg), DBusMessage *msg)
{
    pid_t pid;
    int pfd[2];

    dbus_message_ref(msg);

    pipe(pfd);
    pid = fork();
    if (pid == -1) {
        return NULL;
    }
    if (pid == 0) {
        close(pfd[1]);
        fcntl(pfd[0], F_SETFD, FD_CLOEXEC);

        memset(&my_proc, 0, sizeof(struct Proc));
        my_proc.parent.from = pfd[0];
        my_proc.parent.pid = getppid();

        my_proc.bus_msg = msg;

        handle_signals();

        child_func(msg);
        close(pfd[0]);
        proc_finish();

        while (1) {} // to keep gcc happy
    } else {
        // parent process continues
        close(pfd[0]);
        return add_child(pid, pfd[1], msg);
    }
}
