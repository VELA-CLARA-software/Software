#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS 2017
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QPushButton
from viewSource.Ui_view import Ui_view
from procedure.procedure import procedure
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE


class view(QMainWindow, Ui_view ):
    # custom close signal to send to controller
    #closing = QtCore.pyqtSignal()

    valves = {}

    # create a procedure object to access static data
    procedure = procedure()
    data = procedure.valve_states

    def __init__(self):
        QWidget.__init__(self)
        self.my_name = 'view'
        self.setupUi(self)

        self.setWindowIcon(QIcon('Valve_Status.ico'))

        self.red = "#ff5733"
        self.green = "#75ff33"

        import ctypes
        myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        #print(self.my_name + ', class initiliazed')

    def add_valves(self,names):
        self.vbox = QVBoxLayout()
        for name in names:
            view.valves[name] = QPushButton(self.widget)
            view.valves[name].setObjectName(name)
            view.valves[name].setText(name)
            self.vbox.addWidget(view.valves[name])
        self.vbox.addStretch(1)
        self.groupBox.setLayout(self.vbox)

    def update_gui(self):
        for name, state in view.data.iteritems():
            self.update_valve_widget(view.valves[name],state)

    def update_valve_widget(self,widget,state):
        if state == VALVE_STATE.VALVE_OPEN:
            widget.setStyleSheet("background-color: " + self.green)
            widget.setText( widget.objectName() + ' OPEN' )
        elif state == VALVE_STATE.VALVE_CLOSED:
            widget.setStyleSheet("background-color: " + self.red)
            widget.setText( widget.objectName() + ' CLOSED' )
        elif state == VALVE_STATE.VALVE_TIMING:
            widget.setStyleSheet("background-color: yellow")
            widget.setText( widget.objectName() + ' TIMING' )
        else:
            widget.setStyleSheet("background-color: magenta")
            widget.setText( widget.objectName() + ' ERROR' )
