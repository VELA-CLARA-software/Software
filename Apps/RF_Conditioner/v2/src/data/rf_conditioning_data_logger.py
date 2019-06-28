#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify     //
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
//  Last edit:   243-06-2019
//  FileName:    rf_conditioning_data_logger.py
//  Description: Holds a data logger and knows how to write data specifically for RF
//               conditioning
//*/
'''
# from VELA_CLARA_enums import STATE
from datetime import datetime
# from src.data.state import state
import os
import cPickle as pkl
from src.data.config import config
from src.data.data_logger import data_logger
import numpy
# import src.data.rf_condition_data_base as dat
# import wolframclient.serializers as wxf
# from src.data.state import state
import sys
import traceback


class rf_conditioning_data_logger(data_logger):
    '''
    inherits from data_logger
    knows about all the craziness required for logging RF conditioning data
    this class should only be for the RF conditioning app
    data_logger, should be, and is intended to be, more generic and useable elsewhere
    rf_conditioning_data_logger knows about these files:
        OUTSIDE_MASK_FORWARD_FILENAME =>  WHERETO PUT OUTSIDE FORWARD EVENTS
        OUTSIDE_MASK_REVERSE_FILENAME =>  WHERETO PUT OUTSIDE REVERSE EVENTS
        OUTSIDE_MASK_PROBE_FILENAME   =>  WHERETO PUT OUTSIDE PROBE EVENTS
        PULSE_COUNT_BREAKDOWN_LOG_FILENAME =>  History of pulse number / breakdown count
        AMP_POWER_LOG_FILENAME  =>  History of amp setpoint and KFPOW values
    the base-class data_logger handles the text log and binary data log
    '''

    def __init__(self):
        data_logger.__init__(self)
        self.my_name = 'rf_conditioning_data_logger'

        # has a config reader to get the config parameters to pass to data_logger
        # WE ASSUME THE CONFIG HAS BEEN PARSED CORRECTLY!
        self.config = config()
        self.config_data = self.config.raw_config_data
        #
        # first setup / check the text log files
        self.setup_text_log_files()
        #
        self.log_config()

    def setup_text_log_files(self):
        """
        Creates the working directories, data file objects for writing the various
        rf_conditioning data files
        :return:
        """
        self.set_log_directories()
        self.set_text_log_files()

    def set_log_directories(self):
        """
        creates the log directories and checks they are all ok
        :return:
        """
        # the log directory is given by the config file
        data_logger.log_directory = self.config_data[config.LOG_DIRECTORY]
        data_logger.working_directory = self.config_data[config.LOG_DIRECTORY]
        # individual text and binary logs are kept in a subdirectory of working directory
        data_logger.text_log_directory = os.path.join(data_logger.working_directory,
                                                      data_logger.log_start_str)
        data_logger.binary_log_directory = os.path.join(data_logger.working_directory,
                                                        data_logger.log_start_str)
        # make a directory for text and binary log
        try:
            os.makedirs(str(data_logger.text_log_directory))
        except:
            self.message("Error creating log directory = " + str(data_logger.text_log_directory))
            raise

    def set_text_log_files(self):
        """
        open / check the following log files:
            PULSE_COUNT_BREAKDOWN_LOG_FILENAME
            AMP_POWER_LOG_FILENAME
            TEXT_LOG_FILENAME
            write header to TEXT_LOG_FILENAME,
            write config to TEXT_LOG_FILENAME
        :return:
        """
        try:
            # Raise exception if PULSE_COUNT_BREAKDOWN_LOG_FILENAME can't be found where expected
            pulse_count_file = os.path.join(data_logger.working_directory,self.config_data[
                config.PULSE_COUNT_BREAKDOWN_LOG_FILENAME])
            if not os.path.exists(pulse_count_file):
                err = pulse_count_file
                raise
            else:
                self.pulse_count_log_file_obj = open(pulse_count_file,'a')

            # Raise exception if AMP_POWER_LOG_FILENAME can't be found where expected
            amp_power_file = os.path.join(data_logger.working_directory,self.config_data[
                config.AMP_POWER_LOG_FILENAME])
            if not os.path.exists(amp_power_file):
                err = amp_power_file
                raise Exception
            else:
                self.amp_power_log_file_obj = open(amp_power_file,'a')

        except Exception:
            print >> sys.stderr, "FileError No such file", err
            raise
        # start the text log
        self.open_text_log_file(self.config_data[config.TEXT_LOG_FILENAME])

        print rf_conditioning_data_logger.text_log_header
        self.write_text_log(rf_conditioning_data_logger.text_log_header,show_time_stamp=False)
        self.message_header("Log Started " + data_logger.log_start_str, add_to_text_log = True,
                            show_time_stamp = False)


    def log_config(self):
        """
        dumps the parsed configuration settings to the log file
        :return:
        """
        self.message_header("Configuration", True)
        logdata = ['config file = ' + self.config_data[config.CONFIG_FILE], 'dumping parsed '
                                                                            'config data to text '
                                                                            'log']
        s = ''
        for key, value in self.config_data.iteritems():
            s += ''.join('%s: %s, ' % (key, value))
            #logdata.append(''.join('%s: %s, ' % (key, value)))
        logdata.append(s)
        self.message(logdata, add_to_text_log = True, show_time_stamp = False)



    def start_text_log(self):
        pass

    def start_binary_log(self):
        pass

    def start_data_logging(self):
        self.header(self.my_name + ' start_data_logging')
        self.message(['data_log path = ' + self.data_path,
                      ' starting monitoring, update time = ' + str(
                          self.log_config['DATA_LOG_TIME'])])
        self.message(['AMP_POWER_LOG  path = ' + self.amp_pwr_path,
                      ' starting monitoring, update time = ' + str(
                          self.log_config['AMP_PWR_LOG_TIME'])])

    # @log_config.setter
    # def log_config(self, value):
    #     data_logger._log_config = value
    #     self.log_directory = data_logger.config.log_config['LOG_DIRECTORY'] + self.log_start_str
    #     os.makedirs(self.log_directory)
    #     self.working_directory = self.log_directory + '\\'
    #     self.data_path = self.working_directory + self.log_config[
    #         'DATA_TEXT_LOG_FILENAME']  # MAGIC_STRING
    #     self.amp_pwr_path = self.working_directory + self.log_config[
    #         'AMP_POWER_LOG_FILENAME']  # MAGIC_STRING
    #     self.forward_file = self.working_directory + self._log_config[
    #         'OUTSIDE_MASK_FORWARD_FILENAME']  #
    #     self.probe_file = self.working_directory + self._log_config[
    #         'OUTSIDE_MASK_PROBE_FILENAME']  #
    #     self.reverse_file = self.working_directory + self._log_config[
    #         'OUTSIDE_MASK_REVERSE_FILENAME']
    #     self.log_path = self.working_directory + self._log_config['TEXT_LOG_FILENAME']
    #     self.header(self.my_name + ' log_config')
    #     self.message(['log_directory     = ' + self.log_directory,
    #                   'working_directory = ' + self.working_directory,
    #                   'data_path    = ' + self.data_path, 'forward_file = ' + self.forward_file,
    #                   'probe_file   = ' + self.probe_file,
    #                   'reverse_file = ' + self.reverse_file, 'log_path     = ' + self.log_path])
    #     # open log_file and LEAVE OPEN
    #     self.log_file = open(self.log_path, 'a')

    def add_to_pulse_breakdown_log(self, x):
        # print('add_to_pulse_breakdown_log')
        towrite = " ".join(map(str, x))
        self.pulse_count_log_file.write(towrite + '\n')
        self.pulse_count_log_file.flush()  # previously opened and closed files as we went ...  #
        # with open(self.pulse_count_log,'a') as f:  #     f.write( towrite + '\n')

    def add_to_KFP_Running_stat_log(self, x):
        # WRITE TO amp_power_log but don't write an amp with zero pulses of data in it
        if x[1] != 0:
            # towrite = " ".join(map(str, x))
            # self.message('Adding to Klystron Forward Power Running Stat Log: ' + towrite,
            # True)
            # print('add_to_KFP_Running_stat_log, ', self.amp_power_log_file,' '.join(map(
            # str, x)))
            self.amp_power_log_file.write(' '.join(map(str, x)) + '\n')
            self.amp_power_log_file.flush()  # previously opened and closed files as we went ...
            # with open(self.amp_power_log,'a') as f:  #     f.write( towrite + '\n')

    def num(self, s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def get_amp_power_log(self):
        self.amp_power_log = data_logger.config.log_config['LOG_DIRECTORY'] + \
                             data_logger.config.log_config['AMP_POWER_LOG_FILENAME']
        r_dict = {}

        with open(self.amp_power_log) as f:
            lines = list(line for line in (l.strip() for l in f) if line)
            for line in lines:
                if '#' not in line:
                    log = [self.num(x) for x in line.split()]
                    r_dict[log[0]] = log[
                                     1:]  # print 'get_amp_power_log ' + str(log[0])  # print
                    # log[1:]
        #
        # now open amp_power_log file for appending and LEAVE OPEN
        self.amp_power_log_file = open(self.amp_power_log, 'a')
        #
        self.header(self.my_name + ' get_amp_power_log', True)
        self.message('read get_amp_power_log: ' + self.amp_power_log, True)
        return r_dict

    def get_pulse_count_breakdown_log(self):
        self.pulse_count_log = data_logger.config.log_config['LOG_DIRECTORY'] + \
                               data_logger.config.log_config['PULSE_COUNT_BREAKDOWN_LOG_FILENAME']
        log = []
        with open(self.pulse_count_log) as f:
            lines = list(line for line in (l.strip() for l in f) if line)
            for line in lines:
                if '#' not in line:
                    log.append([int(x) for x in line.split()])
        self.header(self.my_name + ' get_pulse_count_breakdown_log')
        self.message('read pulse_count_log: ' + self.pulse_count_log)
        # for i in log:
        #     self.message(map(str,i),True)
        #
        ## now open pulse_count_log file for appending and LEAVE OPEN
        self.pulse_count_log_file = open(self.pulse_count_log, 'a')
        return log

    # noinspection PyMethodMayBeStatic
    def pickle_file(self, file_name, obj):
        path = self.working_directory + file_name
        self.pickle_dump(path, obj)

    # noinspection PyMethodMayBeStatic
    def pickle_dump(self, path, obj):
        self.message(self.my_name + ' pickle_dumping to ' + path, True)
        try:
            with open(path + '.pkl', 'wb') as f:
                pkl.dump(obj, f, pkl.HIGHEST_PROTOCOL)
        except Exception as e:
            print(e)
            self.message(self.my_name + ' EXCEPTION ' + str(e), True)
            self.message(self.my_name + ' ERROR pickle_dumping to ' + path, True)

    # don't bother with this, convert to wxf offline  # def pkl2wxf(self,path):  #     file =
    # open(path, 'rb')  #     objs = []  #     while True:  #         try:  #
    # objs.append(pkl.load(file))  #         except EOFError:  #             break  #
    # file.close()  #     # print(objs)  #     path2 = path.replace(".pkl", "")  #
    # wxf.export(objs, path2 + '.wxf', target_format='wxf')

    def dump_forward(self, obj, index):
        self.pickle_dump(path=self.forward_file + str(index), obj=obj)

    def dump_reverse(self, obj, index):
        self.pickle_dump(path=self.reverse_file + str(index), obj=obj)

    def dump_probe(self, obj, index):
        self.pickle_dump(path=self.probe_file + str(index), obj=obj)



    text_log_header = \
    "*******************************************************************************\n"\
    "******** __         __    _  _  ___       _   ___  ___   __         __ ********\n"\
    "******** \ \  ___  / /   | \| |/ _ \     /_\ | _ \/ __|  \ \  ___  / / ********\n"\
    "********  \ \/ _ \/ /    | .` | (_) |   / _ \|   / (__    \ \/ _ \/ /  ********\n"\
    "********   \_\___/_/     |_|\_|\___/   /_/ \_\_|_\\\\___|    \_\___/_/   ********\n"\
    "********                                                               ********"


