from matplotlib import pyplot as plt
from decimal import *
import numpy as np, cmath
import time, csv
import HRFOv2_EPICS_data
from HRFOv2_EPICS_reader import reader
from HRFOv2_EPICS_data import data_functions
from HRFOv2_EPICS_figures import figures
class main_controller():
    '''
    The main routine that runs sequentially
    '''

    def __init__(self):
        print('Initiated main_controller()')


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

        figs.subplots_2(29, 1)

        figs.subplots_3(36, 26, 1)
        figs.triple_yaxis_plot(36, 26, 1)
        figs.subplots_x([36, 26, 1, 29])
