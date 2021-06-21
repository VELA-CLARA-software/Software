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
#sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release\\')
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
from numpy import float64
import data
import time



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
        self.data.values[data.y_proj_2_rolling_sum] = 0
        self.data.values[data.x_proj_2_rolling_sum] = 0

        procedure.y_proj_mean = zeros(self.data.values[data.num_y_pix])
        procedure.x_proj_mean = zeros(self.data.values[data.num_x_pix])

        self.data.values[data.rolling_count] = 0



    # called external to update states
    def update_data(self):
        self.update_cam()
        self.update_image()


    def update_cam(self):
        #print '\nIn update_cam'
        self.data.values[data.current_cam] = procedure.cam_cont.getSelectedCamScrName()
        #self.data.values[data.current_cam] = 'VIRTUAL_CATHODE' # set to VC for testing
        procedure.current_cam = procedure.cam_cont.getSelectedCamScrName()
        #procedure.current_cam = 'VIRTUAL_CATHODE' # set to VC for testing
        if self.data.values[data.current_cam] !=self.data.values[data.current_cam]:
            self.reset()
            self.data.values[data.last_cam] = self.data.values[data.current_cam]
        #print '\n\n\n\nCurrent camera = ', self.data.values[data.current_cam]


    def update_image(self):
        self.data.values[data.num_x_pix] = procedure.cam_cont.getNumPixX()
        self.data.values[data.num_y_pix] = procedure.cam_cont.getNumPixY()

        if self.data.values[data.current_cam] == 'C2V-SCR-01':
            self.data.values[data.num_y_pix] = 1280 #hack to make C2V work!
        elif self.data.values[data.current_cam] == 'VIRTUAL_CATHODE':
            self.data.values[data.num_x_pix] = 1280
            self.data.values[data.num_y_pix] = 1080

        if procedure.cam_cont.isAcquiring():
            tfi = procedure.cam_cont.takeFastImage()
            #print 'tfi = ', tfi
            #time.sleep(0.05) # Is this needed?
            if tfi:  # getFastImage_VC():
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

    def mean_index(self, y):
        x = range(len(y))
        xx = array(x, dtype=float64)
        yy = array(y, dtype=float64)
        mean_x = sum(xx*yy)/sum(yy)
        #print 'x position of mean = ', mean_x
        index = min(range(len(xx)), key=lambda i:abs(xx[i]-mean_x))
        #print 'in mean_index', index
        return index

    def update_projections(self,img_data):
        #
        # omfg what a mess

        self.data.values[data.y_proj] = img_data.sum(axis=0)
        self.data.values[data.x_proj] = img_data.sum(axis=1)

        # need to bring forward background subtraction for use in centering
        if self.data.values[data.sub_min]:
            self.data.values[data.x_proj_temp] = self.data.values[data.x_proj] - min(self.data.values[data.x_proj])
        else:
            self.data.values[data.x_proj_temp] = self.data.values[data.x_proj]

        length = len(self.data.values[data.x_proj_temp])
        #print '\n\nlength = ', length
        halflength = int(round(length/2))
        x_offset = self.mean_index(self.data.values[data.x_proj_temp])
        #print 'x_offset = ', x_offset
        self.data.values[data.x_proj_2] = zeros(2*length)
        #print len(self.data.values[data.x_proj_2][length-x_offset:2*length-x_offset])
        self.data.values[data.x_proj_2][length-x_offset:2*length-x_offset] = self.data.values[data.x_proj_temp]

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

####################
            if self.data.values[data.x_proj_2_rolling_sum] is 0:
                self.data.values[data.x_proj_2_rolling_sum] = self.data.values[data.x_proj_2]
            else:
               self.data.values[data.x_proj_2_rolling_sum] = add(self.data.values[
                                                                data.x_proj_2_rolling_sum],
                                                            self.data.values[data.x_proj_2])
####################

            self.data.values[data.y_proj] = true_divide(self.data.values[
                                                                data.y_proj_rolling_sum] ,
                                                            self.data.values[data.rolling_count])
            self.data.values[data.x_proj] = true_divide(self.data.values[
                                                                data.x_proj_rolling_sum] ,
                                                            self.data.values[data.rolling_count])
            self.data.values[data.x_proj_2] = true_divide(self.data.values[
                                                                data.x_proj_2_rolling_sum] ,
                                                            self.data.values[data.rolling_count])

        if self.data.values[data.sub_min]:
            self.data.values[data.y_proj] = self.data.values[data.y_proj] - min(self.data.values[data.y_proj])
            self.data.values[data.x_proj] = self.data.values[data.x_proj] - min(self.data.values[
                                                                                    data.x_proj])
            self.data.values[data.x_proj_2] = self.data.values[data.x_proj_2] - min(self.data.values[
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
        # centred fwhm

        self.data.values[data.fwhm] =  self.data.values[data.fwhm_hi] - self.data.values[
            data.fwhm_lo]
