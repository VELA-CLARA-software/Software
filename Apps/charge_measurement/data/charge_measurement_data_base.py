from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QObject
import datetime
import numpy as np
# import matplotlib.pyplot as plt
from data.config_reader import config_reader


# keys for all the data we monitor
comments = 'comments'
num_shots = 'num_shots'
time_stamp = 'time_stamp'
charge_time_stamp = 'charge_time_stamp'
ophir_time_stamp = 'ophir_time_stamp'
gun_fwd_pwr_mean_time_stamp = 'gun_fwd_pwr_mean_time_stamp'
gun_fwd_pha_mean_time_stamp = 'gun_fwd_pha_mean_time_stamp'
vc_intensity_time_stamp = 'vc_intensity_time_stamp'
vc_x_pix_time_stamp = 'vc_x_pix_time_stamp'
vc_y_pix_time_stamp = 'vc_y_pix_time_stamp'
vc_sig_x_pix_time_stamp = 'vc_sig_x_pix_time_stamp'
vc_sig_y_pix_time_stamp = 'vc_sig_y_pix_time_stamp'
gun_fwd_pwr_time_stamp = 'gun_fwd_pwr_time_stamp'
gun_fwd_pha_time_stamp = 'gun_fwd_pha_time_stamp'
kly_fwd_pwr_time_stamp = 'kly_fwd_pwr_time_stamp'
kly_fwd_pwr_trace_mean = 'gun_fwd_pwr_trace_mean'
kly_fwd_pha_trace_mean = 'gun_fwd_pha_trace_mean'
kly_sp_time_stamp = 'kly_sp_time_stamp'
measurement_type = 'measurement_type'
bunch_charge = 'bunch_charge'
pil_name = 'pil_name'
pil_status = 'pil_status'
llrf_name = 'llrf_name'
llrf_status = 'llrf_status'
mag_names = 'mag_names'
mag_status = 'mag_status'
scan_status = 'scan_status'
pil_object = 'pil_object'
llrf_object = 'llrf_object'
mag_objects = 'mag_objects'
pil_monitoring = 'pil_monitoring'
llrf_monitoring = 'llrf_monitoring'
mag_monitoring = 'mag_monitoring'
all_values_set = 'all_values_set'
ready_to_go = 'ready_to_go'
charge_values = 'charge_values'
ophir_values = 'ophir_values'
hwp_values = 'hwp_values'
sol_values = 'sol_values'
bsol_values = 'bsol_values'
kly_fwd_pwr_values = 'kly_fwd_pwr_values'
kly_sp_values = 'kly_sp_values'
gun_fwd_pwr_mean_values = 'gun_fwd_pwr_mean_values'
gun_fwd_pha_mean_values = 'gun_fwd_pha_mean_values'
gun_fwd_pwr_traces = 'gun_fwd_pwr_traces'
gun_fwd_pha_traces = 'gun_fwd_pha_traces'
gun_fwd_pwr_trace_mean = 'gun_fwd_pwr_trace_mean'
gun_fwd_pha_trace_mean = 'gun_fwd_pha_trace_mean'
vc_intensity_values = 'vc_intensity_values'
vc_x_pix_values = 'vc_x_pix_values'
vc_y_pix_values = 'vc_y_pix_values'
vc_sig_x_pix_values = 'vc_sig_x_pix_values'
vc_sig_y_pix_values = 'vc_sig_y_pix_values'
bsol_time_stamp = 'bsol_time_stamp'
sol_time_stamp = 'sol_time_stamp'
set_hwp_start = 'set_hwp_start'
set_hwp_end = 'set_hwp_end'
num_steps = 'num_steps'
get_current_hwp = 'get_current_hwp'
set_current_hwp = 'set_current_hwp'
plots_done = 'plots_done'
values_saved = 'values_saved'
machine_mode = 'machine_mode'
scan_log = 'scan_log'
scan_type = 'scan_type'
ophir_range_sp = 'ophir_range_sp'
ophir_acquire_start = 'ophir_acquire_start'
ophir_acquire_stop = 'ophir_acquire_stop'
ophir_overrange = 'ophir_overrange'
data_written = 'data_written'
file_names = 'file_names'
progress_bar = 'progress_bar'
off_crest_phase = 'off_crest_phase'
off_crest_phase_dict = 'off_crest_phase_dict'
fit = 'fit'
cross = 'cross'
qe = 'qe'
kly_fwd_mean_all = 'kly_fwd_mean_all'
cancel = 'cancel'
vc_image_directory = 'vc_image_directory'
vc_image_name = 'vc_image_name'

