#!/usr/bin/python
# -*- coding: utf-8 -*-

import pds
import traceback
from time import time
from pds.qiconloader import QIconLoader
from PyQt4.QtGui import QMessageBox
from context import *

Pds = pds.Pds('firewall-manager', debug = True)
# Force to use Default Session for testing
#Pds.session = pds.DefaultDe
print 'Current session is : %s %s' % (Pds.session.Name, Pds.session.Version)

i18n = Pds.i18n
KIconLoader = QIconLoader(Pds,forceCache=True)
KIcon = KIconLoader.icon

time_counter = 0
start_time = time()
last_time = time()

def _time():
    global last_time, time_counter
    trace = list(traceback.extract_stack())
    diff = time() - start_time
    print ('%s ::: %s:%s' % (time_counter, trace[-2][0].split('/')[-1], trace[-2][1])), diff, diff - last_time
    last_time = diff
    time_counter += 1

def createMessage(self,errorTitle, errorMessage):
    errorTitle = i18n(errorTitle)
    errorMessage= i18n(errorMessage)
    self.messageBox = QMessageBox(errorTitle, errorMessage, QMessageBox.Critical, QMessageBox.Ok, 0, 0)
    self.messageBox.show()
