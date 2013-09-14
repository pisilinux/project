#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

from PyQt4 import QtCore, QtGui
from PyKDE4 import kdeui
from PyQt4.QtCore import QTimeLine
from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs, KConfig

from kaptan.screens.ui_kaptan import Ui_kaptan

from kaptan.tools import tools
from kaptan.tools.progress_pie import DrawPie
from kaptan.tools.kaptan_menu import Menu

class Kaptan(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.initializeGlobals()
        self.initializeUI()
        self.signalHandler()

    def initializeGlobals(self):
        ''' initializes global variables '''
        self.screenData = None
        self.moveInc = 1
        self.menuText = ""
        self.titles = []
        self.descriptions = []
        self.currentDir = os.path.dirname(os.path.realpath(__file__))
        self.screensPath = self.currentDir + "/kaptan/screens/scr*py"
        self.kaptanConfig = KConfig("kaptanrc")
        self.plasmaConfig = KConfig("plasma-desktop-appletsrc")

    def signalHandler(self):
        ''' connects signals to slots '''
        self.connect(self.ui.buttonNext, QtCore.SIGNAL("clicked()"), self.slotNext)
        self.connect(self.ui.buttonApply, QtCore.SIGNAL("clicked()"), self.slotNext)
        self.connect(self.ui.buttonBack, QtCore.SIGNAL("clicked()"), self.slotBack)
        self.connect(self.ui.buttonFinish, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))
        self.connect(self.ui.buttonCancel, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))

    def initializeUI(self):
        ''' initializes the human interface '''
        self.ui = Ui_kaptan()
        self.ui.setupUi(self)

        # load screens
        tools.loadScreens(self.screensPath, globals())

        # kaptan screen settings
        self.headScreens = [scrWelcome, scrMouse, scrStyle, scrMenu, scrWallpaper]
        self.tailScreens = [scrSummary, scrGoodbye]
        self.screens = self.screenOrganizer(self.headScreens, self.tailScreens)

        # Add screens to StackWidget
        self.createWidgets(self.screens)

        # Get Screen Titles
        for screen in self.screens:
            title = screen.Widget.title.toString()
            self.titles.append(title)

        # draw progress pie
        self.countScreens = len(self.screens)
        self.pie = DrawPie(self.countScreens, self.ui.labelProgress)

        # Initialize Menu
        self.menu = Menu(self.titles, self.ui.labelMenu)
        self.menu.start()

    def screenOrganizer(self, headScreens, tailScreens):
        ''' appends unsorted screens to the list '''
        screens = []

        allScreens = [value for key, value in globals().iteritems() if key.startswith("scr")]

        otherScreens = list((set(allScreens) - set(headScreens)) - set(tailScreens))
        otherScreens.remove(scrKeyboard)
        otherScreens.remove(scrPackage)
        otherScreens.remove(scrSmolt)

        screens.extend(headScreens)
        screens.extend(otherScreens)

        # Append other screens depending on the following cases
        if tools.isLiveCD():
            screens.append(scrKeyboard)

        else:
            screens.append(scrPackage)

            if not tools.smoltProfileSent():
                screens.append(scrSmolt)

        screens.extend(tailScreens)

        return screens

    def getCur(self, d):
        ''' returns the id of current stack '''
        new   = self.ui.mainStack.currentIndex() + d
        total = self.ui.mainStack.count()
        if new < 0: new = 0
        if new > total: new = total
        return new

    def setCurrent(self, id=None):
        ''' move to id numbered step '''
        if id: self.stackMove(id)

    def slotNext(self,dryRun=False):
        ''' execute next step '''
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex() + 1

        # update pie progress
        self.pie.updatePie(curIndex)

        # animate menu
        self.menu.next()

        _w = self.ui.mainStack.currentWidget()

        ret = _w.execute()
        if ret:
            self.stackMove(self.getCur(self.moveInc))
            self.moveInc = 1

    def slotBack(self):
        ''' execute previous step '''
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex()

        # update pie progress
        self.pie.updatePie(curIndex-1)

        # animate menu
        self.menu.prev()

        _w = self.ui.mainStack.currentWidget()

        _w.backCheck()
        self.stackMove(self.getCur(self.moveInc * -1))
        self.moveInc = 1

    def stackMove(self, id):
        ''' move to id numbered stack '''
        if not id == self.ui.mainStack.currentIndex() or id==0:
            self.ui.mainStack.setCurrentIndex(id)

            # Set screen title
            self.ui.screenTitle.setText(self.descriptions[id])

            _w = self.ui.mainStack.currentWidget()
            _w.update()
            _w.shown()

        if self.ui.mainStack.currentIndex() == len(self.screens) - 3:
            self.ui.buttonNext.show()
            self.ui.buttonApply.hide()
            self.ui.buttonFinish.hide()

        if self.ui.mainStack.currentIndex() == len(self.screens) - 2:
            self.ui.buttonNext.hide()
            self.ui.buttonApply.show()
            self.ui.buttonFinish.hide()

        if self.ui.mainStack.currentIndex() == len(self.screens) - 1:
            self.ui.buttonApply.hide()
            self.ui.buttonFinish.show()

        if self.ui.mainStack.currentIndex() == 0:
            self.ui.buttonBack.hide()
            self.ui.buttonFinish.hide()
            self.ui.buttonApply.hide()
        else:
            self.ui.buttonBack.show()

    def createWidgets(self, screens=[]):
        ''' create all widgets and add inside stack '''
        self.ui.mainStack.removeWidget(self.ui.page)
        for screen in screens:
            _scr = screen.Widget()

            # Append screen descriptions to list
            self.descriptions.append(_scr.desc.toString())

            # Append screens to stack widget
            self.ui.mainStack.addWidget(_scr)


        self.stackMove(0)

    def disableNext(self):
        self.buttonNext.setEnabled(False)

    def disableBack(self):
        self.buttonBack.setEnabled(False)

    def enableNext(self):
        self.buttonNext.setEnabled(True)

    def enableBack(self):
        self.buttonBack.setEnabled(True)

    def isNextEnabled(self):
        return self.buttonNext.isEnabled()

    def isBackEnabled(self):
        return self.buttonBack.isEnabled()

    def __del__(self):
        group = self.kaptanConfig.group("General")
        group.writeEntry("RunOnStart", "False")

if __name__ == "__main__":
    appName     = "kaptan"
    catalog     = ""
    programName = ki18n("kaptan")
    version     = "5.0.1"
    description = ki18n("Kaptan lets you configure your Pisi Linux workspace at first login")
    license     = KAboutData.License_GPL
    copyright   = ki18n("(c) 2013 Pisi Linux")
    text        = ki18n("none")
    homePage    = "http://www.pisilinux.org/"
    bugEmail    = "admins@pisilinux.org"

    aboutData   = KAboutData(appName,catalog, programName, version, description,
                                license, copyright,text, homePage, bugEmail)

    KCmdLineArgs.init(sys.argv, aboutData)
    app =  kdeui.KApplication()

    # attach dbus to main loop
    tools.DBus()

    kaptan = Kaptan()
    kaptan.show()
    tools.centerWindow(kaptan)
    app.exec_()

