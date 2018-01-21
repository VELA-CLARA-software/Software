from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QObject
from VELA_CLARA_enums import STATE
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from VELA_CLARA_RF_Protection_Control import RF_GUN_PROT_STATUS
from VELA_CLARA_LLRF_Control import LLRF_TYPE
import datetime
import numpy as np
import matplotlib.pyplot as plt
from data.config_reader import config_reader


# keys for all the data we monitor
time_stamp = 'time_stamp'
vacuum_level = 'vacuum_level'
vac_spike_status = 'vac_spike_status'
DC_spike_status = 'DC_spike_status'
rev_power_spike_status = 'rev_power_spike_status'
cav_temp = 'cav_temp'
water_temp = 'water_temp'
pulse_length = 'pulse_length'
fwd_cav_pwr = 'fwd_cav_pwr'
fwd_kly_pwr = 'fwd_kly_pwer'
rev_kly_pwr = 'rev_kly_pwr'
rev_cav_pwr = 'rev_cav_pwr'
probe_pwr = 'probe_pwr'
vac_level = 'vac_level'
DC_level = 'DC_level'
vac_valve_status = 'vac_valve_status'
num_outside_mask_traces = 'num_outside_mask_traces'

probe_outside_mask_count = 'probe_outside_mask_count'
forward_outside_mask_count = 'probe_outside_mask_count'
reverse_outside_mask_count = 'reverse_outside_mask_count'

breakdown_status = 'breakdown_status'
breakdown_rate_aim = 'breakdown_rate_aim'

# these are values from the pulse_breakdown_log
log_active_pulse_count = 'log_active_pulse_count'
log_breakdown_count = 'log_breakdown_count'
log_amp_set = 'log_amp_set'
log_index = 'log_index'

breakdown_count = 'breakdown_count'
elapsed_time = 'elapsed_time'
breakdown_rate = 'breakdown_rate'
breakdown_rate_hi= 'breakdown_rate_hi'
last_106_bd_count='last_106_bd_count'

pulse_count = 'pulse_count'
event_pulse_count = 'event_pulse_count'
modulator_state = 'modulator_state'
rfprot_state = 'rfprot_state'
llrf_output = 'llrf_output'
llrf_ff_amp_locked = 'llrf_ff_amp_locked'
llrf_ff_ph_locked = 'llrf_ff_ph_locked'

power_aim = 'power_aim'
pulse_length_aim = 'pulse_length_aim'
pulse_length_step = 'pulse_length_step'
pulse_length_start = 'pulse_length_start'

required_pulses = 'required_pulses'
next_power_increase = 'next_power_increase'
next_power_decrease = 'next_power_decrease'

amp_ff = 'amp_ff'
amp_sp = 'amp_sp'
all_value_keys = [rev_power_spike_status,
                  num_outside_mask_traces,
                  breakdown_rate_aim,
                  vac_spike_status,
                  vac_valve_status,
                  DC_spike_status,
                  DC_level,
                  modulator_state,
                  breakdown_count,
                  breakdown_status,
                  breakdown_rate_hi,
                  breakdown_rate,
                  fwd_cav_pwr,
                  fwd_kly_pwr,
                  rev_kly_pwr,
                  rev_cav_pwr,
                  pulse_length,
                  rfprot_state,
                  llrf_output,
                  elapsed_time,
                  llrf_ff_amp_locked,
                  llrf_ff_ph_locked,
                  probe_pwr,
                  pulse_count,
                  event_pulse_count,
                  water_temp,
                  vac_level,
                  cav_temp,
                  time_stamp,
                  log_active_pulse_count,
                  log_breakdown_count,
                  log_amp_set,
                  log_index,
                  power_aim,
                  pulse_length_aim,
                  pulse_length_step,
                  pulse_length_start,
                  amp_sp,
                  last_106_bd_count
                  ]

class rf_condition_data_base(QObject):
    # whoami
    my_name = 'rf_condition_data'
    # we know there will be some LLRF involved
    llrf_type = LLRF_TYPE.UNKNOWN_TYPE

    # config
    config = config_reader()



    # for logging
    log_param = None
    path = None
    time = None
    log_start = None
    should_write_header = True

    kly_fwd_power_history = []
    amp_sp_history = []
    sp_pwr_hist =[]

    previous_power = 0
    current_power = 0
    old_x0 = 0
    old_x1 = 0
    old_m = 0
    old_c = 0

    values = {}
    [values.update({x: 0}) for x in all_value_keys]
    values[vac_valve_status] = VALVE_STATE.VALVE_ERROR
    values[vac_spike_status] = STATE.UNKNOWN
    values[DC_spike_status] = STATE.UNKNOWN
    values[breakdown_status] = STATE.UNKNOWN
    values[rev_power_spike_status] = STATE.UNKNOWN
    values[modulator_state] = GUN_MOD_STATE.UNKNOWN1
    values[rfprot_state] = RF_GUN_PROT_STATUS.UNKNOWN
    values[llrf_output] = STATE.UNKNOWN
    values[llrf_ff_amp_locked] = STATE.UNKNOWN
    dummy = -999.0
    values[cav_temp] = dummy
    values[water_temp] = dummy + 1
    values[pulse_length] = dummy + 2
    values[rev_kly_pwr] = dummy + 5
    values[rev_cav_pwr] = dummy + 6
    values[probe_pwr] = dummy + 7
    values[vac_level] = dummy
    values[breakdown_rate_aim] = dummy + 10
    values[breakdown_rate_hi] = False
    values[breakdown_rate] = dummy + 11
    values[breakdown_count] = dummy +2
    values[pulse_count] = dummy + 13
    values[event_pulse_count] = dummy +14
    values[elapsed_time] = dummy + 15
    values[DC_level] = dummy + 16

    #logger
    _logger = None
    _llrf_config = None
    _log_config = None

    def __init__(self):
        QObject.__init__(self)
        self.timer = QTimer()
        # matplot lib bplot set-up, plotting needs improving for speed...
        plt.ion()
        plt.show()

    @property
    def logger(self):
        return rf_condition_data_base._logger
    @logger.setter
    def logger(self,value):
        rf_condition_data_base._logger = value
    @property
    def llrf_config(self):
        return rf_condition_data_base._llrf_config
    @llrf_config.setter
    def llrf_config(self,value):
        rf_condition_data_base._llrf_config= value



    def start_logging(self):
        self.log_start = self.logger.start_data_logging()
        self.timer.timeout.connect(self.log)
        self.timer.start(rf_condition_data_base.config.log_config['DATA_LOG_TIME'])

    def timestamp(self):
        ts = datetime.datetime.now() - self.log_start
        #print 'time = ' + str(ts.total_seconds())
        rf_condition_data_base.values[time_stamp] = ts.total_seconds()



    # the main logging data file is binary(!)
    # With the amount of data etc. i think this is the only practical way
    # to save it, the header fo reach file with give types and names
    def log(self):
        self.log_kly_fwd_power_vs_amp()
        self.timestamp()
        if self.should_write_header:
            self.logger.write_data_log_header(rf_condition_data_base.values)
            self.should_write_header = False
        self.logger.write_data(rf_condition_data_base.values)

    def log_kly_fwd_power_vs_amp(self):
        self.kly_fwd_power_history.append(rf_condition_data_base.values[fwd_kly_pwr ])
        self.amp_sp_history.append(rf_condition_data_base.values[amp_sp ])
        self.sp_pwr_hist.append( [rf_condition_data_base.values[amp_sp ],self.values[fwd_kly_pwr]] )
        #self.max_sp = [i[0] for i in self.sp_pwr_hist]







