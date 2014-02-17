#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#


import context as ctx
from context import *


PACKAGE = "User Manager"
appName= "user-manager"
version="3.0.0"



if ctx.Pds.session == ctx.pds.Kde4:

    # PyKDE
    from PyKDE4.kdecore import KAboutData, ki18n, ki18nc

    # Application Data
    appName     = "user-manager"
    modName     = "usermanager"
    programName = ki18n("User Manager")
    version     = "3.0.0"
    description = ki18n("User Manager")
    license     = KAboutData.License_GPL
    copyright   = ki18n("(c) 2006-2010 TUBITAK/UEKAE")
    text        = ki18n(None)
    homePage    = "http://www.pardus.org.tr/eng/projects"
    bugEmail    = "bugs@pardus.org.tr"
    catalog     = appName
    aboutData   = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

    # Author(s)
    aboutData.addAuthor(ki18n("Gökmen Göksel"), ki18n("Current Maintainer"))
    aboutData.addAuthor(ki18n("Bahadır Kandemir"), ki18n("First Developer"))
    aboutData.setTranslator(ki18nc("NAME OF TRANSLATORS", "Your names"), ki18nc("EMAIL OF TRANSLATORS", "Your emails"))

    # Use this if icon name is different than appName
    aboutData.setProgramIconName("drive-harddisk")
