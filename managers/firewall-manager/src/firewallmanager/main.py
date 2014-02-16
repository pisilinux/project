#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui
# UI
from firewallmanager.ui_main import Ui_MainWidget

# Backend
from firewallmanager.backend import Interface

# Config
from firewallmanager.config import ANIM_SHOW, ANIM_HIDE, ANIM_TARGET, ANIM_DEFAULT, ANIM_TIME

# Item widget
from firewallmanager.item import ItemListWidgetItem, ItemWidget

# Service widget
from firewallmanager.service import ServiceWidget

# Page Dialog
from firewallmanager.pagedialog import PageDialog

#Context 
import context as ctx
from context import *

class MainWidget(QtGui.QWidget, Ui_MainWidget):
    def __init__(self, parent, embed=False):
        QtGui.QWidget.__init__(self, parent)

        if embed:
            self.setupUi(parent)
        else:
            self.setupUi(self)

        # Animation
        self.animator = QtCore.QTimeLine(ANIM_TIME, self)
        self.animationLast = ANIM_HIDE

        # Initialize heights of animated widgets
        self.slotAnimationFinished()

        # Backend
        self.iface = Interface()
        self.iface.listenFirewallSignals(self.firewallSignalHandler)
        self.iface.listenServiceSignals(self.serviceSignalHandler)

        # Fail if no packages provide backend
        self.checkBackend()

        # We don't need a "new" button
        self.hideNew()

        # We don't need a filter
        self.hideFilter()

        # Build item list
        self.buildItemList()

        # Set service widget
        self.widgetService = ServiceWidget(self)
        self.widgetService.setState(self.iface.getState())
        self.verticalLayout.insertWidget(0, self.widgetService)

        # Rule edit widget
        # TBD

        # Signals
        self.connect(self.comboFilter, QtCore.SIGNAL("currentIndexChanged(int)"), self.slotFilterChanged)
        self.connect(self.pushNew, QtCore.SIGNAL("triggered(QAction*)"), self.slotOpenEdit)
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.slotSaveEdit)
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.slotCancelEdit)
        self.connect(self.animator, QtCore.SIGNAL("frameChanged(int)"), self.slotAnimate)
        self.connect(self.animator, QtCore.SIGNAL("finished()"), self.slotAnimationFinished)
        self.connect(self.widgetService, QtCore.SIGNAL("stateChanged(int)"), self.slotServiceChanged)

    def checkBackend(self):
        """
            Check if there are packages that provide required backend.
        """
        if not len(self.iface.getPackages()):
            createMessage(self,"Error","There are no packages that provide backend for this application.\nPlease make sure that packages are installed and configured correctly.")
            return False
        return True

    def firewallSignalHandler(self, package, signal, args):
        if signal == "stateChanged":
            state = args[0]
            self.widgetService.setState(state == "on")
        elif signal == "moduleStateChanged":
            pass
        elif signal == "moduleSettingsChanged":
            pass

    def serviceSignalHandler(self, package, signal, args):
        if package == self.iface.package and signal == "Changed":
            state = self.iface.getState()
            self.widgetService.setState(state)

    def clearItemList(self):
        """
            Clears item list.
        """
        self.listItems.clear()

    def hideNew(self):
        """
            Hides new button.
        """
        self.pushNew.hide()

    def hideFilter(self):
        """
            Hide filter.
        """
        self.comboFilter.hide()

    def makeItemWidget(self, id_, title="", description="", type_=None, icon=None, state=None):
        """
            Makes an item widget having given properties.
        """
        widget = ItemWidget(self.listItems, id_, title, description, type_, icon, state)

        self.connect(widget, QtCore.SIGNAL("stateChanged(int)"), self.slotItemState)
        self.connect(widget, QtCore.SIGNAL("editClicked()"), self.slotItemEdit)
        self.connect(widget, QtCore.SIGNAL("deleteClicked()"), self.slotItemDelete)

        return widget

    def addItem(self, id_, name="", description="", icon="security-medium", state=False):
        """
            Adds an item to list.
        """

        type_ = ""

        # Build widget and widget item
        widget = self.makeItemWidget(id_, name, description, type_,KIcon(icon), state)
        widgetItem = ItemListWidgetItem(self.listItems, widget)

        # Rules are static
        widget.hideDelete()

        # Add to list
        self.listItems.setItemWidget(widgetItem, widget)

        # Check if a filter matches item
        if not self.itemMatchesFilter(widgetItem):
            self.listItems.setItemHidden(widgetItem, True)

    def buildItemList(self):
        """
            Builds item list.
        """
        # Clear list
        self.clearItemList()

        def handler(package, exception, args):
            if exception:
                return
            modules = args[0]
            for name in modules:
                title, description, icon = self.iface.moduleInfo(name)
                state = QtCore.Qt.Unchecked
                if self.iface.getModuleState(name) == "on":
                    state = QtCore.Qt.Checked
                self.addItem(name, title, description, icon, state)
        self.iface.listModules(handler)

    def itemMatchesFilter(self, item):
        """
            Checks if item matches selected filter.
        """
        filter = str(self.comboFilter.itemData(self.comboFilter.currentIndex()).toString())
        if filter == "incoming" and item.getType() != "incoming":
            return False
        elif filter == "outcoming" and item.getType() != "outcoming":
            return False
        return True

    def buildFilter(self):
        """
            Builds item filter.
        """
        self.comboFilter.clear()
        self.comboFilter.addItem(i18n("All"), QtCore.QVariant("all"))

    def buildMenu(self):
        """
            Builds "Add New" button menu.
        """
        # Create menu for "new" button
        menu = QtGui.QMenu(self.pushNew)
        self.pushNew.setMenu(menu)

        # New item
        action = QtGui.QAction(i18n("Action"), self)
        action.setData(QtCore.QVariant("action"))
        menu.addAction(action)

    def showEditBox(self, id_, type_):
        """
            Shows edit box.
        """
        if self.animationLast == ANIM_HIDE:
            self.animationLast = ANIM_SHOW
            # Set range
            self.animator.setFrameRange(ANIM_TARGET, self.height() - ANIM_TARGET)
            # Go go go!
            self.animator.start()

    def hideEditBox(self):
        """
            Hides edit box.
        """
        if self.animationLast == ANIM_SHOW:
            self.animationLast = ANIM_HIDE
            # Set range
            self.animator.setFrameRange(self.frameEdit.height(), ANIM_TARGET)
            # Go go go!
            self.animator.start()

    def slotFilterChanged(self, index):
        """
            Filter is changed, refresh item list.
        """
        for i in range(self.listItems.count()):
            widgetItem = self.listItems.item(i)
            if self.itemMatchesFilter(widgetItem):
                self.listItems.setItemHidden(widgetItem, False)
            else:
                self.listItems.setItemHidden(widgetItem, True)

    def slotItemState(self, state):
        """
            Item state changed.
        """
        widget = self.sender()
        try:
            self.iface.setModuleState(widget.getId(), state == QtCore.Qt.Checked)
        except Exception, e:
            if "Comar.PolicyKit" in e._dbus_error_name:
                createMessage(self,"Error","Access denied.")
            else:
                createMessage(self,"Error", unicode(e))
            self.buildItemList()

    def slotItemEdit(self):
        """
            Edit button clicked, show configuration dialog.
        """
        widget = self.sender()

        parameters = self.iface.moduleParameters(widget.getId())
        savedParameters = self.iface.getModuleParameters(widget.getId())
        if not parameters:
            return

        dialog = PageDialog(self, parameters, savedParameters);

        if dialog.exec_():
            try:
                self.iface.setModuleParameters(widget.getId(), dialog.getValues())
            except Exception, e:
                if "Comar.PolicyKit" in e._dbus_error_name:
                    createMessage(self,"Error","Access denied.")
                else:
                    createMessage(self,"Error", unicode(e))

    def slotItemDelete(self):
        """
            Delete button clicked.
        """
        widget = self.sender()

    def slotOpenEdit(self, action):
        """
            New button clicked, show edit box.
        """
        # Get item type to add/
        type_ = str(action.data().toString())
        self.showEditBox(None, type_)

    def slotCancelEdit(self):
        """
            Cancel clicked on edit box, show item list.
        """
        self.hideEditBox()

    def slotSaveEdit(self):
        """
            Save clicked on edit box, save item details then show item list.
        """
        # Hide edit box
        self.hideEditBox()

    def slotServiceChanged(self, state):
        self.widgetService.setEnabled(False)
        try:
            self.iface.setState(state)
        except Exception, e:
            if "Comar.PolicyKit" in e._dbus_error_name:
                createMessage(self,"Error", "Access denied.")
            else:
                createMessage(self,"Error", unicode(e))
        self.widgetService.setEnabled(True)

    def slotAnimate(self, frame):
        """
            Animation frame changed.
        """
        self.frameEdit.setMaximumHeight(frame)
        self.frameList.setMaximumHeight(self.height() - frame)
        self.update()

    def slotAnimationFinished(self):
        """
            Animation is finished.
        """
        if self.animationLast == ANIM_SHOW:
            self.frameEdit.setMaximumHeight(ANIM_DEFAULT)
            self.frameList.setMaximumHeight(ANIM_TARGET)
        else:
            self.frameEdit.setMaximumHeight(ANIM_TARGET)
            self.frameList.setMaximumHeight(ANIM_DEFAULT)
