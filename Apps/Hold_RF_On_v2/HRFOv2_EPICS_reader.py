import yaml, sys, csv, requests
import numpy as np
from decimal import *
import pickle as pkl
import HRFOv2_EPICS_data
from matplotlib import pyplot as plt

from HRFOv2_EPICS_figures import figures
from HRFOv2_EPICS_data import  data_functions

getcontext().prec = 100

class reader():
    '''
    Class that handles reading in any data files like .yml, .txt, .csv, .pkl etc...
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
                    HRFOv2_EPICS_data.values[str(key)] = val
                    print(f'key = {key}, val = {val}')

                else:
                    print(f'{key} not yet added to all_value_keys list in HRFOv2_EPICS_data.py')
                    sys.exit()

    def read_EPICS_PVs(self, verbose=True):
        '''

        :param verbose: if True then function prints out attributes for diagnostics.
        :return:
        '''

        figs = figures()
        df = data_functions()
        self.verbose = verbose
        self.savepath = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
        self.all_mod_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.all_mod_PVs]
        self.interlock_PVs = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.interlock_PVs]
        self.PV_idx_dict = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_idx_dict]

        #pv_name = "CLA-GUNS-HRF-MOD-01:Sys:INTLK5"

        # Define the from and to times
        time_from = "2021-01-19T10:00:00.00Z"
        time_to = "2021-01-21T14:00:00.00Z"

        self.PV_TIME_DATA = []
        self.PV_YAXIS_DATA = []

        for pv_idx, pv_name in enumerate(self.all_mod_PVs):

            self.PV_idx_dict[pv_name] = str(pv_idx)

            url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + pv_name + "&from=" + time_from + "&to=" + time_to


            r = requests.get(url)
            data = r.json()

            yaxis = []
            time = []
            for event in data[0]["data"]:
                time.append(event["secs"] + event["nanos"] * 1E-9)
                yaxis.append(event["val"])

            self.PV_TIME_DATA.append(time)
            self.PV_YAXIS_DATA.append(yaxis)

            self.savename = df.remove_char_from_str(data[0]["meta"]['name'])

            if self.verbose:
                print('\n', pv_idx)
                print(url)
                print(data[0]["meta"])
                print(f'savename_2 = {self.savename}')

            figs.individual_PV_plot(time, yaxis, pv_name, self.savename, pv_idx)

        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_idx_dict] = self.PV_idx_dict
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_TIME_DATA] = self.PV_TIME_DATA
        HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.PV_YAXIS_DATA] = self.PV_YAXIS_DATA

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