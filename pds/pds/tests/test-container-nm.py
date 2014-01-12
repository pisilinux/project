#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services

# Copyright (C) 2010-2011, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Qt Libraries
from PyQt4 import Qt

# PDS Container
from pds.container import PApplicationContainer

class PNetworkManager(PApplicationContainer):
    def __init__(self, parent = None):
        PApplicationContainer.__init__(self, parent)

    def startNetworkManager(self):
        ret = self.start("nm-connection-editor", ("--winid", str(self.winId())))

        if ret[0]:
            self.setMinimumSize(Qt.QSize(450, 200))
            self.show()

        return ret

if __name__ == "__main__":
    import sys

    app = Qt.QApplication(sys.argv)

    ui = PNetworkManager()
    ui.startNetworkManager()

    app.lastWindowClosed.connect(sys.exit)

    app.exec_()