all_value_keys = [comments,
time_stamp,
charge_time_stamp,
ophir_time_stamp,
kly_fwd_pwr_time_stamp,
kly_sp_time_stamp,
gun_fwd_pwr_mean_time_stamp,
gun_fwd_pha_mean_time_stamp,
vc_intensity_time_stamp,
vc_x_pix_time_stamp,
vc_y_pix_time_stamp,
vc_sig_x_pix_time_stamp,
vc_sig_y_pix_time_stamp,
bsol_time_stamp,
sol_time_stamp,
measurement_type,
bunch_charge,
pil_name,
pil_status,
llrf_name,
llrf_status,
mag_names,
mag_status,
scan_status,
pil_object,
llrf_object,
mag_objects,
pil_monitoring,
llrf_monitoring,
mag_monitoring,
all_values_set,
ready_to_go,
charge_values,
ophir_values,
hwp_values,
sol_values,
bsol_values,
kly_fwd_pwr_values,
kly_sp_values,
gun_fwd_pwr_mean_values,
gun_fwd_pha_mean_values,
gun_fwd_pwr_traces,
gun_fwd_pha_traces,
vc_intensity_values,
vc_x_pix_values,
vc_y_pix_values,
vc_sig_x_pix_values,
vc_sig_y_pix_values,
set_hwp_start,
set_hwp_end,
get_current_hwp,
set_current_hwp,
plots_done,
num_shots,
num_steps,
values_saved,
machine_mode,
scan_log,
scan_type,
ophir_range_sp,
ophir_acquire_start,
ophir_acquire_stop,
ophir_overrange,
data_written,
file_names,
progress_bar,
off_crest_phase,
off_crest_phase_dict,
fit,
cross,
qe,
kly_fwd_mean_all,
cancel,
vc_image_directory,
vc_image_name
]

