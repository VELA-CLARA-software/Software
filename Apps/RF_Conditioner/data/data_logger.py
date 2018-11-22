from datetime import  datetime
import struct
from VELA_CLARA_enums import STATE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from VELA_CLARA_RF_Protection_Control import RF_GUN_PROT_STATUS
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
import os
import pickle
from data.config_reader import config_reader
import numpy
import data.rf_condition_data_base as dat


class data_logger(object):
    my_name = 'data_logger'
    config = config_reader()
    _log_config = None

    log_start = datetime.now()
    log_start_str = log_start.isoformat('-').replace(":", "-").split('.', 1)[0]

    def __init__(self):
        self.pulse_count_log = None
        self.amp_power_log = None

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
        self.amp_pwr_path = self.working_directory + self.log_config[
            'AMP_POWER_LOG_FILENAME']  # MAGIC_STRING
        self.forward_file = self.working_directory + self._log_config['OUTSIDE_MASK_FORWARD_FILENAME']  #
        self.probe_file = self.working_directory + self._log_config['OUTSIDE_MASK_PROBE_FILENAME']  #
        self.reverse_file = self.working_directory + self._log_config['OUTSIDE_MASK_REVERSE_FILENAME']
        self.log_path = self.working_directory + self._log_config['LOG_FILENAME']
        self.header(self.my_name + ' log_config')
        self.message([
            'log_directory     = ' + self.log_directory,
            'working_directory = ' + self.working_directory,
            'data_path    = ' + self.data_path,
            'forward_file = ' + self.forward_file,
            'probe_file   = ' + self.probe_file,
            'reverse_file = ' + self.reverse_file,
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


    def add_to_pulse_breakdown_log(self,x):
        towrite = " ".join(map(str, x))
        self.message('Adding to pulse_breakdown_log: ' + towrite, True)
        with open(self.pulse_count_log,'a') as f:
            f.write( towrite + '\n')


    def add_to_KFP_Running_stat_log(self, x):
        towrite = " ".join(map(str, x))
        #self.message('Adding to Klystron Forward Power Running Stat Log: ' + towrite, True)
        with open(self.amp_power_log,'a') as f:
            f.write( towrite + '\n')

    def num(self, s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def get_amp_power_log(self):
        self.amp_power_log = data_logger.config.log_config['LOG_DIRECTORY']+ \
                               data_logger.config.log_config['AMP_POWER_LOG_FILENAME']
        r_dict ={}
        with open(self.amp_power_log) as f:
            lines = list(line for line in (l.strip() for l in f) if line)
            for line in lines:
                if '#' not in line:
                    log = [self.num(x) for x in line.split()]
                    r_dict[str(log[0])] = log[1:]
                    print 'get_amp_power_log ' + str(log[0])
                    print log[1:]


        self.header(self.my_name + ' get_amp_power_log')
        self.message('read get_amp_power_log: ' + self.amp_power_log)
        return r_dict


    def get_pulse_count_breakdown_log(self):
        self.pulse_count_log = data_logger.config.log_config['LOG_DIRECTORY']+ \
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
        return log

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
        names[names.index(dat.time_stamp)] =  dat.time_stamp +  ", (start = " + datetime.now().isoformat(' ') + ")"
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
        elif type(val) is RF_GUN_PROT_STATUS:
            f.write(struct.pack('<B', val))
            #print struct.calcsize('<B')
        elif type(val) is STATE:
            f.write(struct.pack('<B', val))
            #print struct.calcsize('<B')
        elif type(val) is GUN_MOD_STATE:
            f.write(struct.pack('<B', val))
            #print struct.calcsize('<B')
        elif type(val) is VALVE_STATE:
            f.write(struct.pack('<B', val))
            #print struct.calcsize('<B')
        elif type(val) is bool:
            f.write(struct.pack('<?', val))
            #print struct.calcsize('<?')
        elif type(val) is numpy.float64:
            f.write(struct.pack('<f', val))
            #f.write(struct.pack('<?', val))
        elif type(val) is str:
            f.write(struct.pack('<i', -1))
        elif type(val) is state:
            f.write(struct.pack('<B', val))
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