from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QObject
import datetime
import numpy as np
import matplotlib.pyplot as plt
from data.config_reader import config_reader


# keys for all the data we monitor
time_stamp = 'time_stamp'
bunch_charge = 'bunch_charge'
charge_name = 'charge_name'
blm_names = 'bpm_names'
blm_status = 'blm_status'
blm_voltages = 'blm_voltages'
charge_status = 'charge_status'
scan_status = 'scan_status'
charge_monitoring = 'charge_monitoring'
all_values_set = 'all_values_set'
ready_to_go = 'ready_to_go'
charge_values = 'charge_values'
num_shots = 'num_shots'
plots_done = 'plots_done'
values_saved = 'values_saved'
machine_mode = 'machine_mode'
scan_log = 'scan_log'
scan_type = 'scan_type'

all_value_keys = [time_stamp,
                  bunch_charge,
                  blm_names,
                  blm_status,
                  charge_name,
                  charge_status,
                  scan_status,
                  charge_monitoring,
                  all_values_set,
                  ready_to_go,
                  charge_values,
                  scan_status,
                  blm_voltages,
                  plots_done,
                  values_saved,
                  machine_mode,
                  scan_log,
                  scan_type
                  ]

class blm_plotter_data_base(QObject):
    # whoami
    my_name = 'blm_plotter_data'
    # config
    config = config_reader()
    # for logging
    log_param = None
    path = None
    time = None
    log_start = None
    should_write_header = True

    values = {}
    dummy_dbl = -999.0
    dummy_str = "dummy_str"
    dummy_int = int(-999)
    dummy_long = long(-999)
    [values.update({x: 0}) for x in all_value_keys]
    values[time_stamp] = dummy_dbl
    values[bunch_charge] = dummy_dbl + 1
    values[blm_names] = []
    values[blm_status] = {}
    values[blm_voltages] = {}
    values[charge_name] = dummy_str
    values[charge_status] = False
    values[scan_status] = 'dummy_str'
    values[charge_monitoring] = dummy_str
    values[all_values_set] = False
    values[ready_to_go] = False
    values[charge_values] = []
    values[plots_done] = False
    values[values_saved] = False
    values[machine_mode] = dummy_str
    values[scan_log] = dummy_str
    values[scan_type] = dummy_str
    # amp_pwr_mean_data = {}

    #logger
    logger = None
    _bpm_config = None
    _log_config = None
    _charge_config = None

    last_fwd_kly_pwr = None
    last_amp = None

    def __init__(self):
        QObject.__init__(self)
        self.data_log_timer = QTimer()
        # self.amp_pwr_log_timer = QTimer()
        # matplot lib bplot set-up, plotting needs improving for speed...
        plt.ion()
        plt.show()

    @property
    def logger(self):
        return blm_plotter_data_base._logger
    @logger.setter
    def logger(self,value):
        blm_plotter_data_base._logger = value

    @property
    def blm_config(self):
        return blm_plotter_data_base._blm_config
    @blm_config.setter
    def blm_config(self,value):
        blm_plotter_data_base._blm_config = value

    @property
    def charge_config(self):
        return blm_plotter_data_base._charge_config
    @charge_config.setter
    def charge_config(self,value):
        blm_plotter_data_base._charge_config = value

    def start_logging(self):
        self.logger.start_data_logging()
        self.data_log_timer.timeout.connect(self.data_log)
        self.data_log_timer.start(100)

    def timestamp(self):
        ts = datetime.datetime.now() - self.logger.log_start
        #print 'time = ' + str(ts.total_seconds())
        blm_plotter_data_base.values[time_stamp] = ts.total_seconds()

    def data_log(self):
        self.timestamp()
        if self.should_write_header:
            self.logger.write_data_log_header(blm_plotter_data_base.values)
            self.should_write_header = False
        self.logger.write_data(blm_plotter_data_base.values)