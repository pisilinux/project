# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/driveselectionwidget.ui'
#
# Created: Fri Apr  5 17:37:33 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

import gettext
__trans = gettext.translation('yali', fallback=True)
i18n = __trans.ugettext
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DriveSelectionWidget(object):
    def setupUi(self, DriveSelectionWidget):
        DriveSelectionWidget.setObjectName(_fromUtf8("DriveSelectionWidget"))
        DriveSelectionWidget.resize(800, 659)
        DriveSelectionWidget.setStyleSheet(_fromUtf8(""))
        self.gridLayout_2 = QtGui.QGridLayout(DriveSelectionWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setVerticalSpacing(30)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.frame = QtGui.QFrame(DriveSelectionWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(600, 250))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 250))
        self.frame.setStyleSheet(_fromUtf8("QListView {\n"
"show-decoration-selected: 1; /* make the selection span the entire width of the view */\n"
"}\n"
"\n"
"QListView{\n"
"background-color: rgba(0, 0, 0, 0);\n"
"border-radius:2px;\n"
"color:white;\n"
"}\n"
"\n"
"QListView::item {\n"
"border-radius:2;\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0));\n"
"color: rgb(220, 220, 220);\n"
"padding:5\n"
"}\n"
"\n"
"QListView::item:hover {\n"
"border-radius:2;\n"
"color:white;\n"
"}\n"
"\n"
"QListView::item:selected {\n"
"border-radius:2;\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(52, 52, 52, 50));\n"
"color:white;\n"
"}"))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frame)
        self.gridLayout_4.setContentsMargins(0, 30, 0, 10)
        self.gridLayout_4.setHorizontalSpacing(30)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.drives = QtGui.QListWidget(self.frame)
        self.drives.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drives.sizePolicy().hasHeightForWidth())
        self.drives.setSizePolicy(sizePolicy)
        self.drives.setMinimumSize(QtCore.QSize(450, 0))
        self.drives.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.drives.setStyleSheet(_fromUtf8("#drives{\n"
"background-color: rgba(0,0,0,0);\n"
"border: 0px;\n"
"color:white;\n"
"}"))
        self.drives.setFrameShape(QtGui.QFrame.NoFrame)
        self.drives.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.drives.setAutoScrollMargin(15)
        self.drives.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.drives.setAlternatingRowColors(False)
        self.drives.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.drives.setIconSize(QtCore.QSize(128, 128))
        self.drives.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.drives.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.drives.setMovement(QtGui.QListView.Static)
        self.drives.setFlow(QtGui.QListView.LeftToRight)
        self.drives.setProperty("isWrapping", False)
        self.drives.setResizeMode(QtGui.QListView.Adjust)
        self.drives.setLayoutMode(QtGui.QListView.SinglePass)
        self.drives.setSpacing(0)
        self.drives.setGridSize(QtCore.QSize(0, 0))
        self.drives.setViewMode(QtGui.QListView.IconMode)
        self.drives.setModelColumn(0)
        self.drives.setUniformItemSizes(False)
        self.drives.setBatchSize(1)
        self.drives.setWordWrap(True)
        self.drives.setSelectionRectVisible(False)
        self.drives.setObjectName(_fromUtf8("drives"))
        self.gridLayout.addWidget(self.drives, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 3, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(DriveSelectionWidget)
        QtCore.QMetaObject.connectSlotsByName(DriveSelectionWidget)

    def retranslateUi(self, DriveSelectionWidget):
        pass

