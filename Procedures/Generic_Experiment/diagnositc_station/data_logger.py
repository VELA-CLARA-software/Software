from datetime import  datetime
import struct
from VELA_CLARA_enums import STATE
# from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
# from VELA_CLARA_RF_Protection_Control import RF_GUN_PROT_STATUS
# from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
import os
import pickle
import numpy


class Data_Logger(object):
    _my_name = 'data_logger'

    _log_start = datetime.now()
    _log_start_str = _log_start.isoformat('-').replace(":", "-").split('.',1)[0]

    _working_directory = None
    _log_file = None
    _log_path = None

    _slash = '\\'

    _working_dir_set = False
    _log_file_set = False

    def __init__(self):
        pass


    def start_log(self, work_dir, log_file):
        if self.set_working_directory(work_dir):
            self.set_log_file(log_file)
        return Data_Logger._log_file_set


    def set_working_directory(self,work_dir):
        if work_dir != '':
            # try and create a working directory path
            try:
                if work_dir[-1:] == Data_Logger._slash:
                    Data_Logger._working_directory = work_dir + Data_Logger._log_start_str
                else:
                    Data_Logger._working_directory = work_dir + Data_Logger._slash + \
                                            Data_Logger._working_directory
            except:
                self.message('Error setting working directory = ', work_dir)
            # try and create a new working directory
            else:
                try:
                    os.makedirs(Data_Logger._working_directory)
                    Data_Logger._working_dir_set = True
                except:
                    self.message('Error creating working directory = ',
                               Data_Logger._working_directory)
        return Data_Logger._working_dir_set

    def set_log_file(self, log_file):
        if Data_Logger._working_dir_set:
            Data_Logger._log_path = Data_Logger._working_directory + Data_Logger._slash + \
                                    log_file
            m = 'Created log_file = ' + Data_Logger._log_path
            try:
                self.write_log(m)
            except:
                print('FAILED TO CREATE LOG_FILE = ' +  Data_Logger._log_path)
            else:
                Data_Logger._log_file_set = True
                self.message(m)

    def message(self,text=[], add_to_log = False):
        if isinstance(text, basestring):
            s = text
        else:
            s = ' '.join( [str(x) for x in text] )
        print(s)
        if add_to_log and Data_Logger._log_file_set:
            self.write_log(s)

    def multi_line_message(self,text=[]):
        s = [str(x) for x in text]
        self.message( '\n'.join(s))

    def write_log(self, str):
        #write_str = datetime.now().isoformat('-').replace(":", "-").split('.', 1)[0] + ' ' + str + '\n'
        write_str = datetime.now().isoformat(' ') + ' ' + str + '\n'
        with open(Data_Logger._log_path,'a') as f:
            f.write(write_str)
