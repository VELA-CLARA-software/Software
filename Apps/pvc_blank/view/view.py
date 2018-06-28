#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS 2017
# part of MagtnetApp
from PyQt4 import QtGui, QtCore
from viewSource.Ui_view import Ui_view


class view(QtGui.QMainWindow, Ui_view ):
    # custom close signal to send to controller
    closing = QtCore.pyqtSignal()

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.my_name = 'view'
        self.setupUi(self)