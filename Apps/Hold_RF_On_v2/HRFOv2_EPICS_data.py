from dataclasses import dataclass
import numpy as np, cmath, math
from decimal import Decimal, getcontext
import re, sys, os, pandas as pd, requests
from HRFOv2_EPICS_figures import figures
from HRFOv2_EPICS_reader import reader
from HRFOv2_EPICS_utils import utilities


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



        figs.histogram(self.mod_StateRead_groups_delta_time, 'groups_delta_time', 50.0)

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
            #print(f'\ng = {g}')
            for s in g:
                #print(f's = {s}')
                string_state = self.mod_state_dict[str(s)]
                self.mod_StateRead_string_states.append(string_state)

                #print(string_state)


        read.save_two_lists_csv(self.mod_StateRead_string_states[0:-1], self.mod_StateRead_groups_delta_time, r'\Mod_States_Delta_Time')

        values[mod_StateRead_string_states] = self.mod_StateRead_string_states

        # find unique groups and the number of each that there are
        self.unique_groups_delta_time, self.unique_group_member_indices_delta_time, self.unique_group_start_times_delta_time, self.unique_group_end_times_delta_time, self.unique_groups_population_delta_time \
            = self.find_unique_groups(self.mod_StateRead_groups_time_vals, self.mod_StateRead_groups_yaxis_vals, self.mod_StateRead_groups_idxs)

        # Save to csv for ease of comparison
        read.save_mod_state_names_and_populations_to_csv(self.unique_groups_delta_time,
                                self.unique_groups_population_delta_time,
                                r'\unique_groups_population_delta_time')

        values[unique_groups_delta_time] = self.unique_groups_delta_time

        values[unique_group_start_times_delta_time] = self.unique_group_start_times_delta_time
        values[unique_group_member_indices_delta_time] = self.unique_group_member_indices_delta_time
        values[unique_group_end_times_delta_time] = self.unique_group_end_times_delta_time
        values[unique_groups_population_delta_time] = self.unique_groups_population_delta_time


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

            #print(f'\ng = {g}')
            for s in g:
                # print(f's = {s}')
                string_state = self.mod_state_dict[str(s)]
                #self.mod_StateRead_string_states.append(string_state)

                #print(string_state)

        values[mod_StateRead_groups_standby_idxs] = self.mod_StateRead_groups_standby_idxs
        values[mod_StateRead_groups_standby_time_vals] = self.mod_StateRead_groups_standby_time_vals
        values[mod_StateRead_groups_standby_yaxis_vals] = self.mod_StateRead_groups_standby_yaxis_vals

        # find unique groups and the number of each that there are
        self.unique_groups_standby, self.unique_group_member_indices_standby, self.unique_group_start_times_standby, self.unique_group_end_times_standby, self.unique_groups_population_standby \
            = self.find_unique_groups(self.mod_StateRead_groups_standby_time_vals,
                                      self.mod_StateRead_groups_standby_yaxis_vals, self.mod_StateRead_groups_standby_idxs)

        print(f'self.unique_group_member_indices_standby = {self.unique_group_member_indices_standby}')

        # Save to csv for ease of comparison
        read.save_mod_state_names_and_populations_to_csv(self.unique_groups_standby,
                                self.unique_groups_population_standby,
                                r'\unique_groups_population_standby')

        values[unique_groups_standby] = self.unique_groups_standby
        values[unique_group_member_indices_standby] = self.unique_group_member_indices_standby
        values[unique_group_start_times_standby] = self.unique_group_start_times_standby
        values[unique_group_end_times_standby] = self.unique_group_end_times_standby
        values[unique_groups_population_standby] = self.unique_groups_population_standby

        # TODO: save groups as csv for comparison

    def find_unique_groups(self, xaxis_vals, yaxis_vals, group_idxs):
        '''
        Finds unique groups and also determines the number of each type.
        :param yaxis_vals: list of lists containing mod states as integers from 1--> 13 inclusive.
        :param xaxis_vals:
        :param yaxis_vals:
        :param group_idxs:
        :return: unique_groups, unique_groups_population
        '''

        self.xaxis_vals = xaxis_vals
        self.yaxis_vals = yaxis_vals
        self.group_idxs = group_idxs

        print(f'group_idxs = {group_idxs}')
        #input()

        self.unique_groups = []
        for gr in self.yaxis_vals:
            if gr in self.unique_groups:
                pass
            else:
                self.unique_groups.append(gr)


        self.unique_group_start_times = [[] for i in range(len(self.unique_groups))]
        self.unique_group_end_times = [[] for i in range(len(self.unique_groups))]
        self.unique_group_member_indices = [[] for i in range(len(self.unique_groups))]
        self.unique_groups_population = [0] * len(self.unique_groups)
        print(f'self.unique_group_start_times = {self.unique_group_start_times}')
        trying = self.unique_group_member_indices[10]
        trying.append([1, 2, 3, 4, 5])
        print(f'self.unique_group_member_indices[10] = {self.unique_group_member_indices[10]}\n'
              f'self.unique_group_member_indices[0] = {self.unique_group_member_indices[0]}')

        hit_count = 0
        for ug_idx, ug in enumerate(self.unique_groups):
            for gr_idx, gr in enumerate(self.yaxis_vals):
                # print(f'\nug_idx = {ug_idx}\n'
                #       f'gr_idx = {gr_idx}\n'
                #       f'hit_count = {hit_count}\n'
                #       # f'self.unique_groups_population = {self.unique_groups_population}\n'
                #       # f'group_indices = {self.group_idxs[gr_idx]}\n'
                #       # f'self.unique_group_member_indices = {self.unique_group_member_indices}\n'
                #       f'len(self.unique_group_member_indices[3]) = {len(self.unique_group_member_indices[3])}')

                if gr == ug:

                    #print(f'self.unique_group_member_indices = {self.unique_group_member_indices}')

                    start = self.xaxis_vals[gr_idx][0]
                    end = self.xaxis_vals[gr_idx][-1]
                    group_indices = self.group_idxs[gr_idx]

                    self.unique_group_start_times[ug_idx].append(start)
                    self.unique_group_end_times[ug_idx].append(end)
                    #self.unique_group_member_indices[ug_idx].append(group_indices)
                    self.unique_group_member_indices[ug_idx].append(self.group_idxs[gr_idx])

                    self.unique_groups_population[ug_idx] += 1

                    hit_count += 1

                    if ug_idx == 4:
                        print(f'\nug_idx = {ug_idx}\n'
                              f'{gr} = {ug}\n'
                              f'start = {start}\n'        
                              f'end = {end}\n'
                              f'self.unique_groups_population = {self.unique_groups_population}\n'
                              f'self.unique_group_start_times = {self.unique_group_start_times}\n'
                              f'group_indices = {group_indices}\n'
                              f'self.unique_group_member_indices = {self.unique_group_member_indices}\n'
                              f'len(self.unique_group_start_times[10]) = {len(self.unique_group_start_times[10])}\n'
                              f'len(self.unique_group_member_indices[10]) = {len(self.unique_group_member_indices[10])}')

                        #input()
                    else:
                        pass

                else:

                    pass



        self.unique_groups_population = [0]*len(self.unique_groups)
        for gr in self.yaxis_vals:
            for un_gr_idx, un_gr in enumerate(self.unique_groups):
                if gr == un_gr:
                    self.unique_groups_population[un_gr_idx]+= 1
                else:
                    pass

        print('\n\n')
        print(f'unique_groups = {self.unique_groups}\n'
              f'unique_group_member_indices = {self.unique_group_member_indices}\n'
              f'unique_groups_population = {self.unique_groups_population}')

        print(f'len(self.unique_groups) = {len(self.unique_groups)}\n'
              f'len(self.group_idxs) = {len(self.group_idxs)}')

        print(f'len(self.unique_group_member_indices) = {len(self.unique_group_member_indices)}\n'
              f'len(self.unique_group_member_indices[0]) = {len(self.unique_group_member_indices[0])}\n'
              f'len(self.unique_group_member_indices[1]) = {len(self.unique_group_member_indices[1])}\n'
              f'len(self.unique_group_member_indices[-1]) = {len(self.unique_group_member_indices[-1])}\n'
              f'len(self.unique_group_member_indices[0][0]) = {len(self.unique_group_member_indices[0][0])}\n')


        print(f'self.unique_group_start_times = {self.unique_group_start_times}\n'
              f'self.unique_group_end_times) = {self.unique_group_end_times}')

        #input()

        return self.unique_groups, self.unique_group_member_indices, self.unique_group_start_times, self.unique_group_end_times, self.unique_groups_population


    def save_hist_peak_vals_to_csv(self):
        '''
        Specific function that calls in the data returned by the histogram of delta times
        and the peak finding function "find_top_x_peaks_histogram()"
        and saves them as two colums in a .csv for ease of reference.
        :return:
        '''

        read = reader()

        self.peak_x_val = values[hist_peak_x_vals]
        self.peak_y_val = values[hist_peak_y_vals]

        read.save_two_lists_csv(self.peak_x_val, self.peak_y_val, r'\Peak_histogram_vals')


    def find_unique_fault_log_entries(self):
        '''
        Takes the fault log and prints out all unique entries with an associated index ready
        for assignation as a dictionary.
        :return:
        '''
        self.all_full_buffers = values[all_full_buffers]

        self.unique_mod_faults = []
        in_count = 0
        print('\nfault_log_to_index_dict = {')
        for b in self.all_full_buffers:
            for f in b:
                if f not in self.unique_mod_faults:
                    self.unique_mod_faults.append(f)
                    print(f'"{f}": {in_count},')
                    in_count += 1
                else:
                    pass

        print('}')

        print(f'\n\nlen(unique_mod_faults) = {len(self.unique_mod_faults)}')
        values[unique_mod_faults] = self.unique_mod_faults

    def convert_mod_fault_to_indices(self):
        '''
        simple function that uses the fault_log_to_index_dict to convert names to indices
        :return:
        '''

        self.all_full_buffers = values[all_full_buffers]
        for i in self.all_full_buffers:
            print(len(i))

        self.fault_log_to_index_dict = values[fault_log_to_index_dict]

        self.all_full_buffers_indices = []
        for b in self.all_full_buffers:
            b_idx = [self.fault_log_to_index_dict[i] for i in b]
            self.all_full_buffers_indices.append(b_idx)

        values[all_full_buffers_indices] = self.all_full_buffers_indices

    def convert_mod_fault_to_indices_2(self):
        '''
        simple function that uses the fault_log_to_index_dict to convert names to indices
        :return:
        '''

        self.full_buffers = values[full_buffers]
        for i in self.full_buffers:
            print(len(i))

        self.fault_log_to_index_dict = values[fault_log_to_index_dict]

        self.full_buffers_indices = []
        for b in self.full_buffers:
            b_idx = [self.fault_log_to_index_dict[i] for i in b]
            self.full_buffers_indices.append(b_idx)

        values[full_buffers_indices] = self.full_buffers_indices

        print(f'self.full_buffers_indices = {self.full_buffers_indices}')
        print(f'len(self.full_buffers_indices) = {len(self.full_buffers_indices)}')
        #input()

    def get_times_for_full_buffers(self):
        '''
        creates a nested list of lists of times of each fault in the same structure as full buffers.
        THIS IS A NIGHTMARE MACHINE!! it has to be in order to handle the way the data was archived - Sorry!
        :return:
        '''

        #input('get_times_for_full_buffers() is being called!')

        self.raw_buffer_times = values[raw_buffer_times]
        self.raw_buffers = values[raw_buffers]


        print(f'len(self.raw_buffer_times) = {len(self.raw_buffer_times)}')
        print(f'len(self.raw_buffers) = {len(self.raw_buffers)}')

        self.times_matching_full_buffers = []
        self.full_buffers = []
        self.this_time_buffer = []

        self.old_length_buffer = 100000 # placeholder - must not == len(raw_buffers[0])

        self.N_datapoint_to_delete = int(len(self.raw_buffers[0])-1)

        full_buffer_count = 0
        instance_count = 0
        for t_idx, t in enumerate(self.raw_buffer_times):

            # print(f't_idx = {t_idx}')
            # print(f'len(self.raw_buffers[t_idx]) = {len(self.raw_buffers[t_idx])}')
            # print(f'self.raw_buffer_times[t_idx] = {self.raw_buffer_times[t_idx]}')
            # print(f'len(self.this_time_buffer) = {len(self.this_time_buffer)}')

            self.population_diference = len(self.this_time_buffer) - len(self.raw_buffers[t_idx])
            #print(f'population difference = {self.population_diference}')

            if str(int(self.population_diference)) == str(-2):
                if instance_count == 0:
                    print(f'population difference = {self.population_diference}\n'
                          f'self.this_time_buffer = {self.this_time_buffer}\n'
                          f'self.raw_buffers[t_idx-1] = {self.raw_buffers[t_idx-1]}\n'
                          f'self.raw_buffers[t_idx] = {self.raw_buffers[t_idx]}\n'
                          f'self.raw_buffers[t_idx+1] = {self.raw_buffers[t_idx+1]}\n')

                instance_count += 1

                print(f'instance_count = {instance_count}')

            #input()

            if len(self.raw_buffers[t_idx]) == 0:
                #print(f'{t_idx} {len(raw_buffers[t_idx])} {len(this_time_buffer)}')
                self.times_matching_full_buffers.append(self.this_time_buffer)

                if full_buffer_count == 0:
                    print(f'len(self.raw_buffers[t_idx - 1][self.N_datapoint_to_delete:]) = {len(self.raw_buffers[t_idx - 1][self.N_datapoint_to_delete:])}')
                    self.full_buffers.append(self.raw_buffers[t_idx - 1][self.N_datapoint_to_delete:])
                    #input()
                else:
                    self.full_buffers.append(self.raw_buffers[t_idx-1])
                self.this_time_buffer = []

                self.old_length_buffer = len(self.raw_buffers[t_idx])
                full_buffer_count += 1

            else:
                self.new_length_buffer = len(self.raw_buffers[t_idx])
                if self.new_length_buffer == self.old_length_buffer:
                    print(f'dud entry time at index {t_idx}')
                elif self.new_length_buffer - self.old_length_buffer == 2:
                    print(f'found glitch in data at index {t_idx}\n(2 faults appended to list, not 1.)')
                    self.this_time_buffer.append(t)
                    self.this_time_buffer.append(t)
                    self.old_length_buffer = self.new_length_buffer
                else:
                    self.this_time_buffer.append(t)
                    self.old_length_buffer = self.new_length_buffer

                #print(f'{t_idx} {len(raw_buffers[t_idx])} {len(this_time_buffer)}')

        for t in range(len(self.times_matching_full_buffers)):
            print(f'{len(self.times_matching_full_buffers[t])}: {self.times_matching_full_buffers[t]}')
            print(f'{len(self.full_buffers[t])}')

        values[times_matching_full_buffers] = self.times_matching_full_buffers
        values[full_buffers] = self.full_buffers
        self.convert_mod_fault_to_indices_2()
        values[full_buffers] = self.full_buffers

        self.flatten_full_buffers()

    def get_times_for_all_buffer_entries(self):
        '''
        creates a nested list of lists of times of each fault in the same structure as full buffers.
        :return:
        '''
        self.raw_buffer_times = values[raw_buffer_times]
        self.raw_buffers = values[raw_buffers]
        print(f'len(self.raw_buffer_times) = {len(self.raw_buffer_times)}')
        print(f'len(self.raw_buffers) = {len(self.raw_buffers)}')
        self.buffer_entry_times = []
        self.buffer_entries = []
        for b_idx, b in enumerate(self.raw_buffers):

            if len(b) == 0:
                pass
            else:
                self.buffer_entry_times.append(self.raw_buffer_times[b_idx])
                self.buffer_entries.append(b[-1])

        values[buffer_entry_times] = self.buffer_entry_times
        values[buffer_entries] = self.buffer_entries

    def get_times_for_all_buffer_entries_quick_check(self):
        '''
        creates a nested list of lists of times of each fault in the same structure as full buffers.
        :return:
        '''
        self.raw_buffer_times_quick_check = values[raw_buffer_times_quick_check]
        self.raw_buffers_quick_check = values[raw_buffers_quick_check]
        print(f'len(self.raw_buffer_times_quick_check) = {len(self.raw_buffer_times_quick_check)}')
        print(f'len(self.raw_buffers_quick_check) = {len(self.raw_buffers_quick_check)}')
        self.buffer_entry_times_quick_check = []
        self.buffer_entries_quick_check = []
        for b_idx, b in enumerate(self.raw_buffers_quick_check):

            if len(b) == 0:
                pass
            else:
                self.buffer_entry_times_quick_check.append(self.raw_buffer_times_quick_check[b_idx])
                self.buffer_entries_quick_check.append(b[-1])

        values[buffer_entry_times_quick_check] = self.buffer_entry_times_quick_check
        values[buffer_entries_quick_check] = self.buffer_entries_quick_check


    def get_raw_times_of_HV_interlocks(self):
        '''
        Scans the fault log and finds the times at which HV interlock 2 occur.
        :return:
        '''
        self.raw_buffer_times = values[raw_buffer_times]
        self.raw_buffers = values[raw_buffers]

        print(f'len(self.raw_buffer_times) = {len(self.raw_buffer_times)}\n'
              f'len(self.raw_buffers) = {len(self.raw_buffers)}')

        self.HV_interlock_times_FaultLog = []
        for b_idx, b in enumerate(self.raw_buffers):
            if len(b) == 0:
                pass
            else:
                if b[-1] == "Mod:Sys\HwCtr\Hv interlock 2.":
                    print(b)
                    self.HV_interlock_times_FaultLog.append(self.raw_buffer_times[b_idx])

        print(f'HV_interlock_times_FaultLog = {self.HV_interlock_times_FaultLog}')
        values[HV_interlock_times_FaultLog] = self.HV_interlock_times_FaultLog

        #input()


    def convert_EPICS_time_to_real_time(self, time_list):
        '''
        takes a list of seconds since the start of the EPICS epoch (01-01-1970) and converts ist into pandas timestamps
        :param time_list: list of seconds since the start of the EPICS epoch (01-01-1970)
        :return: pandas timestamp list
        '''

        self.time_list = time_list
        self.EPICS_genesis_time = values[EPICS_genesis_time]

        self.timestamp_list = []
        for t in self.time_list:
            timestamp = self.EPICS_genesis_time + pd.Timedelta(seconds=t)
            self.timestamp_list.append(timestamp)

        values[HV_interlock_timestamps] = self.timestamp_list

        return self.timestamp_list


    def create_to_and_from_times_from_HV_interlock_timestamps(self, timestamp_list):
        '''
        Takes a list of timestamps and returns a list of 'time from' and a list of 'time to' for use with EPICS
        :param timestamp_list: list of pandas timestamps
        :return: Formatted string "YYYY-MM-DDTHH:MM:SS.SSZ"
        '''
        self.timestamp_list = timestamp_list

        self.delta_time_before_seconds = values[HV_interlock_window_seconds_before]
        self.delta_time_after_seconds = values[HV_interlock_window_seconds_after]

        self.HV_interlock_EICS_date_time_from = []
        self.HV_interlock_EICS_date_time_to = []
        for t in self.timestamp_list:
            timestamp_before = t - pd.Timedelta(seconds=self.delta_time_before_seconds)
            date_before = str(timestamp_before)[:10]
            time_before = str(timestamp_before)[11:-4]

            timestamp_after = t + pd.Timedelta(seconds=self.delta_time_after_seconds)
            date_after = str(timestamp_after)[:10]
            time_after = str(timestamp_after)[11:-4]

            # print(date_before)
            # print(time_before)
            # print(date_after)
            # print(time_after)

            date_time_from = f"{date_before}T{time_before}Z"
            date_time_to = f"{date_after}T{time_after}Z"

            print(date_time_from)
            print(date_time_to)

            self.HV_interlock_EICS_date_time_from.append(date_time_from)
            self.HV_interlock_EICS_date_time_to.append(date_time_to)

        #input()
        values[HV_interlock_EICS_date_time_from] = self.HV_interlock_EICS_date_time_from
        values[HV_interlock_EICS_date_time_to] = self.HV_interlock_EICS_date_time_to

    def create_to_and_from_times_from_chosen_interlock_timestamps(self, timestamp_list):
        '''
        Takes a list of timestamps and returns a list of 'time from' and a list of 'time to' for use with EPICS
        :param timestamp_list: list of pandas timestamps
        :return: Formatted string "YYYY-MM-DDTHH:MM:SS.SSZ"
        '''
        self.timestamp_list = timestamp_list

        self.delta_time_before_seconds = values[chosen_interlock_window_seconds_before]
        self.delta_time_after_seconds = values[chosen_interlock_window_seconds_after]

        self.chosen_interlock_EICS_date_time_from = []
        self.chosen_interlock_EICS_date_time_to = []
        for t in self.timestamp_list:
            timestamp_before = t - pd.Timedelta(seconds=self.delta_time_before_seconds)
            date_before = str(timestamp_before)[:10]
            time_before = str(timestamp_before)[11:-4]

            timestamp_after = t + pd.Timedelta(seconds=self.delta_time_after_seconds)
            date_after = str(timestamp_after)[:10]
            time_after = str(timestamp_after)[11:-4]

            # print(date_before)
            # print(time_before)
            # print(date_after)
            # print(time_after)

            date_time_from = f"{date_before}T{time_before}Z"
            date_time_to = f"{date_after}T{time_after}Z"

            print(date_time_from)
            print(date_time_to)

            self.chosen_interlock_EICS_date_time_from.append(date_time_from)
            self.chosen_interlock_EICS_date_time_to.append(date_time_to)

        #input()
        values[chosen_interlock_EICS_date_time_from] = self.chosen_interlock_EICS_date_time_from
        values[chosen_interlock_EICS_date_time_to] = self.chosen_interlock_EICS_date_time_to

    def merge_and_sort(self, l, r):
        '''
        Taken from Stack exchange, available at ...
        "https://stackoverflow.com/questions/2488889/how-can-i-merge-two-lists-and-sort-them-working-in-linear-time"
        :param l: list 1
        :param r: list 2
        :return: merged and sorted list
        '''
        result = []
        while l and r:
            if l[-1] > r[-1]:
                result.append(l.pop())
            else:
                result.append(r.pop())

        result += (l + r)[::-1]
        result.reverse()

        return result

    def concatenate_and_sort(self, list_1, list_2):
        '''
        Concatenates two lists and thes sorts thenm in ascending order
        :param list_1:
        :param list_2:
        :return:
        '''
        self.list_1 = list(list_1)
        self.list_2 = list(list_2)
        self.result = np.sort(self.list_1 + self.list_2)

        return self.result

    def compare_fault_log_to_mod_state_HV_interlock_times(self):
        '''
        This function compares the times stated by the HRFO fault log and the times stated by the modulator state read
        regarding the HV interlock
        :return:
        '''
        fig = figures()
        self.mod_StateRead_time = values[mod_StateRead_time]
        self.mod_StateRead_yaxis = values[mod_StateRead_yaxis]
        self.HV_interlock_times_FaultLog = values[HV_interlock_times_FaultLog]

        print(f'self.HV_interlock_times_FaultLog[0:16] = {self.HV_interlock_times_FaultLog[0:16]}')
        print(f'self.mod_StateRead_yaxis[0:16] = {self.mod_StateRead_yaxis[0:16]}')

        #values[HV_interlock_times_FaultLog]
        self.HV_interlock_times_StateRead = [self.mod_StateRead_time[idx] for idx in range(len(self.mod_StateRead_yaxis)) if self.mod_StateRead_yaxis[idx] == 4]

        print(f'len(self.HV_interlock_times_StateRead) = {len(self.HV_interlock_times_StateRead)}\n'
              f'len(self.HV_interlock_times_FaultLog) = {len(self.HV_interlock_times_FaultLog)}\n')

        self.HV_interlock_times_in_common = [self.HV_interlock_times_FaultLog[idx] for idx in range(len(self.HV_interlock_times_FaultLog)) if self.HV_interlock_times_FaultLog[idx] in self.mod_StateRead_time]
        print(f'len(self.HV_interlock_times_in_common) = {len(self.HV_interlock_times_in_common)}')

        self.merged_and_sorted_times = self.concatenate_and_sort(np.copy(self.HV_interlock_times_FaultLog), np.copy(self.mod_StateRead_time))

        print(f'self.HV_interlock_times_FaultLog = {self.HV_interlock_times_FaultLog}\n'
              f'self.mod_StateRead_time = {self.mod_StateRead_time}\n'
              f'self.merged_and_sorted_times = {self.merged_and_sorted_times}')

        self.FaultLog_and_previous_StateRead_times = []
        self.FaultLog_StateRead_delta_times = []
        for ms_idx, ms in enumerate(self.merged_and_sorted_times):
            if ms_idx == 0:
                pass
            else:
                if ms in self.HV_interlock_times_FaultLog:
                    self.FaultLog_and_previous_StateRead_times.append(self.merged_and_sorted_times[ms_idx-1])
                    self.FaultLog_and_previous_StateRead_times.append(ms)
                    self.FaultLog_StateRead_delta_times.append(ms-self.merged_and_sorted_times[ms_idx-1])
                else:
                    pass

        print(f'self.FaultLog_and_previous_StateRead_times :\n{self.FaultLog_and_previous_StateRead_times}')
        print(f'self.FaultLog_StateRead_delta_times :\n{self.FaultLog_StateRead_delta_times}')
        fig.histogram_nbin(self.FaultLog_StateRead_delta_times, 'Delta_times_StateRead_FaultLog', float(np.amax(self.FaultLog_and_previous_StateRead_times)), 100)

    def convert_config_interlock_choice_to_full_name(self):
        '''
        converts the config intelock_chioce name (eg 'HV_2) to
        full name (eg "Mod:Sys\HwCtr\Hv interlock 2.")
        :return:
        '''
        self.interlock_choice = values[interlock_choice]
        self.interlock_choice_to_fault_log_dict = interlock_choice_to_fault_log_dict
        print(f'self.interlock_choice = {self.interlock_choice}')
        print(f'self.interlock_choice_to_fault_log_dict = {self.interlock_choice_to_fault_log_dict}')
        self.interlock_choice_to_full_name = self.interlock_choice_to_fault_log_dict[self.interlock_choice]
        values[interlock_choice_full_name] = self.interlock_choice_to_full_name

    def return_converted_config_interlock_choice_to_full_name(self, interlock_choice):
        '''
        converts the config intelock_chioce name (eg 'HV_2) to
        full name (eg "Mod:Sys\HwCtr\Hv interlock 2.")
        :return: interlock_choice_to_full_name
        '''
        self.interlock_choice = interlock_choice
        self.interlock_choice_to_fault_log_dict = interlock_choice_to_fault_log_dict
        print(f'self.interlock_choice = {self.interlock_choice}')
        print(f'self.interlock_choice_to_fault_log_dict = {self.interlock_choice_to_fault_log_dict}')
        self.interlock_choice_to_full_name = self.interlock_choice_to_fault_log_dict[self.interlock_choice]

        return  self.interlock_choice_to_full_name


    def get_raw_times_of_chosen_interlocks(self):
        '''
        Scans the fault log and finds the times at which the interlock chosen in the config.yaml occur.
        :return:
        '''
        self.raw_buffer_times = values[raw_buffer_times]
        self.raw_buffers = values[raw_buffers]
        self.interlock_choice_full_name = values[interlock_choice_full_name]

        print(f'len(self.raw_buffer_times) = {len(self.raw_buffer_times)}\n'
              f'len(self.raw_buffers) = {len(self.raw_buffers)}')

        self.chosen_interlock_times_FaultLog = []
        for b_idx, b in enumerate(self.raw_buffers):
            if len(b) == 0:
                pass
            else:
                if b[-1] == self.interlock_choice_full_name:
                    print(b)
                    self.chosen_interlock_times_FaultLog.append(self.raw_buffer_times[b_idx])

        print(f'chosen_interlock_times_FaultLog = {self.chosen_interlock_times_FaultLog}')
        values[chosen_interlock_times_FaultLog] = self.chosen_interlock_times_FaultLog

    def flatten_full_buffers(self):
        '''
        Takes the nested list-of-lists that is the fulll buffer list and associated times list
        and flattens them out into a one-dimensional sequential list
        :return:
        '''

        self.full_buffers = values[full_buffers]
        self.times_matching_full_buffers = values[times_matching_full_buffers]
        self.fault_log_to_index_dict = values[fault_log_to_index_dict]

        self.buffers_1D_times = []
        self.buffers_1D_names = []
        for b_idx, b in enumerate(self.times_matching_full_buffers):
            for val_idx, val in enumerate(b):
                self.buffers_1D_times.append(val)
                self.buffers_1D_names.append(self.full_buffers[b_idx][val_idx])

        values[buffers_1D_times] = self.buffers_1D_times
        values[buffers_1D_names] = self.buffers_1D_names
        self.buffers_1D_one_hot = [self.fault_log_to_index_dict[i] for i in self.buffers_1D_names]
        values[buffers_1D_one_hot] = self.buffers_1D_one_hot

        #input()
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

