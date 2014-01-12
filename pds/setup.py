#!/usr/bin/python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Python Libs
import os
import shutil

# DistUtils
from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.clean import clean
from distutils.command.sdist import sdist
from distutils.sysconfig import get_python_lib

PROJECT = 'pds'

def plp():
    return os.path.join(get_python_lib(), PROJECT)

class Clean(clean):
    def run(self):
        print 'Cleaning ...'
        os.system('find -name *.pyc|xargs rm -rf')
        for dirs in ('build', 'dist'):
            if os.path.exists(dirs):
                print ' removing: ', dirs
                shutil.rmtree(dirs)
        clean.run(self)

class Dist(sdist):
    def run(self):
        os.system('python setup.py build')
        sdist.run(self)

class Uninstall(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        print 'Uninstalling ...'
        project_dir = plp()
        if os.path.exists(project_dir):
            print ' removing: ', project_dir
            shutil.rmtree(project_dir)

setup(name=PROJECT,
      version='1.2.6',
      description='Pds: Pisi Desktop Services',
      long_description='Pds is a Python Library that helps developers for '\
                       'creating desktop environment independet UI applications',
      license='GNU GPL2',
      author='Pisi Linux',
      author_email='admins@pisilinux.org',
      url='http://pisilinux.org',
      packages=[PROJECT, 'pds.tests', 'pds.ui'],
      data_files = [(plp(), ['README', 'COPYING', 'HELP'])],
      cmdclass = {
          'uninstall':Uninstall,
          'clean'    :Clean,
          }
     )
