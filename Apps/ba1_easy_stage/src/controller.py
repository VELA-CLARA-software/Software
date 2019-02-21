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
//  Last edit:   11-01-2019
//  FileName:    controller.py
//  Description: template for class for controller in generic High Level Application
//
//
//*/
'''

from PyQt4 import QtCore
from src.data import data
from src.procedure import procedure
from src.gui import gui



class controller(object):# inherit of an python object
    def __init__(self, argv):
        object.__init__(self)
        self.my_name = "controller"
        self.argv = argv
        print('controller created with these arguments: ',self.argv)
        # create the main objects used in this design
        self.data = data()
        self.procedure = procedure()
        self.gui = gui()
        self.hello()
        self.gui.show_gui()
        self.connect_gui_widgets()

        self.start_count = 0
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(100)

    def connect_gui_widgets(self):
        for key, value in self.gui.move_buttons.iteritems():
            print('connect_gui_widgets ', key, value)
            key.clicked.connect(self.move)
            key.setDisabled(True)
        for key, value in self.gui.dev_move_buttons.iteritems():
            key.clicked.connect(self.move_to_device)
            #key.clicked.connect(self.move_to_device)
            print('connect_gui_widgets 2 ', key, value)

    def move(self):
        stage = self.gui.move_buttons[self.gui.sender()]
        position = self.gui.set_labels[stage].value()
        print('move ', stage, position)
        #self.proccedure.move(self.gui.move_buttons[self.gui.sender()])


    def move_to_device(self):
        stage = self.gui.dev_move_buttons[self.gui.sender()]
        device = str(self.gui.device_labels[stage].currentText())
        print('move_to_device',stage,  device)
        self.procedure.move_device(stage,device)

    def hello(self):
        print(self.my_name+ ' says hello')
        self.data.hello()
        self.procedure.hello()
        self.gui.hello()


    def update_gui(self):
        self.procedure.update_values()
        self.gui.update()