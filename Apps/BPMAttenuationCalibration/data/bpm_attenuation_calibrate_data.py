import numpy as np
import matplotlib.pyplot as plt
import bpm_attenuation_calibrate_data_base as dat


class bpm_attenuation_calibrate_data(dat.bpm_attenuation_calibrate_data_base):
    # whoami
    my_name = 'bpm_attenuation_calibrate_data'

    main_monitor_states = {}
    previous_main_monitor_states = {}

    def __init__(self):
        dat.bpm_attenuation_calibrate_data_base.__init__(self)
        self.values = dat.bpm_attenuation_calibrate_data_base.values