# EPICS_genesis_time_dict = {'year': 1970,
#    'month': 1,
#    'day': 1}
# origin=pd.Timestamp('1970-01-01'))
# EPICS_genesis_time_df = pd.DataFrame(EPICS_genesis_time_dict)
#
# pd.to_datetime(EPICS_genesis_time_df)

EPICS_genesis_time = 'EPICS_genesis_time'
all_value_keys.append(EPICS_genesis_time)
values[EPICS_genesis_time] = pd.Timestamp('1970-01-01')

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

INCLUDE_INTERLOCK_PVs = 'INCLUDE_INTERLOCK_PVs'
all_value_keys.append(INCLUDE_INTERLOCK_PVs)
values[INCLUDE_INTERLOCK_PVs] = []

interlock_PVs = 'interlock_PVs'
all_value_keys.append(interlock_PVs)
values[interlock_PVs] = []

fault_log_PVs = 'fault_log_PVs'
all_value_keys.append(fault_log_PVs)
values[fault_log_PVs] = []

PLOT_ALL_PVs = 'PLOT_ALL_PVs'
all_value_keys.append(PLOT_ALL_PVs)
values[PLOT_ALL_PVs] = False

all_mod_PVs_2 = 'all_mod_PVs_2'
all_value_keys.append(all_mod_PVs_2)
values[all_mod_PVs_2] = []

