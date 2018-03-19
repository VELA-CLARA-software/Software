from datetime import datetime
import struct
from VELA_CLARA_enums import STATE
import os
import pickle
import config_reader
import numpy
# import data.scope_writer_data_base as dat


class data_logger(object):
    my_name = 'data_logger'
    config = config_reader.config_reader()
    _log_config = None

    log_start = datetime.now()
    log_start_str = log_start.isoformat('-').replace(":", "-").split('.', 1)[0]

    def __init__(self):
        pass

    @property
    def log_config(self):
        return data_logger._log_config

    @log_config.setter
    def log_config(self,value):
        data_logger._log_config = value
        self.log_directory = data_logger.config.log_config['LOG_DIRECTORY'] + self.log_start_str
        os.makedirs(self.log_directory)
        self.working_directory = self.log_directory + '\\'
        self.data_path = self.working_directory + self.log_config['DATA_LOG_FILENAME']  # MAGIC_STRING
        self.log_path = self.working_directory + self._log_config['LOG_FILENAME']
        self.header(self.my_name + ' log_config')
        self.message([
            'log_directory     = ' + self.log_directory,
            'working_directory = ' + self.working_directory,
            'data_path    = ' + self.data_path,
            'log_path     = ' + self.log_path
        ])


    def header(self, text, add_to_log = False):
        str = '*' + '\n' +'*** ' + text + '***'
        print(str)
        if add_to_log:
            self.write_log(str)

    def message(self,text=[], add_to_log = False):
        if isinstance(text, basestring):
            str = text
        else:
            str = '\n'.join(text)
        print(str)
        if add_to_log:
            self.write_log(str)

    def write_log(self, str):
        #write_str = datetime.now().isoformat('-').replace(":", "-").split('.', 1)[0] + ' ' + str + '\n'
        write_str = datetime.now().isoformat(' ') + ' ' + str + '\n'
        with open(self.log_path,'a') as f:
            f.write(write_str)

    def write_list(self, data, file):
        with open(file,'w') as f:
            for item in data:
                f.write("%s\n" % item)

    def start_data_logging(self):
        self.header(self.my_name + ' start_data_logging')
        self.message([
            'data_path     = ' + self.data_path,
            'starting monitoring, update time = ' + str(self.log_config['DATA_LOG_TIME'])
        ])

    def write_data_log_header(self,values):
        print(self.my_name + ' writing data_log header to ' + self.data_path)
        joiner = '\t'
        names = []
        types = []
        [names.append(x) for x,y in values.iteritems()]
        # names[names.index(dat.time_stamp)] =  dat.time_stamp +  ", (start = " + datetime.now().isoformat(' ') + ")"
        [types.append(str(type(y)))  for x,y in values.iteritems()]
        try:
            with open(self.data_path  + '.dat', 'ab') as f:
                f.write(joiner.join(names)+ "\n")
                f.write(joiner.join(types)+ "\n")
                # f.write(struct.pack('<i', 245))
        except:
            pass

    def write_data(self,values):
        try:
            with open(self.data_path + '.dat', 'ab') as f:
                for val in values.itervalues():
                    self.write_binary(f,val)
        except:
            pass

    def write_binary(self, f, val):
        if type(val) is long:
            f.write(struct.pack('<l', val))
            #print struct.calcsize('<l')
        elif type(val) is int:
            f.write(struct.pack('<i', val))
            #print struct.calcsize('<i')
        elif type(val) is float:
            f.write(struct.pack('<f', val))
            #print struct.calcsize('<f')
        elif type(val) is bool:
            f.write(struct.pack('<?', val))
            #print struct.calcsize('<?')
        elif type(val) is numpy.float64:
            f.write(struct.pack('<f', val))
            #f.write(struct.pack('<?', val))
        elif type(val) is str:
            f.write(struct.pack('<i', -1))
        else:
            print(self.my_name + ' write_binary() error unknown type, ' + str(type(val)) )
        #print str(val) + '   ' + str(type(val))

    # noinspection PyMethodMayBeStatic
    def pickle_file(self, file_name, obj):
        path = self.working_directory + file_name
        self.pickle_dump(path,obj)

    # noinspection PyMethodMayBeStatic
    def pickle_dump(self, path, obj):
        self.message(self.my_name + ' pickle_dumping to ' + path,True)
        try:
            with open(path + '.pkl', 'wb') as f:
                pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        except:
            pass