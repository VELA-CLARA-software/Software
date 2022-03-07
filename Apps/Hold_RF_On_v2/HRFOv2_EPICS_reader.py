import yaml, sys, csv, requests, re, pandas as pd
import numpy as np
from decimal import *
import pickle as pkl
import HRFOv2_EPICS_data
from matplotlib import pyplot as plt

from HRFOv2_EPICS_figures import figures
from HRFOv2_EPICS_utils import utilities
#from HRFOv2_EPICS_data import  data_functions

getcontext().prec = 100

class reader():
    '''
    Class that handles reading in & writing any data files like .yml, .txt, .csv, .pkl etc...
    '''
    _DATA = HRFOv2_EPICS_data
    def __init__(self):
        print('Initiated reader().')


    def read_yaml(self):

        # Read YAML file
        self.config_file = sys.argv[1]
        print(f'config_file = {self.config_file}')
        #self.Decimal_list = ['B_loc', 'B_sigma_intermediate', 'B_alpha']
        with open(self.config_file, 'r') as stream:
            self.raw_config_data = yaml.safe_load(stream)

            print(self.raw_config_data.keys())
            for key, val in self.raw_config_data.items():
                if key in HRFOv2_EPICS_data.all_value_keys:
                    #mod_group_time_spacing = val
                    print(f'key = {key}, val = {val}')
                    HRFOv2_EPICS_data.values[key] = val

                    if key == "mod_group_time_spacing":
                        print(f'HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.mod_group_time_spacing] = '
                              f'{HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.mod_group_time_spacing]}')

                else:
                    print(f'{key} not yet added to all_value_keys list in HRFOv2_EPICS_data.py')
                    sys.exit()

    def remove_char_from_str(self, string_1):
        '''
        Removes characters in '[!@#$:]' form string and returns ammended string
        :param string_1:
        :return:
        '''
        self.string_1 = string_1

        self.string_2 = re.sub('[!@#$:.]', '', self.string_1)

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


    def concatenate_date_time_to_EPICS_format(self, date, time):
        '''
        Takes the inputs from the config yaml and returns a string in the format that EPICS requires
        :param date: String in the format "YYYY-MM-DD"
        :param time: String in the format "HH:MM:SS.SS"
        :return: Formatted string "YYYY-MM-DDTHH:MM:SS.SSZ"
        '''
        self.date = date
        self.time = time
        self.formatted_string = f'{self.date}T{self.time}Z'

        return self.formatted_string

    def read_EPICS_PVs(self, verbose=True):
        '''
        Reads in every PV in the "all_mod_PVs" list
        saves the time data and the yaxis data
        plots each individual PVs yaxis data as a function of time
        :param verbose: if True then function prints out attributes for diagnostics.
        :return:
        '''

        figs = figures()
        #df = data_functions()
        self.verbose = verbose
        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.all_mod_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.all_mod_PVs]
        self.interlock_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.interlock_PVs]
        self.pv_idx_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.pv_idx_dict]
        self.idx_pv_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.idx_pv_dict]
        self.date_from = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.date_from]
        self.time_from = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.time_from]
        self.date_to = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.date_to]
        self.time_to = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.time_to]
        self.PLOT_ALL_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PLOT_ALL_PVs]
        #pv_name = "CLA-GUNS-HRF-MOD-01:Sys:INTLK5"

        # Call in the from and to times saved in the data dictionary originally read in from the config file
        self.EPICS_date_time_from = self.concatenate_date_time_to_EPICS_format(self.date_from, self.time_from)
        self.EPICS_date_time_to = self.concatenate_date_time_to_EPICS_format(self.date_to, self.time_to)


        # save the formatted string in the data dictionary
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.EPICS_date_time_from] = self.EPICS_date_time_from
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.EPICS_date_time_to] = self.EPICS_date_time_to

        # Initiate empty time and yaxis data lists for all PVs
        # These will end up being a list of lists
        self.PV_TIME_DATA = []
        self.PV_YAXIS_DATA = []

        for pv_idx, pv_name in enumerate(self.all_mod_PVs):

            print(f'\n\nAttempting to read {pv_name}')

            # add to the PV_idx_dict & idx_PV_dict dictionaries
            self.pv_idx_dict[pv_name] = str(pv_idx)
            self.idx_pv_dict[str(pv_idx)] = pv_name

            # Construct url from "pv_name", "EPICS_date_time_from" & "EPICS_date_time_to"
            url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + \
                  pv_name + "&from=" + self.EPICS_date_time_from + "&to=" + self.EPICS_date_time_to
            print(url)
            #Retrieve data from EPICS archiver
            r = requests.get(url)
            data = r.json() #######################################################################################<---

            # Initiate empty time and yaxis data lists for each individual PV
            # time_0 = time[0]
            # relative_time = [i - time_0 for i in time]
            # print(relative_time)

            yaxis = []
            time = []
            for event in data[0]["data"]:
                time.append(event["secs"] + event["nanos"] * 1E-9)
                yaxis.append(event["val"])

            # Append time & yaxis data
            self.PV_TIME_DATA.append(time)
            self.PV_YAXIS_DATA.append(yaxis)

            # Create a savename for the PV plot by removing the ":" character from the PV name string
            self.savename = self.remove_char_from_str(data[0]["meta"]['name'])

            # If function arguement verbose=True print out any diagnostic data required
            if self.verbose:
                print(pv_idx)
                print(url)
                print(data[0]["meta"])
                print(f'savename = {self.savename}')
                print(f'len(time) = {len(time)}\n'
                      f'len(yaxis) = {len(yaxis)}')

            # if "PLOT_ALL_PVs:  True" in config yaml then plot each and every PV individually and save in the savepath folder
            if self.PLOT_ALL_PVs:
                figs.individual_PV_plot(time, yaxis, pv_name, self.savename, pv_idx)

            else:
                print('Not plotting individual PVs')

            # Save the modulator state read again for ease of access
            if pv_name == "CLA-GUNS-HRF-MOD-01:Sys:StateRead":
                HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.mod_StateRead_time] = time
                HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.mod_StateRead_yaxis] = yaxis

            # Zero time at the time of the first modulator state change
            #self.PV_TIME_zeroed = self.zero_EPICS_time()

        # Save data to the values dictionary for use later on
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.pv_idx_dict] = self.pv_idx_dict
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.idx_pv_dict] = self.idx_pv_dict
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_TIME_DATA] = self.PV_TIME_DATA
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_YAXIS_DATA] = self.PV_YAXIS_DATA


        # for index in range(len(self.PV_TIME_DATA)):
        #     print(f'len(self.PV_TIME_DATA[self.pv_idx_{index}]) = {len(self.PV_TIME_DATA[index])}\n'
        #           f'len(self.PV_YAXIS_DATA[self.pv_idx_{index}]) = {len(self.PV_YAXIS_DATA[index])}\n')
        #
        # input()

        # Zero time at the time of the first modulator state change
        #self.zero_EPICS_time()


        # Save the values dictionary as a .pkl so that we can re-run the script without having to re-read the data.
        self.save_dict_2_pkl(HRFOv2_EPICS_data.values, r'\post_PV_read_values_dict.pkl')

    def read_gun_fault_log(self):
        '''

        :return:
        '''

        figs = figures()
        # df = data_functions()

        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.date_from = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.date_from]
        self.time_from = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.time_from]
        self.date_to = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.date_to]
        self.time_to = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.time_to]
        self.gun_FaultLog_pv = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.fault_log_PVs][0]
        self.fault_log_to_index_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.fault_log_to_index_dict]
        # pv_name = "CLA-GUNS-HRF-MOD-01:Sys:INTLK5"

        # Call in the from and to times saved in the data dictionary originally read in from the config file
        self.EPICS_date_time_from = self.concatenate_date_time_to_EPICS_format(self.date_from, self.time_from)
        self.EPICS_date_time_to = self.concatenate_date_time_to_EPICS_format(self.date_to, self.time_to)

        # save the formatted string in the data dictionary
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.EPICS_date_time_from] = self.EPICS_date_time_from
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.EPICS_date_time_to] = self.EPICS_date_time_to

        pv_name = self.gun_FaultLog_pv

        print(f'\n\nAttempting to read {pv_name}')

        # Construct url from "pv_name", "EPICS_date_time_from" & "EPICS_date_time_to"
        url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + \
              pv_name + "&from=" + self.EPICS_date_time_from + "&to=" + self.EPICS_date_time_to

        print(f'url: {url}')
        #input()
        # Retrieve data from EPICS archiver
        r = requests.get(url)
        data = r.json()  #######################################################################################<---

        # Initiate empty time and yaxis data lists for each individual PV
        # time_0 = time[0]
        # relative_time = [i - time_0 for i in time]
        # print(relative_time)

        yaxis = []
        time = []
        for event in data[0]["data"]:
            time.append(event["secs"] + event["nanos"] * 1E-9)
            yaxis.append(event["val"])

        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.raw_buffer_times] = raw_buffer_times = time
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.raw_buffers] = raw_buffers = yaxis

        time_array = np.array(time)
        print(f'time_array.shape = {time_array.shape}')
        # Create a savename for the PV plot by removing the ":" character from the PV name string
        self.savename = self.remove_char_from_str(data[0]["meta"]['name'])

        #print(url)
        #print(data[0]["meta"])
        print(f'savename = {self.savename}')
        print(f'len(time) = {len(time)}\n'
              f'len(yaxis) = {len(yaxis)}')
        print(f'type(time) = {type(time)}')

        # print(f'self.yaxis = {self.yaxis}')
        print(f'self.yaxis[-1] = {yaxis[-1]}')

        yaxis_classes = list(set(yaxis[-2]))
        print(f'yaxis_classes = {yaxis_classes}')

        all_full_buffers = []
        for idx, ls in enumerate(yaxis):
            #print(time[idx])
            # identify empty buffers
            if len(ls) == 0:
                # if the first in list ignore
                if idx != 0:
                    # append the list before the empty list to full_buffers
                    all_full_buffers.append(yaxis[idx - 1])
                else:
                    pass
            else:
                pass

        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.all_full_buffers] = all_full_buffers

        # print each full buffer list out
        for buff in all_full_buffers:
            print(f'{len(buff)}: {buff}')

    def read_gun_fault_log_quick_check(self, EPICS_date_time_from, EPICS_date_time_to):
        '''

        :return:
        '''

        figs = figures()
        # df = data_functions()

        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.EPICS_date_time_from = EPICS_date_time_from
        self.EPICS_date_time_to = EPICS_date_time_to
        self.gun_FaultLog_pv = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.fault_log_PVs][0]
        self.fault_log_to_index_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.fault_log_to_index_dict]
        # pv_name = "CLA-GUNS-HRF-MOD-01:Sys:INTLK5"

        # save the formatted string in the data dictionary
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.EPICS_date_time_from] = self.EPICS_date_time_from
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.EPICS_date_time_to] = self.EPICS_date_time_to

        pv_name = self.gun_FaultLog_pv

        print(f'\n\nAttempting to read {pv_name}')

        # Construct url from "pv_name", "EPICS_date_time_from" & "EPICS_date_time_to"
        url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + \
              pv_name + "&from=" + self.EPICS_date_time_from + "&to=" + self.EPICS_date_time_to

        # Retrieve data from EPICS archiver

        print(f'url: {url}')
        r = requests.get(url)
        data = r.json()  #######################################################################################<---

        # Initiate empty time and yaxis data lists for each individual PV
        # time_0 = time[0]
        # relative_time = [i - time_0 for i in time]
        # print(relative_time)

        yaxis = []
        time = []
        for event in data[0]["data"]:
            time.append(event["secs"] + event["nanos"] * 1E-9)
            yaxis.append(event["val"])

        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.raw_buffer_times_quick_check] = raw_buffer_times = time
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.raw_buffers_quick_check] = raw_buffers = yaxis




    def read_EPICS_PVs_for_HV_interlock_periods(self):
        '''
        Reads in every PV in the "all_mod_PVs" list for each HV interlock period created by create_to_and_from_times_from_HV_interlock_timestams()
        saves the time data and the yaxis data
        overplots each individual PVs yaxis data as a function of time
        :param verbose: if True then function prints out attributes for diagnostics.
        :return:
        '''

        figs = figures()
        utils = utilities()
        #self.savepath = f'{HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]}\\HV_interlock_PV_overplots'
        self.savepath = utils.create_bespoke_folder_name('HV_interlock_PV_overplots')
        print(f'self.savepath from read_EPICS_PVs_for_HV_interlock_periods() = {self.savepath}')
        self.all_mod_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.all_mod_PVs]
        self.pv_idx_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.pv_idx_dict]
        self.idx_pv_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.idx_pv_dict]
        self.HV_interlock_EICS_date_time_from = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.HV_interlock_EICS_date_time_from]
        self.HV_interlock_EICS_date_time_to = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.HV_interlock_EICS_date_time_to]

        for pv_idx, pv_name in enumerate(self.all_mod_PVs):

            # Create a savename for the PV plot by removing the ":" character from the PV name string
            #self.savename = self.remove_char_from_str(data[0]["meta"]['name'])
            #print(f'pv_name = {pv_name}')
            self.savename = self.remove_char_from_str(pv_name)
            print(f'self.savename = {self.savename}')
            #input('Press key to continue ...')

            HV_PV_overplot_time_data = []
            HV_PV_overplot_yaxis_data = []

            for HV_idx, HV_from in enumerate(self.HV_interlock_EICS_date_time_from):

                print(f'Reading {pv_name} for period starting {HV_from}')

                # add to the PV_idx_dict & idx_PV_dict dictionaries
                self.pv_idx_dict[pv_name] = str(pv_idx)
                self.idx_pv_dict[str(pv_idx)] = pv_name

                # Construct url from "pv_name", "EPICS_date_time_from" & "EPICS_date_time_to"
                url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + \
                      pv_name + "&from=" + HV_from + "&to=" + self.HV_interlock_EICS_date_time_to[HV_idx]



                #Retrieve data from EPICS archiver
                r = requests.get(url)
                data = r.json() #######################################################################################<---

                # if pv_name == "CLA-GUNS-HRF-MOD-01SysRemainingTime":
                #     print(f'url = {url}')
                #     print(type(data))
                #     input('Press any key to continue....')

                yaxis = []
                time = []
                for event in data[0]["data"]:
                    time.append(event["secs"] + event["nanos"] * 1E-9)
                    yaxis.append(event["val"])

                # normalise time for overplotting
                time_0 = time[0]
                relative_time = [i - time_0 for i in time]


                # Append time & yaxis data
                HV_PV_overplot_time_data.append(relative_time)
                HV_PV_overplot_yaxis_data.append(yaxis)

            figs.overplot_HV_PV_data(HV_PV_overplot_time_data, HV_PV_overplot_yaxis_data, pv_name, self.savepath, self.savename, pv_idx)

    def read_EPICS_PVs_for_single_HV_interlock_period(self):
        '''
        Reads in every PV in the "all_mod_PVs" list for each HV interlock period created by create_to_and_from_times_from_HV_interlock_timestams()
        saves the time data and the yaxis data
        overplots each individual PVs yaxis data as a function of time
        :param verbose: if True then function prints out attributes for diagnostics.
        :return:
        '''

        figs = figures()
        utils = utilities()
        #self.savepath = f'{HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]}\\HV_interlock_PV_overplots'
        self.savepath = utils.create_bespoke_folder_name('HV_interlock_PV_subplots')
        print(f'self.savepath from read_EPICS_PVs_for_HV_interlock_periods() = {self.savepath}')
        self.interlock_pv_fault_to_index_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.interlock_pv_fault_to_index_dict]
        self.HV_interlock_comparison_PVs_raw = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.HV_interlock_comparison_PVs]
        self.INCLUDE_INTERLOCK_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.INCLUDE_INTERLOCK_PVs]
        self.interlock_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.interlock_PVs]
        self.HV_interlock_times_FaultLog = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.HV_interlock_times_FaultLog]
        self.HV_interlock_EICS_date_time_from = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.HV_interlock_EICS_date_time_from]
        self.HV_interlock_EICS_date_time_to = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.HV_interlock_EICS_date_time_to]

        if self.INCLUDE_INTERLOCK_PVs:
            print(f'self.interlock_PVs = {self.interlock_PVs}')
            print(f'len(self.HV_interlock_comparison_PVs) before = {len(self.HV_interlock_comparison_PVs_raw)}')
            self.HV_interlock_comparison_PVs = self.HV_interlock_comparison_PVs_raw + self.interlock_PVs
            print(f'len(self.HV_interlock_comparison_PVs) after = {len(self.HV_interlock_comparison_PVs)}')
            HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.HV_interlock_comparison_PVs] = self.HV_interlock_comparison_PVs
        else:
            self.HV_interlock_comparison_PVs = self.HV_interlock_comparison_PVs_raw

        for HV_idx, HV_from in enumerate(self.HV_interlock_EICS_date_time_from):

            # Create a savename for the PV plot by removing the ":" character from the PV name string
            #self.savename = self.remove_char_from_str(data[0]["meta"]['name'])
            #print(f'pv_name = {pv_name}')
            self.savename = self.remove_char_from_str(str(self.HV_interlock_EICS_date_time_from[HV_idx]))
            print(f'self.savename = {self.savename}')
            # print(f'self.HV_interlock_times_FaultLog = {self.HV_interlock_times_FaultLog}')
            # input('Press key to continue ...')

            HV_PV_subplot_time_data = []
            HV_PV_subplot_yaxis_data = []


            for pv_idx, pv_name in enumerate(self.HV_interlock_comparison_PVs):

                #print(f'Reading {pv_name} for period starting {HV_from}')


                # Construct url from "pv_name", "EPICS_date_time_from" & "EPICS_date_time_to"
                url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + \
                      pv_name + "&from=" + HV_from + "&to=" + self.HV_interlock_EICS_date_time_to[HV_idx]

                print(f'url = {url}')

                #Retrieve data from EPICS archiver
                # r = requests.get(url)
                # data = r.json()
                data = requests.get(url).json()

                yaxis = []
                time = []
                for event in data[0]["data"]:
                    time.append(event["secs"] + event["nanos"] * 1E-9)
                    yaxis.append(event["val"])

                if pv_name in self.interlock_PVs:
                    print(f'yaxis[:7] = {yaxis[:7]}')
                    yaxis = [self.interlock_pv_fault_to_index_dict[i[0]] for i in yaxis]
                    print(f'yaxis[:7] = {yaxis[:7]}')

                # normalise time for overplotting
                time_0 = self.HV_interlock_times_FaultLog[HV_idx]
                relative_time = [i - time_0 for i in time]

                # Append time & yaxis data

                HV_PV_subplot_time_data.append(relative_time)
                HV_PV_subplot_yaxis_data.append(yaxis)

            figs.subplot_HV_PV_data(HV_PV_subplot_time_data, HV_PV_subplot_yaxis_data,
                                    self.HV_interlock_times_FaultLog[HV_idx],
                                    self.savepath,
                                    self.savename)

    def read_EPICS_PVs_for_single_chosen_interlock_period(self):
        '''
        Reads in every PV in the "all_mod_PVs" list for each chosen interlock period created by create_to_and_from_times_from_HV_interlock_timestams()
        saves the time data and the yaxis data
        overplots each individual PVs yaxis data as a function of time
        :param verbose: if True then function prints out attributes for diagnostics.
        :return:
        '''

        figs = figures()
        utils = utilities()
        self.interlock_choce = reader._DATA.values[reader._DATA.interlock_choice]
        print(f'self.interlock_choce = {self.interlock_choce}')
        #self.savepath = f'{HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]}\\HV_interlock_PV_overplots'
        self.savepath = utils.create_bespoke_folder_name(f'{self.interlock_choce}_interlock_PV_subplots')

        print(f'self.savepath from read_EPICS_PVs_for_HV_interlock_periods() = {self.savepath}')
        self.interlock_pv_fault_to_index_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.interlock_pv_fault_to_index_dict]
        self.chosen_interlock_comparison_PVs_raw = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.chosen_interlock_comparison_PVs]
        self.INCLUDE_INTERLOCK_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.INCLUDE_INTERLOCK_PVs]
        self.interlock_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.interlock_PVs]
        self.chosen_interlock_times_FaultLog = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.chosen_interlock_times_FaultLog]
        self.chosen_interlock_EICS_date_time_from = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.chosen_interlock_EICS_date_time_from]
        self.chosen_interlock_EICS_date_time_to = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.chosen_interlock_EICS_date_time_to]

        if self.INCLUDE_INTERLOCK_PVs:
            print(f'self.interlock_PVs = {self.interlock_PVs}')
            print(f'len(self.chosen_interlock_comparison_PVs_raw) before = {len(self.chosen_interlock_comparison_PVs_raw)}')
            self.chosen_interlock_comparison_PVs = self.chosen_interlock_comparison_PVs_raw + self.interlock_PVs
            print(f'len(self.chosen_interlock_comparison_PVs) after = {len(self.chosen_interlock_comparison_PVs)}')
            HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.chosen_interlock_comparison_PVs] = self.chosen_interlock_comparison_PVs
        else:
            self.chosen_interlock_comparison_PVs = self.chosen_interlock_comparison_PVs_raw

        for INTLK_idx, INTLK_from in enumerate(self.chosen_interlock_EICS_date_time_from):

            # Create a savename for the PV plot by removing the ":" character from the PV name string
            #self.savename = self.remove_char_from_str(data[0]["meta"]['name'])
            #print(f'pv_name = {pv_name}')
            self.savename = self.remove_char_from_str(str(self.chosen_interlock_EICS_date_time_from[INTLK_idx]))
            print(f'self.savename = {self.savename}')
            # print(f'self.chosen_interlock_times_FaultLog = {self.chosen_interlock_times_FaultLog}')
            # input('Press key to continue ...')

            chosen_interlock_PV_subplot_time_data = []
            chosen_interlock_PV_subplot_yaxis_data = []


            for pv_idx, pv_name in enumerate(self.chosen_interlock_comparison_PVs):



                #print(f'Reading {pv_name} for period starting {chosen_from}')
                # Construct url from "pv_name", "EPICS_date_time_from" & "EPICS_date_time_to"
                url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + \
                      pv_name + "&from=" + INTLK_from + "&to=" + self.chosen_interlock_EICS_date_time_to[INTLK_idx]

                print(f'url = {url}')

                #Retrieve data from EPICS archiver
                # r = requests.get(url)
                # data = r.json()
                data = requests.get(url).json()

                yaxis = []
                time = []
                for event in data[0]["data"]:
                    if pv_name == "CLA-GUNS-RFHOLD:FaultLog":
                        self.buffers_1D_times = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.buffers_1D_times]
                        self.buffers_1D_one_hot = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.buffers_1D_one_hot]
                        time = (self.buffers_1D_times)
                        yaxis = (self.buffers_1D_one_hot)
                        # print(f'self.buffers_1D_times = {self.buffers_1D_times}\n'
                        #       f'self.buffers_1D_one_hot = {self.buffers_1D_one_hot}')
                        #input()
                    else:
                        time.append(event["secs"] + event["nanos"] * 1E-9)
                        yaxis.append(event["val"])

                if pv_name in self.interlock_PVs:
                    print(f'yaxis[:7] = {yaxis[:7]}')
                    yaxis = [self.interlock_pv_fault_to_index_dict[i[0]] for i in yaxis]
                    print(f'yaxis[:7] = {yaxis[:7]}')

                # normalise time for overplotting
                time_0 = self.chosen_interlock_times_FaultLog[INTLK_idx]
                relative_time = [i - time_0 for i in time]

                # Append time & yaxis data
                chosen_interlock_PV_subplot_time_data.append(relative_time)
                chosen_interlock_PV_subplot_yaxis_data.append(yaxis)

            print(f'chosen_interlock_PV_subplot_yaxis_data[0] = {chosen_interlock_PV_subplot_yaxis_data[0]}')

            figs.subplot_chosen_PV_data(chosen_interlock_PV_subplot_time_data, chosen_interlock_PV_subplot_yaxis_data,
                                    self.chosen_interlock_times_FaultLog[INTLK_idx],
                                    self.savepath,
                                    self.savename)






    def zero_EPICS_time(self):
        '''
        Returns a time line from 0 seconds (start date+time read in from config.yaml) to the end date+time
        in units of seconds.
        :return:
        '''
        self.mod_state_time = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.mod_StateRead_time]
        self.PV_TIME_DATA = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_TIME_DATA]
        self.time_0 = self.mod_state_time[0]
        self.PV_TIME_zeroed = []
        for t_idx, t in enumerate(self.PV_TIME_DATA):
            pv_time_zeroed = [i - self.time_0 for i in self.PV_TIME_DATA[t_idx]]
            self.PV_TIME_zeroed.append(pv_time_zeroed)

        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_TIME_zeroed] = self.PV_TIME_zeroed


    def read_interlock_PVs(self):
        '''
        Specific reader for the interlock PVs
        interlock_PVs:
         - "CLA-GUNS-HRF-MOD-01:Sys:INTLK1"
         - "CLA-GUNS-HRF-MOD-01:Sys:INTLK2"
         - "CLA-GUNS-HRF-MOD-01:Sys:INTLK3"
         - "CLA-GUNS-HRF-MOD-01:Sys:INTLK4"
         - "CLA-GUNS-HRF-MOD-01:Sys:INTLK5"
        :return:
        '''

        figs = figures()
        # df = data_functions()

        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.interlock_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.interlock_PVs]
        self.interlock_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.interlock_PVs]
        self.pv_idx_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.pv_idx_dict]
        self.idx_pv_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.idx_pv_dict]
        self.date_from = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.date_from]
        self.time_from = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.time_from]
        self.date_to = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.date_to]
        self.time_to = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.time_to]
        self.PLOT_ALL_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PLOT_ALL_PVs]
        # pv_name = "CLA-GUNS-HRF-MOD-01:Sys:INTLK5"

        # Call in the from and to times saved in the data dictionary originally read in from the config file
        self.EPICS_date_time_from = self.concatenate_date_time_to_EPICS_format(self.date_from, self.time_from)
        self.EPICS_date_time_to = self.concatenate_date_time_to_EPICS_format(self.date_to, self.time_to)

        # save the formatted string in the data dictionary
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.EPICS_date_time_from] = self.EPICS_date_time_from
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.EPICS_date_time_to] = self.EPICS_date_time_to

        # Initiate empty time and yaxis data lists for all PVs
        # These will end up being a list of lists
        self.PV_TIME_DATA = []
        self.PV_YAXIS_DATA = []

        for pv_idx, pv_name in enumerate(self.interlock_PVs):

            print(f'\n\nAttempting to read {pv_name}')

            # add to the PV_idx_dict & idx_PV_dict dictionaries
            self.pv_idx_dict[pv_name] = str(pv_idx)
            self.idx_pv_dict[str(pv_idx)] = pv_name

            # Construct url from "pv_name", "EPICS_date_time_from" & "EPICS_date_time_to"
            url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + \
                  pv_name + "&from=" + self.EPICS_date_time_from + "&to=" + self.EPICS_date_time_to

            # Retrieve data from EPICS archiver
            r = requests.get(url)
            data = r.json()  #######################################################################################<---

            # Initiate empty time and yaxis data lists for each individual PV
            # time_0 = time[0]
            # relative_time = [i - time_0 for i in time]
            # print(relative_time)

            yaxis = []
            time = []
            for event in data[0]["data"]:
                time.append(event["secs"] + event["nanos"] * 1E-9)
                yaxis.append(event["val"])

            # Append time & yaxis data
            self.PV_TIME_DATA.append(time)
            self.PV_YAXIS_DATA.append(yaxis)

            # Create a savename for the PV plot by removing the ":" character from the PV name string
            self.savename = self.remove_char_from_str(data[0]["meta"]['name'])

            # If function arguement verbose=True print out any diagnostic data required

            print(pv_idx)
            print(url)
            print(data[0]["meta"])
            print(f'savename = {self.savename}')
            print(f'len(time) = {len(time)}\n'
                  f'len(yaxis) = {len(yaxis)}')
            print(f'time[:15] = {time[:15]}\n'
                  f'yaxis[:1000] = {yaxis[:1000]}')

            delta_times = [time[i+1] - time[i] for i in range(len(time)-1)]

            print(f'delta_times[:1000] = {delta_times[:1000]}')

            plt.hist(delta_times, bins=300, range=(0.0, 3.0), histtype='step', color='k', lw=1.2)
            plt.savefig(self.savepath + '\\' + f'Interlock_PV_{pv_idx}_delta_times.png')
            plt.close('all')

            # scan yaxis values for anything meaningful
            dash = 0
            no_error = 0
            misc = []
            for i in yaxis:
                for j in i:
                    if j == '-':
                        dash += 1
                    elif j == 'No Error':
                        no_error += 1
                    else:
                        #print(j)
                        misc.append(j)

            print(f'len(misc) = {len(misc)}')


            misc_classes = list(set(misc))
            print(f'misc_classes = {misc_classes}')




            # if "PLOT_ALL_PVs:  True" in config yaml then plot each and every PV individually and save in the savepath folder
            if self.PLOT_ALL_PVs:
                figs.individual_PV_plot(time, yaxis, pv_name, self.savename, pv_idx)

            else:
                print('Not plotting individual PVs')



        # Save data to the values dictionary for use later on
        # HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.pv_idx_dict] = self.pv_idx_dict
        # HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.idx_pv_dict] = self.idx_pv_dict
        # HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_TIME_DATA] = self.PV_TIME_DATA
        # HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_YAXIS_DATA] = self.PV_YAXIS_DATA
        #
        # # for index in range(len(self.PV_TIME_DATA)):
        # #     print(f'len(self.PV_TIME_DATA[self.pv_idx_{index}]) = {len(self.PV_TIME_DATA[index])}\n'
        # #           f'len(self.PV_YAXIS_DATA[self.pv_idx_{index}]) = {len(self.PV_YAXIS_DATA[index])}\n')
        # #
        # # input()
        #
        # # Zero time at the time of the first modulator state change
        # # self.zero_EPICS_time()
        #
        # # Save the values dictionary as a .pkl so that we can re-run the script without having to re-read the data.
        # self.save_dict_2_pkl(HRFOv2_EPICS_data.values, r'\post_PV_read_values_dict.pkl')


    def PCorllett_read_EPICS_PVs(self):
        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.PVs = ['CLA-GUN-LRF-CTRL-01:ad1:ch1:Power:Wnd:Avg', 'CLA-GUN-LRF-CTRL-01:ad1:ch3:Power:Wnd:Avg']
        self.interlock_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.interlock_PVs]

        #pv_name = "CLA-GUNS-HRF-MOD-01:Sys:INTLK5"

        # Define the from and to times
        time_from = "2021-01-19T10:00:00.00Z"
        time_to = "2021-01-25T14:00:00.00Z"

        self.X_DATA = []
        self.Y_DATA = []

        for pv_idx, pv_name in enumerate(self.PVs):

            print('\n', pv_idx)
            url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + pv_name + "&from=" + time_from + "&to=" + time_to
            print(url)

            r = requests.get(url)
            data = r.json()

            yaxis = []
            time = []
            for event in data[0]["data"]:
                time.append(event["secs"] + event["nanos"] * 1E-9)
                yaxis.append(event["val"])

            self.X_DATA.append(time)
            self.Y_DATA.append(yaxis)

            print(data[0]["meta"])

            savename = data[0]["meta"]['name'][0:19]
            print(self.savepath + "\\" + savename + r".png")

            plt.plot(time, yaxis, ls='-', lw=1.0, color='b')
            plt.scatter(time, yaxis, marker='o', s=3.0, c='r')
            # plt.ylabel(data[0]["meta"]["EGU"])
            plt.title(data[0]["meta"]['name'])
            plt.ylabel(data[0]["meta"]['name'])
            plt.xlabel("Time Since Epics Epoch")
            plt.savefig(self.savepath + "\\" + savename + f"_pv_{pv_idx}_Z.png")
            plt.close('all')

        print(f'len(self.Y_DATA[0]) = {len(self.Y_DATA[0])}')
        print(f'len(self.Y_DATA[1]) = {len(self.Y_DATA[1])}')

        lengths = [len(self.Y_DATA[0]), len(self.Y_DATA[1])]
        length = int(min(lengths))

        self.Y_data_ratio = [self.Y_DATA[0][i] / self.Y_DATA[1][i] for i in range(length)]
        plt.plot(self.X_DATA[0][0:length], self.Y_data_ratio, ls='-', lw=1.0, color='b')
        plt.scatter(self.X_DATA[0][0:length], self.Y_data_ratio, marker='o', s=3.0, c='r')
        # plt.ylabel(data[0]["meta"]["EGU"])
        #plt.title(data[0]["meta"]['name'])
        #plt.ylabel(data[0]["meta"]['name'])
        plt.ylim(0.0, 3.0)
        plt.xlabel("Time Since Epics Epoch")
        plt.savefig(self.savepath + "\\" + "Insertion_loss.png")
        plt.close('all')

        # sub plots:

        PV_idx_0 = 0
        PV_idx_1 = 1

        fig, axs = plt.subplots(2)
        #fig.suptitle(f'{self.all_mod_PVs[PV_idx_0]}\n{self.all_mod_PVs[PV_idx_1]}')
        axs[0].plot(self.X_DATA[PV_idx_0], self.Y_DATA[PV_idx_0], ls='-', lw=1.0, color='b')
        axs[0].scatter(self.X_DATA[PV_idx_0], self.Y_DATA[PV_idx_0], marker='o', s=3.0, c='r')
        axs[1].plot(self.X_DATA[PV_idx_1], self.Y_DATA[PV_idx_1], ls='-', lw=1.0, color='b')
        axs[1].scatter(self.X_DATA[PV_idx_1], self.Y_DATA[PV_idx_1], marker='o', s=3.0, c='r')
        plt.savefig(self.savepath + f"\\Insertion_loss_{PV_idx_0}_{PV_idx_1}.png")
        plt.close('all')


    def save_dict_2_pkl(self, dict_to_save, savename):
        '''
        Saves python dictionary as .pkl
        :param dict_to_save: Which dictionary to save
        :param savename: String of the form r'\post_PV_read_values_dict.pkl'
        :return:
        '''
        self.dict_to_save = dict_to_save
        self.savename = savename
        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]

        with open(self.savepath + self.savename, 'wb') as handle:
            pkl.dump(self.dict_to_save, handle, protocol=pkl.HIGHEST_PROTOCOL)

        print(f'\nSaved {self.savename} in {self.savepath}\n')

    def load_post_PV_read_pkl_2_dict(self, savename):
        '''
        Reads in .pkl and converts it to a Python dictionary.
        :param savename: String of the form r'\post_PV_read_values_dict.pkl'
        :return:
        '''
        self.savename = savename
        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]

        with open(self.savepath + self.savename, 'rb') as handle:
            self.dict = pkl.load(handle)

        HRFOv2_EPICS_data.values = self.dict

        print(f'\nLoaded "{self.savename[1:]}" from {self.savepath}\n')

    def save_two_lists_txt(self, list_1, list_2, savename):
        '''
        Generic function that saves 2 lists as a .txt file.
        :param list_1:
        :param list_2: same length as list 1
        :param savename: excluding the .txt suffix eg r'\best_fit_line'
        :return:
        '''
        self.list_1 = list_1
        self.list_2 = list_2
        self.savename = savename
        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]

        f = open(self.savepath + self.savename + ".csv", "w")
        for i in range(len(self.list_1)):
            f.write(f"{self.list_1[i]}      {self.list_2[i]}\n")

        f.close()

        print(f'\n{self.savename}.txt saved')

    def save_two_lists_csv(self, list_1, list_2, savename):
        '''
        Generic function that saves 2 lists as a .csv file.
        :param list_1:
        :param list_2: same length as list 1
        :param savename: excluding the .csv suffix eg r'\best_fit_line'
        :return:
        '''
        self.list_1 = list_1
        self.list_2 = list_2
        self.savename = savename
        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]

        f = open(self.savepath + self.savename + ".csv", "w")
        for i in range(len(self.list_1)):
            f.write(f"{self.list_1[i]},{self.list_2[i]}\n")

        f.close()

        print(f'\n{self.savename}.csv saved')

    def save_mod_state_names_and_populations_to_csv(self, list_1, list_2, savename):
        '''
        Specific function that save modulator state names of a group
        and the population of that group type to csv in the format:
        :param list_1: list of lists of the modulator state numbers.
        :param list_2: List of population size for each group type. Same length as list 1.
        :param savename: excluding the .csv suffix eg r'\best_fit_line'
        :return:
        '''

        self.list_1 = list_1
        self.list_2 = list_2
        self.savename = savename
        self.mod_state_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.mod_state_dict]
        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.max_length = len(self.list_2)

        f = open(self.savepath + self.savename + ".csv", "w")
        f.write(f"Group Index,Group Population,Mod States\n")
        for Group_list_idx, group_list in enumerate(self.list_1):
            group_length = len(group_list)
            for mod_state_idx, mod_state_number in enumerate(group_list):

                name = self.mod_state_dict[str(mod_state_number)]
                if mod_state_idx == 0:
                    f.write(f"\n{Group_list_idx},{self.list_2[Group_list_idx]},{name}\n")
                elif mod_state_idx == group_length:
                    f.write(f", ,{name}\n\n")
                else:
                    f.write(f", ,{name}\n")

        f.close()

    def print_dictionaries_to_text_file(self, list_of_dicts_objects, list_of_dicts_names):
        '''
        Prints dictionaries to text file for ease of reference when interpreting plots
        :param list_of_dicts: [dict_1, dict_2,, dict_13, ... ,dict_n]
        :return:
        '''
        self.list_of_dicts_objects = list_of_dicts_objects
        self.list_of_dicts_names = list_of_dicts_names
        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.txt_file_name = f'{self.savepath}\\Dictionary_keys.txt'
        self.text_file_obj = open(self.txt_file_name, 'w')

        for d_idx, d in enumerate(self.list_of_dicts_objects):
            self.text_file_obj.write(f'{self.list_of_dicts_names[d_idx]}\n\n')
            for key, val in d.items():
                self.text_file_obj.write(f'{val}:   {key}\n')

            self.text_file_obj.write('\n\n\n')

        self.text_file_obj.close()