class charge_measurement_data_base(QObject):
    # whoami
    my_name = 'charge_measurement_data'
    # config
    config = config_reader()
    # for logging
    log_param = None
    path = None
    time = None
    log_start = None
    should_write_header = True

    dummy_dbl = -999.0
    dummy_str = "dummy_str"
    dummy_int = int(-999)
    dummy_long = int(-999)
    values = {}
    # [values.update({x: 0}) for x in all_value_keys]
    values[comments] = dummy_str
    values[time_stamp] = {}
    values[charge_time_stamp] = {}
    values[ophir_time_stamp] = {}
    values[kly_fwd_pwr_time_stamp] = {}
    values[kly_sp_time_stamp] = {}
    values[gun_fwd_pwr_mean_time_stamp] = {}
    values[gun_fwd_pha_mean_time_stamp] = {}
    values[vc_intensity_time_stamp] = {}
    values[vc_x_pix_time_stamp] = {}
    values[vc_y_pix_time_stamp] = {}
    values[vc_sig_x_pix_time_stamp] = {}
    values[vc_sig_y_pix_time_stamp] = {}
    values[bsol_time_stamp] = {}
    values[sol_time_stamp] = {}
    values[measurement_type] = dummy_str
    values[pil_object] = {}
    values[llrf_object] = {}
    values[mag_objects] = {}
    values[pil_status] = False
    values[llrf_status] = False
    values[mag_status] = False
    values[pil_monitoring] = False
    values[llrf_monitoring] = False
    values[mag_monitoring] = False
    values[scan_status] = 'dummy_str'
    values[pil_name] = 'dummy_str'
    values[llrf_name] = 'dummy_str'
    values[mag_names] = []
    values[bunch_charge] = []
    values[all_values_set] = False
    values[ready_to_go] = False
    values[charge_values] = {}
    values[ophir_values] = {}
    values[hwp_values] = []
    values[sol_values] = {}
    values[bsol_values] = {}
    values[kly_fwd_pwr_values] = {}
    values[kly_sp_values] = {}
    values[gun_fwd_pwr_mean_values] = {}
    values[gun_fwd_pha_mean_values] = {}
    values[gun_fwd_pwr_traces] = [[] for i in range(8)]
    values[gun_fwd_pwr_traces] = [[] for i in range(8)]
    values[vc_intensity_values] = {}
    values[vc_x_pix_values] = {}
    values[vc_y_pix_values] = {}
    values[vc_sig_x_pix_values] = {}
    values[vc_sig_y_pix_values] = {}
    values[set_hwp_start] = dummy_dbl
    values[set_hwp_end] = dummy_dbl + 1
    values[set_current_hwp] = dummy_dbl
    values[get_current_hwp] = dummy_dbl
    values[ophir_range_sp] = dummy_int
    values[ophir_acquire_start] = False
    values[ophir_acquire_stop] = False
    values[ophir_overrange] = False
    values[num_shots] = dummy_int
    values[num_steps] = dummy_int
    values[plots_done] = False
    values[values_saved] = False
    values[machine_mode] = dummy_str
    values[scan_log] = dummy_str
    values[scan_type] = dummy_str
    values[data_written] = False
    values[file_names] = []
    values[progress_bar] = {}
    values[off_crest_phase] = dummy_dbl
    values[off_crest_phase_dict] = {}
    values[fit] = dummy_dbl
    values[cross] = dummy_dbl
    values[qe] = dummy_dbl
    values[kly_fwd_mean_all] = dummy_dbl
    values[cancel] = False
    values[vc_image_directory] = []
    values[vc_image_name] = []
    # amp_pwr_mean_data = {}

    #logger
    logger = None
    _pil_config = None
    _llrf_config = None
    _mag_config = None
    _log_config = None

    last_fwd_kly_pwr = None
    last_amp = None

    def __init__(self):
        QObject.__init__(self)
        self.data_log_timer = QTimer()
        # self.amp_pwr_log_timer = QTimer()
        # matplot lib bplot set-up, plotting needs improving for speed...
        # plt.ion()
        # plt.show()

    @property
    def logger(self):
        return charge_measurement_data_base._logger
    @logger.setter
    def logger(self,value):
        charge_measurement_data_base._logger = value

    @property
    def pil_config(self):
        return charge_measurement_data_base._pil_config

    @pil_config.setter
    def pil_config(self,value):
        charge_measurement_data_base._pil_config = value

    @property
    def llrf_config(self):
        return charge_measurement_data_base._llrf_config

    @llrf_config.setter
    def llrf_config(self, value):
        charge_measurement_data_base._llrf_config = value

    @property
    def mag_config(self):
        return charge_measurement_data_base._mag_config

    @mag_config.setter
    def mag_config(self, value):
        charge_measurement_data_base._mag_config = value

    def start_logging(self):
        self.logger.start_data_logging()
        self.data_log_timer.timeout.connect(self.data_log)
        self.data_log_timer.start(charge_measurement_data_base.config.log_config['DATA_LOG_TIME'])

    def timestamp(self):
        ts = datetime.datetime.now() - self.logger.log_start
        #print 'time = ' + str(ts.total_seconds())
        charge_measurement_data_base.values[time_stamp] = ts.total_seconds()

    def data_log(self):
        self.timestamp()
        if self.should_write_header:
            self.logger.write_data_log_header(charge_measurement_data_base.values)
            self.should_write_header = False
        self.logger.write_data(charge_measurement_data_base.values)