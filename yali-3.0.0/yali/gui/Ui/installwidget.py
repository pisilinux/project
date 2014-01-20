# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/installwidget.ui'
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

class Ui_InstallWidget(object):
    def setupUi(self, InstallWidget):
        InstallWidget.setObjectName(_fromUtf8("InstallWidget"))
        InstallWidget.resize(822, 630)
        InstallWidget.setWindowTitle(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(InstallWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame = QtGui.QFrame(InstallWidget)
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
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(0, 10, 0, 20)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.slideImage = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.slideImage.sizePolicy().hasHeightForWidth())
        self.slideImage.setSizePolicy(sizePolicy)
        self.slideImage.setMinimumSize(QtCore.QSize(318, 150))
        self.slideImage.setMaximumSize(QtCore.QSize(266, 150))
        self.slideImage.setLineWidth(0)
        self.slideImage.setText(_fromUtf8(""))
        self.slideImage.setPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/welcome.png")))
        self.slideImage.setScaledContents(False)
        self.slideImage.setAlignment(QtCore.Qt.AlignCenter)
        self.slideImage.setWordWrap(False)
        self.slideImage.setObjectName(_fromUtf8("slideImage"))
        self.horizontalLayout.addWidget(self.slideImage)
        self.slideText = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.slideText.sizePolicy().hasHeightForWidth())
        self.slideText.setSizePolicy(sizePolicy)
        self.slideText.setMinimumSize(QtCore.QSize(400, 0))
        self.slideText.setMaximumSize(QtCore.QSize(400, 16777215))
        self.slideText.setText(_fromUtf8(""))
        self.slideText.setWordWrap(True)
        self.slideText.setObjectName(_fromUtf8("slideText"))
        self.horizontalLayout.addWidget(self.slideText)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(InstallWidget)
        QtCore.QMetaObject.connectSlotsByName(InstallWidget)

    def retranslateUi(self, InstallWidget):
        pass

