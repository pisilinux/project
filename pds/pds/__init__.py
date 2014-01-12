#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>
# 2010 - H. İbrahim Güngör <ibrahim:pardus.org.tr>
# 2011 - Comak Developers <comak:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Pardus Desktop Services
from os import path
from os import getenv
from os import popen

import piksemel
import gettext

# PyQt4 Core Libraries
from PyQt4.QtCore import QSettings

# Logging
import logging

# Pds Objects
from pds.environments import *

class Pds:

    SupportedDesktops = (DefaultDe, Kde4, Kde3, Xfce, Enlightenment, LXDE,
                        Fluxbox, Gnome, Gnome3)

    def __init__(self, catalogName='', debug=False):
        self._session           = None
        self._version           = None
        self.home               = getenv('HOME').strip()
        self._config_content    = None

        _log_file = path.join(self.home, '.pdsLogfor%s.log' % catalogName)
        if debug:
            logging.basicConfig(filename = _log_file, level = logging.DEBUG, \
                    filemode = 'w')
        else:
            logging.basicConfig(level = logging.INFO)

        if catalogName:
            self.__trans = gettext.translation(catalogName, fallback=True)

            def __i18n(*text):
                if len(text) == 1:
                    return self.__trans.ugettext(text[0])
                ttt = unicode(self.__trans.ugettext(text[0]))
                for i in range(1,len(text)):
                    ttt = ttt.replace('%%%d' % i, unicode(text[i]))
                return ttt

            self.i18n = __i18n
            DefaultDe.i18n = staticmethod(__i18n)

        self._acceptedMethods = filter(lambda x: not x.startswith('__') or \
                                                 not x == 'i18n',
                                                 dir(self.session))

        self.notifierInitialized = False
        self.catalogName = catalogName

    def __getattr__(self, name):

        if str(name) in self._acceptedMethods:
            return getattr(self.session, str(name))

        if not self.__dict__.has_key(name):
            raise AttributeError, name

    def updatei18n(self, lang):
        if self.catalogName:
            self.__trans = gettext.translation(self.catalogName, \
                    languages=[lang], fallback=True)

    def notify(self, title, message, icon = None):
        try:
            import pynotify
            if not self.notifierInitialized:
                pynotify.init(self.catalogName)
                self.notifierInitialized = True
            notifier = pynotify.Notification(unicode(title), unicode(message),\
                    icon or self.catalogName)
            notifier.show()
        except:
            logging.info(message)

    def settings(self, key, default):
        value = None
        if self.session.ConfigType == 'ini':
            # FIXME we dont need to force everytime.
            if path.exists(str(self.config_file)):
                settings = self.parse(self.config_file, force = True)
            else:
                return default
            _value = settings.value(key)
            if not _value.toString():
                # Sometimes kdeglobals stores values without quotes
                _value = _value.toStringList()
                if _value:
                    value = _value.join(',')
            else:
                value = unicode(_value.toString())
            if not value or value == '':
                logging.debug('Switching to default conf')
                alternateConfig = self.session.DefaultConfigPath or \
                        path.join(self.install_prefix, self.session.ConfigFile)
                settings = self.parse(alternateConfig, force = True)
                value = unicode(settings.value(key, default).toString())

        elif self.session.ConfigType == 'xml':
            settings = self.parse(self.config_file, 'xml').getTag('property')
            def getval(settings, key):
                for tag in settings.tags():
                    if tag.getAttribute('name') == key:
                        return tag.getAttribute('value')
            value = getval(settings, key)
            if not value or value == '':
                alternateConfig = self.session.DefaultConfigPath or \
                        path.join(self.install_prefix, self.session.ConfigFile)
                settings = self.parse(alternateConfig, 'xml',
                        force = True).getTag('property')
                value = getval(settings, key)

        elif self.session.ConfigType == 'env':
            value = getenv(key)

        return value or default

    def parse(self, fpath, ftype = 'ini', force = False):
        if self._config_content and not force:
            return self._config_content
        if ftype == 'ini':
            self._config_content = QSettings(fpath, QSettings.IniFormat)
        elif ftype == 'xml':
            self._config_content = piksemel.parse(fpath)
        return self._config_content

    @property
    def session(self):
        if not self._session:
            env = getenv('DESKTOP_SESSION')
            if env == 'default' or not env or env == 'gnome':
                session = readfile('/etc/default/desktop', DefaultDe.Name)
                env     = session.split('=')[1].strip()
            for de in Pds.SupportedDesktops:
                if env:
                    if env in de.SessionTypes or env == de.Name:
                        self._session = de
                else:
                    if de.VersionKey:
                        if getenv(de.VersionKey) == de.Version:
                            self._session = de
            if not self._session:
                self._session = DefaultDe
            else:
                for de in Pds.SupportedDesktops:
                    if de.Version == self.version and (env in de.SessionTypes or env == de.Name):
                        self._session = de
        return self._session

    @property
    def version(self):
        for key in ('KDE_SESSION_VERSION', 'KDEDIR'):
            env = getenv(key)
            if env:
                self._version = env
                break
        if self._version:
            self._version = self._version.split('/')[-1]
        return self._version

    @property
    def config_file(self):
        cf = path.join(self.config_path, self.session.ConfigFile)
        if path.exists(cf):
            return cf
        return None

    @property
    def config_path(self):
        cpaths = self.session.ConfigPath
        if not type(cpaths) is tuple:
            cpaths = [cpaths]

        for cpath in cpaths:
            rpath = cpath.replace('$HOME', self.home)
            if path.exists(rpath):
                return rpath

    @property
    def install_prefix(self):
        return popen('%s --prefix' % self.session.ConfigBin).read().strip()

def readfile(file_path, fallback=None):
    if path.exists(file_path):
        return open(file_path).read()
    return fallback

