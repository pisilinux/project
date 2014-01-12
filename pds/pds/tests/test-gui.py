# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

from PyQt4 import QtCore, QtGui
from pds.gui import *
from pds.tests.ui_gui import Ui_PdsTest

class PTestUI(QtGui.QWidget):

    STYLE = """color:white;
               font-size:16pt;
               background-color:rgba(0,0,0,200);
               border: 1px solid rgba(0,0,0,200);
               border-radius:4px;"""

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_PdsTest()
        self.ui.setupUi(self)

        self.ui.showButton.clicked.connect(self.showClicked)
        self.ui.hideButton.clicked.connect(self.hideClicked)

        self.msg = None

    def act(self, obj, direction):
        start_pos = self.ui.inPos.currentIndex() if direction == IN \
               else CURRENT
        stop_pos = self.ui.stopPos.currentIndex() if direction == IN \
               else self.ui.outPos.currentIndex()
        if direction == IN:
            obj.setMessage(self.ui.lineMessage.text())
        obj.animate(start = start_pos,
                    stop  = stop_pos,
                    direction = direction)

    def resizeEvent(self, event):
        if self.msg:
            self.msg._resizeCallBacks(event)

        QtGui.QWidget.resizeEvent(self, event)

    def showClicked(self):
        if self.msg:
            if self.msg.isVisible():
                return

        self.msg = PMessageBox(self.ui.target)
        self.msg.setStyleSheet(PTestUI.STYLE)
        self.msg._animation = self.ui.animation.value()
        self.msg._duration = self.ui.duration.value()

        if self.ui.enableOverlay.isChecked():
            self.msg.enableOverlay(self.ui.animatedOverlay.isChecked())
        if self.ui.enableBusy.isChecked():
            self.msg.busy.busy()

        self.act(self.msg, IN)

    def hideClicked(self):
        if self.msg:
            if self.msg.isVisible():
                self.act(self.msg, OUT)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PdsTest = PTestUI()
    PdsTest.show()
    sys.exit(app.exec_())

