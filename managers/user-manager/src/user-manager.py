#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import sys
import dbus

from PyQt4 import QtGui
from PyQt4 import QtCore

from usermanager.about import *
from usermanager.main import MainWidget

#PDS Stuff

import usermanager.context as ctx
from usermanager.context import *


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        widget = MainWidget(self)
        self.resize(widget.size())
        self.setCentralWidget(widget)


if __name__ == "__main__":
   
    #DBUS MainLoop
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    if ctx.Pds.session==ctx.pds.Kde4:
        #User Manager PyKDE4 Stuff
       
        from PyKDE4.kdeui import KMainWindow,KApplication,KCModule,KIcon
        from PyKDE4.kdecore import KCmdLineArgs,KGlobal

        #Set Command Line arguments
        KCmdLineArgs.init(sys.argv,aboutData)
        #Create a KApplication instance
        app=KApplication()
        window = MainWindow()
        print "tayfur"
        window.show()
        #Run the application
        app.exec_()
    else:
        import gettext

        __trans=gettext.translation('user-manager',fallback=True)
        i18n=__trans.ugettext

        from pds.quniqueapp import QUniqueApplication
        app=QUniqueApplication(sys.argv, catalog='user-manager')
        window=MainWindow()
        window.show()
        window.resize(680,500)
        window.setWindowTitle(i18n('User Manager'))
        window.setWindowIcon(KIcon('computer'))
        app.exec_()
"""
class Module(KCModule):
   def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        KGlobal.locale().insertCatalog(catalog)

        if not dbus.get_default_main_loop():
            from dbus.mainloop.qt import DBusQtMainLoop
            DBusQtMainLoop(set_as_default = True)

        MainWidget(self, embed=True)
"""
#def CreatePlugin(widget_parent, parent, component_data):
    # return Module(component_data, parent)
