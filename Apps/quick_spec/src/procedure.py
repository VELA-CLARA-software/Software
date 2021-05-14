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
//  FileName:    procedure.py
//  Description: get camera images and calculate projections based on data passed in
//               quite a few different options.
//               Heavily dependant on data.py for options adn to write data to
//*/
'''
import sys
sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\packages\\vcc\\bin\\Release\\')

import VELA_CLARA_Camera_Control as cam
from numpy import array
from numpy import flipud
from numpy import fliplr
from numpy import transpose
from numpy import arange
from numpy import add
from numpy import zeros
from numpy import true_divide
import data



class procedure(object):
    # init HWC
    init = cam.init()
    init.setVerbose()
    cam_cont = init.physical_Camera_Controller()


    def __init__(self):
        self.data = data.data()
        self.my_name = 'procedure'
        print(self.my_name + ', class initiliazed')
        self.reset()

        self.data.values[data.num_x_pix] = 1392
        self.data.values[data.num_y_pix] = 1040


    def reset(self):
        self.data.values[data.y_proj_rolling_sum] = 0
        self.data.values[data.x_proj_rolling_sum] = 0

        procedure.y_proj_mean = zeros(self.data.values[data.num_y_pix])
        procedure.x_proj_mean = zeros(self.data.values[data.num_x_pix])

        self.data.values[data.rolling_count] = 0



    # called external to update states
    def update_data(self):
        self.update_cam()
        self.update_image()


    def update_cam(self):
        self.data.values[data.current_cam] = procedure.cam_cont.getSelectedCamScrName()

        procedure.current_cam = procedure.cam_cont.getSelectedCamScrName()
        if self.data.values[data.current_cam] !=self.data.values[data.current_cam]:
            self.reset()
            self.data.values[data.last_cam] = self.data.values[data.current_cam]


    def update_image(self):
        self.data.values[data.num_x_pix] = procedure.cam_cont.getNumPixX()
        self.data.values[data.num_y_pix] = procedure.cam_cont.getNumPixY()

        #print('x_pix ',procedure.x_pix, ', y_pix ', procedure.y_pix)
        # print 'get_fast_image'
        if procedure.cam_cont.isAcquiring():
            # return random.normal(size=(self.vc_image[0].num_pix_y, self.vc_image[0].num_pix_y))
            if procedure.cam_cont.takeFastImage():  # getFastImage_VC():
                # npData = array( self.vc_image[0].data ).reshape(( self.vc_image[0].num_pix_y,
                #                                              self.vc_image[0].num_pix_x))
                # reshap is rows coolumsn (so y then x (!)
                npData = array( procedure.cam_cont.getFastImage()).reshape(( self.data.values[
                                                                                 data.num_y_pix],
                                                                             self.data.values[
                                                                                 data.num_x_pix]))
                if len(npData) > 0:
                    self.data.values[data.image_data] =  fliplr( transpose(npData) )
                    self.data.values[data.got_image] = True
                else:
                    self.data.values[data.got_image] = False

        else:
            print('failed to get image')
            self.data.values[data.got_image] = False

    def update_projections(self,img_data):
        #
        # omfg what a mess

        self.data.values[data.y_proj] = img_data.sum(axis=0)
        self.data.values[data.x_proj] = img_data.sum(axis=1)

        if self.data.values[data.average]:

            self.data.values[data.rolling_count] += 1

            if self.data.values[data.y_proj_rolling_sum] is 0:
                self.data.values[data.y_proj_rolling_sum] = self.data.values[data.y_proj]
            else:
                self.data.values[data.y_proj_rolling_sum] = add(self.data.values[
                                                                    data.y_proj_rolling_sum],
                                                                self.data.values[data.y_proj])

            if self.data.values[data.x_proj_rolling_sum] is 0:
                self.data.values[data.x_proj_rolling_sum] = self.data.values[data.x_proj]
            else:
               self.data.values[data.x_proj_rolling_sum] = add(self.data.values[
                                                                data.x_proj_rolling_sum] ,
                                                            self.data.values[data.x_proj])

            self.data.values[data.y_proj] = true_divide(self.data.values[
                                                                data.y_proj_rolling_sum] ,
                                                            self.data.values[data.rolling_count])
            self.data.values[data.x_proj] = true_divide(self.data.values[
                                                                data.x_proj_rolling_sum] ,
                                                            self.data.values[data.rolling_count])

        if self.data.values[data.sub_min]:
            self.data.values[data.y_proj] = self.data.values[data.y_proj] - min(self.data.values[data.y_proj])
            self.data.values[data.x_proj] = self.data.values[data.x_proj] - min(self.data.values[
                                                                                    data.x_proj])

        self.data.values[data.x_proj_max] = max(self.data.values[data.x_proj])
        self.data.values[data.y_proj_max] = max(self.data.values[data.y_proj])

        self.data.values[data.x_proj_max_index] = self.data.values[data.x_proj].argmax()
        self.data.values[data.y_proj_max_index] = self.data.values[data.y_proj].argmax()

        self.data.values[data.fwhm_hi] = len(self.data.values[data.x_proj])
        self.data.values[data.fwhm_lo] = 0
        half_max= 0.5*self.data.values[data.x_proj_max]
        #print('half_max = ', half_max)
        for i in range(self.data.values[data.x_proj_max_index], len(self.data.values[data.x_proj])):

            if self.data.values[data.x_proj][i] <=  half_max:
                self.data.values[data.fwhm_hi] = i
                #print('hi_edge = ', self.data.values[data.x_proj][i], ', i = ', i)
                break
        for i in range(self.data.values[data.x_proj_max_index], 0, -1):
            if self.data.values[data.x_proj][i] <= half_max:
                self.data.values[data.fwhm_lo] = abs(i)
                #print('lo_edge = ', self.data.values[data.x_proj][i], ', i = ', i)
                break
        self.data.values[data.fwhm] =  self.data.values[data.fwhm_hi] - self.data.values[
            data.fwhm_lo]




