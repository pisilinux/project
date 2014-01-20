# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/info.ui'
#
# Created: Mon Jan 20 02:08:32 2014
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

class Ui_InfoWidget(object):
    def setupUi(self, InfoWidget):
        InfoWidget.setObjectName(_fromUtf8("InfoWidget"))
        InfoWidget.resize(732, 496)
        InfoWidget.setWindowTitle(_fromUtf8(""))
        self.gridlayout = QtGui.QGridLayout(InfoWidget)
        self.gridlayout.setMargin(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.frame = QtGui.QFrame(InfoWidget)
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
"}"))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame)
        self.gridLayout_3.setContentsMargins(-1, 20, -1, 20)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pix = QtGui.QLabel(self.frame)
        self.pix.setMaximumSize(QtCore.QSize(180, 180))
        self.pix.setText(_fromUtf8(""))
        self.pix.setPixmap(QtGui.QPixmap(_fromUtf8(":/gui/pics/welcome.png")))
        self.pix.setScaledContents(True)
        self.pix.setWordWrap(False)
        self.pix.setObjectName(_fromUtf8("pix"))
        self.horizontalLayout_2.addWidget(self.pix)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(10, -1, 10, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.info = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.info.setFont(font)
        self.info.setLineWidth(1)
        self.info.setMidLineWidth(0)
        self.info.setScaledContents(False)
        self.info.setAlignment(QtCore.Qt.AlignTop)
        self.info.setWordWrap(True)
        self.info.setIndent(0)
        self.info.setObjectName(_fromUtf8("info"))
        self.verticalLayout.addWidget(self.info)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 0, 0, 1, 1)
        self.gridlayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(InfoWidget)
        QtCore.QMetaObject.connectSlotsByName(InfoWidget)

    def retranslateUi(self, InfoWidget):
        self.info.setText(i18n("Welcome to YALI (Yet Another Linux Installer), where you will have the opportunity to verify the installation medium, select your keyboard layout, choose your time-zone, create user accounts and prepare your disk - followed by a summary and final review before committing to the installation of Pisi Linux.\n"
"Further information for each page of the installer may be viewed by clicking the question-mark icon at the top of its page. \n"
"YALI was designed with ease of use in mind and should not pose a problem to the novice Linux user. As with all such procedures though, any valuable data on your system should be backed-up before commencing."))

