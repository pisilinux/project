#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# The QProgressIndicator class lets an application display a progress
# indicator to show that a lengthy task is under way.
# QProgressIndicator is based on http://qt-apps.org/content/show.php?content=115762

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Qt Libraries
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize

from PyQt4.QtGui import QColor
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QPalette

class QProgressIndicator(QWidget):

    def __init__(self, parent, color = None):
        QWidget.__init__(self, parent)

        self.angle = 0
        self.timerId = -1
        self.delay = 80
        self.displayedWhenStopped = False
        self.color = self.palette().color(QPalette.Text) if not color else QColor(color)

    def busy(self):
        self.startAnimation()
        self.show()

    def isAnimated(self):
        return not self.timerId == -1

    def setDisplayedWhenStopped(self, state):
        self.displayedWhenStopped = state
        self.update()

    def isDisplayedWhenStopped(self):
        return self.displayedWhenStopped

    def startAnimation(self):
        self.angle = 0
        if self.timerId == -1:
            self.timerId = self.startTimer(self.delay)

    def stopAnimation(self):
        if not self.timerId == -1:
            self.killTimer(self.timerId)
        self.timerId = -1
        self.update()

    def setAnimationDelay(self, delay):
        if not self.timerId == -1:
            self.killTimer(self.timerId)
        self.delay = delay
        if self.timerId == -1:
            self.timerId = self.startTime(self.delay)

    def setColor(self, color):
        self.color = color
        self.update()

    def sizeHint(self):
        return QSize(20,20)

    def heightForWidth(self, width):
        return width

    def timerEvent(self, event):
        self.angle = (self.angle + 30) % 360
        self.update()

    def paintEvent(self, event):
        if not self.displayedWhenStopped and not self.isAnimated():
            return

        width = min(self.width(), self.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        outerRadius = (width-1) * 0.5
        innerRadius = (width-1) * 0.5 * 0.38

        capsuleHeight = outerRadius - innerRadius
        capsuleWidth  = capsuleHeight * 0.23 if width > 32 else capsuleHeight * 0.35
        capsuleRadius = capsuleWidth / 2

        for i in range(12):
            color = QColor(self.color)
            color.setAlphaF(float(1.0 - float(i / 12.0)))
            p.setPen(Qt.NoPen)
            p.setBrush(color)
            p.save()
            p.translate(self.rect().center())
            p.rotate(self.angle - float(i * 30.0))
            p.drawRoundedRect(-capsuleWidth * 0.5,\
                              -(innerRadius + capsuleHeight),\
                              capsuleWidth,\
                              capsuleHeight,\
                              capsuleRadius,\
                              capsuleRadius)
            p.restore()

