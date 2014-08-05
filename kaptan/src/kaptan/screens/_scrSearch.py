# -*- coding: utf-8 -*-
#
# Copyright (C) 2012, The Chakra Developers
#
# This is a fork of Pardus's Kaptan, which is
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4 import QtGui
from PyQt4.QtCore import *

from PyKDE4.kdecore import ki18n, KConfig, KProcess

from PyKDE4 import kdeui

from kaptan.screen import Screen
from kaptan.screens.ui_scrSearch import Ui_searchWidget

import subprocess

class Widget(QtGui.QWidget, Screen):
    title = ki18n("Search")
    desc = ki18n("Enable / Disable Strigi Desktop Search")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_searchWidget()
        self.ui.setupUi(self)

        # set initial states
        self.ui.checkBoxNepomuk.setChecked(True)

        # set signals
        self.ui.checkBoxNepomuk.connect(self.ui.checkBoxNepomuk, SIGNAL("toggled(bool)"), self.enableSearch)

    def enableSearch(self):
        if self.ui.showTray.isChecked():
            self.ui.checkUpdate.setVisible(True)
            self.ui.updateInterval.setVisible(True)
        else:
            self.ui.checkUpdate.setChecked(False)
            self.ui.checkUpdate.setVisible(False)
            self.ui.checkUpdate.setCheckState(Qt.Unchecked)
            self.ui.updateInterval.setVisible(False)

    def updateSelected(self):
        #if self.ui.checkUpdate.isChecked():
        #    self.ui.updateInterval.setEnabled(True)
        #else:
        #    self.ui.updateInterval.setEnabled(False)
        # TODO: Where are Nepomuk/Strigi settings stored?
        print "This part still needs to be written."

    def applySettings(self):
        # write selected configurations to future package-managerrc
        config = PMConfig()
        config.setSystemTray(QVariant(self.ui.showTray.isChecked()))
        config.setUpdateCheck(QVariant(self.ui.checkUpdate.isChecked()))
        config.setUpdateCheckInterval(QVariant(self.ui.updateInterval.value() * 60))

        if self.ui.showTray.isChecked():
            p = subprocess.Popen(["spun"], stdout=subprocess.PIPE)

    def shown(self):
        pass

    def execute(self):
        self.applySettings()
        return True

class Config:
    def __init__(self, config):
        self.config = KConfig(config)
        self.group = None

    def setValue(self, option, value):
        self.group = self.config.group("General")
        self.group.writeEntry(option, QVariant(value))
        self.config.sync()

class PMConfig(Config):
    def __init__(self):
        Config.__init__(self, "package-managerrc")

    def setSystemTray(self, enabled):
        self.setValue("SystemTray", enabled)

    def setUpdateCheck(self, enabled):
        self.setValue("UpdateCheck", enabled)

    def setUpdateCheckInterval(self, value):
        self.setValue("UpdateCheckInterval", value)
