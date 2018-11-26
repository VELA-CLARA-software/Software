from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QObject
from VELA_CLARA_enums import STATE
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from VELA_CLARA_RF_Protection_Control import RF_GUN_PROT_STATUS
from VELA_CLARA_LLRF_Control import LLRF_TYPE
import datetime
import numpy as np
#import matplotlib.pyplot as plt
from data.config_reader import config_reader


# keys for all the data we monitor
time_stamp = 'time_stamp'
#vacuum_level = 'vacuum_level'
vac_spike_status = 'vac_spike_status'
DC_spike_status = 'DC_spike_status'
rev_power_spike_count = 'rev_power_spike_count'
cav_temp = 'cav_temp'
water_temp = 'water_temp'
pulse_length = 'pulse_length'

fwd_cav_pwr = 'fwd_cav_pwr'
fwd_kly_pwr = 'fwd_kly_pha'
rev_kly_pwr = 'rev_kly_pwr'
rev_cav_pwr = 'rev_cav_pwr'
probe_pwr = 'probe_pwr'
fwd_cav_pha = 'fwd_cav_pwr'
fwd_kly_pha = 'fwd_kly_pha'
rev_kly_pha = 'rev_kly_pha'
rev_cav_pha = 'rev_cav_pha'
probe_pha = 'probe_pha'


krpow = 'krpow'
krpha = 'krpha'
kfpow = 'kfpow'
kfpha = 'kfpha'
crpow = 'crpow'
crpha = 'crpha'
cppow = 'cppow'
cppha = 'cppha'
cfpow = 'cfpow'
cfpha = 'cfpha'




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
log_pulse_count = 'log_pulse_count'
#log_breakdown_count = 'log_breakdown_count'
log_amp_set = 'log_amp_set'
current_ramp_index = 'current_ramp_index'

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
mod_output = 'mod_output'
llrf_ff_amp_locked = 'llrf_ff_amp_locked'
llrf_ff_ph_locked = 'llrf_ff_ph_locked'

power_aim = 'power_aim'
pulse_length_aim = 'pulse_length_aim'
pulse_length_step = 'pulse_length_step'
pulse_length_start = 'pulse_length_start'

required_pulses = 'required_pulses'
next_power_increase = 'next_power_increase'
next_sp_decrease = 'next_sp_decrease'

log_pulse_length = 'log_pulse_length'

llrf_trigger = 'llrf_trigger'

last_mean_power = 'last_mean_power'
sol_value = 'sol_value'

amp_ff = 'amp_ff'
amp_sp = 'amp_sp'


#
# plot straight line fit values, old and current
x_min = 'x_min'
x_max = 'x_max'
old_x_min = 'old_x_min'
old_x_max = 'old_x_max'
y_min = 'y_min'
y_max = 'y_max'
old_y_min = 'old_y_min'
old_y_max = 'old_y_max'
c = 'c'
m = 'm'
old_c = 'old_c'
old_m = 'old_m'







# meh ...
phase_mask_by_power_trace_1_set = 'phase_mask_by_power_trace_1_set'
phase_mask_by_power_trace_2_set = 'phase_mask_by_power_trace_2_set'

phase_end_mask_by_power_trace_1_time = 'phase_end_mask_by_power_trace_1_time'
phase_end_mask_by_power_trace_2_time = 'phase_end_mask_by_power_trace_2_time'

