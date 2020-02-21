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
//  FileName:    virtual_cathode_view.py
//  Description: The main gui for the virtual cathode application
//
//
//
//
//*/
'''
# import sys
# sys.path.append('.')
from PyQt4 import QtGui, QtCore
from viewSource.ellipseROIoverloads import EllipseROI_OneHandle
from viewSource.ellipseROIoverloads import EllipseROI_NoHandle
from viewSource.Ui_virtual_cathode_app import Ui_virtual_cathode_view
from numpy import array
# from numpy import random
from numpy import linspace
from math import ceil
import virtual_cathode_model_data
import pyqtgraph as pg


class virtual_cathode_view(QtGui.QMainWindow, Ui_virtual_cathode_view):
    # custom close signal to send to controller
    closing = QtCore.pyqtSignal()

    def __init__(self):
        QtGui.QWidget.__init__(self)
        '''
        The mainView has a copy of the data so it can update the GUI
        '''
        self.model_data = virtual_cathode_model_data.model_data()
        #
        # startup
        self.setupUi(self)
        self.setWindowTitle("VELA - CLARA Virtual Cathode Setup")
        #
        # the mainView holds a few dictionaries that are iterated over to update widgets
        self.set_widget_dicts()

        '''
        Nominal Style for buttons
        '''
        self.collect_and_save_pushButton_default_style = \
            self.collectAndSave_pushButton.styleSheet()
        '''
        some widgets need only be connected locally, (no significant dependence on model so 
        done		 
        here instead of controller
        '''
        self.pix_gridlines_checkBox_2.released.connect(self.handle_pix_gridlines_checkBox)
        self.pix_gridlines_checkBox.released.connect(self.handle_pix_gridlines_checkBox)
        self.mm_gridlines_checkBox_2.released.connect(self.handle_mm_gridlines_checkBox)
        self.mm_gridlines_checkBox.released.connect(self.handle_mm_gridlines_checkBox)
        self.setWCM_pushButton.setDisabled(True)
        self.setInt_pushButton.setDisabled(True)
        self.load_pushButton.setDisabled(True)
        self.save_pushButton.setDisabled(True)

    def handle_pix_gridlines_checkBox(self):
        '''
        adds girdlines to the plot, in stepsizes related to mm, or pixels
        :return:
        '''
        enable = False
        if self.sender() == self.pix_gridlines_checkBox:
            if self.pix_gridlines_checkBox.isChecked():
                enable = True
            self.pix_gridlines_checkBox_2.setChecked(enable)
        elif self.sender() == self.pix_gridlines_checkBox_2:
            if self.pix_gridlines_checkBox_2.isChecked():
                enable = True
            self.pix_gridlines_checkBox.setChecked(enable)
        self.set_grid(enable, self.x_axis_d, self.y_axis_l)

    def handle_mm_gridlines_checkBox(self):
        enable = False
        if self.sender() == self.mm_gridlines_checkBox:
            if self.mm_gridlines_checkBox.isChecked():
                enable = True
            self.mm_gridlines_checkBox_2.setChecked(enable)
        elif self.sender() == self.mm_gridlines_checkBox_2:
            if self.mm_gridlines_checkBox_2.isChecked():
                enable = True
            self.mm_gridlines_checkBox.setChecked(enable)
        self.set_grid(enable, self.x_axis_u, self.y_axis_r)

    def set_grid(self, enable, axis1, axis2):
        if enable:
            axis1.setGrid(255)  # MAGIC_NUMBER
            axis2.setGrid(255)  # MAGIC_NUMBER
        else:
            axis1.setGrid(False)  # MAGIC_NUMBER
            axis2.setGrid(False)  # MAGIC_NUMBER

    def setLevel(self):
        self.vc_image.setLevels([self.spinBox_minLevel.value(), self.spinBox_maxLevel.value()],
                                update=True)

    def autoSetLevel(self):
        self.spinBox_minLevel.setValue(self.model_data.values[self.model_data.min_level_rbv])
        self.spinBox_maxLevel.setValue(self.model_data.values[self.model_data.max_level_rbv])
        self.setLevel()

    def add_user_ROIEllipse(self):
        self.user_roi.addTranslateHandle([0, 0.5])
        self.vc_imageBox.addItem(self.user_roi)
        self.user_roi.sigRegionChangeFinished.connect(self.user_roiChanged)

    def user_roiChanged(self):
        '''
            I think analysis x,y from the VC are swopped .. ?
        :return:
        '''
        # print 'user_roiChanged called'
        x_rad, y_rad = 0.5 * self.user_roi.size()
        x, y = self.user_roi.pos() + [x_rad, y_rad]
        self.maskX_spinBox.setValue(x)
        self.maskY_spinBox.setValue(y)
        self.maskXRadius_spinBox.setValue(x_rad)
        self.maskYRadius_spinBox.setValue(y_rad)
        self.setMask_pushButton.click()

    def update_gui(self):
        # we only need to update the read_ROI once so keep a flag for it
        not_updated_read_roi = True
        # there are no widgets associated with the cross-hairs so they are updated outside the mask
        self.update_crosshair()
        self.set_disabled_buttons_on_closed_shutter_or_low_pixel_avg()

        ##print('update widget loop')
        for key, value in self.widget_to_dataname.iteritems():
            # print('update widget ', value, key)
            if self.new_value(value):
                if self.is_mask_read(key):
                    if not_updated_read_roi:
                        self.update_read_roi()
                        not_updated_read_roi = False
                # try:
                self.widget_updatefunc[key][0](key, value, self.widget_updatefunc[
                    key])  # except:  #    print('ERROR in updating ', key, value)

        if self.model_data.values[self.model_data.avg_pix_beam_level] <  self.model_data.values[
            self.model_data.avg_pix_mean]:
            self.avg_pix_val.setStyleSheet("background-color: #ffffff")
        else:
            self.avg_pix_val.setStyleSheet("background-color: #ff5733")




    def new_value(self, value):
        '''
            test to see if a value in the values dict is different to the value in previous_values
            if it is different return true
        :param value: value to check if new
        :return: is value new or not
        '''
        ##print self.model_data.values.get(value), self.model_data.previous_values.get(value)
        if value == self.model_data.image:
            return True
        return self.model_data.values.get(value) != self.model_data.previous_values.get(value)

    def set_disabled_buttons_on_closed_shutter_or_low_pixel_avg(self):
        should_enable = False
        if self.model_data.values.get(self.model_data.shutter1_open):
            if self.model_data.values.get(self.model_data.shutter2_open):
                if self.model_data.values[self.model_data.avg_pix_beam_level] <  self.model_data.values[self.model_data.avg_pix_mean]:
                    should_enable = True
        self.move_left_pushButton.setEnabled(should_enable)
        self.move_right_pushButton.setEnabled(should_enable)
        self.move_down_pushButton.setEnabled(should_enable)
        self.move_up_pushButton.setEnabled(should_enable)
        self.set_pos_pushButton.setEnabled(should_enable)
        # get the shutter states ( updated in model.update_shutter_state )
        # then decide what widgets to disable / enable
        # if self.model_data.values.get(self.model_data.shutter1_open) & self.model_data.values.get(
        #         self.model_data.shutter2_open):
        #     self.move_left_pushButton.setEnabled(True)
        #     self.move_right_pushButton.setEnabled(True)
        #     self.move_down_pushButton.setEnabled(True)
        #     self.move_up_pushButton.setEnabled(True)
        #     self.set_pos_pushButton.setEnabled(False)
        # else:
        #     self.move_left_pushButton.setEnabled(False)
        #     self.move_right_pushButton.setEnabled(False)
        #     self.move_down_pushButton.setEnabled(False)
        #     self.move_up_pushButton.setEnabled(False)
        #     self.set_pos_pushButton.setEnabled(False)

    def update_crosshair(self):
        '''
            It seems that the x,y and y for analyhwp_down_pushButtonsis are mixed compared to x,
            y dimensions
        :return:
        '''
        x0 = self.model_data.values[self.model_data.x_pix]
        xmin = self.model_data.values[self.model_data.x_pix] - self.model_data.values[
            self.model_data.sig_x_pix]
        xmax = self.model_data.values[self.model_data.x_pix] + self.model_data.values[
            self.model_data.sig_x_pix]
        y0 = self.model_data.values[self.model_data.y_pix]
        ymin = self.model_data.values[self.model_data.y_pix] - self.model_data.values[
            self.model_data.sig_y_pix]
        ymax = self.model_data.values[self.model_data.y_pix] + self.model_data.values[
            self.model_data.sig_y_pix]
        self.v_cross_hair.setData(x=[x0, x0], y=[ymin, ymax])
        self.h_cross_hair.setData(x=[xmin, xmax], y=[y0, y0])

    """
        Functions to style buttons
    """
    def set_button_color_and_text(self, widget, color, text):
        self.set_button_color(widget=widget, col=color)
        self.setText(text)

    def update_button(self, key, value, param):
        self.set_button(key, value, true_text=param[1], false_text=param[2])

    def set_button(self, key, value, true_text="", true_color="green", false_text="",
                   false_color="red"):
        if self.model_data.values.get(value):
            self.set_button_color(key, true_color)
            key.setText(true_text)
        else:
            self.set_button_color(key, false_color)
            key.setText(false_text)

    def set_button_color(self, widget, col=""):
        if col == "green":
            widget.setStyleSheet("color: white; background-color: QLinearGradient( x1: 0, y1: 0, "
                                 "x2: 0, y2: 1, stop: 0 #0f0, stop: 0.1 #0c0, stop: 0.49 #090)")
        elif col == "red":
            widget.setStyleSheet("color: white; background-color: QLinearGradient( x1: 0, y1: 0, "
                                 "x2: 0, y2: 1, stop: 0 #f00, stop: 0.1 #c00, stop: 0.49 #900)")
        elif col == "yellow":
            widget.setStyleSheet("color: white; background-color: QLinearGradient( x1: 0, y1: 0, "
                                 "x2: 0, y2: 1, stop: 0 #ff0, stop: 0.1 #cc0, stop: 0.49 #990)")
        elif col == "magenta":
            widget.setStyleSheet("color: white; background-color: QLinearGradient( x1: 0, y1: 0, "
                                 "x2: 0, y2: 1, stop: 0 #f0f, stop: 0.1 #c0c, stop: 0.49 #909)")

    def user_roi_hashover(self):
        print 'hover'

    def update_read_roi(self):
        '''
            I think the x and y analysis numebers are swopped for the VC
        :return:
        '''
        self.read_roi.setPos(QtCore.QPoint(
            self.model_data.values[self.model_data.mask_x_rbv] - self.model_data.values[
                self.model_data.mask_x_rad_rbv],
            self.model_data.values[self.model_data.mask_y_rbv] - self.model_data.values[
                self.model_data.mask_y_rad_rbv]))
        self.read_roi.setSize(
            QtCore.QPoint(2 * self.model_data.values[self.model_data.mask_x_rad_rbv],
                          2 * self.model_data.values[self.model_data.mask_y_rad_rbv]))

    def start_up(self):
        ''' here initilise the values to the current reads ... '''
        not_updated_read_roi = True
        # print("ADD CAMERA IMAGE")
        self.add_camera_image()

        self.set_user_mask_to_read_mask()

        self.maskX_spinBox.setRange(0, self.model_data.values[self.model_data.xpix_full])
        self.maskY_spinBox.setRange(0, self.model_data.values[self.model_data.ypix_full])
        self.maskXRadius_spinBox.setRange(0, self.model_data.values[self.model_data.ypix_full])
        self.maskYRadius_spinBox.setRange(0, self.model_data.values[self.model_data.ypix_full])

        self.mirror_h_step_set_spinBox.setValue(self.model_data.values[
                                                    self.model_data.H_step_read])
        self.mirror_v_step_set_spinBox.setValue(self.model_data.values[
                                                    self.model_data.V_step_read])
        # update gui widget
        for key, value in self.widget_to_dataname.iteritems():
            if self.is_mask_read(key):
                if not_updated_read_roi:
                    self.update_read_roi()
                    not_updated_read_roi = False
            try:
                self.widget_updatefunc[key][0](key, value, self.widget_updatefunc[key])
            except:
                print key, value

    def set_user_mask_to_read_mask(self):
        x = self.model_data.values[self.model_data.mask_x_rbv] - self.model_data.values[
            self.model_data.mask_x_rad_rbv]
        y = self.model_data.values[self.model_data.mask_y_rbv] - self.model_data.values[
            self.model_data.mask_y_rad_rbv]
        xRad = 2 * self.model_data.values[self.model_data.mask_x_rad_rbv]
        yRad = 2 * self.model_data.values[self.model_data.mask_y_rad_rbv]
        # make new ellipse here that track sRV ... #
        ##print(x,y,xRad,yRad)
        point = QtCore.QPoint(x, y)
        self.user_roi.setPos(point)
        pointRad = QtCore.QPoint(xRad, yRad)
        self.user_roi.setSize(pointRad)

    '''
        helper functions to clean up update_gui()
    '''

    def is_mask_read(self, key):
        if key == self.mask_x_read:
            return True
        elif key == self.mask_y_read:
            return True
        elif key == self.mask_x_rad_read:
            return True
        elif key == self.mask_y_rad_read:
            return True
        return False

    def update_int(self, widget, value, dummy):
        widget.setText("%i" % self.model_data.values.get(value))

    def update_real(self, widget, value, dummy):
        widget.setText("%.2f" % self.model_data.values.get(value))

    def update_image(self, widget, value, dummy):
        self.vc_image.setImage(image=self.model_data.values.get(value), autoDownsample=True)
        self.vc_image.setLevels([self.spinBox_minLevel.value(), self.spinBox_maxLevel.value()], update=True)

    def update_string(self, widget, value, dummy):
        if self.model_data.values.get(value) != 'UNKNOWN':  # MAGIC_STRING
            widget.setText(QtCore.QString(self.model_data.values.get(value)))

    def update_latest_dir(self, widget, value, dummy):
        if self.model_data.values.get(value) != 'UNKNOWN':  # MAGIC_STRING
            s = self.model_data.values.get(
                self.model_data.image_save_dir_root) + '\\' + self.model_data.values.get(value)
            widget.setText(QtCore.QString(s))

    def update_set_pos_button(self):
        if self.model_data.values[self.model_data.is_setting_pos]:
            self.set_pos_pushButton.setEnabled(False)
            self.set_button_color(self.set_pos_pushButton, 'red')
        else:
            self.set_pos_pushButton.setEnabled(False)
            self.set_button_color(self.set_pos_pushButton, 'green')

    def set_widget_dicts(self):
        '''
            create dict. with all widgets to update, keyed by their values in 'data'
            then loop over this dict and the data dict to update
        '''
        self.widget_to_dataname = {}
        self.widget_to_dataname[self.x_val] = self.model_data.x_val
        self.widget_to_dataname[self.x_val_2] = self.model_data.x_val
        self.widget_to_dataname[self.x_mean] = self.model_data.x_mean
        self.widget_to_dataname[self.x_sd] = self.model_data.x_sd
        self.widget_to_dataname[self.y_val] = self.model_data.y_val
        self.widget_to_dataname[self.y_val_2] = self.model_data.y_val
        self.widget_to_dataname[self.y_mean] = self.model_data.y_mean
        self.widget_to_dataname[self.y_sd] = self.model_data.y_sd
        self.widget_to_dataname[self.sx_val] = self.model_data.sx_val
        self.widget_to_dataname[self.sx_mean] = self.model_data.sx_mean
        self.widget_to_dataname[self.sx_sd] = self.model_data.sx_sd
        self.widget_to_dataname[self.sy_val] = self.model_data.sy_val
        self.widget_to_dataname[self.sy_mean] = self.model_data.sy_mean
        self.widget_to_dataname[self.sy_sd] = self.model_data.sy_sd
        self.widget_to_dataname[self.cov_val] = self.model_data.cov_val
        self.widget_to_dataname[self.cov_mean] = self.model_data.cov_mean
        self.widget_to_dataname[self.cov_sd] = self.model_data.cov_sd
        self.widget_to_dataname[self.avg_pix_val] = self.model_data.avg_pix_val
        self.widget_to_dataname[self.avg_pix_mean] = self.model_data.avg_pix_mean
        self.widget_to_dataname[self.avg_pix_sd] = self.model_data.avg_pix_sd
        self.widget_to_dataname[self.imageLayout] = self.model_data.image
        self.widget_to_dataname[self.mask_x_read] = self.model_data.mask_x_rbv
        self.widget_to_dataname[self.mask_y_read] = self.model_data.mask_y_rbv
        self.widget_to_dataname[self.mask_x_rad_read] = self.model_data.mask_x_rad_rbv
        self.widget_to_dataname[self.mask_y_rad_read] = self.model_data.mask_y_rad_rbv
        self.widget_to_dataname[self.opencloseShut1_pushButton] = self.model_data.shutter1_open
        self.widget_to_dataname[self.opencloseShut2_pushButton] = self.model_data.shutter2_open
        self.widget_to_dataname[self.acquire_pushButton] = self.model_data.is_acquiring
        self.widget_to_dataname[self.analyse_pushButton] = self.model_data.is_analysing
        self.widget_to_dataname[self.analyse_pushButton_2] = self.model_data.is_analysing
        self.widget_to_dataname[
            self.collectAndSave_pushButton] = self.model_data.is_collecting_or_saving
        self.widget_to_dataname[self.useBackground_pushButton] = self.model_data.use_background
        self.widget_to_dataname[self.useNPoint_pushButton] = self.model_data.use_npoint
        self.widget_to_dataname[self.minPixValue] = self.model_data.min_level_rbv
        self.widget_to_dataname[self.maxPixValue] = self.model_data.max_level_rbv
        self.widget_to_dataname[self.step_size_read] = self.model_data.ana_step_size
        self.widget_to_dataname[self.H_step_read] = self.model_data.H_step_read
        self.widget_to_dataname[self.V_step_read] = self.model_data.V_step_read
        self.widget_to_dataname[self.wcm_val] = self.model_data.wcm_val
        self.widget_to_dataname[self.wcm_val_2] = self.model_data.wcm_val
        self.widget_to_dataname[self.wcm_mean] = self.model_data.wcm_mean
        self.widget_to_dataname[self.wcm_sd] = self.model_data.wcm_sd
        self.widget_to_dataname[self.int_val] = self.model_data.int_val  # '[self.update_real]
        self.widget_to_dataname[self.int_mean] = self.model_data.int_mean  # [self.update_real]
        self.widget_to_dataname[self.int_sd] = self.model_data.int_sd  # [self.update_real]
        self.widget_to_dataname[self.hwp_read] = self.model_data.hwp_read
        self.widget_to_dataname[self.last_filename] = self.model_data.last_save_file
        self.widget_to_dataname[self.last_directory] = self.model_data.last_save_dir
        self.widget_to_dataname[self.last_directory] = self.model_data.last_save_dir
        self.widget_to_dataname[self.set_pos_pushButton] = self.model_data.is_setting_pos
        self.widget_to_dataname[self.rs_buffer_size] = self.model_data.rs_buffer_size
        # the below don't exist yet
        # self.widget_to_dataname[self.int_val] = self.model_data.int_val
        # self.widget_to_dataname[self.int_val_2] = self.model_data.int_val
        # self.widget_to_dataname[self.int_mean] = self.model_data.int_mean
        # self.widget_to_dataname[self.int_sd] = self.model_data.int_sd
        '''
            similar to above, but holds the update functions and constant parameters to pass to 
            those functions  
        '''
        self.widget_updatefunc = {}
        # analysis results, x, y, xy,  mean,sigma,and standard deviations of running states
        self.widget_updatefunc[self.x_val] = [self.update_real]
        self.widget_updatefunc[self.x_val_2] = [self.update_real]
        self.widget_updatefunc[self.x_mean] = [self.update_real]
        self.widget_updatefunc[self.x_sd] = [self.update_real]
        self.widget_updatefunc[self.y_val] = [self.update_real]
        self.widget_updatefunc[self.y_val_2] = [self.update_real]
        self.widget_updatefunc[self.y_mean] = [self.update_real]
        self.widget_updatefunc[self.y_sd] = [self.update_real]
        self.widget_updatefunc[self.sx_val] = [self.update_real]
        self.widget_updatefunc[self.sx_mean] = [self.update_real]
        self.widget_updatefunc[self.sx_sd] = [self.update_real]
        self.widget_updatefunc[self.sy_val] = [self.update_real]
        self.widget_updatefunc[self.sy_mean] = [self.update_real]
        self.widget_updatefunc[self.sy_sd] = [self.update_real]
        self.widget_updatefunc[self.cov_val] = [self.update_real]
        self.widget_updatefunc[self.cov_mean] = [self.update_real]
        self.widget_updatefunc[self.cov_sd] = [self.update_real]
        self.widget_updatefunc[self.avg_pix_val] = [self.update_real]
        self.widget_updatefunc[self.avg_pix_mean] = [self.update_real]
        self.widget_updatefunc[self.avg_pix_sd] = [self.update_real]
        self.widget_updatefunc[self.imageLayout] = [self.update_image]
        self.widget_updatefunc[self.mask_x_read] = [self.update_int]
        self.widget_updatefunc[self.mask_y_read] = [self.update_int]
        self.widget_updatefunc[self.mask_x_rad_read] = [self.update_int]
        self.widget_updatefunc[self.mask_y_rad_read] = [self.update_int]
        self.widget_updatefunc[self.opencloseShut1_pushButton] = [self.update_button,
                                                                  "CLOSE SHUTTER 1",
                                                                  "OPEN SHUTTER 1"]
        self.widget_updatefunc[self.opencloseShut2_pushButton] = [self.update_button,
                                                                  "CLOSE SHUTTER 2",
                                                                  "OPEN SHUTTER 2"]
        self.widget_updatefunc[self.acquire_pushButton] = [self.update_button, "STOP ACQUIRING",
                                                           "START ACQUIRING"]
        self.widget_updatefunc[self.analyse_pushButton] = [self.update_button, "STOP ANALYZING",
                                                           "START ANALYZING"]
        self.widget_updatefunc[self.analyse_pushButton_2] = [self.update_button, "STOP ANALYZING",
                                                             "START ANALYZING"]
        self.widget_updatefunc[self.collectAndSave_pushButton] = [self.update_button,
                                                                  "Collect and Save",
                                                                  "COLLECTING AND SAVING"]
        self.widget_updatefunc[self.useBackground_pushButton] = [self.update_button,
                                                                 "No Background", "Use Background"]
        self.widget_updatefunc[self.useNPoint_pushButton] = [self.update_button, "No NPoint",
                                                             "Use NPoint"]
        self.widget_updatefunc[self.minPixValue] = [self.update_int]
        self.widget_updatefunc[self.maxPixValue] = [self.update_int]
        self.widget_updatefunc[self.step_size_read] = [self.update_int]
        self.widget_updatefunc[self.H_step_read] = [self.update_real]
        self.widget_updatefunc[self.V_step_read] = [self.update_real]
        # wcm_val is in the stats panel
        self.widget_updatefunc[self.wcm_val] = [self.update_real]
        # wcm_2 widget is by the laser motors panel
        self.widget_updatefunc[self.wcm_val_2] = [self.update_real]
        self.widget_updatefunc[self.wcm_mean] = [self.update_real]
        self.widget_updatefunc[self.wcm_sd] = [self.update_real]

        self.widget_updatefunc[self.int_val] = [self.update_real]
        self.widget_updatefunc[self.int_mean] = [self.update_real]
        self.widget_updatefunc[self.int_sd] = [self.update_real]

        self.widget_updatefunc[self.hwp_read] = [self.update_real]
        self.widget_updatefunc[self.last_filename] = [self.update_string]
        self.widget_updatefunc[self.last_directory] = [self.update_latest_dir]
        self.widget_updatefunc[self.set_pos_pushButton] = [self.update_set_pos_button]

        self.widget_updatefunc[self.set_pos_pushButton] = [self.update_set_pos_button]
        self.widget_updatefunc[self.rs_buffer_size] = [self.update_int]

    # the below don't exist yet
    # self.widget_updatefunc[self.int_val] = [self.update_real]
    # self.widget_updatefunc[self.int_val_2] = [self.update_real]
    # self.widget_updatefunc[self.int_mean] = [self.update_real]
    # self.widget_updatefunc[self.int_sd] = [self.update_real]

    def closeEvent(self, event):
        print("closeEvent called")
        self.closing.emit()

    def add_camera_image(self):
        '''
            Sets up the camera image and analysis widgets ...
        '''
        # graphics_view is a GraphicsView from QT
        # add  a PlotItem to the graphics_view
        self.plot_item = pg.PlotItem()
        self.graphics_view.setCentralWidget(self.plot_item)
        #
        '''
            vc_image is an ImageItem, the camera image data to plot
            For backward compatibility, image data is assumed to be in column-major order (column, 
            row). However, most image data is stored in row-major order (row, column) and will 
            need 
            to be transposed before calling setImage():
            this should fix it  
            self.vc_image.setOpts(axisOrder='row-major')
            
            this means x is y and y is x   
        '''
        self.vc_image = pg.ImageItem(view=pg.PlotItem())
        self.vc_image.scale(self.model_data.values[self.model_data.x_pix_scale_factor],
                            self.model_data.values[self.model_data.y_pix_scale_factor])

        self.vc_image.setOpts(axisOrder='row-major')
        self.vc_image.setImage(self.model_data.values[self.model_data.image])

        # a color map
        STEPS = linspace(0, 1, 4)
        CLRS = ['k', 'r', 'y', 'w']
        a = array([pg.colorTuple(pg.Color(c)) for c in CLRS])
        clrmp = pg.ColorMap(STEPS, a)
        lut = clrmp.getLookupTable()
        self.vc_image.setLookupTable(lut)
        #
        # add the vc_image to the plot_item
        self.plot_item.addItem(self.vc_image)
        '''
            The masks from the image analysis are indicated by an ROI overlay
            they are initialised with dummy numbers adn updated to the latest read numbers with 
            user_roiChanged()
            for fun and experience i tried overloading ROIs
            read_roi has no handles users can drag, its just a read of what the current mask is
            user_roi, i.e the one that can be moved 
            we connect the user_roi signal to self.user_roiChanged the function to call when the 
            user has changed the mask 
         '''
        self.read_roi = EllipseROI_NoHandle([0, 0], [500, 500], movable=False, pen='g')
        self.user_roi = EllipseROI_OneHandle([0, 0], [500, 500], movable=False, pen='w')
        self.user_roi.sigHoverEvent.connect(self.user_roi_hashover)
        self.user_roi.addTranslateHandle([0, 0.5])
        self.user_roi.sigRegionChangeFinished.connect(self.user_roiChanged)
        # add to our plot item
        self.plot_item.addItem(self.read_roi)
        self.plot_item.addItem(self.user_roi)
        self.user_roiChanged()
        '''
            the analysis gives a mean position and width, indicated via cross hairs added to 
            plot_item
        '''
        self.v_cross_hair = pg.PlotDataItem()
        self.h_cross_hair = pg.PlotDataItem()
        self.v_cross_hair.setData(x=[1000, 1000], y=[900, 1100], pen='g')
        self.h_cross_hair.setData(x=[900, 1100], y=[1000, 1000], pen='g')
        self.plot_item.addItem(self.v_cross_hair)
        self.plot_item.addItem(self.h_cross_hair)
        '''
            limits and axes in pixels and mm
        '''
        border = 50
        self.plot_item.setLimits(xMin=0, xMax=self.model_data.values[self.model_data.xpix_full],
                                 yMin=0, yMax=self.model_data.values[self.model_data.ypix_full],
                                 minXRange=10,
                                 maxXRange=self.model_data.values[self.model_data.xpix_full],
                                 minYRange=10,
                                 maxYRange=self.model_data.values[self.model_data.ypix_full])
        self.plot_item.setRange(
            xRange=[-border, self.model_data.values[self.model_data.xpix_full] + border], \
            yRange=[-border, self.model_data.values[self.model_data.ypix_full] + border])
        '''
            for axes we'll have pixels and mm, so customize the tick marks
            fairly cancerous below, but we only do it once ... 
        '''
        self.plot_item.showAxis('top')
        self.plot_item.showAxis('right')
        self.x_axis_u = self.plot_item.getAxis(name='top')
        self.x_axis_d = self.plot_item.getAxis(name='bottom')
        self.y_axis_l = self.plot_item.getAxis(name='left')
        self.y_axis_r = self.plot_item.getAxis(name='right')

        self.x_axis_u.setZValue(70000)  # MAGIC_NUMBER Higher than max bin value
        self.x_axis_d.setZValue(70000)  # MAGIC_NUMBER Higher than max bin value
        self.y_axis_l.setZValue(70000)  # MAGIC_NUMBER Higher than max bin value
        self.y_axis_r.setZValue(70000)  # MAGIC_NUMBER Higher than max bin value

        # like a lot of QT use a css to define label styles ... meh
        pixlabelStyle = {'color': 'yellow', 'font-size': '14pt'}
        mmlabelStyle = {'color': 'white', 'font-size': '14pt'}
        self.x_axis_d.setLabel(text='horizontal (pixel)', **pixlabelStyle)
        self.x_axis_u.setLabel(text='horizontal (mm)', **mmlabelStyle)
        self.y_axis_l.setLabel(text='vertical (pixel)', **pixlabelStyle)
        self.y_axis_r.setLabel(text='vertical (mm)', **mmlabelStyle)
        self.x_axis_d.setPen('y')
        self.y_axis_l.setPen('y')
        self.x_axis_u.setPen('w')
        self.y_axis_r.setPen('w')
        '''
            custom tick marks, mm on the up and right axes, plus custom tick positions
            more cancer ...  
        '''
        x_u_major_ticks = []
        y_r_major_ticks = []
        x_u_minor_ticks = []
        y_r_minor_ticks = []
        major_tick = 1
        minor_tick = 0.5

        x_range = int(ceil(
            self.model_data.values[self.model_data.xpix_full] * self.model_data.values[
                self.model_data.x_pix_to_mm]))
        y_range = int(ceil(
            self.model_data.values[self.model_data.ypix_full] * self.model_data.values[
                self.model_data.y_pix_to_mm]))
        x_pm = self.model_data.values[self.model_data.x_pix_to_mm]
        y_pm = self.model_data.values[self.model_data.y_pix_to_mm]

        for i in range(2 * x_range):
            x_u_major_ticks.append([i * major_tick / x_pm, str(i * major_tick)])
            x_u_minor_ticks.append([i * minor_tick / x_pm, str(i * minor_tick)])

        for i in range(2 * y_range):
            y_r_major_ticks.append([i * major_tick / y_pm, str(i * major_tick)])
            y_r_minor_ticks.append([i * minor_tick / y_pm, str(i * minor_tick)])

        self.x_axis_u.setTicks([x_u_major_ticks, x_u_minor_ticks])
        self.y_axis_r.setTicks([y_r_major_ticks, y_r_minor_ticks])

        # pixels on the left and down axes
        x_d_major_ticks = []
        y_l_major_ticks = []
        x_d_minor_ticks = []
        y_l_minor_ticks = []
        xmajor_tick = 512  # MAGIC_NUMBER
        xminor_tick = 256  # MAGIC_NUMBER
        ymajor_tick = 360  # MAGIC_NUMBER
        yminor_tick = 180  # MAGIC_NUMBER

        for i in range(10):  # MAGIC_NUMBER
            x_d_major_ticks.append([i * xmajor_tick, str(i * xmajor_tick)])
            x_d_minor_ticks.append([i * xminor_tick, str(i * xminor_tick)])

        for i in range(12):  # MAGIC_NUMBER
            y_l_major_ticks.append([i * ymajor_tick, str(i * ymajor_tick)])
            y_l_minor_ticks.append([i * yminor_tick, str(i * yminor_tick)])

        self.x_axis_d.setTicks([x_d_major_ticks, x_d_minor_ticks])
        self.y_axis_l.setTicks([y_l_major_ticks, y_l_minor_ticks])