X_HIGHEST_PEAKS_HIST = 'X_HIGHEST_PEAKS_HIST'
all_value_keys.append(X_HIGHEST_PEAKS_HIST)
values[X_HIGHEST_PEAKS_HIST] = Dummy_int

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

PV_TIME_zeroed = 'PV_TIME_zeroed'
all_value_keys.append(PV_TIME_zeroed)
values[PV_TIME_zeroed] = []

PV_YAXIS_DATA = 'PV_YAXIS_DATA'
all_value_keys.append(PV_YAXIS_DATA)
values[PV_YAXIS_DATA] = []

READ_PVs = 'READ_PVs'
all_value_keys.append(READ_PVs)
values[READ_PVs] = False

USE_INTERLOCK_LIST = 'USE_INTERLOCK_LIST'
all_value_keys.append(USE_INTERLOCK_LIST)
values[USE_INTERLOCK_LIST] = False

interlock_choice_list = 'interlock_choice_list'
all_value_keys.append(interlock_choice_list)
values[interlock_choice_list] = []

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

hist_peak_x_vals = 'hist_peak_x_vals'
all_value_keys.append(hist_peak_x_vals)
values[hist_peak_x_vals] = []

hist_peak_y_vals = 'hist_peak_y_vals'
all_value_keys.append(hist_peak_y_vals)
values[hist_peak_y_vals] = []

