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
//  Last edit:   24-11-2020
//  FileName:    control.py
//  Description: control class for laser transverse profile  decomposition
//
//
//*/
'''
#from PyQt5.QtCore import QTimer
from src.procedure.procedure import procedure
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
        control.procedure = procedure()
        control.view = view()
        self.set_up_gui()
        # update gui with this:
        # show view
        self.view.show()
        print(__name__ + ', class initialized')

    def set_up_gui(self):
        '''
            Sets up the widget slots / signals from the gui
        '''
        # connect main buttons to functions
        control.view.get_roi_data_button.clicked.connect(self.handle_get_roi_data_button)
        control.view.get_roi_data_button.clicked.connect(self.handle_analyse_button)


    def handle_analyse_button(self):
        print("handle_analyse_button")
        control.procedure.analyse()

    def handle_get_roi_data_button(self):
        print("handle_get_roi_data_button")
        control.procedure.get_roi_data()

        control.view.update_image(control.procedure.roi_data, 0.062,0.062)

