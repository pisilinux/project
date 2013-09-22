#!/usr/bin/python
#-*- coding: utf-8 -*-

from distutils.core import setup

setup(name="panda",
    version="0.2",
    description="Python Modules for panda",
    license="GNU GPL2",
    url="http://www.pisilinux.org/",
    py_modules = ["panda"],
    data_files = [
        ("/usr/libexec", ["panda-helper"]),
    ]
)
