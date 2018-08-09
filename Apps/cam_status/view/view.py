#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS 2017
#from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QPushButton

from viewSource.Ui_view import Ui_CamState
from procedure.procedure import procedure
from VELA_CLARA_Camera_Control import ACQUIRE_STATE

class view(QMainWindow, Ui_CamState ):
    # custom close signal to send to controller
    # closing = QtCore.pyqtSignal()

    # dictionary for each camera
    cams = {}

    # create a procedure object to access static data
    procedure = procedure()
    data = procedure.states

    def __init__(self):
        QWidget.__init__(self)
        self.my_name = 'view'
        self.setupUi(self)
        self.setWindowIcon(QIcon('resources\\cam_status\\moview.ico'))

    def add_cams(self,names):
        self.vbox = QVBoxLayout()
        for name in names:
            view.cams[name] = QPushButton(self.widget)
            view.cams[name].setObjectName(name)
            view.cams[name].setText(name)
            self.vbox.addWidget(view.cams[name])
        self.vbox.addStretch(1)
        self.groupBox.setLayout(self.vbox)

    def update_gui(self):
        for name, state in view.data.iteritems():
            self.update_valve_widget(view.cams[name],state)

    def update_valve_widget(self,widget,state):
        if state == ACQUIRE_STATE.ACQUIRING:
            widget.setStyleSheet("background-color: green")
            widget.setText( widget.objectName() + ' Active' )
        elif state == ACQUIRE_STATE.NOT_ACQUIRING:
            widget.setStyleSheet("background-color: red")
            widget.setText( widget.objectName() + ' ' )
        elif state == ACQUIRE_STATE.ACQUIRING_ERROR:
            widget.setStyleSheet("background-color: magenta")
            widget.setText( widget.objectName() + ' ERROR' )
        else:
            widget.setStyleSheet("background-color: yellow")
            widget.setText( widget.objectName() + ' ERROR' )

