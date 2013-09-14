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
from PyQt4.QtGui import QFileDialog

from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n, KStandardDirs, KGlobal, KConfig
import os, sys, subprocess

from kaptan.screen import Screen
from kaptan.screens.ui_scrWallpaper import Ui_wallpaperWidget
from kaptan.screens.wallpaperItem import WallpaperItemWidget

from kaptan.tools.desktop_parser import DesktopParser
from ConfigParser import ConfigParser


class Widget(QtGui.QWidget, Screen):
    screenSettings = {}
    screenSettings["hasChanged"] = False

    # title and description at the top of the dialog window
    title = ki18n("Wallpaper")
    desc = ki18n("Choose a Wallpaper")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_wallpaperWidget()
        self.ui.setupUi(self)
        # Get system locale
        self.catLang = KGlobal.locale().language()

        # Get screen resolution
        rect =  QtGui.QDesktopWidget().screenGeometry()

        # Get metadata.desktop files from shared wallpaper directory
        lst= KStandardDirs().findAllResources("wallpaper", "*metadata.desktop", KStandardDirs.Recursive)

        for desktopFiles in lst:
            parser = DesktopParser()
            parser.read(str(desktopFiles))

            try:
                wallpaperTitle = parser.get_locale('Desktop Entry', 'Name[%s]'%self.catLang, '')
            except:
                wallpaperTitle = parser.get_locale('Desktop Entry', 'Name', '')

            try:
                wallpaperDesc = parser.get_locale('Desktop Entry', 'X-KDE-PluginInfo-Author', '')
            except:
                wallpaperDesc = "Unknown"

            # Get all files in the wallpaper's directory
            thumbFolder = os.listdir(os.path.join(os.path.split(str(desktopFiles))[0], "contents"))

            """
            Appearantly the thumbnail names doesn't have a standart.
            So we get the file list from the contents folder and
            choose the file which has a name that starts with "scre".

            File names I've seen so far;
            screenshot.jpg, screnshot.jpg, screenshot.png, screnshot.png
            """

            wallpaperThumb = ""

            for thumb in thumbFolder:
                if thumb.startswith('scre'):
                    wallpaperThumb = os.path.join(os.path.split(str(desktopFiles))[0], "contents/" + thumb)

            wallpaperFile = os.path.split(str(desktopFiles))[0]

            # Insert wallpapers to listWidget.
            item = QtGui.QListWidgetItem(self.ui.listWallpaper)
            # Each wallpaper item is a widget. Look at widgets.py for more information.
            widget = WallpaperItemWidget(unicode(wallpaperTitle), unicode(wallpaperDesc), wallpaperThumb, self.ui.listWallpaper)
            item.setSizeHint(QSize(120,170))
            self.ui.listWallpaper.setItemWidget(item, widget)
            # Add a hidden value to each item for detecting selected wallpaper's path.
            item.setStatusTip(wallpaperFile)

        self.ui.listWallpaper.connect(self.ui.listWallpaper, SIGNAL("itemSelectionChanged()"), self.setWallpaper)
        self.ui.checkBox.connect(self.ui.checkBox, SIGNAL("stateChanged(int)"), self.disableWidgets)
        self.ui.buttonChooseWp.connect(self.ui.buttonChooseWp, SIGNAL("clicked()"), self.selectWallpaper)

    def disableWidgets(self, state):
        if state:
            self.__class__.screenSettings["hasChanged"] = False
            self.ui.buttonChooseWp.setDisabled(True)
            self.ui.listWallpaper.setDisabled(True)
        else:
            self.__class__.screenSettings["hasChanged"] = True
            self.ui.buttonChooseWp.setDisabled(False)
            self.ui.listWallpaper.setDisabled(False)

    def setWallpaper(self):
        self.__class__.screenSettings["selectedWallpaper"] =  self.ui.listWallpaper.currentItem().statusTip()
        self.__class__.screenSettings["hasChanged"] = True

    def selectWallpaper(self):
        selectedFile = QFileDialog.getOpenFileName(None,"Open Image", os.environ["HOME"], 'Image Files (*.png *.jpg *bmp)')

        if selectedFile.isNull():
            return
        else:
            item = QtGui.QListWidgetItem(self.ui.listWallpaper)
            wallpaperName = os.path.splitext(os.path.split(str(selectedFile))[1])[0]
            widget = WallpaperItemWidget(unicode(wallpaperName), unicode("Unknown"), selectedFile, self.ui.listWallpaper)
            item.setSizeHint(QSize(120,170))
            self.ui.listWallpaper.setItemWidget(item, widget)
            item.setStatusTip(selectedFile)
            self.ui.listWallpaper.setCurrentItem(item)
            self.resize(120,170)

    def shown(self):
        pass

    def execute(self):
        return True

