from matplotlib import pyplot as plt
from decimal import *
import numpy as np, cmath
import time, csv, os, sys
import HRFOv2_EPICS_data
from HRFOv2_EPICS_reader import reader
from HRFOv2_EPICS_data import data_functions
from HRFOv2_EPICS_figures import figures
from HRFOv2_EPICS_utils import utilities
from datetime import datetime
import pandas as pd

class main_controller():
    '''
    The main routine that runs sequentially
    '''

    def __init__(self):
        print('Initiated main_controller()')

        self.create_folder_time_range_as_name()
        self.main_sequence()

    def main_sequence(self):
        # Instantiate classes
        read = reader()
        df = data_functions()
        #log = logger()
        figs = figures()



        self.READ_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.READ_PVs]

        if self.READ_PVs:
            read.read_EPICS_PVs()

        else:
            read.load_post_PV_read_pkl_2_dict(r'\post_PV_read_values_dict.pkl')
        # read.PCorllett_read_EPICS_PVs()

        #read.read_interlock_PVs()

        #sys.exit()

        # figs.subplots_2(3, 1)
        #
        # figs.subplots_3(3, 2, 1)
        # figs.triple_yaxis_plot(3, 2, 1)
        #
        # # enter PV indeces as a list, eg [1, 2, 3, 4]
        # figs.subplots_x([3, 2, 1, 4])
        #
        # # Scan mod StateRead for groups
        # df.scan_data_for_delta_time_groups()
        # df.scan_data_for_standby_groups()
        #
        # ######################################################################################
        #
        # # for the first run use this:
        # #unique_group_numbers = [1]
        #
        # # find the unique group numbers of interest from the "unique_groups_population_standby.csv"
        # # created on the first run.
        # # for subsequent runs enter unique group numbers of interest into a list (un-hash below)
        # unique_group_numbers = [2, 3, 5]
        #
        # # for all runs enter the pv indices into al list
        # pv_list = [1, 2]
        #
        # # If you require individual plots with Index Number as the x-axis instead of time
        # # set individual_index=True in the function below
        #
        # for ugn in unique_group_numbers:
        #     figs.handle_group_subplots(ugn, pv_list, xaxis='both', individual_index=False)
        #
        # df.save_hist_peak_vals_to_csv()

        ####################################################################################
        # Generalised interlock subplot time window analysis
        # TODO: compare modulator state read with any PVs of interest using subplots
        DATA = HRFOv2_EPICS_data
        gun_pv = DATA.values[DATA.fault_log_PVs][0]
        interlock_choice = DATA.values[DATA.interlock_choice]
        df.convert_config_interlock_choice_to_full_name()
        interlock_choice_full_name = DATA.values[DATA.interlock_choice_full_name]
        print(f'interlock_choice = {interlock_choice}')
        print(f'interlock_choice_full_name = {interlock_choice_full_name}')
        print(f'gun_pv = {gun_pv}')

        read.read_gun_fault_log()
        df.find_unique_fault_log_entries()
        unique_mod_faults = DATA.values[DATA.unique_mod_faults]
        print(f'len(unique_mod_faults = {len(unique_mod_faults)}\n'
              f'unique_mod_faults = {unique_mod_faults}')

        df.convert_mod_fault_to_indices()
        df.get_times_for_full_buffers()

        times_matching_full_buffers = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.times_matching_full_buffers]
        full_buffers_indices = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.full_buffers_indices]

        print(f'times_matching_full_buffers = {times_matching_full_buffers}')
        print(f'len(times_matching_full_buffers) = {len(times_matching_full_buffers)}')
        # print(f'all_full_buffers_indices[0] = {all_full_buffers_indices[0]}')
        # print('HELLO!')
        for t in range(len(times_matching_full_buffers)):
            print(f'{t}: {len(times_matching_full_buffers[t])} {len(full_buffers_indices[t])}')
            # figs.individual_PV_plot(times_matching_full_buffers[t], full_buffers_indices[t], f'Full fault log {t}',
            #                         f'\\Full_fault_log_{t}', 10000 + t)

        # input()
        df.get_raw_times_of_chosen_interlocks()
        chosen_interlock_times_FaultLog = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.chosen_interlock_times_FaultLog]

        chosen_interlock_timestamps = df.convert_EPICS_time_to_real_time(chosen_interlock_times_FaultLog)

        for ts in chosen_interlock_timestamps:
            print(ts)



        df.create_to_and_from_times_from_chosen_interlock_timestamps(chosen_interlock_timestamps)
        read.read_EPICS_PVs_for_single_chosen_interlock_period()

        dict_obj_list = [HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.interlock_pv_fault_to_index_dict],
                        HRFOv2_EPICS_data.interlock_choice_to_fault_log_dict,
                         HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.fault_log_to_index_dict],
                         HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.mod_state_dict]
                         ]
        dict_names_lists = ['interlock_pv_fault_to_index_dict',
                            'interlock_choice_to_fault_log_dict',
                            'fault_log_to_index_dict',
                            'mod_state_dict']
        read.print_dictionaries_to_text_file(dict_obj_list, dict_names_lists)
        figs.barchart_FaultLog()

        df.get_times_for_all_buffer_entries()
        figs.barchart_FaultLog_simplified()

        '''
        date_from:  "2019-11-01"
        time_from:  "17:00:00.00"
 
        date_to:  "2021-07-5"
        time_to:  "09:00:00.00"
        '''




        self.RF_conditioning_modulator_quick_check("2021-07-26", "22:00:00.00")


        sys.exit()

        read.read_EPICS_PVs_for_single_HV_interlock_period()
        read.read_EPICS_PVs_for_HV_interlock_periods()


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Fault logs
        DATA = HRFOv2_EPICS_data
        gun_pv = DATA.values[DATA.fault_log_PVs][0]
        print(f'gun_pv = {gun_pv}')
        read.read_gun_fault_log()
        df.find_unique_fault_log_entries()
        df.convert_mod_fault_to_indices()
        df.get_times_for_full_buffers()

        times_matching_full_buffers = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.times_matching_full_buffers]
        full_buffers_indices = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.full_buffers_indices]

        print(f'times_matching_full_buffers[0] = {times_matching_full_buffers[0]}')
        print(f'len(times_matching_full_buffers) = {len(times_matching_full_buffers)}')
        # print(f'all_full_buffers_indices[0] = {all_full_buffers_indices[0]}')
        # print('HELLO!')
        for t in range(len(times_matching_full_buffers)):
            print(f'{t}: {len(times_matching_full_buffers[t])} {len(full_buffers_indices[t])}')
            figs.individual_PV_plot(times_matching_full_buffers[t], full_buffers_indices[t], f'Full fault log {t}',
                                    f'\\Full_fault_log_{t}', 10000 + t)

        #input()
        df.get_raw_times_of_HV_interlocks()
        HV_interlock_times_FaultLog = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.HV_interlock_times_FaultLog]

        HV_interlock_timestamps = df.convert_EPICS_time_to_real_time(HV_interlock_times_FaultLog)

        for ts in HV_interlock_timestamps:
            print(ts)

        df.create_to_and_from_times_from_HV_interlock_timestamps(HV_interlock_timestamps)

        read.read_EPICS_PVs_for_single_HV_interlock_period()
        read.read_EPICS_PVs_for_HV_interlock_periods()
        df.compare_fault_log_to_mod_state_HV_interlock_times()
        figs.barchart_FaultLog()


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



    def create_folder_time_range_as_name(self):
        '''
        Creates a folder in the savepath folder with a name based on the time range entered into the config yaml
        useful for storing data
        :return:
        '''
        df = data_functions()
        #df.create_folder_named_date_time_from_to()

        self.directory = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]

        self.folder_name = df.create_folder_name()

        self.path = r'{}\{}'.format(self.directory, self.folder_name)  # path to be created

        print('directory = {}\npath = {}'.format(self.directory, self.path))

        try:
            os.makedirs(self.path)
            print(f'\nNew "{self.folder_name}" folder created.\n')
        except OSError:
            try:
                folder_test = self.path
                print(f'\n"{self.folder_name}" folder already exists.')
            except:
                print(f'\n...Problem with setting up "{self.folder_name}" folder.')
                sys.exit()

        # resave new savepath in values dictionary so it includes the newly created folder

        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath] = self.path

    def RF_conditioning_modulator_quick_check(self, start_date, start_time):
        '''

        :param start_date:  Date & time to: date in the format "YYYY-MM-DD"
        :param start_time:  time in the format "HH:MM:SS.SSSS"
        :return:
        '''
        read = reader()
        figs = figures()
        df = HRFOv2_EPICS_data.data_functions()
        self.start_date = str(start_date)
        self.start_time = str(start_time)[:11]
        self.datetime_start = pd.to_datetime(f'{self.start_date} {self.start_time}')
        self.datetime_now = pd.to_datetime(datetime.now())
        self.date_now = str(self.datetime_now)[:10]
        self.time_now = str(self.datetime_now)[11:22]
        print(f'pd.to_datetime(datetime.now()) = {pd.to_datetime(datetime.now())}')
        print(f'\n***{self.datetime_start}\n***{self.datetime_now}')
        print(f'self.start_time = {self.start_time}\nself.date_now = {self.date_now}\nself.time_now = {self.time_now}')
        self.EPICS_datetime_from = read.concatenate_date_time_to_EPICS_format(self.start_date, self.start_time)
        self.EPICS_datetime_now = read.concatenate_date_time_to_EPICS_format(self.date_now, self.time_now)

        print(f'\n{self.EPICS_datetime_from}\n{self.EPICS_datetime_now}')

        read.read_gun_fault_log_quick_check(self.EPICS_datetime_from, self.EPICS_datetime_now)
        df.get_times_for_all_buffer_entries_quick_check()
        figs.barchart_FaultLog_quick_check(self.EPICS_datetime_from, self.EPICS_datetime_now)