all_value_keys = [rev_power_spike_count,
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
                  probe_pwr,
                  fwd_kly_pha,
                  rev_kly_pha,
                  rev_cav_pha,
                  probe_pha,
                  pulse_length,
                  rfprot_state,
                  llrf_output,
                  elapsed_time,
                  llrf_ff_amp_locked,
                  llrf_ff_ph_locked,
                  pulse_count,
                  event_pulse_count,
                  water_temp,
                  vac_level,
                  cav_temp,
                  time_stamp,
                  log_pulse_count,
#                  log_breakdown_count,
                  log_amp_set,
                  current_ramp_index,
                  power_aim,
                  pulse_length_aim,
                  pulse_length_step,
                  pulse_length_start,
                  amp_sp,
                  last_106_bd_count,
                  log_pulse_length,
                  llrf_trigger,
                  next_sp_decrease,
                  last_mean_power,
                  next_power_increase,
                  sol_value,
                  phase_mask_by_power_trace_1_set,
                  phase_mask_by_power_trace_2_set,
                  phase_end_mask_by_power_trace_1_time,
                  phase_end_mask_by_power_trace_2_time,
                  x_min,
                  x_max,
                  old_x_min,
                  old_x_max,
                  y_min,
                  y_max,
                  old_y_min,
                  old_y_max,
                  c,
                  m,
                  old_c,
                  old_m,
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
    # fitting parameters
    previous_power = 0
    current_power = 0


    values = {}
    [values.update({x: 0}) for x in all_value_keys]
    values[vac_valve_status] = VALVE_STATE.VALVE_ERROR
    values[vac_spike_status] = STATE.UNKNOWN
    values[DC_spike_status] = STATE.UNKNOWN
    values[breakdown_status] = STATE.UNKNOWN
    values[rev_power_spike_count] = STATE.UNKNOWN
    values[modulator_state] = GUN_MOD_STATE.UNKNOWN_STATE
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
    values[rev_power_spike_count] = 0
    values[next_power_increase] = -1
    values[phase_mask_by_power_trace_1_set] = False
    values[phase_mask_by_power_trace_2_set] = False
    values[phase_end_mask_by_power_trace_1_time] = -1.0
    values[phase_end_mask_by_power_trace_2_time] = -1.0

    values[old_x_min] = 0
    values[old_y_min] = 0
    values[old_x_max] = 0
    values[old_y_max] = 0
    values[old_m] = 0
    values[old_c] = 0
    values[x_min] = 0
    values[x_max] = 0
    values[y_min] = 0
    values[x_max] = 0
    values[m] = 0
    values[c] = 0

    amp_pwr_mean_data = {}
    amp_vs_kfpow_running_stat = {}

    #logger
    logger = None
    _llrf_config = None
    _log_config = None

    last_fwd_kly_pwr = None
    last_amp = None


    def __init__(self):
        QObject.__init__(self)
        self.data_log_timer = QTimer()
        self.amp_pwr_log_timer = QTimer()
        #
        # previous entry in kfp running stat, so we don't duplicate too much in the file
        self.last_kfp_running_stat_entry = None

    @property
    def llrf_config(self):
        return rf_condition_data_base._llrf_config
    @llrf_config.setter
    def llrf_config(self,value):
        rf_condition_data_base._llrf_config = value

    def start_logging(self):
        self.logger.start_data_logging()
        self.data_log_timer.timeout.connect(self.data_log)
        self.data_log_timer.start(rf_condition_data_base.config.log_config['DATA_LOG_TIME'])
        self.amp_pwr_log_timer.timeout.connect(self.log_kly_fwd_power_vs_amp)
        self.amp_pwr_log_timer.start(rf_condition_data_base.config.log_config['AMP_PWR_LOG_TIME'])

    def timestamp(self):
        ts = datetime.datetime.now() - self.logger.log_start
        #print 'time = ' + str(ts.total_seconds())
        rf_condition_data_base.values[time_stamp] = ts.total_seconds()

    def update_break_down_count(self):
        # if all status are not bad then add tpo breakdown count
        if STATE.BAD not in [rf_condition_data_base.values[DC_spike_status],
                             rf_condition_data_base.values[DC_spike_status],
                             rf_condition_data_base.values[breakdown_status]
                             ]:
            rf_condition_data_base.values[breakdown_count] += 1
            self.logger.message(self.my_name + ' increasing breakdown count = ' + str(rf_condition_data_base.values[breakdown_count]), True)
            self.add_to_pulse_breakdown_log(rf_condition_data_base.amp_sp_history[-1] )
        else:
            self.logger.message(
                self.my_name + ' NOT increasing breakdown count, already in cooldown, = ' + str(rf_condition_data_base.values[breakdown_count]),
                True)

    def reached_min_pulse_count_for_this_step(self):
        return self.values[event_pulse_count] >= self.values[required_pulses]

    # the main logging data file is binary(!)
    # With the amount of data etc. I think this is the only practical way
    # to save it, the header for each file with give types and names
    def data_log(self):
        self.timestamp()
        if self.should_write_header:
            self.logger.write_data_log_header(rf_condition_data_base.values)
            self.should_write_header = False
        self.logger.write_data(rf_condition_data_base.values)

    def log_kly_fwd_power_vs_amp(self):
        next_log_entry = [rf_condition_data_base.values[amp_sp]] + \
        rf_condition_data_base.amp_vs_kfpow_running_stat[rf_condition_data_base.values[amp_sp]]

        if next_log_entry != self.last_kfp_running_stat_entry:
            self.logger.add_to_KFP_Running_stat_log(next_log_entry)
        self.last_kfp_running_stat_entry = next_log_entry

        if rf_condition_data_base.values[amp_sp] > 100:#MAGIC_NUMBER
            if self.kly_power_changed():
                #rf_condition_data_base.kly_fwd_power_history.append( rf_condition_data_base.values[fwd_kly_pwr] )
                if rf_condition_data_base.values[fwd_kly_pwr] > rf_condition_data_base.config.llrf_config['KLY_PWR_FOR_ACTIVE_PULSE']:
                    rf_condition_data_base.sp_pwr_hist.append( [rf_condition_data_base.values[amp_sp],rf_condition_data_base.values[fwd_kly_pwr]] )
                    #self.update_amp_pwr_mean_dict(rf_condition_data_base.values[amp_sp],
                    #                               rf_condition_data_base.values[fwd_kly_pwr])
            # cancer
            if rf_condition_data_base.values[amp_sp] \
                    not in rf_condition_data_base.amp_sp_history:
                rf_condition_data_base.amp_sp_history.append(rf_condition_data_base.values[amp_sp])


    def kly_power_changed(self):
        r = False
        if rf_condition_data_base.last_fwd_kly_pwr != rf_condition_data_base.values[fwd_kly_pwr]:
            r = True
        rf_condition_data_base.last_fwd_kly_pwr = rf_condition_data_base.values[fwd_kly_pwr]
        return r

    def add_to_pulse_breakdown_log(self,amp):
        if amp > 100:
            self.logger.add_to_pulse_breakdown_log(
                [rf_condition_data_base.values[pulse_count],
                 rf_condition_data_base.values[breakdown_count],
                 int(amp),
                 int(rf_condition_data_base.values[current_ramp_index]),
                 int(rf_condition_data_base.values[pulse_length] * 1000)#MAGIC_NUMMBER UNITS
                ]
        )
        else:
            self.logger.message('Not adding to pulse_breakdown_log, amp = ' + str(amp),True)





