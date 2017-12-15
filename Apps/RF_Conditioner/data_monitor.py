# DJS Sept 2017
#
# data monitor
# monitors all the single number data to be regularly recorded
#
# base-class
from monitor import monitor
from numpy import mean
from PyQt4.QtCore import pyqtSignal


class data_monitor(monitor):

    def __init__(self, gen_mon, pv = '',
                 vac_spike_delta = 1e-9,
                 vac_spike_decay_level = 1.1,
                 vac_num_samples_to_average = 3 ):
        # init base-class
        # super(monitor, self).__init__()
        monitor.__init__(self)

    # cavity temp
    # pulse width
    # set rf amp
    # sol
    #
    #
    # trace mean values (over a particular range
    # need to set mean star and stop index, c++ functions
    # these will change with pulse width