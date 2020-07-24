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
import sys
# Add the release folder to the path to get latest HWC
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage')

from src.data import data
from src.procedure import procedure
import gui
from PyQt4.QtCore import QTimer

class controller(object):# inherit of an python object


    def __init__(self, argv):
        object.__init__(self)
        self.my_name = "controller"
        self.argv = argv
        #print('controller created with these arguments: ',self.argv)

        # create the main objects used in this design
        self.data = data()
        self.procedure = procedure()
        self.gui = gui.gui()
        self.gui.show_gui()


        self.connect_gui_widgets()

        print('controller, starting timer')
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)


    def connect_gui_widgets(self):
        self.gui.gun_check_box.clicked.connect(self.handle_gun_check_box)
        self.gui.linac_check_box.clicked.connect(self.handle_linac_check_box)


    def handle_gun_check_box(self):
        self.procedure.set_keep_alive_gun( self.gui.gun_check_box.isChecked() )


    def handle_linac_check_box(self):
        self.procedure.set_keep_alive_linac( self.gui.linac_check_box.isChecked()  )


    def update(self):
        self.procedure.update_data()
        self.gui.update()



