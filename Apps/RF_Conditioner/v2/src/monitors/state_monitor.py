#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify  //
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
//  FileName:    monitor_hub.py
//  Description: The hardware_control_hub, creates and holds all CATAP hardware controllers,
//                they get passed to where they are needed
//
//*/
'''
from src.data import config
from src.data import rf_conditioning_logger
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QObject
from src.data import config
from src.data import rf_conditioning_logger
from src.data.rf_conditioning_data import rf_conditioning_data
from src.controllers.hardware_control_hub import hardware_control_hub
import numbers


class state_monitor(QObject):
    my_name = 'state_monitor'

    def __init__(self,
                 update_time=100,
                 cooldown_time=5000,
                 timed_cooldown=False,
                 level_cooldown=True,
                 no_cooldown=False):
        QObject.__init__(self)
        self.timed_cooldown = timed_cooldown
        self.level_cooldown = level_cooldown
        self.no_cooldown = no_cooldown
        self.update_time = update_time
        self.cool_down_time = cooldown_time
        self.timer = QTimer()
        # owns a config and logging class
        self.config = config.config()
        self.config_data = self.config.raw_config_data
        self.logger = rf_conditioning_logger.rf_conditioning_logger()
        self.llrf_type = self.config_data[self.config.RF_STRUCTURE]

        # the data class
        self.data = rf_conditioning_data()

        # CATAP hardware controllers, these live here and are passed to where they are needed
        self.hardware = hardware_control_hub()

    def alarm(self, alarm):
        print('alarm ' + alarm)
        """
        maybe pyttsx3 ??? 
        https://stackoverflow.com/questions/30612298/text-to-speech-tts-module-that-works-under-python-3
        what general text to speak should we use??? 
        """
        # subprocess.call('espeak -ven+f5 ' + alarm)
        # base.alarm_process.stdin.write('espeak -ven+f5 ' + alarm )
        # p = subprocess.Popen('espeak '+alarm, shell=True)

    def start(self):
        self.check()
        print(self.my_name + ' starting monitoring, update time = ' + str(self.update_time))
        self.timer.timeout.connect(self.check)
        self.timer.start(self.update_time)

    # a timed cooldown will set not ibnn_cooldown = false a set time after an event
    def set_timed_cooldown(self):
        self.timed_cooldown = True
        self.level_cooldown = False
        self.no_cooldown = False

    # a timed cooldown will set not ibnn_cooldown = false a set time after an event
    def set_level_cooldown(self):
        self.timed_cooldown = False
        self.level_cooldown = True
        self.no_cooldown = False

    def set_no_cooldown(self):
        self.timed_cooldown = False
        self.level_cooldown = True
        self.no_cooldown = False

    # you should probably overload this in child class
    def cooldown_function(self):
        self.logger.message(self.my_name + 'monitor function called, cool down ended')
        self.incool_down = False

    def set_cooldown_mode(self, mode):
        if mode == 'LEVEL':  # MAGIC_STRING
            self.set_level_cooldown()
        elif mode == 'TIMED':  # MAGIC_STRING
            self.set_timed_cooldown()
        elif mode == 'LEVEL_NO_SPIKE':  # MAGIC_STRING
            self.set_no_cooldown()
        else:
            self.set_level_cooldown()

    def sanity_checks(self, items):
        i = 0
        for item in items:
            if not isinstance(item, numbers.Real):
                self.logger.message(self.my_name, ' item ', i, ' failed sanity check', True)
                i += 1
                self.set_success = False
        return self.set_success

