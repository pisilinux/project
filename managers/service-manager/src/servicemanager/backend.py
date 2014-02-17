#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import comar

class ServiceIface:
    """ Service Interface """

    def __init__(self, handler):
        self.link = comar.Link()
        self.link.setLocale()
        self.link.useAgent()
        self.handler = handler

    def services(self, func=None):
        if func:
            self.link.System.Service.info( async=func )
        else:
            return list(self.link.System.Service)

    def start(self, service):
        self.link.System.Service[service].start( async=self.handler )

    def stop(self, service):
        self.link.System.Service[service].stop( async=self.handler )

    def restart(self, service):
        # some services does not have reload method in their service
        # scripts, so it should be fixed in Comar itself.
        def handler(package, exception, args):
            if not exception:
                self.link.System.Service[service].start(async=self.handler)
        self.link.System.Service[service].stop(async=handler)

    def setEnable(self, service, state):
        states = {True:'on', False:'off'}
        self.link.System.Service[service].setState(states[state], async = self.handler)

    def info(self, service):
        return self.link.System.Service[service].info()

    def listen(self, func):
        self.link.listenSignals("System.Service", func)

