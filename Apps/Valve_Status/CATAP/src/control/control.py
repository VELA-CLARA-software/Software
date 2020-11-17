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
//  FileName:    control.py
//  Description: control class for valve_status, creates objects and  links procedure to view
//
//
//*/
'''
from PyQt5.QtCore import QTimer
from src.procedure.valve_procedure import valve_procedure
from src.view.view import view as view


class control(object):
    '''
        This class buids teh procedure and the view and handles passing data / signals
        between them
    '''
    procedure = None
    view = None

    def __init__(self, sys_argv=None):
        '''define model and view'''
        control.procedure = valve_procedure()
        control.view = view()
        self.set_up_gui()
        # update gui with this:
        self.start_gui_update()
        # show view
        self.view.show()
        print(__name__ + ', class initialized')

    def set_up_gui(self):
        '''
            Sets up the widget slots / signals from the gui
        '''
        # connect main buttons to functions
        control.view.closeButton.clicked.connect(self.handle_close_all)
        control.view.openButton.clicked.connect(self.handle_open_all)
        control.view.add_valves(control.procedure.valve_names)
        # connect individual valve buttons to functions
        for valve_name, widget in control.view.valves.items():
            widget.clicked.connect(self.handle_open_close)

    def handle_open_all(self):
        '''
            calls procedure function to open all valves. Connected from GUI closeButton widget
        '''
        control.procedure.open_all()

    def handle_close_all(selname):
        '''
            calls procedure function to close all valves. Connected from GUI closeButton widget
        '''
        control.procedure.close_all()

    def handle_open_close(self):
        '''
            toggel open or closed (dpends on current state of valve chosen)
        '''
        sender = control.view.sender()
        control.procedure.open_or_close(str(sender.objectName()))

    def start_gui_update(self):
        '''
            start the timer that calls the update_gui  function every 100 ms
        '''
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(100)

    def update_gui(self):
        '''
            updates states in the procedure and then update gui with the states from procedure
        '''
        control.procedure.update_states()
        control.view.update_gui(control.procedure.valve_states)
