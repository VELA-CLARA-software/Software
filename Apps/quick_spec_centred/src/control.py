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
//  Last edit:   21-09-2018
//  FileName:    control.py
//  Description: controller that coordinstes quick_spec gui and procedure, using data in data.py
//
//
//*/
'''
from PyQt4.QtCore import QTimer
import procedure as procedure
import view as view
import data

class control(object):
    procedure = None
    view  = None
    data = None

    def __init__(self,sys_argv = None):
        self.my_name = 'control'
        '''define model and view'''
        control.procedure = procedure.procedure()
        control.view = view.view()
        control.data = data.data()
        # update gui with this:
        self.start_gui_update()
        # show view
        self.view.show()
        #
        # connect GUI widgets
        control.view.reset_mean_pushButton.released.connect(self.handle_reset_mean_pushButton)
        control.view.setRef_button.released.connect(self.handle_set_ref_pushButton)
        control.view.clearRef_button.released.connect(self.handle_clear_ref_pushButton)
        control.view.average_cbox.clicked.connect(self.handle_average)
        control.view.useROI_cbox.clicked.connect(self.handle_ROI)
        control.view.useBackground_cbox.clicked.connect(self.handle_Back)

    def handle_reset_mean_pushButton(self):
        control.procedure.reset()

    def handle_set_ref_pushButton(self):
        control.data.values[data.y_ref] = control.data.values[data.y_proj]
        control.data.values[data.x_ref] = control.data.values[data.x_proj]
        control.data.values[data.x_ref_2] = control.data.values[data.x_proj_2]
        control.data.values[data.has_ref] = True

    def handle_clear_ref_pushButton(self):
        control.data.values[data.has_ref] = False
        control.data.values[data.ref_plotted] = False

    def handle_Back(self):
        control.data.values[data.sub_min] = control.view.useBackground_cbox.isChecked()

    def handle_ROI(self):
        control.procedure.reset()
        control.data.values[data.use_ROI] = control.view.useROI_cbox.isChecked()

    def handle_average(self):
        control.data.values[data.average] = control.view.average_cbox.isChecked()

    def update_gui(self):
        control.procedure.update_data()
        if control.data.values[data.got_image]:
            if control.data.values[data.use_ROI]:
                control.procedure.update_projections(
                        control.view.roi.getArrayRegion( control.data.values[data.image_data],
                                                         control.view.image_item))
            else:
                control.procedure.update_projections(control.data.values[data.image_data])
        #else:
        #    print 'Not got image'
        control.view.update_gui()

    def start_gui_update(self):
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(100)
