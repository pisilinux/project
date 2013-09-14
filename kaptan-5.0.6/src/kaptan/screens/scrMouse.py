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
from PyKDE4.kdeui import KGlobalSettings

from kaptan.screen import Screen
from kaptan.screens.ui_scrMouse import Ui_mouseWidget

from Xlib import display
RIGHT_HANDED, LEFT_HANDED = range(2)

class Widget(QtGui.QWidget, Screen):
    screenSettings = {}
    screenSettings["hasChanged"] = False

    # title and description at the top of the dialog window
    title = ki18n("Mouse")
    desc = ki18n("Setup Mouse Behavior")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_mouseWidget()
        self.ui.setupUi(self)

        # Our default click behaviour is double click. So make SingleClick = false (kdeglobals)
        self.clickBehaviour = "False"

        # read default settings

        try:
            config = KConfig("kcminputrc")
            group = config.group("Mouse")
            self.__class__.screenSettings["selectedMouse"] =  group.readEntry("MouseButtonMapping")

            config = KConfig("kdeglobals")
            group = config.group("KDE")
            self.__class__.screenSettings["selectedBehaviour"] = str(group.readEntry("SingleClick"))

            self.ui.singleClick.setChecked(self.str2bool(self.__class__.screenSettings["selectedBehaviour"]))
            self.clickBehaviour = self.str2bool(self.__class__.screenSettings["selectedBehaviour"])

            if self.__class__.screenSettings["selectedMouse"] == "LeftHanded":
                self.ui.radioButtonLeftHand.setChecked(True)

        except:
            pass

        # set signals
        self.connect(self.ui.radioButtonRightHand, SIGNAL("toggled(bool)"), self.setHandedness)
        self.connect(self.ui.checkReverse, SIGNAL("toggled(bool)"), self.setHandedness)

    def str2bool(self, s):
        return bool(eval(s.capitalize()))

    def on_singleClick_clicked(self):
        if self.ui.singleClick.isChecked():
            self.clickBehaviour = "True"
        else:
            self.clickBehaviour = "False"

    def getMouseMap(self):
        self.mapMouse = {}

        if self.ui.radioButtonRightHand.isChecked():
            self.handed = RIGHT_HANDED

        else:
            self.handed = LEFT_HANDED

        self.mapMouse = display.Display().get_pointer_mapping()
        self.num_buttons = len(self.mapMouse)

    def setHandedness(self, item):
        self.getMouseMap()

        # mouse has 1 button
        if self.num_buttons == 1:
            self.mapMouse[0] = 1

        # mouse has 2 buttons
        elif self.num_buttons == 2:
            if self.handed == RIGHT_HANDED:
                self.mapMouse[0], self.mapMouse[1] = 1, 3
            else:
                self.mapMouse[0], self.mapMouse[1] = 3, 1

        # mouse has 3 or more buttons
        else:
            if self.handed == RIGHT_HANDED:
                self.mapMouse[0], self.mapMouse[2] = 1, 3
            else:
                self.mapMouse[0], self.mapMouse[2] = 3, 1

            if self.num_buttons >= 5:
                # get wheel position
                for pos in range(0, self.num_buttons):
                    if self.mapMouse[pos] in (4,5): break

                if pos < self.num_buttons -1:
                    if self.ui.checkReverse.isChecked():
                        self.mapMouse[pos], self.mapMouse[pos + 1] = 5, 4
                    else:
                        self.mapMouse[pos], self.mapMouse[pos + 1] = 4, 5

        display.Display().set_pointer_mapping(self.mapMouse)

        config = KConfig("kcminputrc")
        group = config.group("Mouse")

        if self.handed == RIGHT_HANDED:
            group.writeEntry("MouseButtonMapping", QString("RightHanded"))
            self.__class__.screenSettings["selectedMouse"] = "RightHanded"
        else:
            group.writeEntry("MouseButtonMapping", QString("LeftHanded"))
            self.__class__.screenSettings["selectedMouse"] = "LeftHanded"

        group.writeEntry("ReverseScrollPolarity", QString(str(self.ui.checkReverse.isChecked())))
        config.sync()

        KGlobalSettings.self().emitChange(KGlobalSettings.SettingsChanged, KGlobalSettings.SETTINGS_MOUSE)

    def shown(self):
        pass

    def execute(self):
        self.__class__.screenSettings["summaryMessage"] ={}

        self.__class__.screenSettings["summaryMessage"].update({"selectedMouse": ki18n("Left Handed") if self.__class__.screenSettings["selectedMouse"] == "LeftHanded" else ki18n("Right Handed")})
        self.__class__.screenSettings["summaryMessage"].update({"clickBehaviour": ki18n("Single Click ") if self.clickBehaviour == "True" else ki18n("Double Click")})

        config = KConfig("kdeglobals")
        group = config.group("KDE")
        group.writeEntry("SingleClick", QString(self.clickBehaviour))
        config.sync()
        KGlobalSettings.self().emitChange(KGlobalSettings.SettingsChanged, KGlobalSettings.SETTINGS_MOUSE)

        return True

