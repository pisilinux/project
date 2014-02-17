#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import fcntl
import grp
import os
import pwd
import socket
import subprocess
import time

class execReply(int):
    def __init__(self, value):
        super(execReply, self).__init__(value)
        self.stdout = None
        self.stderr = None

def synchronized(func):
    """Syncronize method call with a per method lock.
    
    This decorator makes sure that only one instance of the script's
    method run in any given time.
    """
    class Handler:
        def handler(self, *args, **kwargs):
            lock = FileLock("/var/lock/subsys/%s.comar" % script())
            lock.lock()
            self.myfunc(*args, **kwargs)
            lock.unlock()
    h = Handler()
    h.myfunc = func
    return h.handler

def run(*cmd, **settings):
    """Run a command without running a shell"""
    if "chuid" in settings:
        changeUID(settings["chuid"])

    command = []
    if len(cmd) == 1:
        if isinstance(cmd[0], basestring):
            command = cmd[0].split()
        else:
            command = cmd[0]
    else:
        command = cmd
    proc = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    reply = execReply(proc.wait())
    reply.stdout, reply.stderr = proc.communicate()
    return reply

def waitBus(unix_name, timeout=5, wait=0.1, stream=True):
    if stream:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    else:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    while timeout > 0:
        try:
            sock.connect(unix_name)
            return True
        except:
            timeout -= wait
        time.sleep(wait)
    return False

class FileLock:
    def __init__(self, filename):
        self.filename = filename
        self.fd = None

    def lock(self, shared=False, timeout=-1):
        _type = fcntl.LOCK_EX
        if shared:
            _type = fcntl.LOCK_SH
        if timeout != -1:
            _type |= fcntl.LOCK_NB

        self.fd = os.open(self.filename, os.O_WRONLY | os.O_CREAT, 0600)
        if self.fd == -1:
            raise IOError, "Cannot create lock file"

        while True:
            try:
                fcntl.flock(self.fd, _type)
                return
            except IOError:
                if timeout > 0:
                    time.sleep(0.2)
                    timeout -= 0.2
                else:
                    raise

    def unlock(self):
        fcntl.flock(self.fd, fcntl.LOCK_UN)

def changeUID(chuid):
    """Change to this chuid (user:group)"""
    c_user = chuid
    c_group = None
    if ":" in c_user:
        c_user, c_group = c_user.split(":", 1)
    cpw = pwd.getpwnam(c_user)
    c_uid = cpw.pw_uid
    if c_group:
        cgr = grp.getgrnam(c_group)
        c_gid = cgr.gr_gid
    else:
        c_gid = cpw.pw_gid
        c_group = grp.getgrgid(cpw.pw_gid).gr_name

    c_groups = []
    for item in grp.getgrall():
        if c_user in item.gr_mem:
            c_groups.append(item.gr_gid)
    if c_gid not in c_groups:
        c_groups.append(c_gid)

    os.setgid(c_gid)
    os.setgroups(c_groups)
    os.setuid(c_uid)
