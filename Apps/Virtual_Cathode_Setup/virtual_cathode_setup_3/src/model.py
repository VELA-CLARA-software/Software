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
//  FileName:    model.py
//  Description: The model for the virtual cathode operator application
//
//
//
//
//*/
'''
import sys,os
#sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\')
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release\\')
import VELA_CLARA_PILaser_Control as pil
import VELA_CLARA_Shutter_Control as shut
#import numpy as np
import data as data
from numpy import array
from numpy import amin
from numpy import amax
from numpy import reshape
from numpy import transpose
from numpy import flipud
from numpy import random
import time
#from scipy.stats import multivariate_normal

class model():
    # make these static as there can be only 1
    # PIL control
    init = pil.init()
    init.setVerbose()
    pil = init.physical_PILaser_Controller()
    #
    # shutter control (which i thought was in PIL, maybe i never updated?)
    initShut = shut.init()
    initShut.setVerbose()
    shutter = initShut.physical_PIL_Shutter_Controller()

    def __init__(self):
        # own a reference to the data dictionary
        self.data = data.data()
        # shorten the reference to data.values and data.previous_values
        self.values = self.data.values
        self.previous_values= self.data.previous_values

        '''
            Get some object references. These are used to update values in data dict
            I normally hold these in a list, (maybe one day try holding them in a dictionary
            to see if that makes the code clearer?)
        '''
        self.shutter1  = [model.shutter.getShutterObjConstRef('SHUT01')]#MAGIC_STRING
        self.shutter2  = [model.shutter.getShutterObjConstRef('SHUT02')]#MAGIC_STRING
        self.mirror   = [model.pil.getpilMirrorObjConstRef()]
        self.vc_data  = [model.pil.getVCDataObjConstRef()]
        self.vc_daq   = [model.pil.getClaraDAQObj_VC()]
        self.pil_obj  = [model.pil.getPILObjConstRef()]
        self.vc_cam   = [model.pil.getCameraObj_VC()]
        self.vc_image = [model.pil.getImageObj_VC()]
        self.vc_state = [model.pil.getStateObj_VC()]
        self.vc_mask  = [model.pil.getMaskObj_VC()]
        '''
            Some constants
        '''
        self.values[self.data.y_pix_scale_factor] = self.vc_image[0].y_pix_scale_factor
        self.values[self.data.x_pix_scale_factor] = self.vc_image[0].x_pix_scale_factor
        self.values[self.data.x_pix_to_mm] = self.vc_image[0].x_pix_to_mm
        self.values[self.data.y_pix_to_mm] = self.vc_image[0].y_pix_to_mm
        self.values[self.data.num_pix_x] = self.vc_image[0].num_pix_x
        self.values[self.data.num_pix_y] = self.vc_image[0].num_pix_y
        self.values[self.data.xpix_full] = self.values[self.data.num_pix_x] * \
                                            self.values[self.data.x_pix_scale_factor]
        self.values[self.data.ypix_full] = self.values[self.data.num_pix_y] * \
                                            self.values[self.data.y_pix_scale_factor]
        # get a fake image to start things off (plus used when debugging)
        self.values[self.data.image]  = self.get_fake_image()

        #print(self.values[data.x_pix_to_mm])
        #print(self.values[data.x_pix_to_mm])
        #print(self.values[data.x_pix_to_mm])
        #print(self.values[data.x_pix_to_mm])
        #print(self.values[data.x_pix_to_mm])
        #print(self.values[data.x_pix_to_mm])



    def reset_running_stats(self):
        '''
            Running stats are the 'running mean and sigma calculated in the controller for
            WCM, x, y position, sig_x, sig_y and cov.
        '''
        model.pil.clearRunningValues()

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
        self.values[self.data.is_acquiring] = model.pil.isAcquiring_VC()
        self.values[self.data.is_analysing] = model.pil.isAnalysing_VC()
        self.values[self.data.is_collecting_or_saving] = model.pil.isNotBusy_VC()

        self.values[self.data.x_pix] = self.vc_data[0].x_pix
        self.values[self.data.y_pix] = self.vc_data[0].y_pix
        self.values[self.data.sig_x_pix] = self.vc_data[0].sig_x_pix
        self.values[self.data.sig_y_pix] = self.vc_data[0].sig_y_pix

        self.values[self.data.x_val] = self.vc_data[0].x
        self.values[self.data.y_val] = self.vc_data[0].y
        self.values[self.data.sx_val] = self.vc_data[0].sig_x
        self.values[self.data.sy_val] = self.vc_data[0].sig_y
        self.values[self.data.cov_val] = self.vc_data[0].sig_xy
        self.values[self.data.avg_pix_val] = self.vc_data[0].avg_pix

        self.values[self.data.x_mean] = self.vc_data[0].x_mean
        self.values[self.data.y_mean] = self.vc_data[0].y_mean
        self.values[self.data.sx_mean] = self.vc_data[0].sig_x_mean
        self.values[self.data.sy_mean] = self.vc_data[0].sig_y_mean
        self.values[self.data.cov_mean] = self.vc_data[0].sig_xy_mean
        self.values[self.data.avg_pix_mean] = self.vc_data[0].avg_pix_mean

        self.values[self.data.x_sd] = self.vc_data[0].x_sd
        self.values[self.data.y_sd] = self.vc_data[0].y_sd
        self.values[self.data.sx_sd] = self.vc_data[0].sig_x_sd
        self.values[self.data.sy_sd] = self.vc_data[0].sig_y_sd
        self.values[self.data.cov_sd] = self.vc_data[0].sig_xy_sd
        self.values[self.data.avg_pix_sd] = self.vc_data[0].avg_pix_sd

        self.values[self.data.wcm_val] = self.pil_obj[0].Q
        self.values[self.data.wcm_mean] = self.pil_obj[0].Q_mean
        self.values[self.data.wcm_sd] = self.pil_obj[0].Q_sd

        # these are flakey  laser INTENSITY
        self.values[self.data.int_val] = '-'
        self.values[self.data.int_mean] = '-'
        self.values[self.data.int_sd] = '-'

        self.values[self.data.image]  = self.get_fast_image()
        self.values[self.data.min_level_rbv] = amin(self.values[self.data.image])
        self.values[self.data.max_level_rbv] = amax(self.values[self.data.image])

        self.values[self.data.mask_x_rbv] = self.vc_mask[0].mask_x
        self.values[self.data.mask_y_rbv] = self.vc_mask[0].mask_y
        self.values[self.data.mask_x_rad_rbv] = self.vc_mask[0].mask_x_rad
        self.values[self.data.mask_y_rad_rbv] = self.vc_mask[0].mask_y_rad
        self.values[self.data.use_background] = self.vc_state[0].use_background

        self.values[self.data.use_npoint] = self.vc_state[0].use_npoint
        self.values[self.data.ana_step_size] = self.vc_data[0].step_size

        # Laser Mirrors
        self.values[self.data.H_step_read] = self.mirror[0].hStep
        self.values[self.data.V_step_read] = self.mirror[0].vStep
        #
        # Laser Half wave plate
        self.values[self.data.hwp_read] = self.pil_obj[0].HWP
        #
        # Image saving file and path
        self.values[self.data.last_save_dir] = self.vc_daq[0].latestDirectory.replace('/', '\\')
        self.values[self.data.last_save_file] = self.vc_daq[0].latestFilename
        self.values[self.data.last_save_path] =  self.values[self.data.last_save_dir] + '\\' + \
                                                  self.values[self.data.last_save_file]
        # update_shutter_state
        if self.shutter1[0].state == shut.SHUTTER_STATE.OPEN:
            self.values[self.data.shutter1_open] = True
        else:
            self.values[self.data.shutter1_open] = False
        if self.shutter2[0].state == shut.SHUTTER_STATE.OPEN:
            self.values[self.data.shutter2_open] = True
        else:
            self.values[self.data.shutter2_open] = False


    def move_H_mirror(self,step):
        model.pil.setHstep(step)
        model.pil.moveH()

    def move_V_mirror(self, step):
        model.pil.setVstep(step)
        model.pil.moveV()

    def set_delta_hwp(self, delta_value):
        model.pil.setHWP(self.pil_obj[0].HWP + delta_value)

    def get_fast_image(self):
        if model.pil.isAcquiring_VC():
            # DEBUG
            model.pil.takeFastImage_VC()#getFastImage_VC():
            npData = array(  self.vc_image[0].data ).reshape(( self.vc_image[0].num_pix_y,
                                                                self.vc_image[0].num_pix_x))
              #  never works :((((
              #  npData = array(self.vc_image[0].data2D)
            return flipud(npData)
        else:
            print('failed to get image')
        return self.get_fake_image()

    def get_fake_image(self):
        rows = self.values[self.data.num_pix_y]
        columns = self.values[self.data.num_pix_x]
        return random.normal(size=(rows, columns), loc = 30000, scale = 7000)

    def toggle_shutter1(self):
        print('toggle_shutter1')
        if self.shutter1[0].state == shut.SHUTTER_STATE.CLOSED:
            model.shutter.open('SHUT01')
        elif self.shutter1[0].state == shut.SHUTTER_STATE.OPEN:
            model.shutter.close('SHUT01')

    def toggle_shutter2(self):
        print('toggle_shutter2')
        if self.shutter2[0].state == shut.SHUTTER_STATE.CLOSED:
            model.shutter.open('SHUT02')
        elif self.shutter2[0].state == shut.SHUTTER_STATE.OPEN:
            model.shutter.close('SHUT02')

    def setStepSize(self, stepSize):
        #print(stepSize)
        model.pil.setStepSize(stepSize)

    def setMask(self, x, y, xRad, yRad):
        #print('model setMask called',x, y, xRad, yRad)
        model.pil.setMaskX_VC(x)
        model.pil.setMaskY_VC(y)
        model.pil.setMaskXrad_VC(xRad)
        model.pil.setMaskYrad_VC(yRad)

    def useBkgrnd(self):
        if self.pil.isUsingBackground_VC():
            self.pil.useBackground_VC(False)
        else:
            self.pil.useBackground_VC(True)

    def set_background(self):
        self.pil.setBackground_VC()

    def analyse(self):
        if model.pil.isAnalysing_VC():
            model.pil.stopAnalysis_VC()
        else:
            model.pil.startAnalysis_VC()

    def acquire(self):
        if model.pil.isNotAcquiring_VC():
            model.pil.startAcquiring_VC()
        elif model.pil.isAcquiring_VC():
            model.pil.stopAcquireAndAnalysis_VC()

    def collect_and_save(self, numberOfImages):
        if model.pil.isNotCollectingOrSaving_VC():
            if model.pil.isAcquiring_VC():
                model.pil.collectAndSave_VC(numberOfImages)

    def use_background(self):
        if model.pil.isUsingBackground_VC():
            model.pil.useBackground_VC(False)
        else:
            model.pil.useBackground_VC(True)

    def use_npoint(self):
        if model.pil.isUsingNPoint_VC():
            model.pil.useNPoint_VC(False)
        else:
            model.pil.useNPoint_VC(True)

    def toggle_feedback(self,use):
        #print 'toggle_feedback'
        if use:
            #print 'enable mask feedback'
            model.pil.setMaskFeedBackOn_VC()
        else:
            #print 'disable mask feedback'
            model.pil.setMaskFeedBackOff_VC()

    def center_mask(self):
        x = self.values[self.data.mask_x_rbv] - self.values[self.data.mask_x_rad_rbv]
        y = self.values[self.data.mask_y_rbv] - self.values[self.mask_y_rad_rbv]
        xRad = 2 * self.values[self.data.mask_x_rad_rbv]
        yRad = 2 * self.values[self.data.mask_y_rad_rbv]
        self.setMask(x, y, xRad, yRad)


# '''
#     The below all exists in c++,so i need ot be careful about using it ...
#     in fact we ned to connect this up to the c++
#     what if too programmes are using the
# '''
#
#
#     def setposition(self,setx, sety, delta=5, prec=0.1):
#         self.getposition()
#         # how much to move at a time?
#         move_amount = delta  # seems OK for a small step
#         precision = prec  # as a fraction of sigma x or y
#         #print 'Moving to {:.3f}, {:.3f}'.format(setx, sety)
#         while abs(setx - self.lasx) > self.lassx * precision or abs(sety - self.lasy) > self.lassy * precision:
#             # Gotcha: a negative H move means the beam goes RIGHT, contrary to convention
#             h_step = math.copysign(move_amount, -(setx - self.lasx)) if abs(setx - self.lasx) > self.lassx * precision else 0
#             # Do a bigger step in y
#             v_step = 3 * math.copysign(move_amount, sety - self.lasy) if abs(sety - self.lasy) > self.lassy * precision else 0
#             # #print 'Move amount: H {}, V {}'.format(h_step, v_step)
#             self.move_horiz(h_step)
#             self.move_vert(v_step)
#             self.getposition()
#             # #print 'Position: {:.3f}, {:.3f}'.format(self.lasx, self.lasy)
#             # #print('How far away?', abs(req_x - x), abs(req_y - y), sx / 3, sy / 3)
#         #print 'Final position {:.3f}, {:.3f}'.format(self.lasx, self.lasy)
#
#
#     def set_x_pos(self, value, step):
#         self.reset_running_values()
#         precision = 0.1
#         time.sleep(0.1)
#         # self.values[self.data.x_mean]
#         while abs(value - self.values[self.data.x_val]) > precision:
#             if value > self.values[self.data.x_val]:
#                 self.move_H_mirror(-step)
#             else:
#                 self.move_H_mirror(step)
#
#             #print('set_x_pos',value,self.values[data.x_val])
#
#             time.sleep(0.1)
#
#             # we could add some stats in here when its working ...
#             # then push to c++
#
#
#
#             #
#             # h_step = math.copysign(move_amount, -(setx - self.lasx)) if abs(
#             #     setx - self.lasx) > self.lassx * precision else 0
#             # # Do a bigger step in y
#             # v_step = 3 * math.copysign(move_amount, sety - self.lasy) if abs(
#             #     sety - self.lasy) > self.lassy * precision else 0
#             # # #print 'Move amount: H {}, V {}'.format(h_step, v_step)
#             # self.move_horiz(h_step)
#             # self.move_vert(v_step)
#             # self.getposition()
#             # #print 'Position: {:.3f}, {:.3f}'.format(self.lasx, self.lasy)
#             # #print('How far away?', abs(req_x - x), abs(req_y - y), sx / 3, sy / 3)
#         #print 'Final position {:.3f}, {:.3f}'.format(self.lasx, self.lasy)
#
#
#     def set_y_pos(self, value):
#         setposition()
