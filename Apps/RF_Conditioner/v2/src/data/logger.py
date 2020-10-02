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
//  FileName:    main_controller.py
//  Description: The logger, a generic logging class, designed to be application independent
//               that can log text message data binary data, and TODO:ASCII data
//
//*/
'''

from datetime import datetime
import struct
# from VELA_CLARA_enums import STATE
# this should import all the possible enums that might be logged from CATAP
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from VELA_CLARA_RF_Protection_Control import RF_PROT_STATUS
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
from VELA_CLARA_RF_Modulator_Control import L01_MOD_STATE
from VELA_CLARA_LLRF_Control import TRIG
from VELA_CLARA_LLRF_Control import INTERLOCK_STATE
import os, sys
import cPickle as pkl
import numpy
# import wolframclient.serializers as wxf
from src.data.state import state
from src.data.state import ramp_method
from textwrap import fill
from numpy import float64


class logger(object):
    '''
    This class handles all the data logging, it is designed to be generic, requires a handler class
    to own it adn call its metyhods.
    THIS class should only have generic methods that are application indepedent
    This class has three default files (STATIC so shared throughout an app):
    a text log: text_log_file
    binary log:  binary_log_file
    plaintext_log: binary_log_file
    TODO: For writing binary It does need to know about all the CATAP enums ...
    TODO: static class methods? 'You should really consider creating a static method whenever a
          method does not make substantial use of the instance (self)'

    This class is a use case for Python's double-underscore name mangling ... meh
    https://stackoverflow.com/questions/7841812/inheritance-and-base-class-method-call-python
    classes that inherit from it need access to message, message_header, but they may also want
    to overload it, for example when re-directing print statements to a gui,
    this is the reason for the __do_message and all that
    '''
    # a timestamp, can be used to create a new directory with this timesatmp
    log_start = datetime.now()
    log_start_str = log_start.isoformat('-').replace(":", "-").split('.', 1)[0]
    # the working directory for logging
    working_directory = None
    # these files can be given different directories
    text_log_directory = None
    binary_log_directory = None
    ascii_log_directory = None

    # the file names for log files, you get three
    text_log_file = None
    binary_log_file = None
    ascii_log_file = None

    # A file object that records all messages,
    _text_log_file_obj = None
    _binary_log_file_obj = None
    _ascii_log_file_obj = None

    # binary data starting values. The binary file can become corrupt/broken, if the number of
    # entries in the dictionary to write to file changes, or their type does. To check for this
    # we keep a record of the binary file header to check against each time we write an entry
    _binary_header_length = None
    _binary_header_types = {}
    _binary_header_start_time = None

    # map of python type to struct type https://docs.python.org/2/library/struct.html
    # little endian basic types
    # str IS NOT WELL DEFINED IN THIS !
    # RF_PROT_STATUS and similar enums from our bespoke CATAP controller, SHOULD ALWAYS BE A <B,
    # THINK VERY CAREFULLY about changing this!!!! You have be warned
    # ALL CATAP types and simple types need to be defined here!!
    _python_type_to_bintype = {long: '<q', int: '<i', float: '<f', RF_PROT_STATUS: '<B', L01_MOD_STATE: '<B', GUN_MOD_STATE: '<B', VALVE_STATE: '<B',
                               TRIG: '<B', state: '<B', ramp_method: '<B', INTERLOCK_STATE: '<B', bool: '<?', numpy.float64: '<d', float64: '<d',
                               # BE CAREFUL WiTH str, THE BELOW IS CLEARLY GARBAGE
                               str: '<i'}

    # width of config file text without timestamp (in characters!)
    _column_width = 80
    stars = '\n' + '*' * _column_width + '\n'
    header_format_string = '{:*^' + str(_column_width) + '}'

    # paramters for showing message or adding to text log
    _show_time_stamp = False
    _add_to_text_log = True

    _excluded_key_list = [-9999999]

    def __init__(self, column_width=None):
        if column_width:
            self.column_width = column_width

    @property
    def excluded_key_list(self):
        return logger._excluded_key_list

    @excluded_key_list.setter
    def excluded_key_list(self, value):
        logger._excluded_key_list = value

    # get and set the config file
    @property
    def column_width(self):
        return logger._column_width

    @column_width.setter
    def column_width(self, value):
        logger._config_file = value
        logger.stars = '\n' + '*' * logger._column_width + '\n'
        logger.header_format_string = '{:*^' + str(logger._column_width) + '}'

    def update_timestamp_textlog(self, **kwargs):
        if 'add_to_text_log' in kwargs:
            logger._add_to_text_log = kwargs['add_to_text_log']
        if 'show_time_stamp' in kwargs:
            logger._show_time_stamp = kwargs['show_time_stamp']

    def message(self, text, **kwargs):
        """
        To allow overloads in derived class use the double underscore name-mangling convention
        https://stackoverflow.com/questions/7841812/inheritance-and-base-class-method-call-python
        :param text:  text to print / log, diplay to GUI
        :param kwargs: add_to_text_log=True/False, show_time_stamp=True/False
        """
        self.__do_message(text, **kwargs)

    def message_header(self, text, **kwargs):
        """
        To allow overloads in derived class use the double underscore name-mangling convention
        https://stackoverflow.com/questions/7841812/inheritance-and-base-class-method-call-python
        :param text:  text to print / log, diplay to GUI
        :param kwargs: add_to_text_log=True/False, show_time_stamp=True/False
        """
        self.__do_message_header(text, **kwargs)

    def do_message_header(self, text, **kwargs):
        """
        a header is a specially formatted entry in the text log
        :param text:  text to print / log, diplay to GUI
        :param kwargs: add_to_text_log=True/False, show_time_stamp=True/False
        :return:
        """
        self.update_timestamp_textlog(**kwargs)
        str = logger.stars + logger.header_format_string.format(' ' + text + ' ') + logger.stars
        self.__do_message(str, **kwargs)

    __do_message_header = do_message_header  # !! be careful!! see note at start of class, and link to stackoverflow

    def do_message(self, text, **kwargs):
        '''
        messaging function, print to screen message, adn maybe write to log file
        :param text:  text to print / log, diplay to GUI
        :param kwargs: add_to_text_log=True/False, show_time_stamp=True/False
        :return:
        '''
        self.update_timestamp_textlog(**kwargs)

        # fill is from textwrap  https://docs.python.org/3/library/textwrap.html
        if isinstance(text, basestring):
            str = fill(text, width=logger._column_width)
        elif all(isinstance(item, basestring) for item in text):
            # CANCER
            str = '\n'.join(text)
            str2 = []
            for item in str.splitlines():
                str2.append(fill(item, width=logger._column_width))
            str = '\n'.join(str2)
        else:
            str = "ERROR logger.message was not passed a string "
        if logger._show_time_stamp:
            str = '\n' + datetime.now().isoformat(' ') + '\n' + str
        print(str)
        if logger._add_to_text_log:
            self.write_text_log(str)

    __do_message = do_message  # !! be careful!! see note at start of class, and link to stackoverflow

    def write_text_log(self, str):
        """
        write str, prepended with date-time,  to the log file, NO EXCEPTION Handling here,
        just a quick check to see if the file object exists. I choose this because i thought
        exception handling would be slower and realistically (HAH!), if you've got this far then
        everything should be ok
        :param str: string to write to file
        :return: none
        """
        write_str = str + '\n'
        # if show_time_stamp:
        #     write_str = datetime.now().isoformat(' ') + ' ' + write_str
        if logger._text_log_file_obj:
            logger._text_log_file_obj.write(write_str)
            logger._text_log_file_obj.flush()  # previously opened and closed files as we went ...  # with open(self.log_path,'a') as f:  #     f.write(write_str)
        else:
            print(__name__ + " ERROR Writing to log, logger._text_log_file_obj is None")

    def write_binary_log(self, values):
        '''
        Actually write the binary data, element by element. To ensure the fidelity of the log
        file, we check that the number of elements and their type HAS NOT CHANGED since the
        plaintext header to the file was written. IF it has throw some warning messages
        :param values:  dictionary of values to log,
        '''
        # TODO maybe we don't need to loop over this list twice ...
        written_types = []  # local copy of types actually written
        # print("logger.excluded_key_list = {}".format(logger._excluded_key_list))
        if len(values) == logger._binary_header_length:
            for key, val in values.iteritems():

                if key in logger._excluded_key_list:
                    # print("1 write_binary_log key {} in excluded list ".format(key))
                    pass
                else:
                    # print("1 write_binary_log key {} is NOT in excluded list ".format(key))
                    written_types.append(self.write_binary(val))
        else:
            self.message(["!!!ERROR!!! write_bin_data passed data of incorrect length! ", str(len(values)), "!=", logger._binary_header_length])
            raw_input()

        #todo we are going through thsi loop twcice, i thinkw ecna do it all in a  siingle  pass (if we awant)

        type_list = {}
        for key, val in values.iteritems():  # itervalues means just iterate over the values in the dict

            if key in logger._excluded_key_list:
                # print("2 write_binary_log key {} in excluded list ".format(key))
                pass
            else:
                # print("2 write_binary_log key {} is NOT in excluded list ".format(key))
                rt = self.write_binary(val)
                if rt == False:
                    self.message("!!!ERROR!!! " + key + ", binary log value is NONE-TYPE binary log corrupt ")
                    self.message(" VALUE WAS " + str(val))
                    self.message(" TYPE  WAS " + str(type(val)))
                    raw_input()
                else:
                    type_list[key] = rt
        logger._binary_log_file_obj.flush()
        if type_list != logger._binary_header_types:
            self.message(__name__ + " !!Warning!!, Binary Log File, data types have changed")

            for (k, v) in type_list.iteritems():
                if k in logger._binary_header_types.keys():
                    if type_list[k] != logger._binary_header_types[k]:
                        self.message("write type {} != {} header type, for key = {}".format(type_list[k], logger._binary_header_types[k], k))
                else:
                    print("ERROR! {} key missing".format(k))

    def write_binary(self, val):
        """
        This writes val to fileobject f, it needs to know how to convert all data types to
        struct_format, using logger._python_type_to_bintype
        https://docs.python.org/2/library/struct.html
        TODO: write more cases for logger._python_type_to_bintype
        use a dictionary
        :param val: data to write to file_object
        :return: the type of val (used for error checking)
        """
        val_type = type(val)
        # self.message("val_type = " + str(val_type))
        # for Python enums (used for the general state of things) we need to convert the ENUM
        # to a number
        if val_type is state:
            # self.message("struct_format = <B")
            # self.message("val =  = " + str(val))
            # We use val.value below to get the numerical value of the enum object !!!!!!!
            logger._binary_log_file_obj.write(struct.pack('<B', val.value))
        elif val_type is ramp_method:
            # self.message("struct_format = <B")
            # self.message("val =  = " + str(val))
            # We use val.value below to get the numerical value of the enum object !!!!!!!
            logger._binary_log_file_obj.write(struct.pack('<B', val.value))
        else:
            struct_format = logger._python_type_to_bintype.get(val_type, None)

            if struct_format:
                # self.message("struct_format = " + str(struct_format))
                # self.message("val =  = " + str(val))
                logger._binary_log_file_obj.write(struct.pack(struct_format, val))
            else:
                self.message("ERROR write_binary passed data of {} type. THIS SHOULD NOT HAPPEN! ".format(val_type))
                print(logger._excluded_key_list)
                return False

        return val_type

    def write_binary_log_header(self, data_to_log):
        '''
        This function writes the header for logging binary data
        'data_to_log' is a dictionary of data to log, the binary file header has two line, with each
        column being an entry in data_to_log
        Row 1 gives the key of each entry
        Row 2 gives the type of the value in data_to_log
        It is NECESSARY TO NOT CHANGE THE DATA TYPE FOR EACH ENTRY. If that happens you will not
        know how the binary file is spaced and it will become a corrupt / broken file
        :param data_to_log:  a dictionary of data to log. Whilst logging this dictionary should
        not be added to, nor the type of any entry changed
        :return:
        '''
        # these static variables save the data written to the header, this is so it can be
        # cross-checked against, in further calls to  write_binary()
        logger._binary_header_length = len(data_to_log)  # the number of entries in data_to_log
        logger._binary_header_types = {}  # the type of each entry in data_to_log (filled below)
        header_names = []
        header_types_str = []
        header_types_bytes = []
        # print 'LOGGER excluded_key_list = {}'.format(self.excluded_key_list)
        print("write bin header logger.excluded_key_list = {}".format(logger._excluded_key_list))
        # iterate over data_to_log, and get types for each entry
        for key, value in data_to_log.iteritems():
            if key in logger._excluded_key_list:
                print("write_binary_log_header key {} is in excluded list ".format(key))
            else:
                print("write_binary_log_header key is NOT in excluded list, key = {}, type = {} ".format(key, type(value)))
                value_type = type(value)  # The type of the value being written
                value_type_str = str(value_type)  # the type converted to string
                ''' There is 1 notable exception, we write a time_stamp data type as the time and 
                date this function is called '''
                if key == 'time_stamp':  # MAGIC_STRING
                    header_names.append('time_stamp, (start = ' + datetime.now().isoformat(' ') + ')')
                else:
                    header_names.append(key)
                    size_bytes = sys.getsizeof(value)
                    header_types_str.append(size_bytes)
                logger._binary_header_types[key] = value_type
                header_types_str.append(value_type_str)
        # create the data_log file and write the plaintext header, raise exception if fail
        try:
            # Create rwo strings fro the first two lines of the file, the 1st is tab separated
            # data names, the 2nd is tab separated data types
            joiner = '\t'
            if logger._binary_log_file_obj:
                if type(header_names) != basestring:
                    print(header_names)
                head_names = joiner.join(header_names) + "\n"
                head_types = joiner.join(header_types_str) + "\n"
                head_bytes = joiner.join(header_types_bytes) + "\n"
                logger._binary_log_file_obj.write(head_names)
                logger._binary_log_file_obj.write(head_types)
                logger._binary_log_file_obj.write(head_bytes)
                self.message(["binary log file added ", head_names, head_types], show_time_stamp=False)
            else:
                raise ValueError('logger _binary_log_file_obj not defined')
        except Exception:
            raise

    def open_text_log_file(self, text_TEXT_LOG_FILENAME):
        logger.text_log_file = text_TEXT_LOG_FILENAME
        try:
            if logger.text_log_directory:
                if logger.text_log_file:
                    fp = os.path.join(logger.text_log_directory, logger.text_log_file)
                    logger._text_log_file_obj = open(fp, 'w')
                else:
                    raise ValueError('logger _text_log_file not defined')
            else:
                raise ValueError('logger _text_log_directory not defined')
        except Exception:
            raise

    def open_binary_log_file(self, binary_TEXT_LOG_FILENAME):
        logger.binary_log_file = binary_TEXT_LOG_FILENAME
        try:
            if logger.binary_log_directory:
                if logger.binary_log_file:
                    fp = os.path.join(logger.binary_log_directory, logger.binary_log_file)
                    logger._binary_log_file_obj = open(fp, 'a')
                else:
                    raise ValueError('logger _binary_log_file not defined')
            else:
                raise ValueError('logger _binary_log_directory not defined')
        except Exception:
            raise

    # not implemented yet
    def open_ascii_log_file(self):
        try:
            if logger.ascii_log_directory:
                if logger.ascii_log_file:
                    fp = os.path.join(logger.ascii_log_directory, logger.ascii_log_file)
                    logger._text_log_file_obj = open(fp, 'a')
                else:
                    raise ValueError('logger _ascii_log_file not defined')
            else:
                raise ValueError('logger _ascii_log_directory not defined')
        except Exception:
            raise

    # noinspection PyMethodMayBeStatic
    def pickle_file(self, file_name, obj):
        path = logger.working_directory + file_name
        self.pickle_dump(path, obj)

    # noinspection PyMethodMayBeStatic
    def pickle_dump(self, path, obj):
        self.message(__name__ + ' pickle_dumping ' + path, add_to_text_log=True, show_time_stamp=True)
        try:
            with open(path + '.pkl', 'wb') as f:
                pkl.dump(obj, f, pkl.HIGHEST_PROTOCOL)
        except Exception as e:
            print(e)
            self.message(__name__ + ' EXCEPTION ' + str(e), add_to_text_log=True, show_time_stamp=True)
            self.message(__name__ + ' ERROR pickle_dumping to ' + path, add_to_text_log=True, show_time_stamp=True)

    # '''  # Getters and setter for the 3 different types of log file  # You CAN ONLY SET A FILE IF YOU HAVE A WORKING DIRECTORY  # '''  # @property  # def text_log_file(self):  #     return logger._text_log_file  #  # @text_log_file.setter  # def text_log_file(self, value):  #     logger._text_log_file = value  #  # @property  # def binary_log_file(self):  #     return logger._binary_log_file  #  # @binary_log_file.setter  # def binary_log_file(self, value):  #     logger._binary_log_file = value  #  # @property  # def ascii_log_file(self):  #     return logger._ascii_log_file  #  # @ascii_log_file.setter  # def ascii_log_file(self, value):  #     logger._ascii_log_file = value  #  #  # @property  # def working_directory(self):  #     return logger._working_directory  #  # @working_directory.setter  # def working_directory(self, value):  #     logger._working_directory = value  #  # @property  # def text_log_directory(self):  #     return logger._text_log_directory  #  # @text_log_directory.setter  # def text_log_directory(self, value):  #     print("text_log_directory sdetter")  #     print("text_log_directory sdetter")  #     print("text_log_directory sdetter")  #     print("text_log_directory sdetter")  #     print("text_log_directory sdetter")  #     print("text_log_directory sdetter")  #     print("text_log_directory sdetter")  #     print("text_log_directory sdetter")  #     logger._text_log_directory = value  #  # @property  # def binary_log_directory(self):  #     return logger._binary_log_directory  #  # @binary_log_directory.setter  # def binary_log_directory(self, value):  #     logger._binary_log_directory = value  #  # @property  # def ascii_log_directory(self):  #     return logger._ascii_log_directory  #  # @ascii_log_directory.setter  # def ascii_log_directory(self, value):  #     logger._ascii_log_directory = value

    # TODO Write a converter for wxf files atm convert to wxf offline  # def pkl2wxf(self,path):  #     file = open(path, 'rb')  #     objs = []  #     while True:  #         try:  #             objs.append(pkl.load(file))  #         except EOFError:  #             break  #     file.close()  #     # print(objs)  #     path2 = path.replace(".pkl", "")  #     wxf.export(objs, path2 + '.wxf', target_format='wxf')  #  # def write_binary_old(self, f, val):  #     '''  #     This function needs ot know how to write all data types to binary  #     TODO: write more cases  #     use a dicitonary  #     :param f: fileobject to write binary data to  #     :param val: data to write to file_object  #     :return: the type of val (used for error checking)  #     '''  #     if type(val) is long:  #         f.write(struct.pack('<l', val))  #         #print struct.calcsize('<l')  #     elif type(val) is int:  #         f.write(struct.pack('<i', val))  #         #print struct.calcsize('<i')  #     elif type(val) is float:  #         f.write(struct.pack('<f', val))  #         #print struct.calcsize('<f')  #     elif type(val) is RF_GUN_PROT_STATUS:  #         f.write(struct.pack('<B', val))  #         #print struct.calcsize('<B')  #     elif type(val) is GUN_MOD_STATE:  #         f.write(struct.pack('<B', val))  #         #print struct.calcsize('<B')  #     elif type(val) is VALVE_STATE:  #         f.write(struct.pack('<B', val))  #         #print struct.calcsize('<B')  #     elif type(val) is TRIG:  #         f.write(struct.pack('<B', val))  #         #print struct.calcsize('<B')  #     elif type(val) is INTERLOCK_STATE:  #         f.write(struct.pack('<B', val))  #         #print struct.calcsize('<B')  #     elif type(val) is bool:  #         f.write(struct.pack('<?', val))  #         #print struct.calcsize('<?')  #     elif type(val) is numpy.float64:  #         f.write(struct.pack('<f', val))  #         #f.write(struct.pack('<?', val))  #     elif type(val) is str:  #         f.write(struct.pack('<i', -1))  #     elif type(val) is state:  #         f.write(struct.pack('<B', val))  #     else:  #         print(self.my_name + ' write_binary() error unknown type, ' + str(type(val)) )  #     return type(val)  #     #print str(val) + '   ' + str(type(val))
