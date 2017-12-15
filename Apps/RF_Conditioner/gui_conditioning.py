#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS 2017
# part of MagtnetApp
from PyQt4.QtGui import * # shit python
from PyQt4.QtCore import * # shit python
from conditioning_gui import Ui_MainWindow
import datetime



class gui_conditioning(QMainWindow, Ui_MainWindow):
    def __init__(self, window_name = "", root = "/" ):
        QMainWindow.__init__(self)
        self.setupUi(self)