unique_groups_delta_time = 'unique_groups_delta_time'
all_value_keys.append(unique_groups_delta_time)
values[unique_groups_delta_time] = []

unique_group_member_indices_delta_time = 'unique_group_member_indices_delta_time'
all_value_keys.append(unique_group_member_indices_delta_time)
values[unique_group_member_indices_delta_time] = []

unique_group_start_times_delta_time = 'unique_group_start_times_delta_time'
all_value_keys.append(unique_group_start_times_delta_time)
values[unique_group_start_times_delta_time] = []

unique_group_end_times_delta_time = 'unique_group_end_times_delta_time'
all_value_keys.append(unique_group_end_times_delta_time)
values[unique_group_end_times_delta_time] = []

unique_groups_population_delta_time  = 'unique_groups_population_delta_time'
all_value_keys.append(unique_groups_population_delta_time)
values[unique_groups_population_delta_time] = []

unique_groups_standby = 'unique_groups_standby'
all_value_keys.append(unique_groups_standby)
values[unique_groups_standby] = []

unique_group_member_indices_standby = 'unique_group_member_indices_standby'
all_value_keys.append(unique_group_member_indices_standby)
values[unique_group_member_indices_standby] = []

unique_group_start_times_standby = 'unique_group_start_times_standby'
all_value_keys.append(unique_group_start_times_standby)
values[unique_group_start_times_standby] = []

