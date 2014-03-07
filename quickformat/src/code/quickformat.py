#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2011 TUBITAK/BILGEM
#  Renan Çakırerk <renan at pardus.org.tr>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Library General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#  (See COPYING)

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QVariant, QSize, SIGNAL, QThread

from PyKDE4 import kdeui
from PyKDE4.kdecore import i18n
from PyKDE4.solid import Solid
from PyKDE4.kdecore import KCmdLineArgs

from quickformat.ui_quickformat import Ui_QuickFormat
from quickformat.formatter import Formatter

from quickformat.notifier import Notifier
from quickformat.notifier import PARTITION_TABLE_ERROR, NO_DEVICE, FORMAT_STARTED, FORMAT_SUCCESSFUL, FORMAT_FAILED, LOADING_DEVICES

from quickformat.about import aboutData
from quickformat.ui_volumeitem import Ui_VolumeItem

from quickformat.notifier_backend import OUT, TOPCENTER, MIDCENTER, CURRENT, OUT

import sys, os

import dbus

FILE_SYSTEMS = {"Ext4":"ext4",
                "Ext3":"ext3",
                "Ext2":"ext2",
                "FAT32":"vfat",
                "NTFS":"ntfs-3g",
                }

ACCEPTED_BUSSES = [Solid.StorageDrive.Usb,
                   Solid.StorageDrive.Ieee1394, # Firewire
                   Solid.StorageDrive.Platform] # Card Readers

ACCEPTED_DRIVE_TYPES = [Solid.StorageDrive.HardDisk,
                        Solid.StorageDrive.Floppy,
                        Solid.StorageDrive.CompactFlash,
                        Solid.StorageDrive.MemoryStick,
                        Solid.StorageDrive.SmartMedia,
                        Solid.StorageDrive.SdMmc,
                        Solid.StorageDrive.Xd]

class Volume():
    def __init__(self, volume):
        self.volume = volume

        self.icon = self.get_volume_icon()
        self.name = self.get_volume_name()
        self.path = self.get_volume_path()
        self.file_system = self.get_volume_file_system()
        self.size = self.get_volume_size()

        self.device_type = self.get_device_type()
        self.device_bus = self.get_device_bus()
        self.device_path = self.get_device_path()
        self.device_name = self.get_device_name()

    def has_accepted_bus(self):
        """ controls if the device is appropriate for formatting """
        if self.device_bus in ACCEPTED_BUSSES:
            return True

    def has_accepted_drivetype(self):
       if self.device_type in ACCEPTED_DRIVE_TYPES:
            return True


    # Get Device Information

    def get_device_type(self):
        """ returns the bus of the device """
        try:
            return self.volume.parent().asDeviceInterface(Solid.StorageDrive.StorageDrive).driveType()
        except:
            print "WARNING: get_device_type (no parent?) -> %s" % self.path

    def get_device_bus(self):
        """ returns the bus of the device """
        try:
            return self.volume.parent().asDeviceInterface(Solid.StorageDrive.StorageDrive).bus()
        except:
            print "WARNING: get_device_bus (no parent?) -> %s" % self.path

    def get_device_path(self):
        try:
            return str(self.volume.parent().asDeviceInterface(Solid.Block.Block).device())
        except:
            print "WARNING: get_device_path (no parent?) -> %s" % self.path
            return self.path

    def get_device_name(self):
        """ returns the device name that the volume resides on """
        return str("%s %s" % (self.volume.parent().vendor(), self.volume.parent().product()))


    # Get Volume Information

    def get_volume_icon(self):
        icon = str(self.volume.icon())
        iconPath = ":/images/images/" + icon + ".png"
        return QtGui.QPixmap(iconPath)

    def get_volume_name(self):
        return str(self.volume.product())

    def get_volume_path(self):
        return str(self.volume.asDeviceInterface(Solid.Block.Block).device())

    def get_volume_file_system(self):
        return str(self.volume.asDeviceInterface(Solid.StorageVolume.StorageVolume).fsType())

    def get_volume_size(self):
        return self.volume.asDeviceInterface(Solid.StorageVolume.StorageVolume).size()


