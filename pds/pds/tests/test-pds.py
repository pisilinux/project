#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services Test-Suit
# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

import pds

from time import time
from PyQt4 import QtCore, QtGui
from pds.qiconloader import QIconLoader

class Ui_Test(object):
    def setupUi(self, Test):
        Test.setObjectName("Test")
        Test.resize(460, 300)
        self.gridLayout = QtGui.QGridLayout(Test)
        self.gridLayout.setObjectName("gridLayout")
        self.name = QtGui.QComboBox(Test)
        self.name.setObjectName("name")
        self.name.setEditable(True)
        self.gridLayout.addWidget(self.name, 0, 0, 1, 1)
        self.size = QtGui.QComboBox(Test)
        self.size.setObjectName("size")
        self.size.setMaximumSize(QtCore.QSize(100, 16777215))
        self.size.addItem("128")
        self.size.addItem("64")
        self.size.addItem("48")
        self.size.addItem("32")
        self.size.addItem("22")
        self.size.addItem("16")
        self.gridLayout.addWidget(self.size, 0, 1, 1, 1)
        self.getButton = QtGui.QPushButton(Test)
        self.getButton.setText("Get Icon")
        self.getButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.gridLayout.addWidget(self.getButton, 0, 2, 1, 1)
        self.label = QtGui.QLabel(Test)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 3)
        self.getButton.clicked.connect(self.showIcon)
        QtCore.QMetaObject.connectSlotsByName(Test)

        Pds = pds.Pds(debug = True)
        # Force to use Default Session for testing
        # Pds.session = pds.DefaultDe

        self.loader = QIconLoader(Pds, debug = True)
        completer = QtGui.QCompleter(self.loader._available_icons)
        self.name.setCompleter(completer)
        self.getButton.setShortcut("Return")

        print "Desktop Session :", self.loader.pds.session.Name
        print "Desktop Version :", self.loader.pds.session.Version
        print "Icon Paths      :", self.loader.iconDirs
        print "Theme           :", self.loader.themeName

    def showIcon(self):
        a = time()
        print "Clicked !"
        icons = unicode(self.name.currentText())
        self.label.setPixmap(self.loader.load(icons.split(','), 
            self.size.currentText()))
        print 'It took : ', time() - a

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Test = QtGui.QWidget()
    a = time()
    print "Started !"
    ui = Ui_Test()
    ui.setupUi(Test)
    Test.show()
    print 'It took : ', time() - a
    sys.exit(app.exec_())

