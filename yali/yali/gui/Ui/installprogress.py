# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/installprogress.ui'
#
# Created: Fri Apr  5 17:37:29 2013
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

class Ui_InstallProgress(object):
    def setupUi(self, InstallProgress):
        InstallProgress.setObjectName(_fromUtf8("InstallProgress"))
        InstallProgress.resize(640, 113)
        self.verticalLayout = QtGui.QVBoxLayout(InstallProgress)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.InstallProgressFrame = QtGui.QWidget(InstallProgress)
        self.InstallProgressFrame.setStyleSheet(_fromUtf8("/* #QProgressBar */\n"
"\n"
"    QProgressBar {\n"
"        border-radius: 2px;\n"
"        text-align: center;\n"
"        color: #222222;\n"
"        background-color: rgba(255, 255, 255, 180);\n"
"    }\n"
"\n"
"    QProgressBar:chunk {\n"
"        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.473118 rgba(200, 79, 136, 255), stop:0.489247 rgba(200, 52, 119, 255), stop:1 rgba(200, 0, 105, 255));\n"
"        border-radius: 2px;\n"
"    }"))
        self.InstallProgressFrame.setObjectName(_fromUtf8("InstallProgressFrame"))
        self.gridLayout = QtGui.QGridLayout(self.InstallProgressFrame)
        self.gridLayout.setMargin(20)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.progress = QtGui.QProgressBar(self.InstallProgressFrame)
        self.progress.setMinimumSize(QtCore.QSize(600, 0))
        self.progress.setMaximumSize(QtCore.QSize(600, 16777215))
        self.progress.setProperty("value", 65)
        self.progress.setObjectName(_fromUtf8("progress"))
        self.gridLayout.addWidget(self.progress, 1, 0, 1, 1)
        self.info = QtGui.QLabel(self.InstallProgressFrame)
        self.info.setMinimumSize(QtCore.QSize(0, 40))
        self.info.setAlignment(QtCore.Qt.AlignTop)
        self.info.setWordWrap(True)
        self.info.setIndent(5)
        self.info.setObjectName(_fromUtf8("info"))
        self.gridLayout.addWidget(self.info, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.InstallProgressFrame)

        self.retranslateUi(InstallProgress)
        QtCore.QMetaObject.connectSlotsByName(InstallProgress)

    def retranslateUi(self, InstallProgress):
        self.info.setText(i18n("Installing Package: "))