unique_group_end_times_standby = 'unique_group_end_times_standby'
all_value_keys.append(unique_group_end_times_standby)
values[unique_group_end_times_standby] = []

unique_groups_population_standby  = 'unique_groups_population_standby'
all_value_keys.append(unique_groups_population_standby)
values[unique_groups_population_standby] = []

all_full_buffers = 'all_full_buffers'
all_value_keys.append(all_full_buffers)
values[all_full_buffers] = []

fault_log_to_index_dict = 'fault_log_to_index_dict'
all_value_keys.append(fault_log_to_index_dict)
values[fault_log_to_index_dict] = {"Cavity Interlock":0,
                                    "General Interlock":1,
                                    "Hold RF (Con) Engaged":2,
                                    "Hold RF Deactivated":3,
                                    "Hold RF Engaged":4,
                                    "Hold RF On had to STOP":5,
                                    "Libera: General Interlock":6,
                                    "LLRF:Channel 1":7,
                                    "LLRF:Channel 2":8,
                                    "LLRF:Channel 3":9,
                                    "LLRF:Channel 4":10,
                                    "LLRF:Channel 5":11,
                                    'LLRF:Channel 6': 12,
                                    "Mod is OFF":13,
                                    "Mod:HV Not On":14,
                                    "Mod:HvPs\Ps1\IGBT int.":15,
                                    "Mod:Pt\\Cool\\Klystron Body Flow int.":16,
                                    "Mod:Pt\\Cool\\Tank Flow int.":17,
                                    "Mod:Pt\\Diag\\CT read int.":18,
                                    "Mod:Pt\\FilPs\\Volt int.":19,
                                    "Mod:Pt\Diag\CT arc int.":20,
                                    "Mod:RF Not On":21,
                                    "Mod:Sys\\Cool\\Solenoid Flow int.": 22,
                                    "Mod:Sys\ExtCom\Communication int.": 23,
                                    "Mod:Sys\HwCtr\Hv interlock 1.": 24,
                                    "Mod:Sys\HwCtr\Hv interlock 2.": 25,
                                    "RF Enable Interlock": 26,
                                    "Switched Modulator OFF": 27}

