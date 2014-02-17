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

"""deviceutils module provides device information utilities."""

import os

sysfs_path = "/sys"

def sysValue(*paths):
    path = os.path.join(sysfs_path, *paths)
    f = file(path)
    data = f.read().rstrip("\n")
    f.close()
    return data

def idsQuery(name, vendor, device):
    f = file(name)
    flag = 0
    company = ""
    for line in f.readlines():
        if flag == 0:
            if line.startswith(vendor):
                flag = 1
                company = line[5:].strip()
        else:
            if line.startswith("\t"):
                if line.startswith("\t" + device):
                    return "%s - %s" % (line[6:].strip(), company)
            elif not line.startswith("#"):
                flag = 0
    if company != "":
        return "%s (%s)" % (company, device)
    else:
        return "Unknown (%s:%s)" % (vendor, device)
