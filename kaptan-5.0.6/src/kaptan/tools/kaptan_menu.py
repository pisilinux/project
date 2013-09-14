#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, SIGNAL

class Menu:

    def __init__(self, titles, labelWidget):
        self.bold = "font-weight:bold"
        self.normal = "font-weight:normal"
        self.defaultFontSize = 10
        self.position = 0
        self.menuText = ""
        self.menuNode = " <span style='font-size:%spt; %s'>%s</span> "
        self.seperatorL = "<span style='font-size:11pt'><img src=':/raw/pixmap/menu-arrow-left.png'></span>"
        self.seperatorR = "<span style='font-size:11pt'><img src=':/raw/pixmap/menu-arrow-right.png'></span>"

        # get titles
        self.titles = titles

        # get label widget
        self.label = labelWidget

    def move(self):
        self.menuText = ""
        lastItemIndex = len(self.titles)
        seperatorL = ""
        seperatorR = ""

        for index in range(0, lastItemIndex):
            menuItemText = self.titles[index]

            # set seperators
            if self.position == 0:
                seperatorL = ""
                seperatorR = self.seperatorR
            elif self.position == lastItemIndex - 1:
                seperatorL = self.seperatorL
                seperatorR = ""
            else:
                seperatorL = self.seperatorL
                seperatorR = self.seperatorR

            # prepare menu text
            if index == (self.position - 1):
                self.menuText += self.menuNode % (self.defaultFontSize, self.normal, menuItemText)
            if index == self.position:
                self.menuText += seperatorL
                self.menuText += self.menuNode % (self.defaultFontSize, self.bold, menuItemText)
                self.menuText += seperatorR
            if index == (self.position + 1):
                self.menuText += self.menuNode % (self.defaultFontSize, self.normal, menuItemText)

        # set menu text
        self.label.setText(self.menuText)

    def next(self):
        self.position += 1
        self.move()

    def prev(self):
        self.position -= 1
        self.move()

    def start(self):
        self.position = 0
        self.move()