unique_mod_faults = 'unique_mod_faults'
all_value_keys.append(unique_mod_faults)
values[unique_mod_faults] = []

all_full_buffers_indices = 'all_full_buffers_indices'
all_value_keys.append(all_full_buffers_indices)
values[all_full_buffers_indices] = []

raw_buffer_times = 'raw_buffer_times'
all_value_keys.append(raw_buffer_times)
values[raw_buffer_times] = []

raw_buffers = 'raw_buffers'
all_value_keys.append(raw_buffers)
values[raw_buffers] = []

full_buffers = 'full_buffers'
all_value_keys.append(full_buffers)
values[full_buffers] = []

times_matching_full_buffers = 'times_matching_full_buffers'
all_value_keys.append(times_matching_full_buffers)
values[times_matching_full_buffers] = []

buffers_1D_times = 'buffers_1D_times'
all_value_keys.append(buffers_1D_times)
values[buffers_1D_times] = []

buffers_1D_names = 'buffers_1D_names'
all_value_keys.append(buffers_1D_names)
values[buffers_1D_names] = []

buffers_1D_one_hot = 'buffers_1D_one_hot'
all_value_keys.append(buffers_1D_one_hot)
values[buffers_1D_one_hot] = []

HV_interlock_times_FaultLog = 'HV_interlock_times_FaultLog'
all_value_keys.append(HV_interlock_times_FaultLog)
values[HV_interlock_times_FaultLog] = []

