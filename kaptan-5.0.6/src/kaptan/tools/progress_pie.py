#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class DrawPie(QWidget):
    def __init__(self, totalPiece, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(0, 0, 100, 40)
        self.step = 360 / (totalPiece + 1)
        self.currentPiece = 1

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # pen sets the edge color of the circles
        painter.setPen(QColor(20,20,20, 0))
        w = self.size().width()
        h = self.size().height()

        painter.setBrush(QBrush(QColor(255, 255, 255, 220)))
        x = 13
        y = 6
        r = 23
        rect = QRect(x, y, r, r)

        painter.drawEllipse(rect)

        painter.setBrush(QBrush(QColor(20, 20, 20, 100)))

        startAngle = 90 * 16;
        spanAngle = -((self.currentPiece * self.step) * 16);

        painter.drawPie(rect, startAngle, spanAngle);

        painter.end()


    def updatePie(self, currentIndex):
        self.currentPiece = currentIndex + 1
        self.update()
        #qApp.processEvents()

