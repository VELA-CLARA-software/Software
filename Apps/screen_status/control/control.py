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

import view.view as view
import procedure.procedure as procedure



class control(object):
    procedure = None
    view  = None
    def __init__(self,sys_argv = None,view = None, procedure= None):
        self.my_name = 'control'
        '''define model and view'''
        control.procedure = procedure
        control.view = view

        # update gui with this:
        print('controller, starting timer')
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(100)

        # show view
        self.view.show()
        self.set_up_gui()
        # update gui with this:
        self.start_gui_update()
        # show view
        self.view.show()
        print(self.my_name + ', class initiliazed')

    def set_up_gui(self):
        # connect main buttons to functions
        control.view.stopButton.clicked.connect(self.handle_all_out)
        control.view.add_cams(control.procedure.scr_names)
        # connect individual valve buttons to functions
        for name, widget in control.view.screens.iteritems():
            widget.clicked.connect(self.handle_in_out)

    def handle_screen_in(self):
        control.procedure.screen_in()

    def handle_all_out(self):
        control.procedure.screen_in()

    def handle_in_out(self):
        sender = control.view.sender()
        control.procedure.in_out(str(sender.objectName()))

    def start_gui_update(self):
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(100)

    def update_gui(self):
        '''
            generic function that updates values from the procedure and then updates the gui
        '''
        control.procedure.update_states()
        control.view.update_gui()
        #print('update_gui')



