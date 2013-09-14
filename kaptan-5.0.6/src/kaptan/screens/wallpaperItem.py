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

from PyQt4 import QtGui
from PyQt4.QtCore import *

from kaptan.screens.ui_wallpaperItem import Ui_ServiceItemWidget

class WallpaperItemWidget(QtGui.QWidget):

    def __init__(self, title, desc, pic, parent):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_ServiceItemWidget()
        self.ui.setupUi(self)

        self.ui.labelName.setText(title)
        self.ui.labelDesc.setText("by "+ desc)

        try:
            self.ui.labelStatus.setPixmap(QtGui.QPixmap(pic))
        except:
            pass
