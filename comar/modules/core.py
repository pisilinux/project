#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil

def listModelApplications(model):
    apps = []
    scriptDir = os.path.join(config_datapath(), "scripts", model)
    if not os.path.exists(scriptDir):
        return apps
    for i in os.listdir(scriptDir):
        if i.endswith(".py"):
            apps.append(i[:-3])
    return apps

def listApplicationModels(app):
    models = []
    scriptDir = os.path.join(config_datapath(), "apps", app)
    if not os.path.exists(scriptDir):
        return models
    for i in os.listdir(scriptDir):
        if not i.startswith("."):
            models.append(i)
    return models

def register(app, model, filename):
    scriptDir = os.path.join(config_datapath(), "scripts", model)
    scriptFile = os.path.join(scriptDir, "%s.py" % app)
    try:
        os.mkdir(scriptDir)
    except:
        pass
    shutil.copy(filename, scriptFile)

    scriptDir = os.path.join(config_datapath(), "apps", app)
    scriptFile = os.path.join(scriptDir, model)
    try:
        os.mkdir(scriptDir)
    except:
        pass
    try:
        file(scriptFile, "w").write("")
    except:
        pass

    return True

def remove(app):
    scriptDir = os.path.join(config_datapath(), "apps", app)
    if not os.path.exists(scriptDir):
        return
    for i in os.listdir(scriptDir):
        if not i.startswith("."):
            scriptFile = os.path.join(config_datapath(), "scripts", i, "%s.py" % app)
            try:
                os.unlink(scriptFile)
            except:
                pass
    shutil.rmtree(scriptDir)

def model_xml(modelName):
    if modelName == "Core":
        xml = '<interface name="%s">' % config_interface()
    else:
        xml = '<interface name="%s.%s">' % (config_interface(), modelName)
    for _name, (_type, _action_id, _sig_in, _sig_out) in config_modelbase()[modelName].iteritems():
        if _type == 0:
            xml += '<method name="%s">' % _name
        else:
            xml += '<signal name="%s">' % _name
        for arg in _sig_in:
            xml += '<arg type="%s" direction="in"/>' % arg
        for arg in _sig_out:
            xml += '<arg type="%s" direction="out"/>' % arg
        if _type == 0:
            xml += '</method>'
        else:
            xml += '</signal>'
    xml += '</interface>'
    return xml


def introspect():
    path = bus_path()
    xml = '<node name="%s">' % path
    if path == '/':
        xml += model_xml("Core")
        xml += '<node name="package"/>'
    elif path == '/package':
        scriptDir = os.path.join(config_datapath(), "apps")
        for i in os.listdir(scriptDir):
            if not i.startswith("."):
                xml += '<node name="%s"/>' % i
    elif path.startswith('/package/'):
        app = path.split("/package/")[1]
        for name in listApplicationModels(app):
            xml += model_xml(name)
    xml += '</node>'
    return xml
