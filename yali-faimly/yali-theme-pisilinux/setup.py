#!/usr/bin/env python
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os
from distutils.core import setup
from distutils.command.build import build
from distutils.command.install import install

THEME_DIR = "usr/share/yali/theme/pisilinux"

class Build(build):
    def run(self):
        build.run(self)

        self.mkpath(self.build_base)
        self.spawn(["rcc", "-binary", "data.qrc", "-o", "%s/data.rcc" % self.build_base])


class Install(install):
    def run(self):
        install.run(self)

        self.copy_file("build/data.rcc", os.path.join(self.root or "/", THEME_DIR))


setup(name="yali-theme-pisilinux",
      version= "0.3",
      description="Pisi Linux theme for YALI (Yet Another Linux Installer)",
      license="Latest GNU GPL version",
      author="Pisi Linux Developers",
      author_email="admin@pisilinux.org",
      url="https://github.com/pisilinux/project/tree/master/yali-theme-pisilinux",
      data_files=[("/%s" % THEME_DIR, ["style.qss"])],
      cmdclass = {'build': Build,
                  'install': Install})
