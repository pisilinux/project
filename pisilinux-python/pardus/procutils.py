# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

"""procutils module provides basic process utilities."""

import subprocess


def capture(*cmd):
    """Capture output of the command without running a shell"""
    a = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return a.communicate()

def run(*cmd):
    """Run a command without running a shell, only output errors"""
    f = file("/dev/null", "w")
    return subprocess.call(cmd, stdout=f)

def run_full(*cmd):
    """Run a command without running a shell, with full output"""
    return subprocess.call(cmd)

def run_quiet(*cmd):
    """Run the command without running a shell and no output"""
    f = file("/dev/null", "w")
    return subprocess.call(cmd, stdout=f, stderr=f)

