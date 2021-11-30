'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify     //
//    it under the terms of the GNU General Public License as published by            //
//    the Free Software Foundation, either version 3 of the License, or               //
//    (at your option) any later version.                                             //
//    VELA-CLARA-Software is distributed in the hope that it will be useful,          //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
//    GNU General Public License for more details.                                    //
//                                                                                    //
//    You should have received a copy of the GNU General Public License               //
//    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //
//
//  Author:      DJS
//  Last edit:   16-11-2020
//  FileName:    valve status view.py
//  Description: GUI view for simple valve status app
//
//*/
'''
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from src.view.viewSource.Ui_view import Ui_view
import sys
from CATAP.HardwareFactory import * # would be nice JUST to import STATE here


sys.path.append('\\\\claraserv3\\claranet\\test\\CATAP\\bin\\')
sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\test\\CATAP\\bin\\')


class view(QMainWindow, Ui_view):
    '''
        view clas fro teh valv_status app. This view is ingherited from a QT designer .py file
        generated with pyuic5 from a ui file. DO NOT EDIT  the Ui_view file, insted make changes
        here, so that the computer generated source in Ui_view does not change.
        Dynamically generates a column of buttons for each valve passed to it,
        Changes the color of those buttons based on their STATE
    '''
    # custom close signal to send to controller
    # closing = QtCore.pyqtSignal()
    # dictionary to access valve widgets keyed by their names
    valves = {}

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)  # setup the UI frnm the base class
        self.setWindowIcon(QIcon('Valve_Status.ico'))  # set icon
        self.red = "#ff5733"  # some colors labels for convenience
        self.green = "#75ff33"
        self.magerta = "#ff00ff"
        self.yellow = "#ffff00"
        print(__name__ + ', class initialized')

    def add_valves(self, names):
        '''
            add valves ot the main GUI as Qpushbuttons, kept in a vertical layout
        :param names: valves defined in a list names
        '''
        self.vbox = QVBoxLayout()
        for name in names:
            view.valves[name] = QPushButton(self.widget)
            view.valves[name].setObjectName(name)
            view.valves[name].setText(name)
            self.vbox.addWidget(view.valves[name])
        self.vbox.addStretch(1)
        self.groupBox.setLayout(self.vbox)

    def update_gui(self, valve_state_dict):
        '''
            update the gui
        :param valve_state_dict: dict of valve STATEs keyed by their name
        '''
        for name, state in valve_state_dict.items():
            self.update_valve_widget(view.valves[name], state)

    def update_valve_widget(self, widget, state):
        '''
            update a widget by changing its color based on the state of a valve
        :param widget: widget to update
        :param state: valve STATE (OPEN, CLOSED etc.)
        '''
        if state == STATE.OPEN:
            # print("state is open")
            widget.setStyleSheet("background-color: " + self.green)
            widget.setText(widget.objectName() + ' OPEN')
        elif state == STATE.CLOSED:
            # print("state is clsoed")
            widget.setStyleSheet("background-color: " + self.red)
            widget.setText(widget.objectName() + ' CLOSED')
        elif state == STATE.TIMING:
            widget.setStyleSheet("background-color: yellow")
            widget.setText(widget.objectName() + ' TIMING')
        else:
            # print("state is else")
            widget.setStyleSheet("background-color: " + self.magerta)
            widget.setText(widget.objectName() + ' ERROR')