HV_interlock_EICS_date_time_from = 'HV_interlock_EICS_date_time_from'
all_value_keys.append(HV_interlock_EICS_date_time_from)
values[HV_interlock_EICS_date_time_from] = []

HV_interlock_EICS_date_time_to = 'HV_interlock_EICS_date_time_to'
all_value_keys.append(HV_interlock_EICS_date_time_to)
values[HV_interlock_EICS_date_time_to] = []

HV_interlock_comparison_PVs = 'HV_interlock_comparison_PVs'
all_value_keys.append(HV_interlock_comparison_PVs)
values[HV_interlock_comparison_PVs] = []

chosen_interlock_comparison_PVs = 'chosen_interlock_comparison_PVs'
all_value_keys.append(chosen_interlock_comparison_PVs)
values[chosen_interlock_comparison_PVs] = []

HV_interlock_window_seconds_before = 'HV_interlock_window_seconds_before'
all_value_keys.append(HV_interlock_window_seconds_before)
values[HV_interlock_window_seconds_before] = Dummy_float

HV_interlock_window_seconds_after = 'HV_interlock_window_seconds_after'
all_value_keys.append(HV_interlock_window_seconds_after)
values[HV_interlock_window_seconds_after] = Dummy_float

HV_interlock_timestamps = 'HV_interlock_timestamps'
all_value_keys.append(HV_interlock_timestamps)
values[HV_interlock_timestamps] = []

