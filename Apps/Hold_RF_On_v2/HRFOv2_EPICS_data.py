from dataclasses import dataclass
import numpy as np, cmath, math
from decimal import Decimal, getcontext
import re, sys, os
from HRFOv2_EPICS_figures import figures
from HRFOv2_EPICS_reader import reader


# set number of decimal places for Decimal to use....
getcontext().prec = 20

# @dataclass
# class C2_data:
#     # #def __init__(self, title, author, pages, price):
#     # title : str
#     # author : str
#     # pages : int
#     # price : float
#     Interpolated_datapath: str
#     Master_Dict_path: str
#     savepath: str
#     NBIN: int
#     Results_Power: list

class bcolors:
    '''
    Provides colours for print outs for ease of reading if required
    '''
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class data_functions():
    '''
    handles all operations on data
    '''
    def __init__(self):
        print('Initiated data_functions()')

    def remove_char_from_str(self, string_1):
        '''
        Removes characters in '[!@#$:]' form string and returns ammended string
        :param string_1:
        :return:
        '''
        self.string_1 = string_1

        self.string_2 = re.sub('[!@#$:]', '', self.string_1)

        return self.string_2

    def replace_char_from_str(self, string_1, old_char, new_char):
        '''
        Removes characters in '[!@#$:]' form string and returns ammended string
        :param string_1:
        :return:
        '''
        self.string_1 = string_1
        self.old_char = old_char
        self.new_char = new_char

        self.string_2 = re.sub(self.old_char, self.new_char, self.string_1)

        return self.string_2


    def create_folder_name(self):
        '''

        :return:
        '''
        df = data_functions

        self.date_from = values[date_from]
        self.time_from = values[time_from]
        self.date_to = values[date_to]
        self.time_to = values[time_to]

        self.folder_name = self.concatenate_date_time_to_folder_format(self.date_from,
                                                                     self.time_from,
                                                                     self.date_to,
                                                                     self.time_to)

        return self.folder_name
    
    def concatenate_date_time_to_folder_format(self, folder_date_from, folder_time_from, folder_date_to, folder_time_to):
        '''
        Takes the inputs from the config yaml and returns a string in the format that the save folder requires
        :param date: String in the format "YYYY-MM-DD"
        :param time: String in the format "HH:MM:SS.SS"
        :return: Formatted string "YYYY-MM-DD_HH:MM:SS_to_YYYY-MM-DD_HH:MM:SS"
        '''
        self.date_from = folder_date_from
        self.time_from = folder_time_from
        self.date_to = folder_date_to
        self.time_to = folder_time_to

        self.time_from_formatted = self.replace_char_from_str(self.time_from, ':', '-')[0:-3]
        self.time_to_formatted = self.replace_char_from_str(self.time_to, ':', '-')[0:-3]
        print(f'time_from_formatted = {self.time_from_formatted[0:-3]}')
        #input()
        self.formatted_string = f'{self.date_from}_{self.time_from_formatted}_to_{self.date_to}_{self.time_to_formatted}'

        return self.formatted_string


    def find_pv_name_from_pv_index(self, pv_name):
        '''
        returns the PVs index from the name by looking in the "PV_idx_dict" dictionary.
        :param pv_name: String, eg "CLA-GUNS-HRF-MOD-01:Sys:StateRead".
        :return:
        '''
        self.pv_name = pv_name
        self.pv_idx_dict = values[pv_idx_dict]
        self.pv_idx = self.pv_idx_dict[self.pv_name]

        return self.pv_idx


    def find_pv_index_from_pv_name(self, pv_idx):
        '''
        returns the PVs name from the index by looking in the "idx_pv_dict" dictionary.
        :param pv_name: String, eg "12". The function forces it to be a string if we forget and enter an integer or float
        :return:
        '''
        self.pv_idx = str(int(pv_idx))
        self.idx_pv_dict = values[idx_pv_dict]
        self.pv_name = self.idx_pv_dict[self.pv_idx]

        return self.pv_name


    def scan_data_for_delta_time_groups(self):
        '''
        Initial function that scans the time data of the Mod state read PV ("CLA-GUNS-HRF-MOD-01:Sys:StateRead")
        and finds groups of events.
        :return:
        '''
        figs = figures()
        read = reader()
        self.mod_StateRead_time = values[mod_StateRead_time]
        self.mod_StateRead_yaxis = values[mod_StateRead_yaxis]
        self.mod_group_time_spacing = values[mod_group_time_spacing]
        self.mod_state_dict = values[mod_state_dict]

        self.mod_StateRead_time = [float(i) for i in self.mod_StateRead_time]
        self.mod_StateRead_yaxis = [float(i) for i in self.mod_StateRead_yaxis]

        self.mod_StateRead_groups_idxs = []
        self.mod_StateRead_groups_time_vals = []
        self.mod_StateRead_groups_yaxis_vals = []

        self.local_group_idx = []
        self.local_group_time_val = []
        self.local_group_yaxis_val = []

        self.mod_StateRead_groups_delta_time = []
        self.mod_StateRead_string_states = []

        self.local_group_start_idx = 0
        for idx, time_val in enumerate(self.mod_StateRead_time[0:-1]):
            self.delta_time = self.mod_StateRead_time[idx+1] - time_val
            self.mod_StateRead_groups_delta_time.append(self.delta_time)
            #print(f'self.delta_time = {self.delta_time}')
            if self.delta_time <= self.mod_group_time_spacing:
                self.local_group_idx.append(idx)
                self.local_group_time_val.append(time_val)
                self.local_group_yaxis_val.append(int(self.mod_StateRead_yaxis[idx]))
                #print(f'delta_time = {self.delta_time}\n')
                #       f'mod_group_time_spacing = {self.mod_group_time_spacing}')
                # print(f'len(local_group_idx) = {len(self.local_group_idx)}')
            else:
                self.local_group_idx.append(idx)
                self.local_group_time_val.append(time_val)
                self.local_group_yaxis_val.append(int(self.mod_StateRead_yaxis[idx]))

                self.mod_StateRead_groups_idxs.append(self.local_group_idx)
                self.mod_StateRead_groups_time_vals.append(self.local_group_time_val)
                self.mod_StateRead_groups_yaxis_vals.append(self.local_group_yaxis_val)

                self.local_group_idx = []
                self.local_group_time_val = []
                self.local_group_yaxis_val = []

                self.local_group_start_idx = self.mod_StateRead_time[idx + 1]

                #print(f'*** delta_time = {self.delta_time}\n')
                #       f'*** mod_group_time_spacing = {self.mod_group_time_spacing}')
                # print(f'*** len(local_group_idx) = {len(self.local_group_idx)}')

        # append the last values on to lists as the loop missed them out

        self.mod_StateRead_groups_idxs.append([int(len(mod_StateRead_time))])
        self.mod_StateRead_groups_time_vals.append([self.mod_StateRead_time[-1]])
        self.mod_StateRead_groups_yaxis_vals.append([int(self.mod_StateRead_yaxis[-1])])



        figs.histogram(self.mod_StateRead_groups_delta_time, 'groups_delta_time', 120.0)

        self.mod_StateRead_groups_length = [len(i) for i in self.mod_StateRead_groups_idxs]



        values[mod_StateRead_groups_length] = self.mod_StateRead_groups_length
        values[mod_StateRead_groups_idxs] = self.mod_StateRead_groups_idxs
        values[mod_StateRead_groups_time_vals] = self.mod_StateRead_groups_time_vals
        values[mod_StateRead_groups_yaxis_vals] = self.mod_StateRead_groups_yaxis_vals

        print(f'self.mod_StateRead_groups_length = {self.mod_StateRead_groups_length}\n'
              f'len(self.mod_StateRead_time) = {len(self.mod_StateRead_time)}\n'
              f'len(self.mod_StateRead_groups_idxs) = {len(self.mod_StateRead_groups_idxs)}\n'
              f'self.mod_StateRead_groups_idxs = {self.mod_StateRead_groups_idxs}')

        for g in self.mod_StateRead_groups_yaxis_vals:
            print(f'\ng = {g}')
            for s in g:
                #print(f's = {s}')
                string_state = self.mod_state_dict[str(s)]
                self.mod_StateRead_string_states.append(string_state)

                print(string_state)


        read.save_two_lists_csv(self.mod_StateRead_string_states[0:-1], self.mod_StateRead_groups_delta_time, r'\Mod_States_Delta_Time')

        values[mod_StateRead_string_states] = self.mod_StateRead_string_states

        # find unique groups and the number of each that there are
        self.unique_groups_delta_time, self.unique_groups_population_delta_time \
            = self.find_unique_groups(self.mod_StateRead_groups_yaxis_vals)

        # Save to csv for ease of comparison
        read.save_two_lists_csv(self.unique_groups_delta_time,
                                self.unique_groups_population_delta_time,
                                r'\unique_groups_population_delta_time')


    def scan_data_for_standby_groups(self):
        '''
        Initial function that reads the Mod state read PV ("CLA-GUNS-HRF-MOD-01:Sys:StateRead")
        and finds groups of events each group starts with a standby state.
        Standby state == 6 in the yaxis data (values[mod_StateRead_yaxis)
        :return:
        '''
        figs = figures()
        read = reader()
        self.mod_StateRead_time = values[mod_StateRead_time]
        self.mod_StateRead_yaxis = values[mod_StateRead_yaxis]
        self.mod_state_dict = values[mod_state_dict]

        self.mod_StateRead_time = [float(i) for i in self.mod_StateRead_time]
        self.mod_StateRead_yaxis = [int(i) for i in self.mod_StateRead_yaxis]

        self.mod_StateRead_groups_standby_idxs = []
        self.mod_StateRead_groups_standby_time_vals = []
        self.mod_StateRead_groups_standby_yaxis_vals = []

        self.local_group_idx = []
        self.local_group_time = []
        self.local_group_yaxis = []
        for idx, yval in enumerate(self.mod_StateRead_yaxis):
            if yval == 6:

                self.mod_StateRead_groups_standby_idxs.append(self.local_group_idx)
                self.mod_StateRead_groups_standby_time_vals.append(self.local_group_time)
                self.mod_StateRead_groups_standby_yaxis_vals.append(self.local_group_yaxis)

                self.local_group_idx = []
                self.local_group_time = []
                self.local_group_yaxis = []

                self.local_group_idx.append(idx)
                self.local_group_time.append(self.mod_StateRead_time[idx])
                self.local_group_yaxis.append(yval)

            else:
                self.local_group_idx.append(idx)
                self.local_group_time.append(self.mod_StateRead_time[idx])
                self.local_group_yaxis.append(yval)

        for g in self.mod_StateRead_groups_standby_yaxis_vals:

            print(f'\ng = {g}')
            for s in g:
                # print(f's = {s}')
                string_state = self.mod_state_dict[str(s)]
                #self.mod_StateRead_string_states.append(string_state)

                print(string_state)

        values[mod_StateRead_groups_standby_idxs] = self.mod_StateRead_groups_standby_idxs
        values[mod_StateRead_groups_standby_time_vals] = self.mod_StateRead_groups_standby_time_vals
        values[mod_StateRead_groups_standby_yaxis_vals] = self.mod_StateRead_groups_standby_yaxis_vals

        # find unique groups and the number of each that there are
        self.unique_groups_standby, self.unique_groups_population_standby \
            = self.find_unique_groups(self.mod_StateRead_groups_standby_yaxis_vals)

        # Save to csv for ease of comparison
        read.save_two_lists_csv(self.unique_groups_standby,
                                self.unique_groups_population_standby,
                                r'\unique_groups_population_standby')

        # TODO: save groups as csv for comparison

    def find_unique_groups(self, yaxis_vals):
        '''
        Finds unique groups and also determines the number of each type.
        :param yaxis_vals: list of lists containing mod states as integers from 1--> 13 inclusive.
        :return: unique_groups, unique_groups_population
        '''
        self.yaxis_vals = yaxis_vals

        self.unique_groups = []
        for gr in self.yaxis_vals:
            if gr in self.unique_groups:
                pass
            else:
                self.unique_groups.append(gr)

        self.unique_groups_population = [0]*len(self.unique_groups)
        for gr in self.yaxis_vals:
            for un_gr_idx, un_gr in enumerate(self.unique_groups):
                if gr == un_gr:
                    self.unique_groups_population[un_gr_idx]+= 1
                else:
                    pass
        print('\n\n')
        print(f'unique_groups = {self.unique_groups}\n'
              f'unique_groups_population = {self.unique_groups_population}')

        return self.unique_groups, self.unique_groups_population






    '''
    interesting group from the delta time method.
    it looks like an operator spamming the mod with HV request..... could have been me!
    
    g = [4]
    HV Interlock
    
    g = [6, 4, 6, 9, 4, 6, 9, 4, 6, 9, 4, 6, 9, 10, 12, 13]
    Standby
    HV Interlock
    Standby
    HV Request
    HV Interlock
    Standby
    HV Request
    HV Interlock
    Standby
    HV Request
    HV Interlock
    Standby
    HV Request
    HV On
    Trig Request
    Trig
    
    g = [4]
    HV Interlock
    '''









