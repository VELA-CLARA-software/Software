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
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets, uic, QtGui
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
        self.view.raise_()
        self.view.activateWindow()
        print(__name__ + ', class initialized')

    def set_up_gui(self):
        '''
            Sets up the widget slots / signsetDataals from the gui
        '''
        #pass image data to view
        self.view.setup_full_image(**control.procedure.get_full_image_paramters())
        control.view.update_mask_read_and_set(**control.procedure.get_mask())
        # connect main buttons to functions
        control.view.get_roi_data_button.clicked.connect(self.handle_get_roi_data_button)
        control.view.get_image_data_button.clicked.connect(self.handle_get_image_data_button)
        control.view.print_button.clicked.connect(self.handle_print_button)
        control.view.set_roi_from_mask.clicked.connect(self.handle_set_roi_from_mask)
        control.view.analyse_button.clicked.connect(self.handle_analyse_button)
        self.procedure.set_roi_from_mask()
        #control.view.get_roi_data_button.clicked.connect(self.handle_analyse_button)
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(200)

    def handle_get_image_data_button(self):
        print("handle_get_image_data_button")
        control.procedure.get_image()
        control.view.update_vc_image(control.procedure.full_image_data)
        r = control.procedure.get_ROI()
        m = control.procedure.get_mask()
        print("GET ROI = {} ".format(r))
        print("GET MASK = {} ".format(m))
        control.view.update_roi_read(**r)
        control.view.update_mask_read(**m)
        self.update_crosshairs()
        print(r)

    def handle_get_roi_data_button(self):
        print("handle_get_roi_data_button")
        control.procedure.get_roi_data()
        print("update_image")
        #control.view.update_image(control.procedure.roi_data, 0.062, 0.062)
        control.view.update_roi_image(control.procedure.roi_data, 1, 1)

    def handle_set_roi_from_mask(self):
        print('ellipse_roi_userChanged called')
        x_rad, y_rad = 0.5 * self.view.ellipse_roi_user.size()
        x, y = self.view.ellipse_roi_user.pos() + [x_rad, y_rad]
        print(x_rad, y_rad,x,y)
        self.procedure.set_mask_ROI(roi_x = int(x), roi_y = int(y), x_rad= int(x_rad) , y_rad=int(
            y_rad))

    def update_crosshairs(self):
        analysis = control.procedure.getAnalysisData()
        print(analysis)
        control.view.update_crosshair( x0 = analysis["x_pix"] , y0= analysis["y_pix"],
                                       sx= analysis["sigma_x_pix"], sy= analysis["sigma_y_pix"] )

        roi = control.procedure.get_ROI()

        control.view.update_crosshair_ROI( x0 = analysis["x_pix"] - roi["x_min"] ,
                                           y0= analysis["y_pix"] - roi["y_min"],
                                       sx= analysis["sigma_x_pix"], sy= analysis["sigma_y_pix"] )


    def handle_analyse_button(self):
        print("handle_analyse_button")
        control.procedure.analyse()

    def handle_print_button(self):
        print("handle_print_button")
        control.procedure.print_values()

    def update_gui(self):
        pass
