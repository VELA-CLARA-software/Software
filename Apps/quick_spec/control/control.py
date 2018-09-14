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
//  Last edit:   05-06-2018
//  FileName:    mainApp.oy
//  Description: Generic template for control class for general High Level Application
//
//
//*/
'''
from PyQt4.QtCore import QTimer

class control(object):
    procedure = None
    view  = None
    def __init__(self,sys_argv = None,view = None, procedure= None):
        self.my_name = 'control'
        '''define model and view'''
        control.procedure = procedure
        control.view = view
        self.set_up_gui()
        # update gui with this:
        self.start_gui_update()
        # show view
        self.view.show()
        print(self.my_name + ', class initiliazed')

        control.view.reset_mean_pushButton.released.connect(self.handle_reset_mean_pushButton)

    def handle_reset_mean_pushButton(self):
        control.procedure.reset()


    def set_up_gui(self):
        # connect main buttons to functions
        # control.view.closeButton.clicked.connect(self.handle_close_all)
        # control.view.openButton.clicked.connect(self.handle_open_all)
        # control.view.add_valves(control.procedure.valve_names)
        # connect individual valve buttons to functions
        pass

    def update_gui(self):
        '''
            generic function that updates values from the procedure and then updates the gui
        '''
        control.procedure.update_image()
        control.view.update_gui()
        #print('update_gui')



    def start_gui_update(self):
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(100)

