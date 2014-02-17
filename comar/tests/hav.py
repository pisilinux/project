#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import locale
import sys
import os

def handleError(exception):
    error = exception.get_dbus_name()
    message = exception.message
    if error.endswith("Comar.PolicyKit"):
        print "Access denied. '%s' access required" % message
    else:
        print message
    sys.exit(1)

def printUsage():
    print "Usage: %s <command>" % sys.argv[0]
    print "Commands:"
    print "  list-apps <model>"
    print "  list-models <app>"
    print "  register <app> <model> <script.py>"
    print "  remove <app>"
    sys.exit(1)

def main():
    if len(sys.argv) == 1:
        printUsage()

    bus = dbus.SystemBus()
    obj = bus.get_object('tr.org.pardus.comar3', '/', introspect=False)

    lang = locale.getdefaultlocale()[0].split("_")[0]
    obj.setLocale(lang, dbus_interface='tr.org.pardus.comar3')

    if sys.argv[1] == "list-apps":
        try:
            model = sys.argv[2]
        except IndexError:
            printUsage()
        try:
            apps = obj.listModelApplications(model, dbus_interface='tr.org.pardus.comar3')
        except dbus.DBusException, e:
            handleError(e)
            return
        for app in apps:
            print app
    elif sys.argv[1] == "list-models":
        try:
            app = sys.argv[2]
        except IndexError:
            printUsage()
        try:
            models = obj.listApplicationModels(app, dbus_interface='tr.org.pardus.comar3')
        except dbus.DBusException, e:
            handleError(e)
        for model in models:
            print model
    elif sys.argv[1] == "register":
        try:
            app = sys.argv[2]
            model = sys.argv[3]
            script = sys.argv[4]
        except IndexError:
            printUsage()
        path = os.path.realpath(script)
        try:
            obj.register(app, model, path, dbus_interface='tr.org.pardus.comar3')
        except dbus.DBusException, e:
            handleError(e)
    elif sys.argv[1] == "remove":
        try:
            app = sys.argv[2]
        except IndexError:
            printUsage()
        try:
            obj.remove(app, dbus_interface='tr.org.pardus.comar3')
        except dbus.DBusException, e:
            handleError(e)
    else:
        printUsage()

if __name__ == "__main__":
    main()
