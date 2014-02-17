#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import dbus
import locale
import sys
import os

import piksemel

def printUsage():
    print "Usage: %s <command>" % sys.argv[0]
    print "Commands:"
    print "  call <app> <model> <method> <arguments>"
    print "  list-apps [model]"
    print "  list-models <app>"
    print "  list-methods <app> <model>"
    print "  register <app> <model> <script.py>"
    print "  remove <app>"
    sys.exit(1)

def introspect(link, path="/"):
    bus = dbus.SystemBus()
    obj = bus.get_object(link.address, path)

    nodes = []
    interfaces = {}

    xml = piksemel.parseString(obj.Introspect(dbus_interface="org.freedesktop.DBus.Introspectable"))
    for tag in xml.tags():
        if tag.name() == "node":
            nodes.append(tag.getAttribute("name"))
        elif tag.name() == "interface":
            # Remove root interface address
            iface = tag.getAttribute("name")
            iface = iface.split(link.interface)[1]
            iface = iface[1:]
            interfaces[iface] = []
            for child in tag.tags():
                if child.name() == "method":
                    method = child.getAttribute("name")
                    interfaces[iface].append(method)

    return nodes, interfaces

def main():
    if len(sys.argv) == 1:
        printUsage()

    link = comar.Link()
    link.setLocale()

    if sys.argv[1] == "list-apps":
        try:
            model = sys.argv[2]
        except IndexError:
            model = None
        if model:
            try:
                _group, _class = model.split(".")
            except ValueError:
                print "Invalid model name"
                return -1
            apps = list(comar.Call(link, _group, _class))
        else:
            apps, interfaces = introspect(link, "/package")
        for app in apps:
            print app
    elif sys.argv[1] == "list-models":
        try:
            app = sys.argv[2]
        except IndexError:
            print "Application name is required."
            return -1
        apps, interfaces = introspect(link, "/package/%s" % app)
        for interface in interfaces:
            print interface
    elif sys.argv[1] == "list-methods":
        try:
            app = sys.argv[2]
            model = sys.argv[3]
        except IndexError:
            print "Application and model name are required."
            return -1
        apps, interfaces = introspect(link, "/package/%s" % app)
        if model in interfaces:
            for method in interfaces[model]:
                print method
    elif sys.argv[1] == "register":
        try:
            app = sys.argv[2]
            model = sys.argv[3]
            script = os.path.realpath(sys.argv[4])
        except IndexError:
            printUsage()
        link.register(app, model, script)
    elif sys.argv[1] == "remove":
        try:
            app = sys.argv[2]
        except IndexError:
            printUsage()
        link.remove(app)
    elif sys.argv[1] == "call":
        try:
            app = sys.argv[2]
            model = sys.argv[3]
            method = sys.argv[4]
        except IndexError:
            printUsage()
        try:
            _group, _class = model.split(".")
        except ValueError:
            print "Invalid model name"
            return -1
        met = comar.Call(link, _group, _class, app, method)
        try:
            if len(sys.argv) > 5:
                args = []
                for i in sys.argv[5:]:
                    if i.startswith("[") or i.startswith("(") or i.startswith("{"):
                        args.append(eval(i))
                    else:
                        args.append(i)
                print met.call(*args)
            else:
                print met.call()
        except dbus.exceptions.DBusException, e:
            if e._dbus_error_name.endswith(".Comar.PolicyKit"):
                print "Access to '%s' PolicyKit action required." % e.get_dbus_message()
            else:
                print "Error:"
                print "  %s" % e.get_dbus_message()
            return -1
    else:
        printUsage()

    return 0

if __name__ == "__main__":
    sys.exit(main())
