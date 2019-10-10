#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Controllers is free software: you can redistribute it and/or modify  //
//    it under the terms of the GNU General Public License as published by            //
//    the Free Software Foundation, either version 3 of the License, or               //
//    (at your option) any later version.                                             //
//    VELA-CLARA-Controllers is distributed in the hope that it will be useful,       //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
//    GNU General Public License for more details.                                    //
//                                                                                    //
//    You should have received a copy of the GNU General Public License               //
//    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //
//
//  Author:      DJS
//  Last edit:   03-07-2018
//  FileName:    virtual_cathode_model.py
//  Description: The model for the virtual cathode operator application
//
//
//
//
//*/
'''
import sys,os
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\')
#sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release\\')
import VELA_CLARA_PILaser_Control as pil
import virtual_cathode_model_data as model_data
from numpy import array
from numpy import amin
from numpy import amax
from numpy import reshape
from numpy import transpose
from numpy import flipud
from numpy import random
import time
#from scipy.stats import multivariate_normal




class virtual_cathode_model():

    def __init__(self):
        # PIL control
        self.init = pil.init()
        #self.init.setVerbose()
        self.pil = self.init.physical_PILaser_Controller()
        #
        # own a reference to the data dictionary
        self.data = model_data.model_data()
        # shorten the reference to data.values and data.previous_values
        self.values = self.data.values
        self.previous_values = self.data.previous_values
        '''
            Get some object references. These are used to update values in data dict. Object 
            references MUST be contained within a mutable type (e.g. list, dictionary, ... ) 
            Then, make some friendlier names to reference these objects'
        '''
        self.hardware_objects = {}
        # shutter 1 object
        self.hardware_objects[self.data.shut1] = self.pil.getShutterObjConstRef(self.data.shut1)
        self.shutter1  = self.hardware_objects[self.data.shut1]
        # shutter 2 object
        self.hardware_objects[self.data.shut2] = self.pil.getShutterObjConstRef(self.data.shut2)
        self.shutter2  = self.hardware_objects[self.data.shut2]
        # VC DAQ object
        self.hardware_objects[self.data.vc_daq] = self.pil.getClaraDAQObj_VC()
        self.vc_daq  = self.hardware_objects[self.data.vc_daq]
        # Photo-Injector Laser Object
        self.hardware_objects[self.data.pil_object] = self.pil.getPILObjConstRef()
        self.pil_obj = self.hardware_objects[self.data.pil_object]
        # VC image data (i.e. the online analysis) object
        self.hardware_objects[self.data.vc_image_data] = self.pil.getVCDataObjConstRef()
        self.vc_data  = self.hardware_objects[self.data.vc_image_data]
        # VC camera object
        self.hardware_objects[self.data.vc_cam] = self.pil.getCameraObj()
        self.vc_cam = self.hardware_objects[self.data.vc_cam]
        # VC camera image object object
        self.hardware_objects[self.data.vc_image] = self.pil.getImageObj()
        self.vc_image = self.hardware_objects[self.data.vc_image]
        # the VC camera state object
        self.hardware_objects[self.data.vc_state] = self.pil.getStateObj()
        self.vc_state = self.hardware_objects[self.data.vc_state] = self.pil.getStateObj()
        # the VC mask object
        self.hardware_objects[self.data.vc_mask] = self.pil.getMaskObj()
        self.vc_mask = self.hardware_objects[self.data.vc_mask]
        # PIL mirror object
        self.hardware_objects[self.data.pil_mirror] = self.pil.getpilMirrorObjConstRef()
        self.mirror = self.hardware_objects[self.data.pil_mirror]
        '''
            Some constants
        '''
        self.values[self.data.y_pix_scale_factor] = self.vc_image.y_pix_scale_factor
        self.values[self.data.x_pix_scale_factor] = self.vc_image.x_pix_scale_factor
        self.values[self.data.x_pix_to_mm] = self.vc_image.x_pix_to_mm
        self.values[self.data.y_pix_to_mm] = self.vc_image.y_pix_to_mm
        self.values[self.data.num_pix_x] = self.vc_image.num_pix_x
        self.values[self.data.num_pix_y] = self.vc_image.num_pix_y
        self.values[self.data.xpix_full] = self.values[self.data.num_pix_x] * \
                                            self.values[self.data.x_pix_scale_factor]
        self.values[self.data.ypix_full] = self.values[self.data.num_pix_y] * \
                                            self.values[self.data.y_pix_scale_factor]
        # get a fake image to start things off (plus used when debugging)
        self.values[self.data.image]  = self.get_fake_image()

    def reset_running_stats(self):
        '''
            Running stats are the 'running mean and sigma calculated in the controller for
            WCM, x, y position, sig_x, sig_y and cov.
        '''
        self.pil.clearRunningValues()

    def update_values(self):
        '''
            set previous_values to values, then update values
            https://stackoverflow.com/questions/2465921/how-to-copy-a-dictionary-and-only-edit-the-copy
            we don't need to keep a history of the image, so manually opt out of that
        '''
        for key, value in  self.values.iteritems():
            if key != self.data.image:
                self.previous_values[key] = value
        '''
            Get latest values from controllers and put them in the data dict
        '''
        self.values[self.data.is_acquiring] = self.pil.isAcquiring()
        self.values[self.data.is_analysing] = self.pil.isAnalysing()
        self.values[self.data.is_collecting_or_saving] = self.pil.isNotBusy()

        self.values[self.data.x_pix] = self.vc_data.x_pix
        self.values[self.data.y_pix] = self.vc_data.y_pix
        self.values[self.data.sig_x_pix] = self.vc_data.sig_x_pix
        self.values[self.data.sig_y_pix] = self.vc_data.sig_y_pix

        self.values[self.data.x_val] = self.vc_data.x
        self.values[self.data.y_val] = self.vc_data.y
        self.values[self.data.sx_val] = self.vc_data.sig_x
        self.values[self.data.sy_val] = self.vc_data.sig_y
        self.values[self.data.cov_val] = self.vc_data.sig_xy
        self.values[self.data.avg_pix_val] = self.vc_data.avg_pix

        self.values[self.data.x_mean] = self.vc_data.x_mean
        self.values[self.data.y_mean] = self.vc_data.y_mean
        self.values[self.data.sx_mean] = self.vc_data.sig_x_mean
        self.values[self.data.sy_mean] = self.vc_data.sig_y_mean
        self.values[self.data.cov_mean] = self.vc_data.sig_xy_mean
        self.values[self.data.avg_pix_mean] = self.vc_data.avg_pix_mean

        self.values[self.data.x_sd] = self.vc_data.x_sd
        self.values[self.data.y_sd] = self.vc_data.y_sd
        self.values[self.data.sx_sd] = self.vc_data.sig_x_sd
        self.values[self.data.sy_sd] = self.vc_data.sig_y_sd
        self.values[self.data.cov_sd] = self.vc_data.sig_xy_sd
        self.values[self.data.avg_pix_sd] = self.vc_data.avg_pix_sd

        self.values[self.data.wcm_val] = self.pil_obj.Q
        self.values[self.data.wcm_mean] = self.pil_obj.Q_mean
        self.values[self.data.wcm_sd] = self.pil_obj.Q_sd
#        self.values[self.data.wcm_buffer_full] = self.pil_obj.Q_full

        # these are flakey  laser INTENSITY
        self.values[self.data.int_val] = self.pil_obj.energy * 1000000
        self.values[self.data.int_mean] = self.pil_obj.energy_mean * 1000000
        self.values[self.data.int_sd] = self.pil_obj.energy_sd * 1000000
 #       self.values[self.data.laser_buffer_full] = self.pil_obj.energy_full

        #print('take image START')
        self.values[self.data.image] = self.get_fast_image()

        self.values[self.data.is_setting_pos] = self.pil.isSettingPos()
        #print('take image FIN')

        self.values[self.data.min_level_rbv] = amin(self.values[self.data.image])
        self.values[self.data.max_level_rbv] = amax(self.values[self.data.image])

        self.values[self.data.mask_x_rbv] = self.vc_mask.mask_x
        self.values[self.data.mask_y_rbv] = self.vc_mask.mask_y
        self.values[self.data.mask_x_rad_rbv] = self.vc_mask.mask_x_rad
        self.values[self.data.mask_y_rad_rbv] = self.vc_mask.mask_y_rad
        self.values[self.data.use_background] = self.vc_state.use_background

        self.values[self.data.use_npoint] = self.vc_state.use_npoint
        self.values[self.data.ana_step_size] = self.vc_data.step_size

        # Laser Mirrors
        self.values[self.data.H_step_read] = self.mirror.hStep
        self.values[self.data.V_step_read] = self.mirror.vStep
        #
        # Laser Half wave plate
        self.values[self.data.hwp_read] = self.pil_obj.HWP
        #
        # Image saving file and path
        self.values[self.data.last_save_dir]  = self.vc_daq.latestDirectory.replace('/', '\\')
        self.values[self.data.last_save_file] = self.vc_daq.latestFilename
        self.values[self.data.last_save_path] = self.values[self.data.last_save_dir] + '\\' + \
                                                self.values[self.data.last_save_file]
        # update_shutter_state
        if self.shutter1.state == pil.SHUTTER_STATE.OPEN:
            self.values[self.data.shutter1_open] = True
        else:
            self.values[self.data.shutter1_open] = False
        if self.shutter2.state == pil.SHUTTER_STATE.OPEN:
            self.values[self.data.shutter2_open] = True
        else:
            self.values[self.data.shutter2_open] = False

        self.values[self.data.x_buffer_full] = self.vc_data.x_full
        self.values[self.data.y_buffer_full] = self.vc_data.y_full
        self.values[self.data.sig_x_buffer_full] = self.vc_data.sig_x_full
        self.values[self.data.sig_y_buffer_full] = self.vc_data.sig_y_full
        self.values[self.data.cov_xy_buffer_full] = self.vc_data.sig_xy_full
        self.values[self.data.pixel_avg_buffer_full] = self.vc_data.avg_pix_full


    def move_left(self, step):
        self.pil.moveLeft(step)

    def move_right(self, step):
        self.pil.moveRight(step)

    def move_up(self, step):
        self.pil.moveUp(step)

    def move_down(self, step):
        self.pil.moveDown(step)

    def set_pos(self,x,y):
        self.pil.setVCPos(x,y)

    def set_delta_hwp(self, delta_value):
        self.pil.setHWP(self.pil_obj.HWP + delta_value)

    def get_fast_image(self):
        if self.pil.isAcquiring_VC():
            # DEBUG
            #print('take image 1')
            self.pil.takeFastImage_VC()#getFastImage_VC():
            npData = array(  self.vc_image.data ).reshape(( self.vc_image.num_pix_y,
                                                                self.vc_image.num_pix_x))
              #  never works :((((
              #  npData = array(self.vc_image.data2D)
            #print('return image')
            return flipud(npData)
        else:
            print('failed to get image')
        return self.get_fake_image()

    def get_fake_image(self):
        rows = self.values[self.data.num_pix_y]
        columns = self.values[self.data.num_pix_x]
        return random.normal(size=(rows, columns), loc = 30000, scale = 7000)

    def toggle_shutter1(self):
        if self.shutter1.state == pil.SHUTTER_STATE.CLOSED:
            self.pil.open(self.data.shut1)
        elif self.shutter1.state == pil.SHUTTER_STATE.OPEN:
            self.pil.close(self.data.shut1)

    def toggle_shutter2(self):
        if self.shutter2.state == pil.SHUTTER_STATE.CLOSED:
            self.pil.open(self.data.shut2)
        elif self.shutter2.state == pil.SHUTTER_STATE.OPEN:
            self.pil.close(self.data.shut2)

    def setStepSize(self, stepSize):
        #print(stepSize)
        self.pil.setStepSize(stepSize)

    def setMask(self, x, y, xRad, yRad):
        #print('model setMask called',x, y, xRad, yRad)
        self.pil.setMaskX_VC(x)
        self.pil.setMaskY_VC(y)
        self.pil.setMaskXrad_VC(xRad)
        self.pil.setMaskYrad_VC(yRad)

    def useBkgrnd(self):
        if self.pil.isUsingBackground_VC():
            self.pil.useBackground_VC(False)
        else:
            self.pil.useBackground_VC(True)

    def set_background(self):
        self.pil.setBackground_VC()

    def analyse(self):
        if self.pil.isAnalysing_VC():
            self.pil.stopAnalysis_VC()
        else:
            self.pil.startAnalysis_VC()

    def acquire(self):
        if self.pil.isNotAcquiring_VC():
            self.pil.startAcquiring_VC()
        elif self.pil.isAcquiring_VC():
            self.pil.stopAcquireAndAnalysis_VC()

    def collect_and_save(self, numberOfImages):
        if self.pil.isNotCollectingOrSaving_VC():
            if self.pil.isAcquiring_VC():
                self.pil.collectAndSave_VC(numberOfImages)

    def use_background(self):
        if self.pil.isUsingBackground_VC():
            self.pil.useBackground_VC(False)
        else:
            self.pil.useBackground_VC(True)

    def use_npoint(self):
        if self.pil.isUsingNPoint_VC():
            self.pil.useNPoint_VC(False)
        else:
            self.pil.useNPoint_VC(True)

    def toggle_feedback(self,use):
        #print 'toggle_feedback'
        if use:
            #print 'enable mask feedback'
            self.pil.setMaskFeedBackOn_VC()
        else:
            #print 'disable mask feedback'
            self.pil.setMaskFeedBackOff_VC()

    def center_mask(self):
        x = self.values[self.data.mask_x_rbv] - self.values[self.data.mask_x_rad_rbv]
        y = self.values[self.data.mask_y_rbv] - self.values[self.mask_y_rad_rbv]
        xRad = 2 * self.values[self.data.mask_x_rad_rbv]
        yRad = 2 * self.values[self.data.mask_y_rad_rbv]
        self.setMask(x, y, xRad, yRad)

