# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/summarywidget.ui'
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

class Ui_SummaryWidget(object):
    def setupUi(self, SummaryWidget):
        SummaryWidget.setObjectName(_fromUtf8("SummaryWidget"))
        SummaryWidget.resize(903, 514)
        SummaryWidget.setStyleSheet(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(SummaryWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame = QtGui.QFrame(SummaryWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(600, 350))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 350))
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
        self.gridLayout_5 = QtGui.QGridLayout(self.frame)
        self.gridLayout_5.setContentsMargins(0, 10, 0, 5)
        self.gridLayout_5.setHorizontalSpacing(30)
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.content = QtGui.QTextEdit(self.frame)
        self.content.setMaximumSize(QtCore.QSize(600, 16777215))
        self.content.setStyleSheet(_fromUtf8("#content{\n"
"background-color: rgba(255, 255, 255, 0);\n"
"border:0px;\n"
"color:white\n"
"}"))
        self.content.setFrameShape(QtGui.QFrame.NoFrame)
        self.content.setLineWidth(0)
        self.content.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.content.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.content.setUndoRedoEnabled(False)
        self.content.setReadOnly(True)
        self.content.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.content.setObjectName(_fromUtf8("content"))
        self.horizontalLayout.addWidget(self.content)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_5.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 1, 1, 1)

        self.retranslateUi(SummaryWidget)
        QtCore.QMetaObject.connectSlotsByName(SummaryWidget)

    def retranslateUi(self, SummaryWidget):
        pass