interlock_pv_fault_to_index_dict = 'interlock_pv_fault_to_index_dict'
all_value_keys.append(interlock_pv_fault_to_index_dict)
values[interlock_pv_fault_to_index_dict] = {'No Error'	:	0,
                                            ''	:	 0,
                                            '-'	:	 0,
                                            ' '	:	0,
                                            'HvPs\\Ps1\\IGBT int.'	:	1,
                                            'HvPs\\Ps1\\Phase loss int.'	:	2,
                                            'HvPs\\Ps1\\Soft start int.'	:	3,
                                            'Pt\\BiasPs\\Curr int.'	:	4,
                                            'Pt\\Cool\\HPSU Flow int.'	:	5,
                                            'Pt\\Cool\\HVPS Flow int.' :6,
                                            'Pt\\Cool\\Klystron Body Flow int.'	:	7,
                                            'Pt\\Cool\\Klystron Collector Flow int.': 8,
                                            'Pt\\Diag\\CT arc int.'	:	9,
                                            'Pt\\Diag\\CT read int.'	:	10,
                                            'Pt\\FilPs\\Volt int.'	:	11,
                                            'Rf\\Unidentified int.'	:	12,
                                            'Sw\\Section3\\Switch 1 curr int.'	:	13,
                                            'Sw\\Section3\\Switch 2 curr int.'	:	14,
                                            'Sw\\Section3\\Switch 3 curr int.'	:	15,
                                            'Sw\\Section3\\Switch 4 curr int.'	:	16,
                                            'Sw\\Section3\\Switch 5 curr int.'	:	17,
                                            'Sw\\Section3\\Switch 6 curr int.'	:	18,
                                            'Sys\\Cool\\Solenoid Flow int.': 19,
                                            'Sys\\ExtCom\\Communication int.'	:	20,
                                            'Sys\\HwCtr\\Hv interlock 1.'	:	21,
                                            'Sys\\HwCtr\\Hv interlock 2.'	:	22}

full_buffers_indices = 'full_buffers_indices'
all_value_keys.append(full_buffers_indices)
values[full_buffers_indices] = []

interlock_choice = 'interlock_choice'
all_value_keys.append(interlock_choice)
values[interlock_choice] = ''

# interlock_choice_to_fault_log_dict= 'interlock_choice_to_fault_log_dict'
# all_value_keys.append(interlock_choice_to_fault_log_dict)
interlock_choice_to_fault_log_dict = {'Comms': "Mod:Sys\ExtCom\Communication int.",
                                        'CT_arc': "Mod:Pt\Diag\CT arc int.",
                                        'IGBT': "Mod:HvPs\Ps1\IGBT int.",
                                        'RF_enable': "RF Enable Interlock",
                                        'Cavity': "Cavity Interlock",
                                        'HV_2': "Mod:Sys\HwCtr\Hv interlock 2.",
                                        'General': "General Interlock",
                                        'Libera_General': "Libera: General Interlock",
                                        'Klystron_Body_Flow': "Mod:Pt\\Cool\\Klystron Body Flow int.",
                                        'FilPS_Volt': "Mod:Pt\\FilPs\\Volt int."}

interlock_choice_full_name = 'interlock_choice_full_name'
all_value_keys.append(interlock_choice_full_name)
values[interlock_choice_full_name] = ''

chosen_interlock_times_FaultLog = 'chosen_interlock_times_FaultLog'
all_value_keys.append(chosen_interlock_times_FaultLog)
values[chosen_interlock_times_FaultLog] = []

chosen_interlock_window_seconds_before = 'chosen_interlock_window_seconds_before'
all_value_keys.append(chosen_interlock_window_seconds_before)
values[chosen_interlock_window_seconds_before] = Dummy_float

chosen_interlock_window_seconds_after = 'chosen_interlock_window_seconds_after'
all_value_keys.append(chosen_interlock_window_seconds_after)
values[chosen_interlock_window_seconds_after] = Dummy_float

chosen_interlock_EICS_date_time_from = 'chosen_interlock_EICS_date_time_from'
all_value_keys.append(chosen_interlock_EICS_date_time_from)
values[chosen_interlock_EICS_date_time_from] = []

chosen_interlock_EICS_date_time_to = 'chosen_interlock_EICS_date_time_to'
all_value_keys.append(chosen_interlock_EICS_date_time_to)
values[chosen_interlock_EICS_date_time_to] = []

buffer_entry_times = 'buffer_entry_times'
all_value_keys.append(buffer_entry_times)
values[buffer_entry_times] = []

buffer_entries = 'buffer_entries'
all_value_keys.append(buffer_entries)
values[buffer_entries] = []

raw_buffer_times_quick_check = 'raw_buffer_times_quick_check'
all_value_keys.append(raw_buffer_times_quick_check)
values[raw_buffer_times_quick_check] = []

raw_buffers_quick_check = 'raw_buffers_quick_check'
all_value_keys.append(raw_buffers_quick_check)
values[raw_buffers_quick_check] = []

buffer_entry_times_quick_check = 'buffer_entry_times_quick_check'
all_value_keys.append(buffer_entry_times_quick_check)
values[buffer_entry_times_quick_check] = []

buffer_entries_quick_check = 'buffer_entries_quick_check'
all_value_keys.append(buffer_entries_quick_check)
values[buffer_entries_quick_check] = []


