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
//  FileName:    mainView.py
//  Description: The main gui for the virtual cathode application
//
//
//
//
//*/
'''
from PyQt4 import QtGui, QtCore
from viewSource.ellipseROIoverloads import EllipseROI_OneHandle
from viewSource.ellipseROIoverloads import EllipseROI_NoHandle
from viewSource.Ui_mainView import Ui_mainView
from numpy import array
from numpy import random
from numpy import linspace
import pyqtgraph as pg
import  model.data
import inspect

pg.setConfigOptions(imageAxisOrder='row-major')




class mainView(QtGui.QMainWindow, Ui_mainView ):
    print('mainView')
    closing = QtCore.pyqtSignal()# custom close signal to send to controller


    def __init__(self):
        print('mainView 2')
        QtGui.QWidget.__init__(self)
        '''
            The mainView has a copy of the data so it can update the GUI
        '''
        print('mainView 3')
        self.data = model.data.data()
        #
        # startup
        print('mainView 4')
        self.setupUi(self)
        print('mainView 4a')
        self.setWindowTitle("VELA - CLARA Virtual Cathode Setup")
        print('mainView 4b')
        #
        # the mainView holds a few dictionaries that are iterated over to update widgets
        print('mainView 4c')
        self.set_widget_dicts()

        print('mainView 5')

        '''Nominal Style for buttons'''
        self.collect_and_save_pushButton_default_style = self.collectAndSave_pushButton.styleSheet()
        #
        # some widgets need only be connected locally, (no significant dependence on model)
        self.pix_gridlines_checkBox.released.connect(self.handle_pix_gridlines_checkBox)
        self.mm_gridlines_checkBox.released.connect(self.handle_mm_gridlines_checkBox)

        self.load_pushButton.setDisabled(True)
        self.save_pushButton.setDisabled(True)
        self.setInt_pushButton.setDisabled(True)
        self.setWCM_pushButton.setDisabled(True)
        self.set_xpos_pushButton.setDisabled(True)
        self.set_ypos_pushButton.setDisabled(True)

        print('mainView 7')

    def add_camera_image(self):
        '''
            Sets up the camera widget images ... first set some local constants
            the image-data is decimated by a scale factor, but the analysis results are for the
            whole image, this is taken into account with x_pix_scale_factor
        '''
        self.xpix = self.data.values[model.data.num_pix_x]
        print ('self.xpix ', self.xpix)
        self.ypix = self.data.values[model.data.num_pix_y]
        print ('self.ypix ', self.ypix)

        self.xpix_full = self.data.values[model.data.num_pix_x] * self.data.values[
            model.data.x_pix_scale_factor]
        self.ypix_full = self.data.values[model.data.num_pix_y] * self.data.values[
            model.data.y_pix_scale_factor]

        #
        # self.vc_image = pg.ImageItem(np.random.normal(size=(self.xpix, self.ypix)))
        # self.vc_image.scale(self.data.values[model.data.x_pix_scale_factor],
        #                     self.data.values[model.data.y_pix_scale_factor])
        # self.plot_item = self.graphics_view.addPlot(lockAspect=True)
        # self.graphicsView.addWidget(self.vc_image, 0, 2, 23, 3)
        # STEPS = np.linspace(0, 1, 4)
        # CLRS = ['k', 'r', 'y', 'w']
        # a = np.array([pg.colorTuple(pg.Color(c)) for c in CLRS])
        # clrmp = pg.ColorMap(STEPS, a)
        # lut = clrmp.getLookupTable()
        # self.vc_image.setLookupTable(lut)
        # self.plot_item.setRange(xRange=[0, self.xpix_full], yRange=[0, self.ypix_full])
        # self.plot_item.addItem(self.vc_image)
        #
        # self.plot_item.setAspectLocked(True)
        # self.plot_item.setLimits(xMin=0, xMax=self.xpix_full, yMin=0, yMax=self.ypix_full,
        #                          minXRange=10, maxXRange=self.xpix_full, minYRange=10,
        #                          maxYRange=self.ypix_full)
        # self.plot_item.setRange(xRange=[0, self.xpix_full], yRange=[0, self.ypix_full])
        # #         #
        # #         # add in extra graphic items
        # #         # 1. Cross Hairs (with dummy initial values
        # self.v_cross_hair = self.plot_item.plot(x=[1000, 1000], y=[900, 1100], pen='g')
        # self.h_cross_hair = self.plot_item.plot(x=[900, 1100], y=[1000, 1000], pen='g')
        # self.read_roi = EllipseROI_NoHandle([0, 0], [500, 500], movable=False, pen='g')
        # self.plot_item.addItem(self.read_roi)
        # #         #
        # #         # user roi, i.e the one that can be moved
        # #         print 'adding user_roi '
        # self.user_roi = EllipseROI_OneHandle([0, 0], [500, 500], movable=False, pen='w')
        # self.user_roi.sigHoverEvent.connect(self.user_roi_hashover)
        # self.user_roi.addTranslateHandle([0, 0.5])
        # self.plot_item.addItem(self.user_roi)
        # self.user_roi.sigRegionChangeFinished.connect(self.user_roiChanged)
        # #         #
        # #         # set the user (i.,e. changeable) ROI
        # self.user_roiChanged()

    def handle_pix_gridlines_checkBox(self):
        if self.pix_gridlines_checkBox.isChecked():
            self.l1 = self.plot_item.plot(x=[500, 500], y=[0, 2000], pen='b')
            self.l2 = self.plot_item.plot(x=[1000, 1000], y=[0, 2000], pen='b')
            self.l3 = self.plot_item.plot(x=[1500, 1500], y=[0, 2000], pen='b')
            self.l4 = self.plot_item.plot(x=[0, 1040], y=[500, 500], pen='b')
            self.l5 = self.plot_item.plot(x=[0, 1040], y=[1000,1000], pen='b')
            self.l6 = self.plot_item.plot(x=[0, 1040], y=[1500, 1500], pen='b')

    def handle_mm_gridlines_checkBox(self):
        print 'handle_mm_gridlines_checkBox'

    def setLevel(self):
        self.vc_image.setLevels([self.spinBox_minLevel.value(),
                              self.spinBox_maxLevel.value()], update=True)

    def autoSetLevel(self):
        self.spinBox_minLevel.setValue( self.data.values[model.data.min_level_rbv] )
        self.spinBox_maxLevel.setValue( self.data.values[model.data.max_level_rbv] )
        self.setLevel()

    def add_user_ROIEllipse(self):
        self.user_roi.addTranslateHandle([0,0.5])
        self.vc_imageBox.addItem(self.user_roi)
        self.user_roi.sigRegionChangeFinished.connect(self.user_roiChanged)

    def user_roiChanged(self):
        '''
            I think analysis x,y fro the VC are swopped .. ?
        :return:
        '''
        print 'user_roiChanged called'
        x_rad, y_rad = 0.5 * self.user_roi.size()
        x,y = self.user_roi.pos() + [x_rad, y_rad]
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
        self.set_disabled_buttons_on_closed_shutter(model.data.shutter_open)
        for key, value in self.widget_to_dataname.iteritems():
            if self.new_value(value):
                if self.is_mask_read(key):
                    if not_updated_read_roi:
                        self.update_read_roi()
                        not_updated_read_roi = False
                try:
                    self.widget_updatefunc[key][0](key, value, self.widget_updatefunc[key])
                except:
                    print key, value

    def new_value(self,value):
        '''
            test to see if a value in the values dict is different to the value in previous_values
            if it is different return true
        :param value: value to check if new
        :return: is value new or not
        '''
        #print self.data.values.get(value), self.data.previous_values.get(value)
        if value ==  model.data.image:
            return True
        return self.data.values.get(value) != self.data.previous_values.get(value)

    def set_disabled_buttons_on_closed_shutter(self,value):
        v = self.data.values.get(value)
        self.move_H_left_pushButton.setEnabled(v)
        self.move_H_right_pushButton.setEnabled(v)
        self.move_V_down_pushButton.setEnabled(v)
        self.move_V_up_pushButton.setEnabled(v)
        # self.setPosition_pushButton.setEnabled(v)
        # self.setInt_pushButton.setEnabled(v)
        # self.setWCM_pushButton.setEnabled(v)
        # self.set_xpos_pushButton.setEnabled(v)
        # self.set_ypos_pushButton.setEnabled(v)

    def update_crosshair(self):
        '''
            It seems that the x,y and y for analysis are mixed compared to x,y dimensions
        :return:
        '''
        x0 = self.data.values[model.data.x_pix]
        xmin = self.data.values[model.data.x_pix] - self.data.values[model.data.sig_x_pix]
        xmax = self.data.values[model.data.x_pix] + self.data.values[model.data.sig_x_pix]
        y0 = self.data.values[model.data.y_pix]
        ymin = self.data.values[model.data.y_pix] - self.data.values[model.data.sig_y_pix]
        ymax = self.data.values[model.data.y_pix] + self.data.values[model.data.sig_y_pix]
        self.v_cross_hair.setData(x=[x0,x0],y=[ymin,ymax])
        self.h_cross_hair.setData(x=[xmin,xmax],y=[y0,y0])

    """
        Functions to style buttons
    """
    def set_button_color_and_text(self,widget,color,text):
         self.set_button_color( widget = widget, col = color)
         self.setText(text)

    def update_button(self,key, value, param):
        self.set_button(key,value, true_text = param[1], false_text = param[2])

    def set_button(self,key,value,true_text="",true_color="green",false_text="",false_color="red"):
        if self.data.values.get(value):
            self.set_button_color(key, true_color)
            key.setText(true_text)
        else:
            self.set_button_color(key, false_color)
            key.setText(false_text)

    def set_button_color(self,widget,col=""):
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
        self.read_roi.setPos(QtCore.QPoint(self.data.values[model.data.mask_x_rbv] -
                                           self.data.values[model.data.mask_x_rad_rbv],
                                           self.data.values[model.data.mask_y_rbv] -
                                           self.data.values[model.data.mask_y_rad_rbv]))
        self.read_roi.setSize(QtCore.QPoint(2 * self.data.values[model.data.mask_x_rad_rbv],
                                            2 * self.data.values[model.data.mask_y_rad_rbv]))

    def start_up(self):
        ''' here initilise the values to the current reads ... '''
        not_updated_read_roi = True
        self.add_camera_image()
        self.set_user_mask_to_read_mask()

        self.maskX_spinBox.setRange(0,self.xpix_full)
        self.maskY_spinBox.setRange(0,self.ypix_full)
        self.maskXRadius_spinBox.setRange(0,self.xpix_full)
        self.maskYRadius_spinBox.setRange(0,self.ypix_full)

        self.mirror_h_step_set_spinBox.setValue(self.data.values[model.data.H_step_read])
        self.mirror_v_step_set_spinBox.setValue(self.data.values[model.data.V_step_read])
        # update gui wi
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
        x = self.data.values[model.data.mask_x_rbv] - self.data.values[
            model.data.mask_x_rad_rbv]
        y = self.data.values[model.data.mask_y_rbv] - self.data.values[
            model.data.mask_y_rad_rbv]
        xRad = 2*self.data.values[model.data.mask_x_rad_rbv]
        yRad = 2*self.data.values[model.data.mask_y_rad_rbv]
        # make new ellipse here that track sRV ... #
        #print(x,y,xRad,yRad)
        point = QtCore.QPoint(x,y)
        self.user_roi.setPos(point)
        pointRad = QtCore.QPoint(xRad,yRad)
        self.user_roi.setSize(pointRad)
    '''
        helper function to clean up update_gui()
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
    '''
        helper function to clean up update_gui()
    '''

    def update_int(self, widget, value, dummy):
        widget.setText("%i" % self.data.values.get(value))

    def update_real(self, widget, value, dummy):
        widget.setText("%.3f" % self.data.values.get(value))

    def update_image(self, widget, value, dummy):
        self.vc_image.setImage(image = self.data.values.get(value))
        self.vc_image.setLevels([self.spinBox_minLevel.value(),
                             self.spinBox_maxLevel.value()], update=True)

    def update_string(self, widget, value, dummy):
        if self.data.values.get(value) != 'UNKNOWN': # MAGIC_STRING
            widget.setText(QtCore.QString(self.data.values.get(value)))

    def update_latest_dir(self,widget, value, dummy):
        if self.data.values.get(value) != 'UNKNOWN': # MAGIC_STRING
            s = self.data.values.get(model.data.image_save_dir_root) + '\\' + \
                self.data.values.get(value)
            widget.setText(QtCore.QString(s))

    def set_widget_dicts(self):
        '''
            create dict. with all widgets to update, keyed by their values in 'data'
            then loop over this dict and the data dict to update
        '''
        self.widget_to_dataname = {}
        self.widget_to_dataname[self.x_val]=  model.data.x_val
        self.widget_to_dataname[self.x_val_2]=  model.data.x_val
        self.widget_to_dataname[self.x_mean]= model.data.x_mean
        self.widget_to_dataname[self.x_sd]= model.data.x_sd
        self.widget_to_dataname[self.y_val]= model.data.y_val
        self.widget_to_dataname[self.y_val_2]= model.data.y_val
        self.widget_to_dataname[self.y_mean]=model.data.y_mean
        self.widget_to_dataname[self.y_sd]=model.data.y_sd
        self.widget_to_dataname[self.sx_val]=model.data.sx_val
        self.widget_to_dataname[self.sx_mean]=model.data.sx_mean
        self.widget_to_dataname[self.sx_sd]=model.data.sx_sd
        self.widget_to_dataname[self.sy_val]=model.data.sy_val
        self.widget_to_dataname[self.sy_mean]=model.data.sy_mean
        self.widget_to_dataname[self.sy_sd]= model.data.sy_sd
        self.widget_to_dataname[self.cov_val]= model.data.cov_val
        self.widget_to_dataname[self.cov_mean]= model.data.cov_mean
        self.widget_to_dataname[self.cov_sd]= model.data.cov_sd
        self.widget_to_dataname[self.avg_pix_val]= model.data.avg_pix_val
        self.widget_to_dataname[self.avg_pix_mean]= model.data.avg_pix_mean
        self.widget_to_dataname[self.avg_pix_sd]= model.data.avg_pix_sd
        self.widget_to_dataname[self.imageLayout]= model.data.image
        self.widget_to_dataname[self.mask_x_read]= model.data.mask_x_rbv
        self.widget_to_dataname[self.mask_y_read]= model.data.mask_y_rbv
        self.widget_to_dataname[self.mask_x_rad_read]= model.data.mask_x_rad_rbv
        self.widget_to_dataname[self.mask_y_rad_read]= model.data.mask_y_rad_rbv
        self.widget_to_dataname[self.opencloseShut_pushButton]= model.data.shutter_open
        self.widget_to_dataname[self.acquire_pushButton]= model.data.is_acquiring
        self.widget_to_dataname[self.analyse_pushButton]= model.data.is_analysing
        self.widget_to_dataname[self.analyse_pushButton_2]= model.data.is_analysing
        self.widget_to_dataname[self.collectAndSave_pushButton]= model.data.is_collecting_or_saving
        self.widget_to_dataname[self.useBackground_pushButton]= model.data.use_background
        self.widget_to_dataname[self.useNPoint_pushButton]= model.data.use_npoint
        self.widget_to_dataname[self.minPixValue] = model.data.min_level_rbv
        self.widget_to_dataname[self.maxPixValue] = model.data.max_level_rbv
        self.widget_to_dataname[self.step_size_read] = model.data.ana_step_size
        self.widget_to_dataname[self.H_step_read] = model.data.H_step_read
        self.widget_to_dataname[self.V_step_read] = model.data.V_step_read
        self.widget_to_dataname[self.wcm_val] = model.data.wcm_val
        self.widget_to_dataname[self.wcm_val_2] = model.data.wcm_val
        self.widget_to_dataname[self.wcm_mean] = model.data.wcm_mean
        self.widget_to_dataname[self.wcm_sd] = model.data.wcm_sd
        self.widget_to_dataname[self.hwp_read] = model.data.hwp_read
        self.widget_to_dataname[self.last_filename] = model.data.last_save_file
        self.widget_to_dataname[self.last_directory] = model.data.last_save_dir
        # the below don't exist yet
        # self.widget_to_dataname[self.int_val] = model.data.int_val
        # self.widget_to_dataname[self.int_val_2] = model.data.int_val
        # self.widget_to_dataname[self.int_mean] = model.data.int_mean
        # self.widget_to_dataname[self.int_sd] = model.data.int_sd
        '''
            similar to above, but holds the update functions and constant parameters to pass to 
            those functions  
        '''
        self.widget_updatefunc = {}
        self.widget_updatefunc[self.x_val]=  [self.update_real]
        self.widget_updatefunc[self.x_val_2]=  [self.update_real]
        self.widget_updatefunc[self.x_mean]= [self.update_real]
        self.widget_updatefunc[self.x_sd]= [self.update_real]
        self.widget_updatefunc[self.y_val]= [self.update_real]
        self.widget_updatefunc[self.y_val_2]= [self.update_real]
        self.widget_updatefunc[self.y_mean]= [self.update_real]
        self.widget_updatefunc[self.y_sd]= [self.update_real]
        self.widget_updatefunc[self.sx_val]= [self.update_real]
        self.widget_updatefunc[self.sx_mean]= [self.update_real]
        self.widget_updatefunc[self.sx_sd]= [self.update_real]
        self.widget_updatefunc[self.sy_val]= [self.update_real]
        self.widget_updatefunc[self.sy_mean]= [self.update_real]
        self.widget_updatefunc[self.sy_sd]=  [self.update_real]
        self.widget_updatefunc[self.cov_val]= [self.update_real]
        self.widget_updatefunc[self.cov_mean]= [self.update_real]
        self.widget_updatefunc[self.cov_sd]= [self.update_real]
        self.widget_updatefunc[self.avg_pix_val]= [self.update_real]
        self.widget_updatefunc[self.avg_pix_mean]= [self.update_real]
        self.widget_updatefunc[self.avg_pix_sd]= [self.update_real]
        self.widget_updatefunc[self.imageLayout]= [self.update_image]
        self.widget_updatefunc[self.mask_x_read]= [self.update_int]
        self.widget_updatefunc[self.mask_y_read]= [self.update_int]
        self.widget_updatefunc[self.mask_x_rad_read]= [self.update_int]
        self.widget_updatefunc[self.mask_y_rad_read]= [self.update_int]
        self.widget_updatefunc[self.opencloseShut_pushButton]=  [self.update_button,"CLOSE SHUTTERS","OPEN SHUTTERS"]
        self.widget_updatefunc[self.acquire_pushButton]= [self.update_button, "STOP ACQUIRING", "START ACQUIRING"]
        self.widget_updatefunc[self.analyse_pushButton]= [self.update_button,"STOP ANALYZING",
                                                          "START ANALYZING"]
        self.widget_updatefunc[self.analyse_pushButton_2]= [self.update_button,"STOP ANALYZING", "START ANALYZING"]
        self.widget_updatefunc[self.collectAndSave_pushButton]= [self.update_button,"Collect and Save", "COLLECTING AND SAVING"]
        self.widget_updatefunc[self.useBackground_pushButton]= [self.update_button, "No Background", "Use Background"]
        self.widget_updatefunc[self.useNPoint_pushButton] = [self.update_button, "No NPoint",
                                                             "Use NPoint"]
        self.widget_updatefunc[self.minPixValue] = [self.update_int]
        self.widget_updatefunc[self.maxPixValue] = [self.update_int]
        self.widget_updatefunc[self.step_size_read] = [self.update_int]
        self.widget_updatefunc[self.H_step_read] = [self.update_real]
        self.widget_updatefunc[self.V_step_read] = [self.update_real]
        self.widget_updatefunc[self.wcm_val] = [self.update_real]
        self.widget_updatefunc[self.wcm_val_2] = [self.update_real]
        self.widget_updatefunc[self.wcm_mean] = [self.update_real]
        self.widget_updatefunc[self.wcm_sd] = [self.update_real]
        self.widget_updatefunc[self.hwp_read] = [self.update_real]
        self.widget_updatefunc[self.last_filename] = [self.update_string]
        self.widget_updatefunc[self.last_directory] = [self.update_latest_dir]
        # the below don't exist yet
        # self.widget_updatefunc[self.int_val] = [self.update_real]
        # self.widget_updatefunc[self.int_val_2] = [self.update_real]
        # self.widget_updatefunc[self.int_mean] = [self.update_real]
        # self.widget_updatefunc[self.int_sd] = [self.update_real]

    def closeEvent(self,event):
        self.closing.emit()












    def add_camera_image(self):
        '''
            Sets up the camera widget images ... first set some local constants
            the image-data is decimated by a scale factor, but the analysis results are for the
            whole image, this is taken into account with x_pix_scale_factor
        '''
        self.xpix = self.data.values[model.data.num_pix_x]
        print ('self.xpix ', self.xpix)
        self.ypix = self.data.values[model.data.num_pix_y]
        print ('self.ypix ', self.ypix)

        self.xpix_full = self.data.values[model.data.num_pix_x] * self.data.values[
            model.data.x_pix_scale_factor]
        self.ypix_full = self.data.values[model.data.num_pix_y] * self.data.values[
            model.data.y_pix_scale_factor]
        #

        print self.xpix_full
        print self.xpix_full
        print self.xpix_full
        print
        print self.ypix_full
        print self.ypix_full
        print self.ypix_full

        self.vc_image = pg.ImageItem(random.normal(size=(self.xpix, self.ypix)))
        self.vc_image.scale(self.data.values[model.data.x_pix_scale_factor],
                            self.data.values[model.data.y_pix_scale_factor])
        self.plot_item = self.graphics_view.addPlot(lockAspect=True)
        # self.graphics_view.addWidget(monitor, 0, 2, 23, 3)
        STEPS = linspace(0, 1, 4)
        CLRS = ['k', 'r', 'y', 'w']
        a = array([pg.colorTuple(pg.Color(c)) for c in CLRS])
        clrmp = pg.ColorMap(STEPS, a)
        lut = clrmp.getLookupTable()
        self.vc_image.setLookupTable(lut)
        self.plot_item.setRange(xRange=[0, self.xpix_full], yRange=[0, self.ypix_full])
        self.plot_item.addItem(self.vc_image)

        #
        #         #self.view_box = self.graphics_view.addViewBox()
        #         # vc_image is an ImageItem, the camera image data to plot
        #         self.vc_image = pg.ImageItem(np.random.normal(size=(self.xpix, self.ypix)))  # MAGIC_NUM
        #         self.vc_image.setImage(np.random.normal(size=(self.xpix, self.ypix)))  # MAGIC_NUM
        #         self.vc_image.setOpts(axisOrder='row-major')

        # self.vc_image.scale(self.data.values[model.data.x_pix_scale_factor], self.data.values[
        #    model.data.y_pix_scale_factor])
        #         #
        #         # the image is held in a plot item, the plot item is added to graphics_view
        #         self.plot_item = self.graphics_view.addViewBox()
        #         #
        #         # vc_image is added to the plot_item
        #         self.plot_item.addItem(self.vc_image)
        #         #
        #         # the ViewBox for the plot_item controls some display parameters
        #         self.vc_imageBox =  pg.ViewBox()
        #         self.vc_imageBox.addItem(self.vc_image)
        #
        #
        self.plot_item.setAspectLocked(True)
        self.plot_item.setLimits(xMin=0, xMax=self.xpix_full, yMin=0, yMax=self.ypix_full,
                                 minXRange=10, maxXRange=self.xpix_full, minYRange=10,
                                 maxYRange=self.ypix_full)
        self.plot_item.setRange(xRange=[0, self.xpix_full], yRange=[0, self.ypix_full])
        #         #
        #         # add in extra graphic items
        #         # 1. Cross Hairs (with dummy initial values
        self.v_cross_hair = self.plot_item.plot(x=[1000, 1000], y=[900, 1100], pen='g')
        self.h_cross_hair = self.plot_item.plot(x=[900, 1100], y=[1000, 1000], pen='g')
        #         #
        #         # set up color scaling
        #         STEPS = np.linspace(0, 1, 4)
        #         CLRS = ['k', 'r', 'y', 'w']
        #         a = np.array([pg.colorTuple(pg.Color(c)) for c in CLRS])
        #         clrmp = pg.ColorMap(STEPS, a)
        #         lut = clrmp.getLookupTable()
        #         self.vc_image.setLookupTable(lut)
        #         #
        #         # read ellipse (Region Of Interest)
        #         print 'adding read_roi '
        self.read_roi = EllipseROI_NoHandle([0, 0], [500, 500], movable=False, pen='g')
        self.plot_item.addItem(self.read_roi)
        #         #
        #         # user roi, i.e the one that can be moved
        #         print 'adding user_roi '
        self.user_roi = EllipseROI_OneHandle([0, 0], [500, 500], movable=False, pen='w')
        self.user_roi.sigHoverEvent.connect(self.user_roi_hashover)
        self.user_roi.addTranslateHandle([0, 0.5])
        self.plot_item.addItem(self.user_roi)
        self.user_roi.sigRegionChangeFinished.connect(self.user_roiChanged)
        #         #
        #         # set the user (i.,e. changeable) ROI
        self.user_roiChanged()


    def add_camera_image(self):
        '''
            Sets up the camera widget images ... first set some local constants
            the image-data is decimated by a scale factor, but the analysis results are for the
            whole image, this is taken into account with x_pix_scale_factor
        '''
        self.xpix = self.data.values[model.data.num_pix_x]
        print ('self.xpix ', self.xpix)
        self.ypix = self.data.values[model.data.num_pix_y]
        print ('self.ypix ', self.ypix)

        self.xpix_full = self.data.values[model.data.num_pix_x] * self.data.values[
            model.data.x_pix_scale_factor]
        self.ypix_full = self.data.values[model.data.num_pix_y] * self.data.values[
            model.data.y_pix_scale_factor]
    #     #
    #
    #     print self.xpix_full
    #     print self.xpix_full
    #     print self.xpix_full
    #     print
    #     print self.ypix_full
    #     print self.ypix_full
    #     print self.ypix_full
    #
    #     self.vc_image = pg.ImageItem(random.normal(size=(self.xpix, self.ypix)))
    #     self.vc_image.scale(self.data.values[model.data.x_pix_scale_factor],
    #                         self.data.values[model.data.y_pix_scale_factor])
    #     self.plot_item = self.graphics_view.addPlot(lockAspect=True)
    #     # self.graphics_view.addWidget(monitor, 0, 2, 23, 3)
    #     STEPS = linspace(0, 1, 4)
    #     CLRS = ['k', 'r', 'y', 'w']
    #     a = array([pg.colorTuple(pg.Color(c)) for c in CLRS])
    #     clrmp = pg.ColorMap(STEPS, a)
    #     lut = clrmp.getLookupTable()
    #     self.vc_image.setLookupTable(lut)
    #     self.plot_item.setRange(xRange=[0, self.xpix_full], yRange=[0, self.ypix_full])
    #     self.plot_item.addItem(self.vc_image)
    #
    #     #
                #self.view_box = self.graphics_view.addViewBox()
                # vc_image is an ImageItem, the camera image data to plot
                # self.vc_image = pg.ImageItem(np.random.normal(size=(self.xpix, self.ypix)))  # MAGIC_NUM
                # self.vc_image.setImage(np.random.normal(size=(self.xpix, self.ypix)))  # MAGIC_NUM
                # self.vc_image.setOpts(axisOrder='row-major')
    #
    #     # self.vc_image.scale(self.data.values[model.data.x_pix_scale_factor], self.data.values[
    #     #    model.data.y_pix_scale_factor])
    #     #         #
    #     #         # the image is held in a plot item, the plot item is added to graphics_view
    #     #         self.plot_item = self.graphics_view.addViewBox()
    #     #         #
    #     #         # vc_image is added to the plot_item
    #     #         self.plot_item.addItem(self.vc_image)
    #     #         #
    #     #         # the ViewBox for the plot_item controls some display parameters
    #     #         self.vc_imageBox =  pg.ViewBox()
    #     #         self.vc_imageBox.addItem(self.vc_image)
    #     #
    #     #
    #     self.plot_item.setAspectLocked(True)
    #     self.plot_item.setLimits(xMin=0, xMax=self.xpix_full, yMin=0, yMax=self.ypix_full,
    #                              minXRange=10, maxXRange=self.xpix_full, minYRange=10,
    #                              maxYRange=self.ypix_full)
    #     self.plot_item.setRange(xRange=[0, self.xpix_full], yRange=[0, self.ypix_full])
    #     #         #
    #     #         # add in extra graphic items
    #     #         # 1. Cross Hairs (with dummy initial values
    #     self.v_cross_hair = self.plot_item.plot(x=[1000, 1000], y=[900, 1100], pen='g')
    #     self.h_cross_hair = self.plot_item.plot(x=[900, 1100], y=[1000, 1000], pen='g')
    #     #         #
    #     #         # set up color scaling
    #     #         STEPS = np.linspace(0, 1, 4)
    #     #         CLRS = ['k', 'r', 'y', 'w']
    #     #         a = np.array([pg.colorTuple(pg.Color(c)) for c in CLRS])
    #     #         clrmp = pg.ColorMap(STEPS, a)
    #     #         lut = clrmp.getLookupTable()
    #     #         self.vc_image.setLookupTable(lut)
    #     #         #
    #     #         # read ellipse (Region Of Interest)
    #     #         print 'adding read_roi '
    #     self.read_roi = EllipseROI_NoHandle([0, 0], [500, 500], movable=False, pen='g')
    #     self.plot_item.addItem(self.read_roi)
    #     #         #
    #     #         # user roi, i.e the one that can be moved
    #     #         print 'adding user_roi '
    #     self.user_roi = EllipseROI_OneHandle([0, 0], [500, 500], movable=False, pen='w')
    #     self.user_roi.sigHoverEvent.connect(self.user_roi_hashover)
    #     self.user_roi.addTranslateHandle([0, 0.5])
    #     self.plot_item.addItem(self.user_roi)
    #     self.user_roi.sigRegionChangeFinished.connect(self.user_roiChanged)
    #     #         #
    #     #         # set the user (i.,e. changeable) ROI
    #     self.user_roiChanged()
