import yaml, sys, csv, requests, re
import numpy as np
from decimal import *
import pickle as pkl
import HRFOv2_EPICS_data
from matplotlib import pyplot as plt

from HRFOv2_EPICS_figures import figures
#from HRFOv2_EPICS_data import  data_functions

getcontext().prec = 100

class reader():
    '''
    Class that handles reading in & writing any data files like .yml, .txt, .csv, .pkl etc...
    '''

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

            # add to the PV_idx_dict & idx_PV_dict dictionaries
            self.pv_idx_dict[pv_name] = str(pv_idx)
            self.idx_pv_dict[str(pv_idx)] = pv_name

            # Construct url from "pv_name", "EPICS_date_time_from" & "EPICS_date_time_to"
            url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + \
                  pv_name + "&from=" + self.EPICS_date_time_from + "&to=" + self.EPICS_date_time_to

            #Retrieve data from EPICS archiver
            r = requests.get(url)
            data = r.json()

            # Initiate empty time and yaxis data lists for each individual PV
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
                print('\n', pv_idx)
                print(url)
                print(data[0]["meta"])
                print(f'savename = {self.savename}')

            # if "PLOT_ALL_PVs:  True" in config yaml then plot each and every PV individually and save in the savepath folder
            if self.PLOT_ALL_PVs:
                figs.individual_PV_plot(time, yaxis, pv_name, self.savename, pv_idx)

            else:
                print('Not plotting individual PVs')

            # Save the modulator state read again for ease of access
            if pv_name == "CLA-GUNS-HRF-MOD-01:Sys:StateRead":
                HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.mod_StateRead_time] = time
                HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.mod_StateRead_yaxis] = yaxis

        # Save data to the values dictionary for use later on
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.pv_idx_dict] = self.pv_idx_dict
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.idx_pv_dict] = self.idx_pv_dict
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_TIME_DATA] = self.PV_TIME_DATA
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_YAXIS_DATA] = self.PV_YAXIS_DATA

        # Save the values dictionary as a .pkl so that we can re-run the script without having to re-read the data.
        self.save_dict_2_pkl(HRFOv2_EPICS_data.values, r'\post_PV_read_values_dict.pkl')



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
        :param savename: excluding the .csv suffix eg '\best_fit_line'
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