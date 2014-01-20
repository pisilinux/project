# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yali/gui/Ui/bg.ui'
#
# Created: Mon Jan 20 02:08:33 2014
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(797, 475)
        Form.setStyleSheet(_fromUtf8("#Form{\n"
"      background-image: url(:/gui/pics/bg.png);\n"
"      background-color: rgb(50, 50, 50);\n"
"      /*background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:0.572, y2:0.688, stop:0 rgba(75, 114, 137, 255), stop:1 rgba(29, 42, 51, 255));*/\n"
"      padding: 0px;\n"
"      margin: 0px;\n"
"}\n"
"\n"
"QPushButton{\n"
"    padding: 3px 10px 3px 10px;\n"
"    color: white;\n"
"    border:0px;\n"
"    border-radius:2px;\n"
"    background-color: qlineargradient(spread:repeat, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(27, 27, 27, 0), stop:0.510753 rgba(9, 9, 9, 10), stop:1 rgba(0, 0, 0, 0));\n"
"    /*background-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgba(120, 146, 172, 255), stop:0.0155729 rgba(99, 141, 164, 255), stop:0.538376 rgba(49, 84, 106, 255), stop:1 rgba(51, 72, 91, 255))*/\n"
"}\n"
"\n"
"QPushButton::flat:hover{\n"
"    border:1px solid  rgba(255, 255, 255, 40);\n"
"    border-radius:2px;\n"
"    background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(127, 127, 127, 10), stop:0.513661 rgba(231, 231, 231, 50), stop:1 rgba(94, 94, 94, 10))\n"
"}\n"
"\n"
"QPushButton::flat{\n"
"    border:1px solid  rgba(255, 255, 255, 30);\n"
"    border-radius:2px;\n"
"    background-color: qlineargradient(spread:repeat, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(27, 27, 27, 0), stop:0.510753 rgba(9, 9, 9, 10), stop:1 rgba(0, 0, 0, 0));\n"
"}\n"
"\n"
"QPushButton::flat:pressed{\n"
"    border:1px solid  rgba(255, 255, 255, 15);\n"
"    border-radius:2px;\n"
"    padding: 3px 10px 3px 10px;\n"
"    background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(52, 52, 52, 50));\n"
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
"}\n"
"\n"
"\n"
" QComboBox {\n"
"     border:1px solid  rgba(255, 255, 255, 30);\n"
"     border-radius:2px;\n"
"     padding: 1px 18px 1px 3px;\n"
"     min-width: 6em;\n"
"     color: white;\n"
" }\n"
"\n"
" QComboBox:editable {\n"
"     background: white;\n"
" }\n"
"\n"
" QComboBox:!editable, QComboBox::drop-down:editable {\n"
"    background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(52, 52, 52, 10));\n"
" }\n"
"\n"
" /* QComboBox gets the \"on\" state when the popup is open */\n"
" QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"    background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(52, 52, 52, 10));\n"
" }\n"
"\n"
" QComboBox:on { /* shift the text when the popup opens */\n"
"     padding-top: 3px;\n"
"     padding-left: 4px;\n"
" }\n"
"\n"
" QComboBox::drop-down {\n"
"     subcontrol-origin: padding;\n"
"     subcontrol-position: top right;\n"
"     width: 20px;\n"
"     border:0px solid  rgba(34, 49, 60, 100);\n"
" }\n"
"\n"
" QComboBox::down-arrow {\n"
"    image:url(:/images/arrow-down.png)\n"
" }\n"
"\n"
" QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"     top: 1px;\n"
"     left: 1px;\n"
" }\n"
"\n"
""))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