#
#         '''
#             Sets up the camera widget images ... first set some local constants
#             the image-data is decimated by a scale factor, but the analysis results are for the
#             whole image, this is taken into account with x_pix_scale_factor
#         '''
#         self.xpix = self.data.values[model.data.num_pix_x]
#         #print ('self.xpix ',self.xpix)
#         self.ypix = self.data.values[model.data.num_pix_y]
#         #print ('self.ypix ',self.ypix)
#
#         self.xpix_full = self.data.values[model.data.num_pix_x] * self.data.values[
#             model.data.x_pix_scale_factor]
#         self.ypix_full = self.data.values[model.data.num_pix_y] * self.data.values[
#             model.data.y_pix_scale_factor]
#         #
#
#         #https://groups.google.com/forum/#!topic/pyqtgraph/hsy1mVaSNLs
#         #https://groups.google.com/forum/#!topic/pyqtgraph/hsy1mVaSNLs
#         #https://groups.google.com/forum/#!topic/pyqtgraph/hsy1mVaSNLs
#         #https://groups.google.com/forum/#!topic/pyqtgraph/hsy1mVaSNLs
#
#         #self.vc_image = pg.ImageView(random.normal(size=(self.xpix, self.ypix)))
#
#         self.vc_image = self.graphicsView.getImageItem()
#         self.vc_image.setImage(random.normal(size=(self.xpix, self.ypix)))
#
#
#         #imv = pg.ImageView()
#
#
#         self.vc_image.scale(self.data.values[model.data.x_pix_scale_factor],
#                             self.data.values[model.data.y_pix_scale_factor])
#         #self.plot_item = self.graphicsView.addPlot(lockAspect=True)
#         #self.graphics_view.addWidget(monitor, 0, 2, 23, 3)
#
#         colors = [
#             (0, 0, 0),
#             (45, 5, 61),
#             (84, 42, 55),
#             (150, 87, 60),
#             (208, 171, 141),
#             (255, 255, 255)
#         ]
#         cmap = pg.ColorMap(pos=linspace(0.0, 1.0, 6), color=colors)
#         self.graphicsView.setColorMap(cmap)
#
#
#         # STEPS = linspace(0, 1, 4)
#         # CLRS = ['k', 'r', 'y', 'w']
#         # a = array([pg.colorTuple(pg.Color(c)) for c in CLRS])
#         # clrmp = pg.ColorMap(STEPS, a)
#         # self.vc_image_view.setColorMap(clrmp)
#
#         # lut = clrmp.getLookupTable()
#         # self.vc_image.setLookupTable(lut)
#
#         self.vc_image.setRange(xRange=[0, self.xpix_full],yRange=[0, self.ypix_full])
#         self.vc_image.addItem(self.vc_image_view)
#         #self.plot_item.addItem(self.hist_widget)
#
# #
# #         #self.view_box = self.graphics_view.addViewBox()
# #         # vc_image is an ImageItem, the camera image data to plot
# #         self.vc_image = pg.ImageItem(np.random.normal(size=(self.xpix, self.ypix)))  # MAGIC_NUM
# #         self.vc_image.setImage(np.random.normal(size=(self.xpix, self.ypix)))  # MAGIC_NUM
# #         self.vc_image.setOpts(axisOrder='row-major')
#
#
#         # self.vc_image.scale(self.data.values[model.data.x_pix_scale_factor], self.data.values[
#         #    model.data.y_pix_scale_factor])
# #         #
# #         # the image is held in a plot item, the plot item is added to graphics_view
# #         self.plot_item = self.graphics_view.addViewBox()
# #         #
# #         # vc_image is added to the plot_item
# #         self.plot_item.addItem(self.vc_image)
# #         #
# #         # the ViewBox for the plot_item controls some display parameters
# #         self.vc_imageBox =  pg.ViewBox()
# #         self.vc_imageBox.addItem(self.vc_image)
# #
# #
#         self.plot_item.setAspectLocked(True)
#         self.plot_item.setLimits(xMin = 0, xMax = self.xpix_full, yMin = 0, yMax = self.ypix_full,
#                                     minXRange = 10, maxXRange = self.xpix_full, minYRange = 10,
#                                     maxYRange = self.ypix_full)
#         self.plot_item.setRange(xRange=[0, self.xpix_full], yRange=[0, self.ypix_full])
# #         #
# #         # add in extra graphic items
# #         # 1. Cross Hairs (with dummy initial values
#         self.v_cross_hair = self.plot_item.plot(x=[1000, 1000], y=[900,  1100], pen='g')
#         self.h_cross_hair = self.plot_item.plot(x=[900,  1100], y=[1000, 1000], pen='g')
# #         #
# #         # set up color scaling
# #         STEPS = np.linspace(0, 1, 4)
# #         CLRS = ['k', 'r', 'y', 'w']
# #         a = np.array([pg.colorTuple(pg.Color(c)) for c in CLRS])
# #         clrmp = pg.ColorMap(STEPS, a)
# #         lut = clrmp.getLookupTable()
# #         self.vc_image.setLookupTable(lut)
# #         #
# #         # read ellipse (Region Of Interest)
# #         print 'adding read_roi '
#         self.read_roi = EllipseROI_NoHandle([0, 0], [500, 500], movable=False, pen='g')
#         self.plot_item.addItem(self.read_roi)
# #         #
# #         # user roi, i.e the one that can be moved
# #         print 'adding user_roi '
#         self.user_roi = EllipseROI_OneHandle([0, 0], [500, 500], movable=False, pen='w')
#         self.user_roi.sigHoverEvent.connect(self.user_roi_hashover)
#         self.user_roi.addTranslateHandle([0,0.5])
#         self.plot_item.addItem(self.user_roi)
#         self.user_roi.sigRegionChangeFinished.connect(self.user_roiChanged)
# #         #
# #         # set the theuser (i.,e. changeable) ROI
#         self.user_roiChanged()