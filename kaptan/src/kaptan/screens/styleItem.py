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

# Application Stuff
from kaptan.screens.ui_scrStyleItem import Ui_StyleItemWidget

class StyleItemWidget(QtGui.QWidget):

    def __init__(self, title, desc, pic, parent):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_StyleItemWidget()
        self.ui.setupUi(self)

        self.ui.styleName.setText(title)
        self.ui.styleDesc.setText(desc)
        self.ui.stylePreview.setPixmap(QtGui.QPixmap(pic))

