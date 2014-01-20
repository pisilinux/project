# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/goodbyewidget.ui'
#
# Created: Mon Jan 20 02:08:31 2014
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

class Ui_GoodByeWidget(object):
    def setupUi(self, GoodByeWidget):
        GoodByeWidget.setObjectName(_fromUtf8("GoodByeWidget"))
        GoodByeWidget.resize(789, 514)
        self.gridLayout = QtGui.QGridLayout(GoodByeWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame = QtGui.QFrame(GoodByeWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(600, 250))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 250))
        self.frame.setStyleSheet(_fromUtf8("#frame{\n"
"background-color: rgba(0, 0, 0, 20);\n"
"border-top: 1px solid rgba(255, 255, 255, 75);/*white*/\n"
"border-bottom: 1px solid rgba(255, 255, 255, 75);/*white*/\n"
"background-repeat: no-repeat;\n"
"}\n"
"\n"
"QListView {\n"
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
        self.gridLayout_4.setContentsMargins(0, 10, 0, 10)
        self.gridLayout_4.setHorizontalSpacing(30)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/postinstall.png")))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.info = QtGui.QLabel(self.frame)
        self.info.setStyleSheet(_fromUtf8("font:12px Droid Sans;"))
        self.info.setText(_fromUtf8(""))
        self.info.setObjectName(_fromUtf8("info"))
        self.verticalLayout.addWidget(self.info)
        self.gridLayout_4.addLayout(self.verticalLayout, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(GoodByeWidget)
        QtCore.QMetaObject.connectSlotsByName(GoodByeWidget)

    def retranslateUi(self, GoodByeWidget):
        pass

