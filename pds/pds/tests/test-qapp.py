#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

import sys
from pds.quniqueapp import QUniqueApplication

app = QUniqueApplication(sys.argv, catalog = 'test-app')

if app.readyToRun:
    print 'Application started !'

app.exec_()
