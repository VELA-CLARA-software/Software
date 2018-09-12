from datetime import datetime
import struct
import os
import pickle
from data.config_reader import config_reader
import numpy
import data.blm_plotter_data_base as dat
import yaml,json


class data_logger(object):
    my_name = 'data_logger'
    config = config_reader()
    _log_config = None
    _bpm_name = None
    _scan_type = None

    log_start = datetime.now()
    log_start_str = log_start.isoformat('-').replace(":", "-").split('.', 1)[0]
    bpm_name = "dummy"
    scan_type = "dummy"

    def __init__(self):
        self.log_directory = self.getdirectory()
        self.working_directory = self.log_directory
        # self.data_path = self.working_directory + 'data_log'  # MAGIC_STRING
        self.log_path = self.working_directory + 'blmlog.txt'

    @property
    def log_config(self):
        return data_logger._log_config

    @log_config.setter
    def log_config(self,value):
        data_logger._log_config = value
        self.log_directory = self.getdirectory()
        self.working_directory = self.log_directory
        # self.data_path = self.working_directory + 'data_log'  # MAGIC_STRING
        self.log_path = self.working_directory + 'log.txt'
        self.header(self.my_name + ' log_config')
        # self.message([
        #     'log_directory     = ' + self.log_directory,
        #     'working_directory = ' + self.working_directory,
        #     'data_path    = ' + self.data_path,
        #     'log_path     = ' + self.log_path
        # ])

    def getdirectory(self):
        self.now = datetime.now()
        self.year = str(self.now.year)
        self.month = str(self.now.month)
        self.day = str(self.now.day)
        if len(self.month) == 1:
            self.month = "0" + self.month
        if len(self.day) == 1:
            self.day = "0" + self.day
        self.directory = "\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\" + self.year + "\\" + self.month + "\\" + self.day + "\\"
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)
        # data_logger.config.log_config['LOG_DIRECTORY'] = self.directory
        return self.directory

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

    def add_to_blm_scan_log(self,x):
        towrite = " ".join(map(str, x))
        self.message('Adding to bpm scan log =  ' + towrite, True)
        with open(self.blm_scan_log,'a') as f:
            f.write( towrite + '\n')

    def add_to_blm_scan_yaml(self,d):
        with open(self.blm_scan_log, 'w') as outfile:
            yaml.dump(d, outfile, default_flow_style=False)

    def add_to_blm_scan_json(self,d):
        with open(self.blm_scan_log, 'a') as outfile:
            outfile.write(json.dumps(d, indent=4, sort_keys=True))
            outfile.write('\n')

    def get_blm_scan_log(self):
        self.scan_log_start = datetime.now()
        self.scan_log_start_str = self.scan_log_start.isoformat('-').replace(":", "-").split('.', 1)[0]
        self.scan_directory = self.log_directory + self.blm_name + '\\' + self.scan_type
        if not os.path.isdir(self.blm_directory):
            os.makedirs(self.blm_directory)
        if not os.path.isdir(self.scan_directory):
            os.makedirs(self.scan_directory)
        self.blm_scan_log = self.scan_directory + '\\' + self.scan_log_start_str + ".json"
        log = []
        with open(self.blm_scan_log,"w+") as f:
            lines = list(line for line in (l.strip() for l in f) if line)
            for line in lines:
                if '#' not in line:
                    log.append([int(x) for x in line.split()])
        self.header(self.my_name + ' get_blm_scan_log')
        self.message('read blm_scan_log: ' + self.blm_scan_log)
        for i in log:
            self.message(map(str,i),True)
        return 1

    def start_data_logging(self):
        self.header(self.my_name + ' start_data_logging')
        # self.message([
        #     'data_path     = ' + self.data_path,
        #     'starting monitoring, update time = ' + str(self.log_config['DATA_LOG_TIME'])
        # ])

    def write_data_log_header(self,values):
        print(self.my_name + ' writing data_log header to ' + self.log_path)
        joiner = '\t'
        names = []
        types = []
        [names.append(x) for x,y in values.iteritems()]
        # names[names.index(dat.time_stamp)] =  dat.time_stamp +  ", (start = " + datetime.now().isoformat(' ') + ")"
        [types.append(str(type(y)))  for x,y in values.iteritems()]
        try:
            with open(self.log_path  + '.dat', 'ab') as f:
                f.write(joiner.join(names)+ "\n")
                f.write(joiner.join(types)+ "\n")
                # f.write(struct.pack('<i', 245))
        except:
            pass

    def write_data(self,values):
        pass
        # try:
        #     with open(self.log_path + '.dat', 'ab') as f:
        #         for val in values.itervalues():
        #             self.write_binary(f,val)
        # except:
        #     pass

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
        # elif type(val) is RF_GUN_PROT_STATUS:
        #     f.write(struct.pack('<B', val))
            #print struct.calcsize('<B')
        # elif type(val) is STATE:
        #     f.write(struct.pack('<B', val))
        #     #print struct.calcsize('<B')
        # elif type(val) is GUN_MOD_STATE:
        #     f.write(struct.pack('<B', val))
        #     #print struct.calcsize('<B')
        # elif type(val) is VALVE_STATE:
        #     f.write(struct.pack('<B', val))
        #     #print struct.calcsize('<B')
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


    def dump_forward(self, obj, index):
        self.pickle_dump(path=self.forward_file + str(index), obj=obj)

    def dump_reverse(self, obj, index):
        self.pickle_dump(path=self.reverse_file + str(index), obj=obj)

    def dump_probe(self, obj, index):
        self.pickle_dump(path=self.probe_file + str(index), obj=obj)

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