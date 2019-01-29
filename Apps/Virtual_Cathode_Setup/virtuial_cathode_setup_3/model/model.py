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
import VELA_CLARA_PILaser_Control as pil
import VELA_CLARA_Shutter_Control as shut
#import numpy as np
import data
from numpy import array
from numpy import reshape
from numpy import transpose
from numpy import flipud
from numpy import random
import time

class model():
    init = pil.init()
    init.setVerbose()
    pil = init.physical_PILaser_Controller()

    # holds a copy of the data dictionary
    data = data.data()

    initShut = shut.init()
    initShut.setVerbose()
    shutter = initShut.physical_PIL_Shutter_Controller()

    def __init__(self):
        '''
            Get some object references. These are used to update values in data dict
            I normally hold these in a list, (maybe one day try holding them in a dictionary
            to see if that the code clearer?)
        '''
        self.shutter  = [model.shutter.getShutterObjConstRef('SHUT01')]#MAGIC_STRING
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
        model.data.values[data.y_pix_scale_factor] = self.vc_image[0].y_pix_scale_factor
        model.data.values[data.x_pix_scale_factor] = self.vc_image[0].x_pix_scale_factor
        model.data.values[data.x_pix_to_mm] = self.vc_image[0].x_pix_to_mm
        model.data.values[data.y_pix_to_mm] = self.vc_image[0].y_pix_to_mm
        model.data.values[data.num_pix_x] = self.vc_image[0].num_pix_x
        model.data.values[data.num_pix_y] = self.vc_image[0].num_pix_y
        print 'model init complete'

    def reset_running_values(self):
        model.pil.clearRunningValues()

    def update_values(self):
        return 0
        '''
            set previous_values to values, then update values
            https://stackoverflow.com/questions/2465921/how-to-copy-a-dictionary-and-only-edit-the-copy
        '''
        for key, value in  model.data.values.iteritems():
            model.data.previous_values[key] = value
        '''
            Get latest values from controllers adn put them in the data dict
        '''
        model.data.values[data.is_acquiring] = model.pil.isAcquiring_VC()
        model.data.values[data.is_analysing] = model.pil.isAnalysing_VC()
        model.data.values[data.is_collecting_or_saving] = model.pil.isNotBusy_VC()


        # if model.data.values[data.is_collecting_or_saving]:
        #     print 'COLLECTING AND SAVING'
        # else:
        #     print 'NOT COLLECTING AND SAVING'
        model.data.values[data.x_pix] = self.vc_data[0].x_pix
        model.data.values[data.y_pix] = self.vc_data[0].y_pix
        model.data.values[data.sig_x_pix] = self.vc_data[0].sig_x_pix
        model.data.values[data.sig_y_pix] = self.vc_data[0].sig_y_pix

        model.data.values[data.x_val] = self.vc_data[0].x
        model.data.values[data.y_val] = self.vc_data[0].y
        model.data.values[data.sx_val] = self.vc_data[0].sig_x
        model.data.values[data.sy_val] = self.vc_data[0].sig_y
        model.data.values[data.cov_val] = self.vc_data[0].sig_xy
        model.data.values[data.avg_pix_val] = self.vc_data[0].avg_pix

        model.data.values[data.x_mean] = self.vc_data[0].x_mean
        model.data.values[data.y_mean] = self.vc_data[0].y_mean
        model.data.values[data.sx_mean] = self.vc_data[0].sig_x_mean
        model.data.values[data.sy_mean] = self.vc_data[0].sig_y_mean
        model.data.values[data.cov_mean] = self.vc_data[0].sig_xy_mean
        model.data.values[data.avg_pix_mean] = self.vc_data[0].avg_pix_mean

        model.data.values[data.x_sd] = self.vc_data[0].x_sd
        model.data.values[data.y_sd] = self.vc_data[0].y_sd
        model.data.values[data.sx_sd] = self.vc_data[0].sig_x_sd
        model.data.values[data.sy_sd] = self.vc_data[0].sig_y_sd
        model.data.values[data.cov_sd] = self.vc_data[0].sig_xy_sd
        model.data.values[data.avg_pix_sd] = self.vc_data[0].avg_pix_sd

        model.data.values[data.image]  = self.get_fast_image()
        model.data.values[data.mask_x_rbv] = self.vc_mask[0].mask_x
        model.data.values[data.mask_y_rbv] = self.vc_mask[0].mask_y
        model.data.values[data.mask_x_rad_rbv] = self.vc_mask[0].mask_x_rad
        model.data.values[data.mask_y_rad_rbv] = self.vc_mask[0].mask_y_rad
        model.data.values[data.use_background] = self.vc_state[0].use_background

        model.data.values[data.use_npoint] = self.vc_state[0].use_npoint
        model.data.values[data.min_level_rbv] = self.vc_image[0].data_min
        model.data.values[data.max_level_rbv] = self.vc_image[0].data_max

        model.data.values[data.ana_step_size] = self.vc_data[0].step_size
        #print('self.vc_data[0].step_size = ', self.vc_data[0].step_size)
        if self.shutter[0].state == shut.SHUTTER_STATE.OPEN:
            model.data.values[data.shutter_open] = True
        else:
            model.data.values[data.shutter_open] = False

        model.data.values[data.wcm_val] = self.pil_obj[0].Q
        model.data.values[data.wcm_mean] = self.pil_obj[0].Q_mean
        model.data.values[data.wcm_sd] = self.pil_obj[0].Q_sd
        #
        # these don't exist yet, laser INTENSITY
        model.data.values[data.int_val] = '-'
        model.data.values[data.int_mean] = '-'
        model.data.values[data.int_sd] = '-'

        model.data.values[data.H_step_read] = self.mirror[0].hStep
        model.data.values[data.V_step_read] = self.mirror[0].vStep
        model.data.values[data.hwp_read] = self.pil_obj[0].HWP
        model.data.values[data.last_save_dir] = self.vc_daq[0].latestDirectory.replace('/', '\\')
        model.data.values[data.last_save_file] = self.vc_daq[0].latestFilename
        model.data.values[data.last_save_path] =  model.data.values[data.last_save_dir] + '\\' + \
                                                  model.data.values[data.last_save_file]


    def set_x_pos(self, value, step):
        self.reset_running_values()
        precision = 0.1
        time.sleep(0.1)
        # model.data.values[data.x_mean]
        while abs(value - model.data.values[data.x_val]) > precision:
            if value > model.data.values[data.x_val]:
                self.move_H_mirror(-step)
            else:
                self.move_H_mirror(step)

            print('set_x_pos',value,model.data.values[data.x_val])

            time.sleep(0.1)

            # we could add some stats in here when its working ...
            # then push to c++



            #
            # h_step = math.copysign(move_amount, -(setx - self.lasx)) if abs(
            #     setx - self.lasx) > self.lassx * precision else 0
            # # Do a bigger step in y
            # v_step = 3 * math.copysign(move_amount, sety - self.lasy) if abs(
            #     sety - self.lasy) > self.lassy * precision else 0
            # # print 'Move amount: H {}, V {}'.format(h_step, v_step)
            # self.move_horiz(h_step)
            # self.move_vert(v_step)
            # self.getposition()
            # print 'Position: {:.3f}, {:.3f}'.format(self.lasx, self.lasy)
            # print('How far away?', abs(req_x - x), abs(req_y - y), sx / 3, sy / 3)
        print 'Final position {:.3f}, {:.3f}'.format(self.lasx, self.lasy)


    def set_y_pos(self, value):
        setposition()

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
            #if model.pil.getFastImage_VC():
            # reshape works as: reshape(( n rows, m columns) )

            #return random.normal(size=(self.vc_image[0].num_pix_y, self.vc_image[0].num_pix_y))

            print 'HERE'
            print 'HERE'
            print 'HERE'
            print 'HERE'

            npData = random.normal(size=(self.vc_image[0].num_pix_x,self.vc_image[0].num_pix_y))

            # npData = array(  self.vc_image[0].data ).reshape(( self.vc_image[0].num_pix_y,
            #                                                 self.vc_image[0].num_pix_x))
            # # This needs to be checked,
            # it matches the old imageviewer, but is this correct?? !!

            return flipud(npData)
        else:
            print('failed to get image')

    def toggle_shutter(self):
        if self.shutter[0].state == shut.SHUTTER_STATE.CLOSED:
            model.shutter.open('SHUT01')
        elif self.shutter[0].state == shut.SHUTTER_STATE.OPEN:
            model.shutter.close('SHUT01')

    def setStepSize(self, stepSize):
        print(stepSize)
        model.pil.setStepSize(stepSize)

    def setMask(self, x, y, xRad, yRad):
        print('model setMask called',x, y, xRad, yRad)
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
                # self.camerasDAQ.collectAndSaveJPG()
        #elif self.selectedCameraDAQ[0].DAQ.captureState == self.cap.CAPTURING:
        #    self.camerasDAQ.killCollectAndSave()
        # self.camerasDAQ.killCollectAndSaveJPG()

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
        print 'toggle_feedback'
        if use:
            print 'enable mask feedback'
            model.pil.setMaskFeedBackOn_VC()
        else:
            print 'disable mask feedback'
            model.pil.setMaskFeedBackOff_VC()


            # height = 2160#self.selectedCameraIA.IA.imageHeight
            # width = 2560#self.selectedCameraIA.IA.imageWidth
            # x  = self.vc_data[0].x_pix
            # y  = self.vc_data[0].y_pix
            # sX = self.vc_data[0].sig_x_pix
            # sY = self.vc_data[0].sig_y_pix
            # if x-5*sX > 0 and x+5*sX < width and y-5*sY > 0 and y+5*sY < height:
            #     #print(x-sX)
            #     #print(y-sY)
            #     self.setMask(int(x),int(y),int(5*sX),int(5*sY))

    def center_mask(self):
        x = model.data.values[data.mask_x_rbv] - model.data.values[data.mask_x_rad_rbv]
        y = model.data.values[data.mask_y_rbv] - model.data.values[model.data.mask_y_rad_rbv]
        xRad = 2 * model.data.values[data.mask_x_rad_rbv]
        yRad = 2 * model.data.values[data.mask_y_rad_rbv]
        self.setMask(x, y, xRad, yRad)

    def setposition(self,setx, sety, delta=5, prec=0.1):
        self.getposition()
        # how much to move at a time?
        move_amount = delta  # seems OK for a small step
        precision = prec  # as a fraction of sigma x or y
        print 'Moving to {:.3f}, {:.3f}'.format(setx, sety)
        while abs(setx - self.lasx) > self.lassx * precision or abs(sety - self.lasy) > self.lassy * precision:
            # Gotcha: a negative H move means the beam goes RIGHT, contrary to convention
            h_step = math.copysign(move_amount, -(setx - self.lasx)) if abs(setx - self.lasx) > self.lassx * precision else 0
            # Do a bigger step in y
            v_step = 3 * math.copysign(move_amount, sety - self.lasy) if abs(sety - self.lasy) > self.lassy * precision else 0
            # print 'Move amount: H {}, V {}'.format(h_step, v_step)
            self.move_horiz(h_step)
            self.move_vert(v_step)
            self.getposition()
            # print 'Position: {:.3f}, {:.3f}'.format(self.lasx, self.lasy)
            # print('How far away?', abs(req_x - x), abs(req_y - y), sx / 3, sy / 3)
        print 'Final position {:.3f}, {:.3f}'.format(self.lasx, self.lasy)