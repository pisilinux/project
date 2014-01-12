#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Copyright (C) 2011, TUBITAK/UEKAE
# 2011 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# D-Bus
import dbus
from dbus.mainloop.qt import DBusQtMainLoop

# Qt Libraries
from PyQt4 import QtGui
from PyQt4.QtCore import *

# UI
from pds.ui.ui_connectionitem import Ui_ConnectionItem

# Pds
from pds.gui import *
from pds.qiconloader import QIconLoader
from pds.qprogressindicator import QProgressIndicator

QIconLoader = QIconLoader()

# NetworkManager
from networkmanager import State
from networkmanager import NetworkManager
from networkmanager import ActiveConnectionState

NM_BUS_NAME = 'org.freedesktop.NetworkManager'
NM_OBJECT_PATH = '/org/freedesktop/NetworkManager'
NM_SETTINGS_OBJECT_PATH = '/org/freedesktop/NetworkManagerSettings'

NM_SETTINGS = 'org.freedesktop.NetworkManagerSettings'
NM_INTERFACE = 'org.freedesktop.NetworkManager'
NM_SETTINGS_CONNECTION = 'org.freedesktop.NetworkManagerSettings.Connection'

def get_icon(conn_type, state = False):
    state = ("dialog-ok", "ok") if state else None

    CONN_TYPES = {"802-11-wireless":
                    QIconLoader.loadOverlayed("network-wireless", state, 32, position = QIconLoader.TopLeft),
                  "802-3-ethernet" :
                    QIconLoader.loadOverlayed("network-wired", state, 32, position = QIconLoader.TopLeft)}

    return CONN_TYPES.get(conn_type,
                QIconLoader.loadOverlayed("network-wired", state, 32, position = QIconLoader.TopLeft))

class ConnectionItem(QtGui.QWidget, Ui_ConnectionItem):

    def __init__(self, parent, connection):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.available = True
        self.parent = parent
        self.connection = connection

        bus = parent.bus.get_object(NM_BUS_NAME, str(connection.proxy.object_path))
        interface = dbus.Interface(bus, NM_SETTINGS_CONNECTION)

        interface.connect_to_signal("Removed", parent.fillConnections)
        interface.connect_to_signal("Updated", self.updateState)

        self.busy = QProgressIndicator(self)
        self.busy.setMinimumSize(QSize(32, 32))
        self.mainLayout.insertWidget(0, self.busy)
        self.busy.hide()

        self.connect(parent, SIGNAL("stateChanged()"), self.updateState)
        self.button.clicked.connect(lambda: self.parent.setState(self))

        self.updateState()
        self.toggleButtons()

    def updateState(self, *args):
        if self.available is not True:
            return

        active = self.parent.isActive(self.connection)

        if active:
            state = self.parent.getState(self.connection)
            if state == ActiveConnectionState.ACTIVATED.value:
                self.setIcon(get_icon(self.connection.settings.conn_type, True))
            elif state == ActiveConnectionState.ACTIVATING.value:
                self.showBusy()
        else:
            self.setIcon(get_icon(self.connection.settings.conn_type, False))

        self.name.setText(unicode(self.connection.settings.id))
        self.details.setText(unicode(self.connection.settings.conn_type))
        self.button.setText("Disconnect" if active else "Connect")

    def showBusy(self):
        self.busy.busy()
        self.icon.hide()

    def setIcon(self, icon):
        self.busy.hide()
        self.icon.setPixmap(icon)
        self.icon.show()

    def resizeEvent(self, event):
        if self.parent.msgbox:
            self.parent.msgbox._resizeCallBacks(event)

    def enterEvent(self, event):
        if not self.button.isVisible():
            self.toggleButtons(True)

    def leaveEvent(self, event):
        if self.button.isVisible():
            self.toggleButtons()

    def toggleButtons(self, toggle=False):
        self.button.setVisible(toggle)

class QNetworkManager(QtGui.QListWidget):

    def __init__(self, parent = None):
        QtGui.QListWidget.__init__(self, parent)
        self.setAlternatingRowColors(True)

        self.nm = NetworkManager()

        self.bus = dbus.SystemBus()
        nm_bus = self.bus.get_object(NM_BUS_NAME, NM_OBJECT_PATH)

        nm_interface = dbus.Interface(nm_bus, NM_INTERFACE)
        nm_interface.connect_to_signal("DeviceAdded", lambda *args: self.showMessage("A new device added.", True))
        nm_interface.connect_to_signal("DeviceAdded", self.fillConnections)
        nm_interface.connect_to_signal("DeviceRemoved", lambda *args: self.showMessage("A device removed.", True))
        nm_interface.connect_to_signal("DeviceRemoved", self.fillConnections)
        nm_interface.connect_to_signal("PropertiesChanged", lambda *args: self.emit(SIGNAL("stateChanged()")))

        nm_settings_bus = self.bus.get_object(NM_BUS_NAME, NM_SETTINGS_OBJECT_PATH)
        nm_settings = dbus.Interface(nm_settings_bus, NM_SETTINGS)
        nm_settings.connect_to_signal("NewConnection", lambda *args: self.showMessage("A new connection added.", True))
        nm_settings.connect_to_signal("NewConnection", self.fillConnections)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hideMessage)

        self.msgbox = None
        self.fillConnections()

    def isActive(self, connection):
        if not self.nm.active_connections:
            return False
        return len(self.filterByConnection(connection)) > 0

    def getState(self, connection):
        return self.filterByConnection(connection)[0].state.value

    def filterByConnection(self, connection):
        return filter(lambda x: x.connection.settings.uuid == \
                                  connection.settings.uuid and \
                        unicode(x.connection.settings.id) == \
                          unicode(connection.settings.id), self.nm.active_connections)

    def fillConnections(self, *args):
        self.clearList()
        actives = self.nm.active_connections
        for connection in self.nm.connections:
            item = QtGui.QListWidgetItem()
            item.setSizeHint(QSize(200, 38))
            self.addItem(item)
            self.setItemWidget(item, ConnectionItem(self, connection))

    def clearList(self):
        for i in range(self.count()):
            item = self.item(i)
            widget = self.itemWidget(item)
            widget.available = False
            del widget, item
        self.clear()

    def hideMessage(self):
        if self.msgbox.isVisible():
            self.msgbox.animate(start = CURRENT, stop = BOTCENTER, direction = OUT)

    def showMessage(self, message, timed=False):
        if not self.msgbox:
            self.msgbox = PMessageBox(self.viewport())
            self.msgbox.setStyleSheet(PMessageBox.Style)

        self.msgbox.setMessage(message)
        self.msgbox.animate(start = BOTCENTER, stop = BOTCENTER)

        if timed:
            self.timer.start(2000)

    def setState(self, sender):
        if self.isActive(sender.connection):
            self.disconnect(sender.connection)
        else:
            self.connect(sender.connection)

    def disconnect(self, connection):
        self.nm.disconnect_connection_devices(connection)
        self.showMessage("Disconnected from %s... " % connection.settings.id, True)

    def connect(self, connection):
        if connection in self.nm.available_connections:
            self.nm.activate_connection(connection)
            self.showMessage("Connecting to %s... " % connection.settings.id, True)
        else:
            self.showMessage("Device is not ready for %s connection." % connection.settings.id, True)

# Basic test app
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DBusQtMainLoop(set_as_default = True)
    nm = QNetworkManager()
    nm.show()
    sys.exit(app.exec_())

