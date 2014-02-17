# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

modules_s = set(dir())
from pardus import *
modules_s = set(dir()) - modules_s - set(["modules_s"])

import inspect
import re


def print_functions(m):
    for f in inspect.getmembers(m, inspect.isfunction):

        print f[0],
        args = inspect.getargspec(f[1])[0]
        if args:
            print "(" + ",".join(args) + ")"
        else:
            print "()"

        doc = inspect.getdoc(f[1])
        if doc:
            print doc
        print

def print_modules(modules):
    for m in modules:
        s = `m`
        r = re.compile("module '.*' from").search(s)
        print s[r.start():r.end()][:-5].capitalize()
        print "-"*40
        print m.__doc__
        print

        pkg_modules = [x[1] for x in inspect.getmembers(m, inspect.ismodule)
                       if "site-packages/pardus" in `x[1]` and x[0]]
        print_modules(pkg_modules)

        print_functions(m)
        print
        print

if __name__ == "__main__":
    modules = []
    for s in modules_s:
        modules.append(__import__("pardus."+s, globals(), locals(), [""]))
    print_modules(modules)    