class VolumeUiItem(Ui_VolumeItem, QtGui.QWidget):
    def __init__(self, volume, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.device.hide()

        self.name.setText(volume.device_name)
        self.device.setText(volume.device_path)

        self.label.setText(volume.name)
        self.path.setText(volume.path)

        size_human = self.size_to_human(volume.size)

        self.size.setText(size_human)
        self.format.setText("(%s)" % volume.file_system)
        self.icon.setPixmap(volume.icon)

    def size_to_human(self, size):
        size = size / 1024.0 ** 2

        if size >= 1000 and size < 100000:
            size = str("%.2f" % (size / 1024.0)) + " GB"
        elif size > 100000:
            size = str(int(size / 1024)) + " GB"
        else:
            size = str(int(size)) + " MB"

        return size


class QuickFormat(QtGui.QWidget):
    def __init__(self, parent = None, args = None):
        QtGui.QWidget.__init__(self, parent)
        self.__sysargs = args

        self.ui = Ui_QuickFormat()
        self.ui.setupUi(self)

        self.formatter = Formatter()

        self.first_run = True

        # Initial selection is the first partition found (see next comment)
        self.initial_selection = 0

        # If a partition path is given as argument, intial selection becomes the parition given
        self.__process_args__()

        # Connect Qt Signals
        self.__init_signals__()

        # Initialize custom widgets such as the new combobox
        self.__set_custom_widgets__()

        # Initialize the fancy notification widget (Derrived from PDS by Gokmen Goksel)
        self.__init_notifier__()

        self.show_volume_list()
        self.generate_file_system_list()

        self.volume_to_format = ""

        self.__make_initial_selection__(self.initial_selection)

        self.refreshing_devices = False

        # Monitor USB ports for any new devices
        notifier = Solid.DeviceNotifier().instance()
        self.connect(notifier, SIGNAL("deviceAdded(const QString&)"), self.slot_refresh_volume_list)
        self.connect(notifier, SIGNAL("deviceRemoved(const QString&)"), self.slot_refresh_volume_list)

    def __make_initial_selection__(self, index):
        self.ui.volumeName.setCurrentIndex(index)
        self.set_info()

    def __init_notifier__(self):
        self.notifier = Notifier(self)
        self.notifier.enableOverlay()

        self.notifier.busy.busy()
        self.notifier.setStyleSheet("color:white")

        self.notifier.adjustSize()
        self.notifier.label.adjustSize()

    def __set_custom_widgets__(self):
        self.ui.listWidget = QtGui.QListWidget(self)
        self.ui.volumeName.setModel(self.ui.listWidget.model())
        self.ui.volumeName.setView(self.ui.listWidget)

    def __process_args__(self):
        self.volumePathArg = ""
        if len(self.__sysargs) == 2:
            if not self.__sysargs[1].startswith("-"):
                self.volumePathArg = self.__sysargs[1]

    def __init_signals__(self):
        self.connect(self.ui.volumeName, SIGNAL("activated(int)"), self.set_info)
        self.connect(self.ui.btn_format, SIGNAL("clicked()"), self.format_device)
        self.connect(self.ui.btn_cancel, SIGNAL("clicked()"), self.close)

        # Formatter signals
        self.connect(self.formatter, SIGNAL("format_started()"), self.slot_format_started)
        self.connect(self.formatter, SIGNAL("format_successful()"), self.slot_format_successful)
        self.connect(self.formatter, SIGNAL("format_failed()"), self.slot_format_failed)
        self.connect(self.formatter, SIGNAL("partition_table_error()"), self.slot_partition_table_error)

    def filter_file_system(self, volume):
        if volume.has_accepted_bus() and volume.has_accepted_drivetype():
            return True

    def get_volumes(self):
        volumes = []

        # Get volumes
        for v in Solid.Device.listFromType(Solid.StorageDrive.StorageVolume):
            # Apply filter
            volume = Volume(v)
            if self.filter_file_system(volume):
                volumes.append(volume)
        return volumes

    def show_volume_list(self):
        self.ui.listWidget.clear()
        self.ui.volumeName.hidePopup()

        selectedIndex = 0
        currentIndex = 0

        volumes = self.get_volumes()

        if not volumes:
            self.no_device_notification()
        else:
            for volume in volumes:
                self.add_volume_to_list(volume)

            # select the appropriate volume from list
            self.ui.volumeName.setCurrentIndex(selectedIndex)

            # Auto-hide notifier
            if not self.formatter.formatting and not self.first_run and self.notifier.okButton.isHidden():
                QtCore.QTimer.singleShot(2000, self.hide_notifier)

            self.set_info()

        self.first_run = False


    def format_device(self):
        """ Starts the formatting operation """
        selected_file_system = FILE_SYSTEMS[str(self.ui.fileSystem.currentText())]
        selected_label = self.ui.volumeLabel.text()
        self.formatter.set_volume_to_format(self.volume_to_format, selected_file_system, selected_label)
        self.formatter.start()

    def slot_format_started(self):
        self.notifier.notify(FORMAT_STARTED)

    def slot_format_successful(self):
        self.notifier.notify(FORMAT_SUCCESSFUL)
        self.refresh_volume_list(notify=False)

    def slot_format_failed(self):
        self.notifier.notify(FORMAT_FAILED)

    def slot_partition_table_error(self):
        self.notifier.notify(PARTITION_TABLE_ERROR)

    def no_device_notification(self):
        if self.first_run:
            msgBox = QtGui.QMessageBox(1, i18n("QuickFormat"), i18n("There aren't any removable devices."))
            msgBox.exec_()
            sys.exit()
        else:
            self.notifier.notify(NO_DEVICE)

    def notify_refreshing_device_list(self):
        if not self.refreshing_devices and not self.formatter.formatting:
            self.refreshing_devices = True
            self.notifier.notify(LOADING_DEVICES)

    def refresh_volume_list(self, notify=True):
        if notify:
            self.notify_refreshing_device_list()

        self.show_volume_list()
        self.refreshing_devices = False

    def slot_refresh_volume_list(self, device):
        #FIX doesnt work if hal is used in system
        if not self.formatter.formatting:
            if str(device).find("UDisks")>=0:
                self.refresh_volume_list()

    def hide_notifier(self):
        self.notifier.animate(start=MIDCENTER, stop=MIDCENTER, direction=OUT)

    def generate_file_system_list(self):
        self.ui.fileSystem.clear()

        # Temporary sapce for file system list
        self.tempFileSystems = []

        # Get file system list
        for fs in FILE_SYSTEMS:
            self.tempFileSystems.append(fs)

        # Sort file system list
        self.tempFileSystems.sort()
        self.sortedFileSystems = self.tempFileSystems

        # Display file system list in combobox
        for fs in self.sortedFileSystems:
            self.ui.fileSystem.addItem(fs)

    def __find_key(self, dic, val):
        """return the key of a value of a dictionary"""
        return [k for k, v in dic.iteritems() if v == val][0]

    def set_info(self):
        """ Displays the selected volume info on Quickformat.ui """
        currentIndex = self.ui.volumeName.currentIndex()
        item = self.ui.listWidget.item(currentIndex)

        # Get item data (QVariant) convert to Python Object
        volume = item.data(32).toPyObject()

        # Display volume file system on UI if supported
        try:
            # find fileSystem index from list
            fsIndex = self.ui.fileSystem.findText(
                                                  self.__find_key(FILE_SYSTEMS, volume.file_system))
            # select fileSystem type
            self.ui.fileSystem.setCurrentIndex(fsIndex)
        except:
            self.ui.fileSystem.setCurrentIndex(0)
            print "Cannot match file system. Selecting Ext2 as default."

        self.ui.volumeLabel.setText(volume.name)
        self.ui.icon.setPixmap(volume.icon)

        # Set selected volume as the volume to format
        self.volume_to_format = volume


    def _prepare_selection_text(self, volume):
        if volume.name != "":
            return "%s - %s" % (volume.name, volume.path)

        return "%s - %s" % (device.name, volume.path)

    def add_volume_to_list(self, volume):

        # Create custom widget
        volume_item_widget = VolumeUiItem(volume, self.ui.listWidget)

        # Create an empty list widget item
        # First parameter is the text shown on the combobox when a selection is made
        selectionText = self._prepare_selection_text(volume)
        item = QtGui.QListWidgetItem(selectionText, self.ui.listWidget)

        # Add whole volume as the item data
        item.setData(32, QVariant(volume))

        # Set the item's widget to custom widget and append to list
        self.ui.listWidget.setItemWidget(item, volume_item_widget)

        item.setSizeHint(QSize(200,70))

        if volume.path == self.volumePathArg:
            self.initial_selection = self.ui.listWidget.count() - 1


if __name__ == "__main__":
    args = []
    if len(sys.argv) >= 2:
        if not sys.argv[1].startswith("-"):
            args = sys.argv
            sys.argv = [sys.argv[0]]

    # DBUS MainLoop
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    KCmdLineArgs.init(sys.argv, aboutData)
    app = kdeui.KApplication()

    quick_format = QuickFormat(args = args)
    quick_format.show()

    app.exec_()
