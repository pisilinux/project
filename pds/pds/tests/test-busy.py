#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# The QProgressIndicator class lets an application display a progress
# indicator to show that a lengthy task is under way.
# QProgressIndicator is based on http://qt-apps.org/content/show.php?content=115762

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

from PyQt4 import QtCore, QtGui
from pds.qprogressindicator import QProgressIndicator

class UI(QtGui.QWidget):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.gl = QtGui.QGridLayout(self)

        butonh = QtGui.QPushButton("click to hide", self)
        butons = QtGui.QPushButton("click to show", self)
        self.busy = QProgressIndicator(self)

        self.gl.addWidget(butonh)
        self.gl.addWidget(self.busy)
        self.gl.addWidget(butons)

        self.busy.startAnimation()
        butonh.clicked.connect(self.busy.stopAnimation)
        butons.clicked.connect(self.busy.startAnimation)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())

