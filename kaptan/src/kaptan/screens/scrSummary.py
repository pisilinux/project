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
from PyQt4.QtGui import QMessageBox
from PyKDE4.kdecore import ki18n, KConfig

import subprocess,os, dbus

from kaptan.screen import Screen
from kaptan.screens.ui_scrSummary import Ui_summaryWidget
from PyKDE4 import kdeui

# import other widgets to get the latest configuration
import kaptan.screens.scrWallpaper as wallpaperWidget
import kaptan.screens.scrMouse as mouseWidget
import kaptan.screens.scrStyle as styleWidget
import kaptan.screens.scrMenu as menuWidget
import kaptan.screens.scrSmolt  as smoltWidget
import kaptan.screens.scrAvatar  as avatarWidget

from kaptan.tools import tools

class Widget(QtGui.QWidget, Screen):
    title = ki18n("Summary")
    desc = ki18n("Save Your Settings")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_summaryWidget()
        self.ui.setupUi(self)

    def shown(self):
        self.wallpaperSettings = wallpaperWidget.Widget.screenSettings
        self.mouseSettings = mouseWidget.Widget.screenSettings
        self.menuSettings = menuWidget.Widget.screenSettings
        self.styleSettings = styleWidget.Widget.screenSettings
        self.smoltSettings = smoltWidget.Widget.screenSettings
        self.avatarSettings = avatarWidget.Widget.screenSettings

        subject = "<p><li><b>%s</b></li><ul>"
        item    = "<li>%s</li>"
        end     = "</ul></p>"
        content = QString("")

        content.append("""<html><body><ul>""")

        # Mouse Settings
        content.append(subject % ki18n("Mouse Settings").toString())

        content.append(item % ki18n("Selected Mouse configuration: <b>%s</b>").toString() % self.mouseSettings["summaryMessage"]["selectedMouse"].toString())
        content.append(item % ki18n("Selected clicking behaviour: <b>%s</b>").toString() % self.mouseSettings["summaryMessage"]["clickBehaviour"].toString())
        content.append(end)

        # Menu Settings
        content.append(subject % ki18n("Menu Settings").toString())
        content.append(item % ki18n("Selected Menu: <b>%s</b>").toString() % self.menuSettings["summaryMessage"].toString())
        content.append(end)

        # Wallpaper Settings
        content.append(subject % ki18n("Wallpaper Settings").toString())
        if not self.wallpaperSettings["hasChanged"]:
            content.append(item % ki18n("You haven't selected any wallpaper.").toString())
        else:
            content.append(item % ki18n("Selected Wallpaper: <b>%s</b>").toString() % os.path.basename(str(self.wallpaperSettings["selectedWallpaper"])))
        content.append(end)

        # Style Settings
        content.append(subject % ki18n("Style Settings").toString())

        if not self.styleSettings["hasChanged"]:
            content.append(item % ki18n("You haven't selected any style.").toString())
        else:
            content.append(item % ki18n("Selected Style: <b>%s</b>").toString() % unicode(self.styleSettings["summaryMessage"]))

        content.append(end)

        # Smolt Settings
        try:
            if self.smoltSettings["summaryMessage"]:
                content.append(subject %ki18n("Smolt Settings").toString())
                content.append(item % ki18n("Send my profile: <b>%s</b>").toString() % self.smoltSettings["summaryMessage"])
                #content.append(ki18n("(<i><u>Warning:</u> Sending profile requires to set up communication with Smolt server and can take between 30 seconds to a minute. Kaptan may freeze during this time.</i>)").toString())
                content.append(end)
        except:
            print "WARNING: Your Smolt profile is already sent."

        content.append("""</ul></body></html>""")
        self.ui.textSummary.setHtml(content)

    def killPlasma(self):
        try:
            p = subprocess.Popen(["pidof", "-s", "plasma-desktop"], stdout=subprocess.PIPE)
            out, err = p.communicate()
            pidOfPlasma = int(out)

            try:
                os.kill(pidOfPlasma, 15)
            except OSError, e:
                print 'WARNING: failed os.kill: %s' % e
                print "Trying SIGKILL"
                os.kill(pidOfPlasma, 9)

            finally:
                self.startPlasma()
        except:
            QMessageBox.critical(self, ki18n("Error").toString(), ki18n("Cannot restart plasma-desktop. Kaptan will now shutdown.").toString())
            from PyKDE4 import kdeui
            kdeui.KApplication.kApplication().quit()

    def startPlasma(self):
        p = subprocess.Popen(["plasma-desktop"], stdout=subprocess.PIPE)


    def execute(self):
        hasChanged = False

        # Wallpaper Settings
        if self.wallpaperSettings["hasChanged"]:
            hasChanged = True
            if self.wallpaperSettings["selectedWallpaper"]:
                config =  KConfig("plasma-desktop-appletsrc")
                group = config.group("Containments")
                for each in list(group.groupList()):
                    subgroup = group.group(each)
                    subcomponent = subgroup.readEntry('plugin')
                    if subcomponent == 'desktop' or subcomponent == 'folderview':
                        subg = subgroup.group('Wallpaper')
                        subg_2 = subg.group('image')
                        subg_2.writeEntry("wallpaper", self.wallpaperSettings["selectedWallpaper"])

        # Menu Settings
        if self.menuSettings["hasChanged"]:
            hasChanged = True
            config = KConfig("plasma-desktop-appletsrc")
            group = config.group("Containments")

            for each in list(group.groupList()):
                subgroup = group.group(each)
                subcomponent = subgroup.readEntry('plugin')
                if subcomponent == 'panel':
                    subg = subgroup.group('Applets')
                    for i in list(subg.groupList()):
                        subg2 = subg.group(i)
                        launcher = subg2.readEntry('plugin')
                        if str(launcher).find('launcher') >= 0:
                            subg2.writeEntry('plugin', self.menuSettings["selectedMenu"] )


        def removeFolderViewWidget():
            config = KConfig("plasma-desktop-appletsrc")

            sub_lvl_0 = config.group("Containments")

            for sub in list(sub_lvl_0.groupList()):
                sub_lvl_1 = sub_lvl_0.group(sub)

                if sub_lvl_1.hasGroup("Applets"):
                    sub_lvl_2 = sub_lvl_1.group("Applets")

                    for sub2 in list(sub_lvl_2.groupList()):
                        sub_lvl_3 = sub_lvl_2.group(sub2)
                        plugin = sub_lvl_3.readEntry('plugin')

                        if plugin == 'folderview':
                            sub_lvl_3.deleteGroup()


        # Desktop Type
        if self.styleSettings["hasChangedDesktopType"]:
            hasChanged = True
            config =  KConfig("plasma-desktop-appletsrc")
            group = config.group("Containments")

            for each in list(group.groupList()):
                subgroup = group.group(each)
                subcomponent = subgroup.readEntry('plugin')
                subcomponent2 = subgroup.readEntry('screen')
                if subcomponent == 'desktop' or subcomponent == 'folderview':
                    if int(subcomponent2) == 0:
                        subgroup.writeEntry('plugin', self.styleSettings["desktopType"])

            # Remove folder widget - normally this would be done over dbus but thanks to improper naming of the plasma interface
            # this is not possible
            # ValueError: Invalid interface or error name 'org.kde.plasma-desktop': contains invalid character '-'
            #
            # Related Bug:
            # Bug 240358 - Invalid D-BUS interface name 'org.kde.plasma-desktop.PlasmaApp' found while parsing introspection
            # https://bugs.kde.org/show_bug.cgi?id=240358

            if self.styleSettings["desktopType"] == "folderview":
                removeFolderViewWidget()

            config.sync()

        # Number of Desktops
        if self.styleSettings["hasChangedDesktopNumber"]:
            hasChanged = True
            config = KConfig("kwinrc")
            group = config.group("Desktops")
            group.writeEntry('Number', self.styleSettings["desktopNumber"])
            group.sync()

            info =  kdeui.NETRootInfo(QtGui.QX11Info.display(), kdeui.NET.NumberOfDesktops | kdeui.NET.DesktopNames)
            info.setNumberOfDesktops(int(self.styleSettings["desktopNumber"]))
            info.activate()

            session = dbus.SessionBus()

            try:
                proxy = session.get_object('org.kde.kwin', '/KWin')
                proxy.reconfigure()
            except dbus.DBusException:
                pass

            config.sync()


        def deleteIconCache():
            try:
                os.remove("/var/tmp/kdecache-%s/icon-cache.kcache" % os.environ.get("USER"))
            except:
                pass

            for i in range(kdeui.KIconLoader.LastGroup):
                kdeui.KGlobalSettings.self().emitChange(kdeui.KGlobalSettings.IconChanged, i)


        # Theme Settings
        if self.styleSettings["hasChanged"]:
            if self.styleSettings["iconChanged"]:
                hasChanged = True
                configKdeGlobals = KConfig("kdeglobals")
                group = configKdeGlobals.group("General")

                groupIconTheme = configKdeGlobals.group("Icons")
                groupIconTheme.writeEntry("Theme", self.styleSettings["iconTheme"])

                configKdeGlobals.sync()

                # Change Icon theme
                kdeui.KIconTheme.reconfigure()
                kdeui.KIconCache.deleteCache()
                deleteIconCache()

            if self.styleSettings["styleChanged"]:
                hasChanged = True
                configKdeGlobals = KConfig("kdeglobals")
                group = configKdeGlobals.group("General")
                group.writeEntry("widgetStyle", self.styleSettings["styleDetails"][unicode(self.styleSettings["styleName"])]["widgetStyle"])

                groupIconTheme = configKdeGlobals.group("Icons")
                groupIconTheme.writeEntry("Theme", self.styleSettings["iconTheme"])
                #groupIconTheme.writeEntry("Theme", self.styleSettings["styleDetails"][unicode(self.styleSettings["styleName"])]["iconTheme"])

                configKdeGlobals.sync()

                # Change Icon theme
                kdeui.KIconTheme.reconfigure()
                kdeui.KIconCache.deleteCache()
                deleteIconCache()

                for i in range(kdeui.KIconLoader.LastGroup):
                    kdeui.KGlobalSettings.self().emitChange(kdeui.KGlobalSettings.IconChanged, i)

                # Change widget style & color
                for key, value in self.styleSettings["styleDetails"][unicode(self.styleSettings["styleName"])]["colorScheme"].items():
                    colorGroup = configKdeGlobals.group(key)
                    for key2, value2 in value.items():
                            colorGroup.writeEntry(str(key2), str(value2))

                configKdeGlobals.sync()
                kdeui.KGlobalSettings.self().emitChange(kdeui.KGlobalSettings.StyleChanged)

                configPlasmaRc = KConfig("plasmarc")
                groupDesktopTheme = configPlasmaRc.group("Theme")
                groupDesktopTheme.writeEntry("name", self.styleSettings["styleDetails"][unicode(self.styleSettings["styleName"])]["desktopTheme"])
                configPlasmaRc.sync()

                configPlasmaApplet = KConfig("plasma-desktop-appletsrc")
                group = configPlasmaApplet.group("Containments")
                for each in list(group.groupList()):
                    subgroup = group.group(each)
                    subcomponent = subgroup.readEntry('plugin')
                    if subcomponent == 'panel':
                        #print subcomponent
                        subgroup.writeEntry('location', self.styleSettings["styleDetails"][unicode(self.styleSettings["styleName"])]["panelPosition"])

                configPlasmaApplet.sync()

                configKwinRc = KConfig("kwinrc")
                groupWindowDecoration = configKwinRc.group("Style")
                groupWindowDecoration.writeEntry("PluginLib", self.styleSettings["styleDetails"][unicode(self.styleSettings["styleName"])]["windowDecoration"])
                configKwinRc.sync()

            session = dbus.SessionBus()

            try:
                proxy = session.get_object('org.kde.kwin', '/KWin')
                proxy.reconfigure()
            except dbus.DBusException:
                pass

        # Smolt Settings
        if self.smoltSettings["profileSend"]:
            self.procSettings = QProcess()
            command = "smoltSendProfile"
            arguments = ["-a", "--submitOnly"]
            self.procSettings.startDetached(command, arguments)

        # Avatar Settings
        if self.avatarSettings["hasChanged"]:
            hasChanged = True

        if hasChanged:
            self.killPlasma()

        return True
