# -*- coding: utf-8 -*-
#
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
from PyKDE4.kdecore import ki18n
from PyKDE4.kdecore import i18n

from kaptan.screen import Screen
from kaptan.screens.ui_scrWelcome import Ui_welcomeWidget
from kaptan.tools import tools

import subprocess

class Widget(QtGui.QWidget, Screen):

    title = ki18n("Welcome")
    desc = ki18n("Welcome to %s")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_welcomeWidget()
        self.ui.setupUi(self)
        Widget.desc = QVariant(unicode(Widget.desc.toString()) % tools.getRelease())

    def shown(self):
        pass

    def execute(self):
        return True