# Values dictionary:

values = {}  # Initiated empty dictionary
all_value_keys = []  # A list of the keys for values
Dummy_int = int(-999999)
Dummy_float = float(-999.999)
Dummy_decimal = Decimal(-999.999)


savepath = 'savepath'
all_value_keys.append(savepath)
values[savepath] = 'Dummy str'

date_from = 'date_from'
all_value_keys.append(date_from)
values[date_from] = 'Dummy str'

time_from = 'time_from'
all_value_keys.append(time_from)
values[time_from] = 'Dummy str'

date_to= 'date_to'
all_value_keys.append(date_to)
values[date_to] = 'Dummy str'

time_to= 'time_to'
all_value_keys.append(time_to)
values[time_to] = 'Dummy str'

all_mod_PVs = 'all_mod_PVs'
all_value_keys.append(all_mod_PVs)
values[all_mod_PVs] = []

interlock_PVs = 'interlock_PVs'
all_value_keys.append(interlock_PVs)
values[interlock_PVs] = []

PLOT_ALL_PVs = 'PLOT_ALL_PVs'
all_value_keys.append(PLOT_ALL_PVs)
values[PLOT_ALL_PVs] = False

mod_group_time_spacing = 'mod_group_time_spacing'
all_value_keys.append(mod_group_time_spacing)
values[mod_group_time_spacing] = Dummy_float

