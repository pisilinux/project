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

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# Pds vs KDE
import servicemanager.context as ctx
if ctx.Pds.session == ctx.pds.Kde4:
    from PyKDE4.kdeui import KIcon
    from PyKDE4.kdecore import i18n
else:
    from servicemanager.context import KIcon, i18n

# Application Stuff
from servicemanager.ui_item import Ui_ServiceItemWidget
from servicemanager.ui_info import Ui_InfoWidget

# PDS Stuff
from pds.gui import *
from pds.qprogressindicator import QProgressIndicator

# Python Stuff
import time
import textwrap
import locale

# Pisi Stuff
import pisi

class ServiceItem(QtGui.QListWidgetItem):

    def __init__(self, package, parent):
        QtGui.QListWidgetItem.__init__(self, parent)

        self.package = package

class ServiceItemWidget(QtGui.QWidget):

    def __init__(self, package, parent, item):
        QtGui.QWidget.__init__(self, None)

        self.ui = Ui_ServiceItemWidget()
        self.ui.setupUi(self)

        self.busy = QProgressIndicator(self)
        self.busy.setMinimumSize(QtCore.QSize(32, 32))
        self.ui.mainLayout.insertWidget(0, self.busy)
        self.ui.spacer.hide()
        self.busy.hide()

        self.ui.labelName.setText(package)

        self.toggleButtons()

        self.ui.buttonStart.setIcon(KIcon("media-playback-start"))
        self.ui.buttonStop.setIcon(KIcon("media-playback-stop"))
        self.ui.buttonReload.setIcon(KIcon("view-refresh"))
        self.ui.buttonInfo.setIcon(KIcon("dialog-information"))

        self.toggled = False
        self.root = parent
        self.iface = parent.iface
        self.item = item
        self.package = package
        self.info = ServiceItemInfo(self)

        self.type = None
        self.desc = None
        self.connect(self.ui.buttonStart, SIGNAL("clicked()"), self.setService)
        self.connect(self.ui.buttonStop, SIGNAL("clicked()"), self.setService)
        self.connect(self.ui.buttonReload, SIGNAL("clicked()"), self.setService)
        self.connect(self.ui.checkStart, SIGNAL("clicked()"), self.setService)
        self.connect(self.ui.buttonInfo, SIGNAL("clicked()"), self.info.showDescription)

    def updateService(self, data, firstRun):
        self.type, self.desc, serviceState = data
        self.setState(serviceState, firstRun)
        self.ui.labelDesc.setText(self.desc)

    def setState(self, state, firstRun=False):
        if not firstRun:
            # There is a raise condition, FIXME in System.Service
            time.sleep(1)
            state = self.iface.info(self.package)[2]
        if state in ('on', 'started', 'conditional_started'):
            self.running = True
            icon = 'flag-green'
        else:
            self.running = False
            icon = 'flag-black'

        self.ui.buttonStop.setEnabled(self.running)
        self.ui.buttonReload.setEnabled(self.running)

        self.ui.labelStatus.setPixmap(KIcon(icon).pixmap(32, 32))
        self.showStatus()
        self.runningAtStart = False
        if state in ('on', 'stopped'):
            self.runningAtStart = True
        elif state in ('off', 'started', 'conditional_started'):
            self.runningAtStart = False
        self.ui.checkStart.setChecked(self.runningAtStart)
        self._last_state = self.ui.checkStart.isChecked()
        # print self.package, state

    def setService(self):
        try:
            self.showBusy()
            self._last_state = not self.ui.checkStart.isChecked()
            if self.sender() == self.ui.buttonStart:
                self.iface.start(self.package)
            elif self.sender() == self.ui.buttonStop:
                self.iface.stop(self.package)
            elif self.sender() == self.ui.buttonReload:
                self.iface.restart(self.package)
            elif self.sender() == self.ui.checkStart:
                self.iface.setEnable(self.package, self.ui.checkStart.isChecked())
        except Exception, msg:
            self.showStatus()
            self.root.showFail(msg)

    def switchToOld(self):
        self.ui.checkStart.setChecked(self._last_state)

    def showStatus(self):
        self.busy.hide()
        self.ui.spacer.hide()
        self.ui.labelStatus.show()

    def showBusy(self):
        self.busy.busy()
        self.ui.spacer.show()
        self.ui.labelStatus.hide()

    def enterEvent(self, event):
        if not self.toggled:
            self.toggleButtons(True)
            self.toggled = True

    def leaveEvent(self, event):
        if self.toggled:
            self.toggleButtons()
            self.toggled = False

    def toggleButtons(self, toggle=False):
        self.ui.buttonStart.setVisible(toggle)
        self.ui.buttonReload.setVisible(toggle)
        self.ui.buttonStop.setVisible(toggle)
        self.ui.buttonInfo.setVisible(toggle)
        self.ui.checkStart.setVisible(toggle)

def getDescription(service):
    try:
        # TODO add a package map for known services
        service = service.replace('_','-')
        lang = str(locale.getdefaultlocale()[0].split("_")[0])
        desc = pisi.api.info_name(service)[0].package.description
        if desc.has_key(lang):
            return unicode(desc[lang])
        return unicode(desc['en'])
    except Exception, msg:
        # print "ERROR:", msg
        return unicode(i18n('Service information is not available'))

class ServiceItemInfo(PAbstractBox):

    def __init__(self, parent):
        PAbstractBox.__init__(self, parent)

        self.ui = Ui_InfoWidget()
        self.ui.setupUi(self)
        self.ui.buttonHide.clicked.connect(self.hideDescription)
        self.ui.buttonHide.setIcon(KIcon("dialog-close"))

        self._animation = 2
        self._duration = 500

        self.enableOverlay()
        self.hide()

    def showDescription(self):
        self.resize(self.parentWidget().size())
        desc = getDescription(self.parentWidget().package)
        self.ui.description.setText(desc)
        self.ui.description.setToolTip('\n'.join(textwrap.wrap(desc)))
        self.animate(start = MIDLEFT, stop = MIDCENTER)
        QtGui.qApp.processEvents()

    def hideDescription(self):
        if self.isVisible():
            self.animate(start = MIDCENTER,
                         stop  = MIDRIGHT,
                         direction = OUT)

