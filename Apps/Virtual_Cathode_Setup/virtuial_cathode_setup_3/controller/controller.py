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
//  FileName:    controller.py
//  Description: The controller for the virtual cathode operator application
//
//
//
//
//*/
'''
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qt
import view.mainView as view
import model.model as model
import model.data as data


class controller(object):
    model = None
    view  = None
    def __init__(self,sys_argv = None,view = None, model= None):
        '''define model and view'''
        controller.model = model
        controller.view = view
        #
        # connect widgest to functions
        # self.connect_widgets()
        # #
        # # The app updates states, values and the gui via a timer
        # # to allow some time for start-up we have a counter
        self.start_count = 0
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.start_up_update)
        self.timer.start(100)
        # #
        # # show the gui
        self.view.show()
        self.view.activateWindow()
        #
        # # a clipboad item fro copying paths to
        # self.cb = QtGui.QApplication.clipboard()
        # self.cb.clear(mode = self.cb.Clipboard)


    def start_up_update(self):
        # we give the app a few ticks to init the hardware controllers before updating the mainView
        if self.start_count < 5:
            self.start_count += 1
        elif self.start_count == 5:
            self.start_count += 1
            controller.model.update_values()
            self.view.start_up()
        else:
            self.timer.stop()
            self.timer = QtCore.QTimer()
            self.timer.setSingleShot(False)
            self.timer.timeout.connect(self.update)
            self.timer.start(100)


    def update(self):
        # we give the app a few ticks to init the hardware controllers before updating the mainView
        controller.model.update_values()
        controller.view.update_gui()

    def handle_collect_and_save_pushButton(self):
        controller.model.collect_and_save(controller.view.numImages_spinBox.value())

    def handle_setPosition_pushButton(self):
        print 'handle_setPosition_pushButton'

    def handle_setMask_pushButton(self):
        controller.model.setMask( x = controller.view.maskX_spinBox.value(),
                                  y = controller.view.maskY_spinBox.value(),
                                  xRad = controller.view.maskXRadius_spinBox.value(),
                                  yRad = controller.view.maskYRadius_spinBox.value()
                                  )

    def handle_setIntensity_pushButton(self):
        print 'handle_setIntensity_pushButton'

    def handle_load_pushButton(self):
        print 'handle_load_pushButton'

    def handle_save_pushButton(self):
        print 'handle_save_pushButton'

    def handle_resetMeanSD_pushButton(self):
        controller.model.reset_running_stats()

    def handle_analyse_pushButton(self):
        #print 'handle_analyse_pushButton'
        controller.model.analyse()

    def handle_reset_background_pushButton(self):
        controller.model.set_background()
        #print 'handle_reset_background_pushButton'

    def handle_useBackground_pushButton(self):
        controller.model.use_background()
        #print 'handle_useBackground_checkBox'

    def handle_use_npoint_pushButton(self):
        controller.model.use_npoint()
        #print 'handle_use_npoint_checkBox'

    def handle_acquire_pushButton(self):
        controller.model.acquire()
        #print 'handle_acquire_pushButton'

    def handle_numImages_spinBox(self):
        print 'handle_numImages_spinBox'

    def handle_stepSize_spinBox(self):
        controller.model.setStepSize(controller.view.stepSize_spinBox.value())
        #print 'handle_stepSize_spinBox'

    def handle_autoLevel_pushButton(self):
        controller.view.autoSetLevel()
        #print 'handle_stepSize_spinBox'

    def handle_setLevel_pushButton(self):
        controller.view.setLevel()
        #print 'handle_stepSize_spinBox'

    def handle_feed_back_check(self):
        #print 'handle_feed_back_check'
        controller.model.toggle_feedback(controller.view.feed_back_check.isChecked())

    def handle_spinBox_minLevel(self):
        print 'handle_spinBox_minLevel'

    def handle_spinBox_maxLevel(self):
        print 'handle_spinBox_maxLevel'

    def handle_opencloseShut1_pushButton(self):
        controller.model.toggle_shutter()
        #print 'handle_opencloseShut_pushButton'

    def handle_opencloseShut2_pushButton(self):
        controller.model.toggle_shutter()
        #print 'handle_opencloseShut_pushButton'

    def handle_hwp_up_pushButton(self):
        controller.model.set_delta_hwp(controller.view.hwp_set_spinBox.value())

    def handle_hwp_down_pushButton(self):
        controller.model.set_delta_hwp(-controller.view.hwp_set_spinBox.value())

    def handle_move_H_left_pushButton(self):
        controller.model.move_H_mirror(controller.view.mirror_h_step_set_spinBox.value())

    def handle_move_H_right_pushButton(self):
        controller.model.move_H_mirror(-controller.view.mirror_h_step_set_spinBox.value())

    def handle_move_V_down_pushButton(self):
        controller.model.move_V_mirror(-controller.view.mirror_v_step_set_spinBox.value())

    def handle_move_V_up_pushButton(self):
        controller.model.move_V_mirror(controller.view.mirror_v_step_set_spinBox.value())

    def handle_open_path_push_button(self):
        f = '\\\\claraserv3'
        if controller.model.data.values[data.last_save_dir] == 'UNKNOWN':
            f.join('\\CameraImages\\')
        else:
            f = f + controller.model.data.values[data.last_save_path]
        QtGui.QFileDialog.getOpenFileNames(self.view.centralwidget, 'Images', f)

    def handle_copy_path_pushButton(self):
        if controller.model.data.values.get(data.last_save_path) != 'UNKNOWN':#
            # MAGIC_STRING
            s = controller.model.data.values.get(data.image_save_dir_root)+ \
                controller.model.data.values.get(data.last_save_dir)
            self.cb.setText(s, mode = self.cb.Clipboard)

    def handle_center_mask_pushButton(self):
        controller.model.center_mask()

    def handle_set_xpos_pushButton(self):
        controller.model.set_x_pos(self.view.xpos_spinBox.value(),
                                   controller.view.mirror_h_step_set_spinBox.value())

    def handle_set_ypos_pushButton(self):
        controller.model.set_y_pos(self.view.ypos_spinBox.value(),
                                   controller.view.mirror_v_step_set_spinBox.value())



    def connect_widgets(self):
        #print('connect_widgets')
        controller.view.copy_path_pushButton.clicked.connect(self.handle_copy_path_pushButton)
        controller.view.set_xpos_pushButton.clicked.connect(self.handle_set_xpos_pushButton)
        controller.view.set_ypos_pushButton.clicked.connect(self.handle_set_ypos_pushButton)
        controller.view.open_path_push_button.clicked.connect(self.handle_open_path_push_button)
        controller.view.collectAndSave_pushButton.clicked.connect(self.handle_collect_and_save_pushButton)
        #controller.view.setPosition_pushButton.clicked.connect(self.handle_setPosition_pushButton)
        controller.view.setInt_pushButton.clicked.connect(
                self.handle_setIntensity_pushButton)
        controller.view.setMask_pushButton.clicked.connect(self.handle_setMask_pushButton)
        controller.view.load_pushButton.clicked.connect(self.handle_load_pushButton)
        controller.view.save_pushButton.clicked.connect(self.handle_save_pushButton)
        controller.view.resetMeanSD_pushButton.clicked.connect(self.handle_resetMeanSD_pushButton)
        controller.view.analyse_pushButton.clicked.connect(self.handle_analyse_pushButton)
        controller.view.analyse_pushButton_2.clicked.connect(self.handle_analyse_pushButton)
        controller.view.resetBackground_pushButton.clicked.connect(self.handle_reset_background_pushButton)
        controller.view.feed_back_check.released.connect(self.handle_feed_back_check)
        controller.view.acquire_pushButton.clicked.connect(self.handle_acquire_pushButton)
        controller.view.numImages_spinBox.valueChanged.connect(self.handle_numImages_spinBox)
        controller.view.stepSize_spinBox.valueChanged.connect(self.handle_stepSize_spinBox)
        controller.view.spinBox_minLevel.valueChanged.connect(self.handle_spinBox_minLevel)
        controller.view.spinBox_maxLevel.valueChanged.connect(self.handle_spinBox_maxLevel)
        controller.view.opencloseShut1_pushButton.clicked.connect(
                self.handle_opencloseShut1_pushButton)
        controller.view.opencloseShut2_pushButton.clicked.connect(
                self.handle_opencloseShut2_pushButton)
        controller.view.hwp_down_pushButton.clicked.connect(self.handle_hwp_down_pushButton)
        controller.view.hwp_up_pushButton.clicked.connect(self.handle_hwp_up_pushButton)
        controller.view.move_H_left_pushButton.clicked.connect(self.handle_move_H_left_pushButton)
        controller.view.move_H_right_pushButton.clicked.connect(
                self.handle_move_H_right_pushButton)
        controller.view.move_V_up_pushButton.clicked.connect(self.handle_move_V_up_pushButton)
        controller.view.move_V_down_pushButton.clicked.connect(
                self.handle_move_V_down_pushButton)


        controller.view.useNPoint_pushButton.clicked.connect(self.handle_use_npoint_pushButton)
        controller.view.useBackground_pushButton.clicked.connect(
                self.handle_useBackground_pushButton)

        controller.view.autoLevel_pushButton.clicked.connect(
                self.handle_autoLevel_pushButton)

        controller.view.center_mask_pushButton.clicked.connect(
                self.handle_center_mask_pushButton)