folder_name = 'folder_name'
all_value_keys.append(folder_name)
values[folder_name] = 'Dummy str'

# if you want the index of a PV and have the name
# pv_idx = PV_idx_dict[pv_name]
pv_idx_dict = 'pv_idx_dict'
all_value_keys.append(pv_idx_dict)
values[pv_idx_dict] = {}

# if you want the name of a PV and have the index
# pv_name = PV_idx_dict[pv_idx]
idx_pv_dict = 'idx_pv_dict'
all_value_keys.append(idx_pv_dict)
values[idx_pv_dict] = {}

PV_TIME_DATA = 'PV_TIME_DATA'
all_value_keys.append(PV_TIME_DATA)
values[PV_TIME_DATA] = []

PV_YAXIS_DATA = 'PV_YAXIS_DATA'
all_value_keys.append(PV_YAXIS_DATA)
values[PV_YAXIS_DATA] = []

READ_PVs = 'READ_PVs'
all_value_keys.append(READ_PVs)
values[READ_PVs] = True

EPICS_date_time_from = "EPICS_date_time_from"
all_value_keys.append(EPICS_date_time_from)
values[EPICS_date_time_from] = 'Dummy str'

EPICS_date_time_to = "EPICS_date_time_to"
all_value_keys.append(EPICS_date_time_to)
values[EPICS_date_time_to] = 'Dummy str'

