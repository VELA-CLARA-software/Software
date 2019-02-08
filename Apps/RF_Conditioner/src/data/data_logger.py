from datetime import  datetime
import struct
#from VELA_CLARA_enums import STATE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from VELA_CLARA_RF_Protection_Control import RF_GUN_PROT_STATUS
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
from VELA_CLARA_LLRF_Control import TRIG
from VELA_CLARA_LLRF_Control import INTERLOCK_STATE
from src.data.state import state
import os
import cPickle as pkl
from src.data.config_reader import config_reader
import numpy
import src.data.rf_condition_data_base as dat
import wolframclient.serializers as wxf
from src.data.state import state

class data_logger(object):
    my_name = 'data_logger'
    config = config_reader()
    _log_config = None

    log_start = datetime.now()
    log_start_str = log_start.isoformat('-').replace(":", "-").split('.', 1)[0]

    def __init__(self):
        self.pulse_count_log = None
        self.amp_power_log = None
        # these are file objecs that we write th edata to, we're going to keep them open all the time ?!?
        self.log_file = None
        self.pulse_count_log_file = None
        self.amp_power_log_file = None
        self.data_log_file = None

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
        # open log_file and LEAVE OPEN
        self.log_file = open(self.log_path, 'a')

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
        #print('write_log')
        write_str = datetime.now().isoformat(' ') + ' ' + str + '\n'
        self.log_file.write(write_str)
        self.log_file.flush()
        # previously opened and closed files as we went ...
        # with open(self.log_path,'a') as f:
        #     f.write(write_str)

    def add_to_pulse_breakdown_log(self,x):
        #print('add_to_pulse_breakdown_log')
        towrite = " ".join(map(str, x))
        self.pulse_count_log_file.write( towrite + '\n')
        self.pulse_count_log_file.flush()
        #previously opened and closed files as we went ...
        # with open(self.pulse_count_log,'a') as f:
        #     f.write( towrite + '\n')

    def add_to_KFP_Running_stat_log(self, x):
        # WRITE TO amp_power_log but don't write an amp with zero pulses of data in it 
        if x[1] != 0:
            #towrite = " ".join(map(str, x))
            #self.message('Adding to Klystron Forward Power Running Stat Log: ' + towrite, True)
            #print('add_to_KFP_Running_stat_log, ', self.amp_power_log_file,' '.join(map(str, x)))
            self.amp_power_log_file.write( ' '.join(map(str, x)) + '\n')
            self.amp_power_log_file.flush()
            # previously opened and closed files as we went ...
            # with open(self.amp_power_log,'a') as f:
            #     f.write( towrite + '\n')

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
                    r_dict[log[0]] = log[1:]
                    #print 'get_amp_power_log ' + str(log[0])
                    #print log[1:]
        #
        # now open amp_power_log file for appending and LEAVE OPEN
        self.amp_power_log_file = open(self.amp_power_log, 'a')
        #
        self.header(self.my_name + ' get_amp_power_log', True)
        self.message('read get_amp_power_log: ' + self.amp_power_log, True)
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
        #
        ## now open pulse_count_log file for appending and LEAVE OPEN
        self.pulse_count_log_file = open(self.pulse_count_log, 'a')
        return log

    def start_data_logging(self):
        self.header(self.my_name + ' start_data_logging')
        self.message(['data_log path = ' + self.data_path,' starting monitoring, update time = ' +
                      str(self.log_config['DATA_LOG_TIME'])])
        self.message(['AMP_POWER_LOG  path = ' + self.amp_pwr_path,' starting monitoring, update time = ' +
                      str(self.log_config['AMP_PWR_LOG_TIME'])])

    def write_data_log_header(self,values):
        print(self.my_name + ' writing data_log header to ' + self.data_path)

        joiner = '\t'
        names = []
        types = []

        counter  = 0
        name_index = 0

        for key, value in values.iteritems():
            print key
            print str(type(value))
            names.append(key)
            types.append(str(type(value)))
            if key == dat.time_stamp:
                print('name index = ',counter)
                name_index = counter
            counter += 1



        #[names.append(x) for x,y in values.iteritems()]
        names[name_index] =  dat.time_stamp +  ", (start = " + datetime.now().isoformat(' ') + ")"
        #names[names.index(dat.time_stamp)] =  dat.time_stamp +  ", (start = " + datetime.now().isoformat(' ') + ")"
        #[types.append(str(type(y)))  for x,y in values.iteritems()]
        #
        # create the data_log file and write the plaintext header


        #print joiner.join(names)
        #print joiner.join(types)


        try:
            with open(self.data_path  + '.dat', 'ab') as f:
                f.write(joiner.join(names)+ "\n")
                f.write(joiner.join(types)+ "\n")
                # f.write(struct.pack('<i', 245))
        except Exception as e:
            print(e)
            print(self.my_name + ' MAJOR ERROR CAN NOT CREATE data_log.dat, FILE = ' + self.data_path)
            raw_input()
        #
        # now try and open the file and leave open for appending data to
        try:
            self.data_path_file = open(self.data_path  + '.dat','ab')
            print( 'data_path_file set correctly ', self.data_path_file )
        except Exception as e:
            print(e)
            print(self.my_name + ' MAJOR ERROR CAN NOT OPEN LOG FILES: ' + self.data_path)
            raw_input()

    def write_data(self,values):
        #print('write_data')
        for val in values.itervalues():
            self.write_binary( self.data_path_file, val)
        self.data_path_file.flush()
        # try:
        #     with open(self.data_path + '.dat', 'ab') as f:
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
        elif type(val) is RF_GUN_PROT_STATUS:
            f.write(struct.pack('<B', val))
            #print struct.calcsize('<B')
        elif type(val) is GUN_MOD_STATE:
            f.write(struct.pack('<B', val))
            #print struct.calcsize('<B')
        elif type(val) is VALVE_STATE:
            f.write(struct.pack('<B', val))
            #print struct.calcsize('<B')
        elif type(val) is TRIG:
            f.write(struct.pack('<B', val))
            #print struct.calcsize('<B')
        elif type(val) is INTERLOCK_STATE:
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
        self.message(self.my_name + ' pickle_dumping to ' + path, True)
        try:
            with open(path + '.pkl', 'wb') as f:
                pkl.dump(obj, f, pkl.HIGHEST_PROTOCOL)
        except Exception as e:
            print(e)
            self.message(self.my_name + ' EXCEPTION ' + str(e), True)
            self.message(self.my_name + ' ERROR pickle_dumping to ' + path, True)

    # don't bother with this, convert to wxf offline
    # def pkl2wxf(self,path):
    #     file = open(path, 'rb')
    #     objs = []
    #     while True:
    #         try:
    #             objs.append(pkl.load(file))
    #         except EOFError:
    #             break
    #     file.close()
    #     # print(objs)
    #     path2 = path.replace(".pkl", "")
    #     wxf.export(objs, path2 + '.wxf', target_format='wxf')
    #
