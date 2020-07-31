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
//  FileName:    rf_conditioning_logger.py
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
from src.data.logger import logger
import numpy
# import src.data.rf_condition_data_base as dat
# import wolframclient.serializers as wxf
# from src.data.state import state
import sys
import numpy as np
import traceback
import collections
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QTimer

class rf_conditioning_logger(logger):
    '''
    inherits from logger
    knows about all the craziness required for logging RF conditioning data
    this class should only be for the RF conditioning app
    logger, should be, and is intended to be, more generic and useable elsewhere
    rf_conditioning_logger knows about these files:
        OUTSIDE_MASK_FORWARD_FILENAME =>  WHERE TO PUT OUTSIDE FORWARD EVENTS
        OUTSIDE_MASK_REVERSE_FILENAME =>  WHERE TO PUT OUTSIDE REVERSE EVENTS
        OUTSIDE_MASK_PROBE_FILENAME   =>  WHERE TO PUT OUTSIDE PROBE EVENTS
        PULSE_COUNT_BREAKDOWN_LOG_FILENAME =>  History of pulse number / breakdown count
        KFPOW_AMPSP_RUNNING_STATS_LOG_FILENAME  =>  History of amp setpoint and KFPOW values
    the base-class logger handles the text log and binary data log
    rf_conditioning_logger.debug is a flag that when true, the working directory is not
    created anew, with the current timestamp, instead all files go in config.LOG_DIRECTORY
    This class overloads the message and message_header function from the base logger class
    This is so that we can call QApplication.processEvents(), and keep logger free of QT imports

    '''
    debug = False

    _pulse_count_log_file = None
    _pulse_count_log_file_obj = None

    _kfow_running_stats_log_file_obj = None
    _kfow_running_stats_log_file = None

    def __init__(self, debug=False, column_width=80):
        logger.__init__(self,column_width)
        # debug = True sets the working directory directory to not be timestamped,
        # folder, to make
        rf_conditioning_logger.debug = debug
        self.column_width = column_width

        # has a config reader to get the config parameters to pass to logger
        # WE ASSUME THE CONFIG HAS BEEN PARSED CORRECTLY!
        self.config = config()
        self.config_data = self.config.raw_config_data

        self.data_log_timer = QTimer() # A thread to write the binary log

        self.values = None

    # TODO AJG: define function to bin amp-power data after amp-power log is read in.
    #  Need to make sure bin_width, max_amp & max_pow are defined in the config.yml


    def set_data_values(self, values):
        '''
        Data Values is the main data values dictionary that is logged to a bianry file
        :param values:
        :return:
        '''
        self.values = values


    def start_binary_data_logging(self, values):
        '''
        set local self.values to values and  Start the binary data log,
        :param values: main data values dictionary that is logged to a binary file
        rf_condition_data.values[]
        '''
        self.values = values
        self.data_log_timer = QTimer()
        self.open_binary_log_file( self.config_data[self.config.BINARY_DATA_LOG_FILENAME] )

        self.message_header(__name__ + ' start_binary_data_logging ', show_time_stamp=True)

        ''' Write the plaintext header to the log file '''
        self.write_binary_log_header(self.values)
        self.log_binary_data()
        self.data_log_timer.timeout.connect(self.log_binary_data)
        self.data_log_timer.start( self.config_data[self.config.BINARY_DATA_LOG_TIME] )

    def log_binary_data(self):
        '''
        Calls logger write_binary_log
        This function is generally called in a new thread controlled by a Qtimer
        '''
        self.write_binary_log(self.values)

    # NNeds re-writing
    def start_data_logging(self):
        self.header(__name__ + ' start_data_logging')
        self.message(['data_log path = ' + self.data_path, ' starting monitoring, update time = ' + str(self.log_config['DATA_LOG_TIME'])])
        self.message(
            ['AMP_POWER_LOG  path = ' + self.amp_pwr_path, ' starting monitoring, update time = ' + str(self.log_config['AMP_PWR_LOG_TIME'])])


    def num(self, s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def add_to_kfpow_running_stat_log(self, x):
        '''
        WRITE x TO kfpow_running_stat_log but don't write for an amp with zero pulses of data in it
        x is a list of:
        [amp_sp, num_pulses (with beam), rolling mean, rolling variance * (num_pulses -1)]
        '''
        if x[1] != 0:
            self._kfow_running_stats_log_file_obj.write(' '.join(map(str, x)) + '\n')
            self._kfow_running_stats_log_file_obj.flush()

            # def add_to_pulse_breakdown_log(self, x):

    def add_to_pulse_count_breakdown_log(self, new_values):
        """
        update the _pulse_count_log_file with latest numbers
        Adds x to the pulse_breakdown_log, x is a list of: [Total ACTIVE Pulses, Num breakdowns,
        amp_set, ramp_index (point on pulse / power curve) , pulse length]
        :param new_values: A LIST OF NUMBERS ! that are converted to a string and written to
        _pulse_count_log_file_obj
        """
        rf_conditioning_logger._pulse_count_log_file_obj.write(" ".join(map(str, new_values)) + '\n')
        rf_conditioning_logger._pulse_count_log_file_obj.flush()

    def get_pulse_count_breakdown_log(self):
        '''
        read the pulse_breakdown_count log file and put the contents in log
        create a file object _pulse_count_log_file_obj to use for appending new data
        :return: log (nested list of pulse_breakdown_log entries
        '''
        self.message(__name__ + ' get pulse_count_breakdown_log', show_time_stamp=False)
        self.message('FileName = ' + rf_conditioning_logger._pulse_count_log_file)
        log = []
        with open(rf_conditioning_logger._pulse_count_log_file) as f:
            lines = list(line for line in (l.strip() for l in f) if line)
            for line in lines:
                if '#' not in line:
                    log.append([int(x) for x in line.split()])
        self.message('Read pulse_count_breakdown_log')
        rf_conditioning_logger._pulse_count_log_file_obj = open(rf_conditioning_logger._pulse_count_log_file, 'a')
        return log

    def get_kfpow_running_stat_log(self):
        '''
        This reads the _kfow_running_stats_log_file. During conditioning this file is updated,
        new running stats values replaces old ones for the same amp_sp. This makes the
        _kfow_running_stats_log_file continually grow in size. It can become overly large. To
        minimize this size we can create a new version of the file after parsing the old version
        :return: a dictionary of amp_sp keys and KFPow running stat values
        '''
        r_dict = {}
        self.message('get_kfpow_running_stat_log')
        self.message('kfpow_running_stat_log filename = '
                     '' + rf_conditioning_logger._kfow_running_stats_log_file)
        with open(rf_conditioning_logger._kfow_running_stats_log_file) as f:
            lines = list(line for line in (l.strip() for l in f) if line)
            got_header = False
            header_string = ''
            for line in lines:
                if got_header:
                    if '#' not in line:
                        log = [self.num(x) for x in line.split()]
                        r_dict[log[0]] = log[1:]  # print 'get_amp_power_log ' + str(log[0])
                else:
                    if '#' in line:
                        header_string += line + '\n'
                    else:
                        log = [self.num(x) for x in line.split()]
                        r_dict[log[0]] = log[1:]
                        got_header = True
        # write the dictionary to file only the latest values for each amp_sp will be kept
        # also write the data in order of ascending amp_sp
        ordered_r_dict = collections.OrderedDict(sorted(r_dict.items()))
        self.message_header('Print Rationalized kfpow_running_stat_log ', show_time_stamp=False, add_to_text_log=True)
        full_string = ''
        with open(rf_conditioning_logger._kfow_running_stats_log_file, 'w') as f:
            f.write(header_string)
            for key, value in ordered_r_dict.iteritems():
                # str(key) + ' '.join(map(str, value)) + '\n'

                f.write(str(key) + ' ' + ' '.join(map(str, value)) + '\n')
        self.message('get_kfpow_running_stat_log complete', show_time_stamp=False,
                     add_to_text_log=True)
                # s = str(key) + ' ' + ' '.join(map(str, value)) + '\n'
                # f.write(s)
                # full_string += s + '\n'
                # print(s)
        # #self.message(full_string, show_time_stamp=False, add_to_text_log=True)
        # self.message('get_kfpow_running_stat_log complete', show_time_stamp=False, add_to_text_log=True)

        # now open amp_power_log file for appending and LEAVE OPEN
        rf_conditioning_logger._kfow_running_stats_log_file_obj = open(rf_conditioning_logger._kfow_running_stats_log_file, 'a')
        return r_dict

    def setup_text_log_files(self):
        """
        Creates the working directories, data file objects for writing the various
        rf_conditioning text data files, only call this once per application
        """
        self.set_log_directories()
        self.set_text_log_files()

    def set_log_directories(self):
        """
        creates the log directories and checks they are all ok
        :return: nothing
        """
        # the log directory is given by the config file
        logger.log_directory = self.config_data[config.LOG_DIRECTORY]
        logger.working_directory = self.config_data[config.LOG_DIRECTORY]

        # set where to save Outside mask Event data
        self.forward_file = self.working_directory + self.config_data[config.OUTSIDE_MASK_FORWARD_FILENAME]
        self.probe_file = logger.working_directory + self.config_data[config.OUTSIDE_MASK_PROBE_FILENAME]
        self.reverse_file = logger.working_directory + self.config_data[config.OUTSIDE_MASK_REVERSE_FILENAME]

        # if in debug mode all files go in  working_directory
        if rf_conditioning_logger.debug:
            logger.text_log_directory = logger.working_directory
            logger.binary_log_directory = logger.working_directory
        else:
            # individual text and binary logs are kept in a subdirectory of working directory
            logger.text_log_directory = os.path.join(logger.working_directory, logger.log_start_str)
            logger.binary_log_directory = os.path.join(logger.working_directory, logger.log_start_str)
            # make a directory for text and binary log
            try:
                os.makedirs(str(logger.text_log_directory))
            except:
                self.message("Error creating log directory = " + str(logger.text_log_directory))
                raise

    def set_text_log_files(self):
        """
        open / check the following log files:
            PULSE_COUNT_BREAKDOWN_LOG_FILENAME
            KFPOW_AMPSP_RUNNING_STATS_LOG_FILENAME
            TEXT_LOG_FILENAME
            write header to TEXT_LOG_FILENAME,
            write config to TEXT_LOG_FILENAME
        """
        # local alias to make lines shorter
        rcl = rf_conditioning_logger
        try:
            # Raise exception if PULSE_COUNT_BREAKDOWN_LOG_FILENAME can't be found where expected
            rcl._pulse_count_log_file = os.path.join(logger.working_directory, self.config_data[config.PULSE_COUNT_BREAKDOWN_LOG_FILENAME])
            if not os.path.exists(rf_conditioning_logger._pulse_count_log_file):
                err = rcl._pulse_count_log_file
                raise
            # Raise exception if KFPOW_AMPSP_RUNNING_STATS_LOG_FILENAME can't be found where
            # expected
            rcl._kfow_running_stats_log_file = os.path.join(logger.working_directory, self.config_data[config.KFPOW_AMPSP_RUNNING_STATS_LOG_FILENAME])
            if not os.path.exists(rcl._kfow_running_stats_log_file):
                err = rcl._kfow_running_stats_log_file
                raise Exception
        except Exception:
            print >> sys.stderr, "FileError No such file", err
            raise
        # start the text log
        self.open_text_log_file(self.config_data[config.TEXT_LOG_FILENAME])

        print rcl.text_log_header
        self.write_text_log(rcl.text_log_header)
        self.message_header("Log Started " + logger.log_start_str, add_to_text_log=True, show_time_stamp=False)

    def log_config(self):
        """
        dumps the parsed configuration settings to the log file
        """
        self.message_header("Configuration", add_to_text_log=True, show_time_stamp=False)
        logdata = ['config file = ' + self.config_data[config.CONFIG_FILE], 'dumping parsed '
                                                                            'config data to text '
                                                                            'log']
        s = ''
        for key, value in self.config_data.iteritems():
            s += ''.join('%s: %s, ' % (key, value))  # logdata.append(''.join('%s: %s, ' % (key,   # value)))
        logdata.append(s)
        self.message(logdata)

    def dump_ome_data(self, filename, object):
        """
        Pickle dump an ome data dictionary to file (called from outside_mask_trace_monitor )
        """
        self.pickle_dump(path=os.path.join(logger.working_directory, filename), obj=object)

    # noinspection PyMethodMayBeStatic
    def pickle_dump(self, path, obj):
        try:
            with open(path + '.pkl', 'wb') as f:
                pkl.dump(obj, f, pkl.HIGHEST_PROTOCOL)
        except Exception as e:
            print(e)
            self.message(__name__ + ' EXCEPTION ' + str(e))
            self.message(__name__ + ' ERROR pickle_dumping to ' + path)
        self.message(__name__ + ' pickle_dumped  ' + path)

    def start_text_log(self):
        pass

    def message(self, text, **kwargs):
        """
        overloaded from the logger base class so we can include QApplication.processEvents()
        https://stackoverflow.com/questions/7841812/inheritance-and-base-class-method-call-python
        :param text:  text to print / log, diplay to GUI
        :param kwargs: add_to_text_log=True/False, show_time_stamp=True/False
        """
        logger.message(self,text,**kwargs)
        QApplication.processEvents()

    def message_header(self, text, **kwargs):
        """
        overloaded from the logger base class so we can include QApplication.processEvents()
        https://stackoverflow.com/questions/7841812/inheritance-and-base-class-method-call-python
        :param text:  text to print / log, diplay to GUI
        :param kwargs: add_to_text_log=True/False, show_time_stamp=True/False
        """
        logger.message_header(self,text, **kwargs)
        QApplication.processEvents()


    # noinspection PyMethodMayBeStatic
    def pickle_file(self, file_name, obj):
        path = self.working_directory + file_name
        self.pickle_dump(path, obj)
    # don't bother with this, convert to wxf offline  # def pkl2wxf(self,path):  #     file =
    # open(path, 'rb')  #     objs = []  #     while True:  #         try:  #
    # objs.append(pkl.load(file))  #         except EOFError:  #             break  #
    # file.close()  #     # print(objs)  #     path2 = path.replace(".pkl", "")  #
    # wxf.export(objs, path2 + '.wxf', target_format='wxf')

    text_log_header = \
        "****************************************************************************************************\n" \
                      "******************* __         __    _  _  ___       _   ___  ___   __     " \
        "" \
                      "    __ ******************\n" \
                      "******************* \ \  ___  / /   | \| |/ _ \     /_\ | _ \/ __|  \ \  " \
                      "___  / / ******************\n" \
                      "*******************  \ \/ _ \/ /    | .` | (_) |   / _ \|   / (__    \ \/ " \
                      "_ \/ /  ******************\n" \
                      "*******************   \_\___/_/     |_|\_|\___/   /_/ \_\_|_\\\\___|    " \
                      "\_\___/_/   ******************\n" \
                      "*******************                                                               ******************"