mod_StateRead_time = 'mod_StateRead_time'
all_value_keys.append(mod_StateRead_time)
values[mod_StateRead_time] = []

mod_StateRead_yaxis = 'mod_StateRead_yaxis'
all_value_keys.append(mod_StateRead_yaxis)
values[mod_StateRead_yaxis] = []

mod_StateRead_groups_length = 'mod_StateRead_groups_length'
all_value_keys.append(mod_StateRead_groups_length)
values[mod_StateRead_groups_length] = []

mod_StateRead_groups_idxs = 'mod_StateRead_groups_idxs'
all_value_keys.append(mod_StateRead_groups_idxs)
values[mod_StateRead_groups_idxs] = []

mod_StateRead_groups_time_vals = 'mod_StateRead_groups_time_vals'
all_value_keys.append(mod_StateRead_groups_time_vals)
values[mod_StateRead_groups_time_vals] = []

mod_StateRead_groups_yaxis_vals = 'mod_StateRead_groups_yaxis_vals'
all_value_keys.append(mod_StateRead_groups_yaxis_vals)
values[mod_StateRead_groups_yaxis_vals] = []

mod_StateRead_groups_delta_time = 'mod_StateRead_groups_delta_time'
all_value_keys.append((mod_StateRead_groups_delta_time))
values[mod_StateRead_groups_delta_time] = []

mod_StateRead_groups_states = 'mod_StateRead_groups_states'
all_value_keys.append(mod_StateRead_groups_states)
values[mod_StateRead_groups_states] = []

mod_state_dict = 'mod_state_dict'
all_value_keys.append(mod_state_dict)
values[mod_state_dict] = {  '0': "Init/not connected",
                    '1': "Standby Interlock",
                    '2': "OFF",
                    '3': "Off Request",
                    '4': "HV Interlock",
                    '5': "Standby Request",
                    '6': "Standby",
                    '7': "HV Off Request",
                    '8': "Trigger Interlock",
                    '9': "HV Request",
                    '10': "HV On",
                    '11': "Trig Off Request",
                    '12': "Trig Request",
                    '13': "Trig"}

mod_StateRead_string_states = 'mod_StateRead_string_states'
all_value_keys.append(mod_StateRead_string_states)
values[mod_StateRead_string_states] = []

mod_StateRead_groups_standby_idxs = 'mod_StateRead_groups_standby_idxs'
all_value_keys.append(mod_StateRead_groups_standby_idxs)
values[mod_StateRead_groups_standby_idxs] = []

mod_StateRead_groups_standby_time_vals = 'mod_StateRead_groups_standby_time_vals'
all_value_keys.append(mod_StateRead_groups_standby_time_vals)
values[mod_StateRead_groups_standby_time_vals] = []

mod_StateRead_groups_standby_yaxis_vals = 'mod_StateRead_groups_standby_yaxis_vals'
all_value_keys.append(mod_StateRead_groups_standby_yaxis_vals)
values[mod_StateRead_groups_standby_yaxis_vals] = []





