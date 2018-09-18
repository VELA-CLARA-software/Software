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
        # update gui with this:
        self.start_gui_update()
        # show view
        self.view.show()
        print(self.my_name + ', class initiliazed')
        control.view.reset_mean_pushButton.released.connect(self.handle_reset_mean_pushButton)
        control.view.setRef_button.released.connect(self.handle_set_ref_pushButton)
        control.view.clearRef_button.released.connect(self.handle_clear_ref_pushButton)
        control.view.average_cbox.clicked.connect(self.handle_average)

    def handle_reset_mean_pushButton(self):
        control.procedure.reset()

    def handle_set_ref_pushButton(self):
        control.procedure.set_ref(control.view.average_cbox.isChecked())

    def handle_clear_ref_pushButton(self):
        control.procedure.clear_ref()

    def handle_average(self):
        if control.view.average_cbox.isChecked():
            control.procedure.use_average = True
        else:
            control.procedure.use_average = False
        print 'handle_average use average = ' + str(control.procedure.use_average )

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

