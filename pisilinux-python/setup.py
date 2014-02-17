#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import os.path
import sys
import glob
import shutil
from distutils.core import setup, Extension
from distutils.command.install import install

import pardus

distfiles = """
    setup.py
    pardus/*.py
    pardus/*.c
    pardus/xorg/*.py
    pardus/xorg/*.c
    po/*.po
    po/*.pot
    tools/*.py
    tools/*.sh
    MODULES
    README
"""

def make_dist():
    distdir = "pardus-python-%s" % pardus.versionString()
    list = []
    for t in distfiles.split():
        list.extend(glob.glob(t))
    if os.path.exists(distdir):
        shutil.rmtree(distdir)
    os.mkdir(distdir)
    for file_ in list:
        cum = distdir[:]
        for d in os.path.dirname(file_).split('/'):
            dn = os.path.join(cum, d)
            cum = dn[:]
            if not os.path.exists(dn):
                os.mkdir(dn)
        shutil.copy(file_, os.path.join(distdir, file_))
    os.popen("tar -czf %s %s" % ("pardus-python-" + pardus.versionString() + ".tar.gz", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)

class Install(install):
    def finalize_options(self):
        # NOTE: for Pardus distribution
        if os.path.exists("/etc/pardus-release"):
            self.install_platlib = '$base/lib/pardus'
            self.install_purelib = '$base/lib/pardus'
        install.finalize_options(self)

    def run(self):
        install.run(self)
        self.installi18n()

    def installi18n(self):
        for name in os.listdir('po'):
            if not name.endswith('.po'):
                continue
            lang = name[:-3]
            print "Installing '%s' translations..." % lang
            os.popen("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
            if not self.root:
                self.root = "/"
            destpath = os.path.join(self.root, "usr/share/locale/%s/LC_MESSAGES" % lang)
            if not os.path.exists(destpath):
                os.makedirs(destpath)
            shutil.copy("po/%s.mo" % lang, os.path.join(destpath, "pardus-python.mo"))

setup(name="pardus",
      version=pardus.versionString(),
      description="Python Modules for Pardus",
      long_description="Python Modules for Pardus.",
      license="GNU GPL2",
      author="Pardus Developers",
      author_email="info@pardus.org.tr",
      url="http://www.pardus.org.tr/",
      packages = ['pardus', 'pardus.xorg'],
      ext_modules = [Extension('pardus.xorg.capslock',
                               sources=['pardus/xorg/capslock.c'],
                               libraries=['X11']),
                     Extension('pardus.csapi',
                               sources=['pardus/csapi.c'],
                               libraries=[]),
                    ],
      cmdclass = {'install' : Install})
