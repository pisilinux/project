#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

import time
a = time.time()

from pds import Pds

b = Pds('package-manager')

print 'Current Desktop Environment         :', b.session.Name
print 'Current Desktop Environment Version :', b.session.Version
print 'I18n test result for session        :', b.session.i18n('Package Manager')
print 'I18n test result for gettext        :', b.i18n('Package Manager')
print 'It took                             :', time.time()-a

