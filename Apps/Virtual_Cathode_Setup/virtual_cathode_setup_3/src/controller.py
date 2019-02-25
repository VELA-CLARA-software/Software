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
import sys
# meh  https://stackoverflow.com/questions/11953618/pyinstaller-importerror-no-module-named-pyinstaller
sys.path.append('.')
# sys.path.append('C:\\Python27\\Lib\\site-packages\\PyQt4')
# sys.path.append('C:\\Python27\\Scripts')
# sys.path.append('C:\\Python27\\DLLs')
from mainView import mainView
from model import model
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qt

class controller(QtGui.QApplication):
    def __init__(self, sys_argv = None):
        QtGui.QApplication.__init__(self, sys_argv)
        '''define model and view'''
        self.model = model()
        self.view = mainView()
        self.passed_arg = sys_argv
        #
        # connect widgest to functions
        self.connect_widgets()
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
            self.model.update_values()
            self.view.start_up()
        else:
            self.timer.stop()
            self.timer = QtCore.QTimer()
            self.timer.setSingleShot(False)
            self.timer.timeout.connect(self.update)
            self.timer.start(100)


    def update(self):
        # we give the app a few ticks to init the hardware controllers before updating the mainView
        self.model.update_values()
        self.view.update_gui()

    def handle_collect_and_save_pushButton(self):
        self.model.collect_and_save(self.view.numImages_spinBox.value())

    def handle_setPosition_pushButton(self):
        print 'handle_setPosition_pushButton'

    def handle_setMask_pushButton(self):
        self.model.setMask( x = self.view.maskX_spinBox.value(),
                                  y = self.view.maskY_spinBox.value(),
                                  xRad = self.view.maskXRadius_spinBox.value(),
                                  yRad = self.view.maskYRadius_spinBox.value()
                                  )

    def handle_setIntensity_pushButton(self):
        print 'handle_setIntensity_pushButton'

    def handle_load_pushButton(self):
        print 'handle_load_pushButton'

    def handle_save_pushButton(self):
        print 'handle_save_pushButton'

    def handle_resetMeanSD_pushButton(self):
        self.model.reset_running_stats()

    def handle_analyse_pushButton(self):
        #print 'handle_analyse_pushButton'
        self.model.analyse()

    def handle_reset_background_pushButton(self):
        self.model.set_background()
        #print 'handle_reset_background_pushButton'

    def handle_useBackground_pushButton(self):
        self.model.use_background()
        #print 'handle_useBackground_checkBox'

    def handle_use_npoint_pushButton(self):
        self.model.use_npoint()
        #print 'handle_use_npoint_checkBox'

    def handle_acquire_pushButton(self):
        self.model.acquire()
        #print 'handle_acquire_pushButton'

    def handle_numImages_spinBox(self):
        print 'handle_numImages_spinBox'

    def handle_stepSize_spinBox(self):
        self.model.setStepSize(self.view.stepSize_spinBox.value())
        #print 'handle_stepSize_spinBox'

    def handle_autoLevel_pushButton(self):
        self.view.autoSetLevel()
        #print 'handle_stepSize_spinBox'

    def handle_setLevel_pushButton(self):
        self.view.setLevel()
        #print 'handle_stepSize_spinBox'

    def handle_feed_back_check(self):
        #print 'handle_feed_back_check'
        self.model.toggle_feedback(self.view.feed_back_check.isChecked())

    def handle_spinBox_minLevel(self):
        print 'handle_spinBox_minLevel'

    def handle_spinBox_maxLevel(self):
        print 'handle_spinBox_maxLevel'

    def handle_opencloseShut1_pushButton(self):
        print 'handle_opencloseShut1_pushButton'
        self.model.toggle_shutter1()

    def handle_opencloseShut2_pushButton(self):
        print 'handle_opencloseShut2_pushButton'
        self.model.toggle_shutter2()

    def handle_hwp_up_pushButton(self):
        self.model.set_delta_hwp(self.view.hwp_set_spinBox.value())

    def handle_hwp_down_pushButton(self):
        self.model.set_delta_hwp(self.view.hwp_set_spinBox.value())

    def handle_move_left_pushButton(self):
        self.model.move_left(self.view.mirror_h_step_set_spinBox.value())

    def handle_move_right_pushButton(self):
        self.model.move_right(self.view.mirror_h_step_set_spinBox.value())

    def handle_move_down_pushButton(self):
        self.model.move_down(self.view.mirror_v_step_set_spinBox.value())

    def handle_move_up_pushButton(self):
        self.model.move_up(self.view.mirror_v_step_set_spinBox.value())

    def handle_open_path_push_button(self):
        f = '\\\\claraserv3'
        if controller.self.data[data.last_save_dir] == 'UNKNOWN':
            f.join('\\CameraImages\\')
        else:
            f = f + controller.self.data[data.last_save_path]
        QtGui.QFileDialog.getOpenFileNames(self.view.centralwidget, 'Images', f)

    def handle_copy_path_pushButton(self):
        if controller.self.data.get(data.last_save_path) != 'UNKNOWN':#
            # MAGIC_STRING
            s = controller.self.data.get(data.image_save_dir_root)+ \
                controller.self.data.get(data.last_save_dir)
            self.cb.setText(s, mode = self.cb.Clipboard)

    def handle_center_mask_pushButton(self):
        self.model.center_mask()

    def handle_set_pos_pushButton(self):
        self.model.set_pos(self.view.ypos_spinBox.value(),
                           self.view.mirror_v_step_set_spinBox.value())

    def connect_widgets(self):
        #print('connect_widgets')
        self.view.copy_path_pushButton.clicked.connect(self.handle_copy_path_pushButton)
        self.view.set_pos_pushButton.clicked.connect(self.handle_set_pos_pushButton)
        self.view.open_path_push_button.clicked.connect(self.handle_open_path_push_button)
        self.view.collectAndSave_pushButton.clicked.connect(self.handle_collect_and_save_pushButton)
        self.view.setInt_pushButton.clicked.connect(self.handle_setIntensity_pushButton)
        self.view.setMask_pushButton.clicked.connect(self.handle_setMask_pushButton)
        self.view.load_pushButton.clicked.connect(self.handle_load_pushButton)
        self.view.save_pushButton.clicked.connect(self.handle_save_pushButton)
        self.view.resetMeanSD_pushButton.clicked.connect(self.handle_resetMeanSD_pushButton)
        self.view.analyse_pushButton.clicked.connect(self.handle_analyse_pushButton)
        self.view.analyse_pushButton_2.clicked.connect(self.handle_analyse_pushButton)
        self.view.resetBackground_pushButton.clicked.connect(self.handle_reset_background_pushButton)
        self.view.feed_back_check.released.connect(self.handle_feed_back_check)
        self.view.acquire_pushButton.clicked.connect(self.handle_acquire_pushButton)
        self.view.numImages_spinBox.valueChanged.connect(self.handle_numImages_spinBox)
        self.view.stepSize_spinBox.valueChanged.connect(self.handle_stepSize_spinBox)
        self.view.spinBox_minLevel.valueChanged.connect(self.handle_spinBox_minLevel)
        self.view.spinBox_maxLevel.valueChanged.connect(self.handle_spinBox_maxLevel)

        self.view.opencloseShut1_pushButton.clicked.connect(
                self.handle_opencloseShut1_pushButton)
        self.view.opencloseShut2_pushButton.clicked.connect(
                self.handle_opencloseShut2_pushButton)

        self.view.hwp_down_pushButton.clicked.connect(self.handle_hwp_down_pushButton)
        self.view.hwp_up_pushButton.clicked.connect(self.handle_hwp_up_pushButton)
        self.view.move_left_pushButton.clicked.connect(self.handle_move_left_pushButton)
        self.view.move_right_pushButton.clicked.connect(
                self.handle_move_right_pushButton)
        self.view.move_up_pushButton.clicked.connect(self.handle_move_up_pushButton)
        self.view.move_down_pushButton.clicked.connect(
                self.handle_move_down_pushButton)

        self.view.useNPoint_pushButton.clicked.connect(self.handle_use_npoint_pushButton)
        self.view.useBackground_pushButton.clicked.connect(self.handle_useBackground_pushButton)

        self.view.autoLevel_pushButton.clicked.connect(self.handle_autoLevel_pushButton)

        self.view.center_mask_pushButton.clicked.connect(self.handle_center_mask_pushButton)






