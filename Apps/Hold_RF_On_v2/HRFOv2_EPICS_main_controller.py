from matplotlib import pyplot as plt
from decimal import *
import numpy as np, cmath
import time, csv, os, sys
import HRFOv2_EPICS_data
from HRFOv2_EPICS_reader import reader
from HRFOv2_EPICS_data import data_functions
from HRFOv2_EPICS_figures import figures
from HRFOv2_EPICS_utils import utilities

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

        figs.subplots_2(3, 1)

        figs.subplots_3(3, 2, 1)
        figs.triple_yaxis_plot(3, 2, 1)

        # enter PV indeces as a list, eg [1, 2, 3, 4]
        figs.subplots_x([3, 2, 1, 0])

        # Scan mod StateRead for groups
        df.scan_data_for_groups()

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
