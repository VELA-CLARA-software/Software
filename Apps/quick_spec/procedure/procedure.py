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
//  FileName:    procedure.oy
//  Description: Generic template for procedure class for High Level Application
//               has simple interface (i.e. just an dictionary, and well-named functions)
//
//*/
'''
import VELA_CLARA_Camera_Control as cam
from numpy import array
from numpy import flipud
from numpy import transpose
from numpy import arange
from numpy import add
from numpy import zeros
from numpy import true_divide



class procedure(object):
    # init HWC
    init = cam.init()
    init.setVerbose()
    cam_cont = init.physical_Camera_Controller()

    last_image = []
    x_pix = 1392
    y_pix = 1040
    x_proj = None
    y_proj = None

    y_coords = []

    x_proj_rolling_sum = zeros(x_pix)
    x_proj_mean = []
    y_proj_rolling_sum = zeros(y_pix)
    y_proj_mean = []
    current_cam = 'UNKNOWN'

    def __init__(self):
        self.my_name = 'procedure'
        print(self.my_name + ', class initiliazed')
        self.reset()

    def reset(self):
        procedure.x_proj_rolling_sum = zeros(procedure.x_pix)
        procedure.x_proj_mean = zeros(procedure.x_pix)
        procedure.y_proj_rolling_sum = zeros(procedure.y_pix)
        procedure.y_proj_mean = zeros(procedure.x_pix)
        self.count = 0

    # called external to update states
    def update_image(self):
        if procedure.cam_cont.isVelaCam():
            procedure.x_pix = 1392
            procedure.y_pix = 1040
        else:
            procedure.x_pix = 1280
            procedure.y_pix = 1080

        # print 'get_fast_image'
        if procedure.cam_cont.isAcquiring():
            # return random.normal(size=(self.vc_image[0].num_pix_y, self.vc_image[0].num_pix_y))
            if procedure.cam_cont.takeFastImage():  # getFastImage_VC():
                # npData = array( self.vc_image[0].data ).reshape(( self.vc_image[0].num_pix_y,
                #                                              self.vc_image[0].num_pix_x))
                npData = array( procedure.cam_cont.getFastImage()).reshape(( procedure.x_pix,
                                                                             procedure.y_pix))

                self.count += 1

                procedure.last_image = flipud(npData)


                procedure.y_proj = procedure.last_image.sum(axis=0)
                procedure.x_proj = transpose(procedure.last_image.sum(axis=1))

                procedure.x_proj_rolling_sum = add(procedure.x_proj_rolling_sum, procedure.x_proj)
                procedure.y_proj_rolling_sum = add(procedure.y_proj_rolling_sum, procedure.y_proj)


                procedure.y_coords = range(procedure.y_pix)

                procedure.x_proj_mean = true_divide(procedure.x_proj_rolling_sum, self.count)
                procedure.y_proj_mean = true_divide(procedure.y_proj_rolling_sum, self.count)

        else:
            print('failed to get image')

        #procedure.current_cam = procedure.cam_cont.getSelectedCam()



