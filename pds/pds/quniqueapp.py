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
import signal

# PyQt4 Core Libraries
from PyQt4 import QtNetwork
from PyQt4.QtGui import QApplication

from PyQt4.QtCore import QLocale
from PyQt4.QtCore import QIODevice
from PyQt4.QtCore import QTranslator
from PyQt4.QtCore import QLibraryInfo

class QUniqueApplication(QApplication):

    def __init__(self, argv, catalog):
        QApplication.__init__(self, argv)
        self.aboutToQuit.connect(self.cleanup)
        self.control = QtNetwork.QLocalServer(self)
        self.control.newConnection.connect(self.onControlConnect)
        self.mainwindow = None
        self.catalog = '%s-pds.socket' % catalog

        self._init_translations()

        self.readyToRun = self.control.listen(self.catalog)

        if not self.readyToRun:
            if self.sendToInstance('show-mainwindow'):
                sys.exit()
            else:
                self.control.removeServer(self.catalog)
                self.readyToRun = self.control.listen(self.catalog)

    def _init_translations(self):
        self.qTrans = QTranslator()
        self.qTrans.load("qt_" + QLocale.system().name(),
                QLibraryInfo.location(QLibraryInfo.TranslationsPath))
        self.installTranslator(self.qTrans)

    def setMainWindow(self, window):
        self.mainwindow = window

    def exec_(self):
        if self.readyToRun:
            # Let Ctrl+C work ;)
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            QApplication.exec_()

    def cleanup(self):
        self.control.removeServer(self.catalog)

    def sendToInstance(self, data = ''):
        socket = QtNetwork.QLocalSocket()
        socket.connectToServer(self.catalog, QIODevice.WriteOnly)
        if socket.waitForConnected( 500 ):
            if len(data) > 0:
                socket.write(data)
                socket.flush()
            socket.close()
            return True
        return False

    def onControlConnect(self):
        self.socket = self.control.nextPendingConnection()
        self.socket.readyRead.connect(self.onControlRequest)

    def onControlRequest(self):
        request = self.socket.readAll()
        for cmd in request.split(' '):
            self.parseCommand(cmd)
        self.socket.flush()
        self.socket.close()
        self.socket.deleteLater()

    def parseCommand(self, cmd):
        if cmd == 'show-mainwindow':
            if hasattr(self.mainwindow, 'show'):
                self.mainwindow.show()

