from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QObject
import datetime
import numpy as np
import collections
import matplotlib.pyplot as plt
from data.config_reader import config_reader
from scipy import constants


# keys for all the data we monitor
blm_name = 'blm_name'
time_stamp = 'time_stamp'
bunch_charge = 'bunch_charge'
charge_name = 'charge_name'
blm_names = 'blm_names'
blm_pvs = 'blm_pvs'
blm_time_pvs = 'blm_time_pvs'
blm_waveform_pvs = 'blm_waveform_pvs'
blm_status = 'blm_status'
blm_voltages = 'blm_voltages'
blm_buffer = 'blm_buffer'
blm_time_buffer = 'blm_time_buffer'
blm_distance_start = 'blm_distance_start'
blm_distance_end = 'blm_distance_end'
blm_time = 'blm_time'
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
num_shots = 'num_shots'
num_shots_request = 'num_shots_request'
scan_type = 'scan_type'
has_blm_data = 'has_blm_data'
blm_num_values = 'blm_num_values'
save_request = 'save_request'
blm_buffer_full = 'blm_buffer_full'
charge_buffer_full = 'charge_buffer_full'
buffers_full = 'buffers_full'
buffer_message = 'buffer_message'
noise_data = 'noise_data'
single_photon_data = 'single_photon_data'
apply_filter = 'apply_filter'
blackman_size = 'blackman_size'
deconvolution_filter = 'deconvolution_filter'
has_sparsified = 'has_sparsified'
blm_object = 'blm_object'
fibre_speed = 'fibre_speed'
peak_voltages = 'peak_voltages'
calibrate_request = 'calibrate_request'
calibrate_channel_names = 'calibrate_channel_names'
str_to_pv = 'str_to_pv'
delta_x = 'delta_x'
calibration_time = 'calibration_time'
rolling_average = 'rolling_average'
blm_voltage_average = 'blm_voltage_average'
blm_time_average = 'blm_time_average'
shot_num = 'shot_num'

all_value_keys = [time_stamp,
                  blm_name,
                  bunch_charge,
                  blm_names,
                  blm_pvs,
                  blm_time_pvs,
                  blm_waveform_pvs,
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
                  blm_buffer,
                  blm_time_buffer,
                  blm_distance_start,
                  blm_distance_end,
                  blm_time,
                  plots_done,
                  values_saved,
                  machine_mode,
                  scan_log,
                  scan_type,
                  num_shots,
                  num_shots_request,
                  has_blm_data,
                  blm_num_values,
                  save_request,
                  blm_buffer_full,
                  charge_buffer_full,
                  buffers_full,
                  buffer_message,
                  noise_data,
                  single_photon_data,
                  apply_filter,
                  blackman_size,
                  deconvolution_filter,
                  has_sparsified,
                  blm_object,
                  fibre_speed,
                  peak_voltages,
                  calibrate_request,
                  calibrate_channel_names,
                  str_to_pv,
                  delta_x,
                  calibration_time,
                  rolling_average,
                  blm_voltage_average,
                  blm_time_average,
                  shot_num
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
    values[blm_name] = dummy_str
    values[time_stamp] = dummy_dbl
    values[bunch_charge] = dummy_dbl + 1
    values[blm_names] = []
    values[blm_pvs] = []
    values[blm_time_pvs] = []
    values[blm_waveform_pvs] = []
    values[blm_status] = {}
    values[blm_voltages] = {}
    values[blm_buffer] = {}
    values[blm_time_buffer] = {}
    values[charge_name] = dummy_str
    values[charge_status] = False
    values[scan_status] = 'dummy_str'
    values[charge_monitoring] = dummy_str
    values[all_values_set] = False
    values[ready_to_go] = False
    values[charge_values] = []
    values[blm_distance_start] = dummy_dbl
    values[blm_distance_end] = dummy_dbl
    values[blm_time] = {}
    values[plots_done] = False
    values[values_saved] = False
    values[machine_mode] = dummy_str
    values[scan_log] = dummy_str
    values[scan_type] = dummy_str
    values[num_shots] = 2
    values[has_blm_data] = False
    values[blm_num_values] = []
    values[save_request] = False
    values[num_shots_request] = False
    values[blm_buffer_full] = False
    values[charge_buffer_full] = False
    values[buffers_full] = False
    values[buffer_message] = ""
    values[apply_filter] = False
    values[noise_data] = []
    values[single_photon_data] = []
    values[blackman_size] = dummy_int
    values[deconvolution_filter] = []
    values[has_sparsified] = False
    values[blm_object] = {}
    values[fibre_speed] = constants.speed_of_light / 1.46
    values[peak_voltages] = {}
    values[calibrate_request] = False
    values[calibrate_channel_names] = []
    values[str_to_pv] = {}
    values[delta_x] = dummy_dbl
    values[calibration_time] = dummy_dbl
    values[rolling_average] = 1
    values[shot_num] = 0
    values[blm_voltage_average] = {}
    values[blm_time_average] = {}
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