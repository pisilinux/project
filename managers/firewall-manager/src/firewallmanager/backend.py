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

# Comar
import comar


class Interface:
    def __init__(self):
        self.link = comar.Link()
        self.link.setLocale()
        self.link.useAgent()
        self.package = self.getMainPackage()

    def listenFirewallSignals(self, func):
        self.link.listenSignals("Network.Firewall", func)

    def listenServiceSignals(self, func):
        self.link.listenSignals("System.Service", func)

    def getPackages(self):
        """
            List of packages that provide Net.Firewall model
        """
        return list(self.link.Network.Firewall)

    def getMainPackage(self):
        """
            Net.Firewall is heavily IPTables dependent.
        """
        return "iptables"

    def getState(self):
        return self.link.Network.Firewall[self.package].getState() == "on"

    def setState(self, state, func=None):
        if func:
            if state:
                self.link.Network.Firewall[self.package].setState("on", async=func)
            else:
                self.link.Network.Firewall[self.package].setState("off", async=func)
        else:
            if state:
                self.link.Network.Firewall[self.package].setState("on")
            else:
                self.link.Network.Firewall[self.package].setState("off")

    def listModules(self, func=None):
        if func:
            self.link.Network.Firewall[self.package].listModules(async=func)
        else:
            return self.link.Network.Firewall[self.package].listModules()

    def moduleInfo(self, module, func=None):
        if func:
            self.link.Network.Firewall[self.package].moduleInfo(module, async=func)
        else:
            return self.link.Network.Firewall[self.package].moduleInfo(module)

    def moduleParameters(self, module, func=None):
        if func:
            self.link.Network.Firewall[self.package].moduleParameters(module, async=func)
        else:
            return self.link.Network.Firewall[self.package].moduleParameters(module)

    def getModuleState(self, module):
        return self.link.Network.Firewall[self.package].getModuleState(module)

    def setModuleState(self, module, state):
        if state:
            state = "on"
        else:
            state = "off"
        self.link.Network.Firewall[self.package].setModuleState(module, state)

    def getModuleParameters(self, module, func=None):
        if func:
            self.link.Network.Firewall[self.package].getModuleParameters(module, async=func)
        else:
            return self.link.Network.Firewall[self.package].getModuleParameters(module)

    def setModuleParameters(self, module, parameters, func=None):
        if func:
            self.link.Network.Firewall[self.package].setModuleParameters(module, parameters, async=func)
        else:
            return self.link.Network.Firewall[self.package].setModuleParameters(module, parameters)
