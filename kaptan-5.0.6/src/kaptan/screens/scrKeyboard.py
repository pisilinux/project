# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
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
from PyKDE4.kdecore import ki18n, KConfig

from kaptan.screen import Screen
from kaptan.screens.ui_scrKeyboard import Ui_keyboardWidget

import subprocess

from pardus import localedata

class Widget(QtGui.QWidget, Screen):
    screenSettings = {}
    screenSettings["hasChanged"] = False

    # title and description at the top of the dialog window
    title = ki18n("Keyboard")
    desc = ki18n("Keyboard Layout Language")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_keyboardWidget()
        self.ui.setupUi(self)

        # get layout config
        self.config = KConfig("kxkbrc")
        self.group = self.config.group("Layout")
        self.layoutList = str(self.group.readEntry("LayoutList"))
        self.lastLayout = 0

        # get language list
        self.languageList = self.getLanguageList()

        # generate language list
        for language in self.languageList:
            languageCode, languageName, languageLayout, languageVariant = language

            item = QtGui.QListWidgetItem(self.ui.listWidgetKeyboard)
            item.setText(languageName)
            item.setToolTip(languageLayout)
            item.setStatusTip(languageVariant)
            self.ui.listWidgetKeyboard.addItem(item)

            # select appropriate keymap
            if self.getCurrentSystemLanguage().strip() == languageCode.strip():
                if languageCode.strip()=="tr" and languageVariant.strip() == "f":
                    break
                else:
                    self.ui.listWidgetKeyboard.setCurrentItem(item)

        self.ui.listWidgetKeyboard.sortItems()
        self.ui.listWidgetKeyboard.connect(self.ui.listWidgetKeyboard, SIGNAL("itemSelectionChanged()"), self.setKeyboard)

    def getCurrentSystemLanguage(self):
        lang = "en"

        try:
            langFile = open('/etc/mudur/language', 'r')
            lang = langFile.readline().rstrip('\n').strip()
        except IOError:
            print "Cannot read /etc/mudur/language file"

        return lang

    def getLanguageList(self):
        languageList = []

        for language in localedata.languages.items():
            lcode, lprops = language

            lkeymaps = lprops.keymaps

            for lmap in lkeymaps:
                lname = lmap.name
                llayout = lmap.xkb_layout
                lvariant = lmap.xkb_variant

                languageList.append([lcode, lname, llayout, lvariant])

        return languageList

    def setKeyboard(self):
        layout = self.ui.listWidgetKeyboard.currentItem().toolTip()
        variant = self.ui.listWidgetKeyboard.currentItem().statusTip()

        subprocess.Popen(["setxkbmap", layout, variant])
        if variant:
            self.lastLayout = layout + "(" + variant + ")"
        else:
            self.lastLayout = layout

    def shown(self):
        pass

    def execute(self):
        if self.lastLayout:
            layoutArr = self.layoutList.split(",")

            if self.lastLayout not in layoutArr:
                layoutArr.insert(0, str(self.lastLayout))
            else:
                layoutArr.remove(self.lastLayout)
                layoutArr.insert(0, str(self.lastLayout))

            for i in layoutArr:
                if i == "":
                    layoutArr.remove(i)

            layoutList =  ",".join(layoutArr)
            self.group.writeEntry("LayoutList", layoutList)
            self.group.writeEntry("DisplayNames", layoutList)
            self.config.sync()
        return True


