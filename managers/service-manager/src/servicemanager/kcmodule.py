#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

# DBUS
import dbus

# Service Manager
from servicemanager.base import MainManager

class ServiceManager(KCModule):
    def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        # This is very important for translations when running as kcm_module
        KGlobal.locale().insertCatalog("service-manager")

        if not dbus.get_default_main_loop():
            from dbus.mainloop.qt import DBusQtMainLoop
            DBusQtMainLoop(set_as_default = True)

        MainManager(self, standAlone = False)

