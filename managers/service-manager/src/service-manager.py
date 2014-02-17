#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# System
import sys
import dbus

# Pds Stuff
import servicemanager.context as ctx

# Application Stuff
import servicemanager.about as about

# Qt Stuff
from PyQt4.QtCore import SIGNAL

# Enable plugin if session is Kde4
if ctx.Pds.session == ctx.pds.Kde4:
    def CreatePlugin(widget_parent, parent, component_data):
        from servicemanager.kcmodule import ServiceManager
        return ServiceManager(component_data, parent)

if __name__ == '__main__':

    # DBUS MainLoop
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    # Pds vs KDE
    if ctx.Pds.session == ctx.pds.Kde4:

        # PyKDE4 Stuff
        from PyKDE4.kdeui import *
        from PyKDE4.kdecore import *

        # Application Stuff
        from servicemanager.standalone import ServiceManager
        from servicemanager.about import aboutData

        # Set Command-line arguments
        KCmdLineArgs.init(sys.argv, aboutData)

        # Create a Kapplitcation instance
        app = KApplication()

        # Create Main Widget
        mainWindow = ServiceManager(None, aboutData.appName)
        mainWindow.show()

    else:

        # Application Stuff
        from servicemanager.base import MainManager

        # Pds Stuff
        from pds.quniqueapp import QUniqueApplication
        from servicemanager.context import KIcon, i18n

        # Create a QUniqueApllication instance
        app = QUniqueApplication(sys.argv, catalog=about.appName)

        # Create Main Widget and make some settings
        mainWindow = MainManager(None)
        mainWindow.show()
        mainWindow.resize(640, 480)
        mainWindow.setWindowTitle(i18n(about.PACKAGE))
        mainWindow.setWindowIcon(KIcon(about.icon))

    # Create connection for lastWindowClosed signal to quit app
    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

    # Run the applications
    app.exec_()
