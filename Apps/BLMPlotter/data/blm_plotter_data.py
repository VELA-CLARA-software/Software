import numpy as np
import matplotlib.pyplot as plt
import blm_plotter_data_base as dat


class blm_plotter_data(dat.blm_plotter_data_base):
    # whoami
    my_name = 'blm_plotter_data'

    main_monitor_states = {}
    previous_main_monitor_states = {}

    def __init__(self):
        dat.blm_plotter_data_base.__init__(self)
        self.values = dat.blm_plotter_data_base.values