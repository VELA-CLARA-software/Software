from datetime import  datetime
import struct
from VELA_CLARA_enums import STATE
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from VELA_CLARA_RF_Protection_Control import RF_GUN_PROT_STATUS
import os
import pickle
from data.config_reader import config_reader


class data_logger(object):
    my_name = 'data_logger'
    config = config_reader()
    _log_config = None

    log_start = datetime.now()
    log_start_str = log_start.isoformat('-').replace(":", "-").split('.', 1)[0]

    def __init__(self):
        log_param = data_logger.config.log_config

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
        self.forward_file = self.working_directory + self._log_config['OUTSIDE_MASK_FORWARD_FILENAME']  #
        self.probe_file = self.working_directory + self._log_config['OUTSIDE_MASK_PROBE_FILENAME']  #
        self.reverse_file = self.working_directory + self._log_config['OUTSIDE_MASK_REVERSE_FILENAME']
        #


    def get_pulse_count_breakdown_log(self):
        self.pulse_count_log = data_logger.config.log_config['LOG_DIRECTORY']+ \
                               data_logger.config.log_config['PULSE_COUNT_BREAKDOWN_LOG_FILENAME']
        log = []
        with open(self.pulse_count_log) as f:
            for line in f:
                if '#' not in line:
                    log.append([int(x) for x in line.split()])
        print('*')
        print('*** ' + self.my_name + ' read pulse_count_log: ' + self.pulse_count_log + '***')
        for i in log:
            print i
        log.append(log[-1])
        return log

    def start_data_logging(self):
        print('*')
        print('*** start_data_logging****')
        print(self.my_name + ', data_path = ' + self.data_path)
        print(self.my_name + ' starting monitoring, update time = ' + str(self.log_config['DATA_LOG_TIME']))#MAGIC_STRING
        return self.log_start


    def write_data_log_header(self,values):
        print(self.my_name + ' writing data_log header to ' + self.data_path)
        joiner = '\t'
        names = []
        types = []
        [names.append(x) for x,y in values.iteritems()]
        [types.append(str(type(y)))  for x,y in values.iteritems()]
        with open(self.data_path  + '.dat', 'ab') as f:
            f.write(joiner.join(names)+ "\n")
            f.write(joiner.join(types)+ "\n")
            # f.write(struct.pack('<i', 245))

    def write_data(self,values):
        with open(self.data_path + '.dat', 'ab') as f:
            for val in values.itervalues():
                self.write_binary(f,val)

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
    def pickle_dump(self, path, obj):
        print(self.my_name + ' pickle_dumping to ' + path)
        with open(path + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)