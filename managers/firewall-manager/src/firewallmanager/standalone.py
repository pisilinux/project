#!/usr/bin/python
# -*- coding: utf-8 -*-

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import KGlobal
from main import * 
class FirewallManager(KMainWindow):
    
    def __init__(self, parent=None):
        KMainWindow.__init__(self, parent)
        self.setWindowIcon(KIcon("security-high"))
        widget = MainWidget(self)
        KGlobal.locale().insertCatalog("firewall-manager")
        self.resize(widget.size())
        self.setCentralWidget(widget)

class Module(KCModule):
    def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        KGlobal.locale().insertCatalog(catalog)

        if not dbus.get_default_main_loop():
            from dbus.mainloop.qt import DBusQtMainLoop
            DBusQtMainLoop(set_as_default=True)

        MainWidget(self, embed=True)

