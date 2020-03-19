from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QObject

from src.data.state import state
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from VELA_CLARA_RF_Protection_Control import RF_PROT_STATUS
from VELA_CLARA_LLRF_Control import LLRF_TYPE
import datetime
import numpy as np
# for beeps
import winsound
#import matplotlib.pyplot as plt
from src.data.config_reader import config_reader


# keys for all the data we monitor
time_stamp = 'time_stamp'
#vacuum_level = 'vacuum_level'
vac_spike_status = 'vac_spike_status'
DC_spike_status = 'DC_spike_status'
rev_power_spike_count = 'rev_power_spike_count'
cav_temp = 'cav_temp'
water_temp = 'water_temp'

fwd_cav_pwr = 'fwd_cav_pwr'
fwd_kly_pwr = 'fwd_kly_pwr'
rev_kly_pwr = 'rev_kly_pwr'
rev_cav_pwr = 'rev_cav_pwr'
probe_pwr = 'probe_pwr'
fwd_cav_pha = 'fwd_cav_pha'
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
duplicate_pulse_count = 'duplicate_pulse_count'

# Hold RF ON handle scontrolling these, we just monitor
rfprot_state = 'rfprot_state'
modulator_state = 'modulator_state'
mod_output_status = 'mod_output_status'

can_rf_output_OLD = 'can_rf_output_OLD'
can_rf_output = 'can_rf_output'

llrf_interlock = 'llrf_interlock' # The read value from EPICS
llrf_interlock_status = 'llrf_interlock_status' # the apps internal state, good, new_bad etc


llrf_trigger = 'llrf_trigger'
llrf_trigger_status = 'llrf_trigger_status'

pulse_length = 'pulse_length'
pulse_length_status = 'pulse_length_status' # the apps internal state, good, new_bad etc

llrf_output = 'llrf_output' # RF Output on LLRF panel
llrf_output_status = 'llrf_output_status' # the apps internal state, good, new_bad etc

llrf_ff_amp_locked = 'llrf_ff_amp_locked'
llrf_ff_amp_locked_status = 'llrf_ff_amp_locked_status' # the apps internal state, good, new_bad etc
llrf_ff_ph_locked  = 'llrf_ff_ph_locked'
llrf_ff_ph_locked_status  = 'llrf_ff_ph_locked_status' # the apps internal state, good, new_bad etc

llrf_DAQ_rep_rate = 'llrf_DAQ_rep_rate'
llrf_DAQ_rep_rate_aim = 'llrf_DAQ_rep_rate_aim'
llrf_DAQ_rep_rate_status = 'llrf_DAQ_rep_rate_status'
llrf_DAQ_rep_rate_status_previous = 'llrf_DAQ_rep_rate_status_previous'
llrf_DAQ_rep_rate_max = 'llrf_DAQ_rep_rate_max'
llrf_DAQ_rep_rate_min = 'llrf_DAQ_rep_rate_min'


power_aim = 'power_aim'
pulse_length_aim = 'pulse_length_aim'
pulse_length_aim_error = 'pulse_length_aim_error'
pulse_length_min = 'pulse_length_min'
pulse_length_max = 'pulse_length_max'

required_pulses = 'required_pulses'
next_power_increase = 'next_power_increase'


log_pulse_length = 'log_pulse_length'


last_mean_power = 'last_mean_power'
sol_value = 'sol_value'

amp_ff = 'amp_ff'
amp_sp = 'amp_sp'
phi_sp = 'phi_sp'


TOR_ACQM = 'TOR_ACQM'
TOR_SCAN = 'TOR_SCAN'

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

#latest_ramp_up_sp = 'latest_ramp_up_sp'
last_sp_above_100 = 'last_sp_above_100'
max_sp_increase = 'max_sp_increase'
next_sp_decrease = 'next_sp_decrease'


#latest_ramp_up_sp_key = 'latest_ramp_up_sp_key'


vac_val_limit_status = 'vac_val_limit'



# meh ...
phase_mask_by_power_trace_1_set = 'phase_mask_by_power_trace_1_set'
phase_mask_by_power_trace_2_set = 'phase_mask_by_power_trace_2_set'

phase_end_mask_by_power_trace_1_time = 'phase_end_mask_by_power_trace_1_time'
phase_end_mask_by_power_trace_2_time = 'phase_end_mask_by_power_trace_2_time'

Initial_Bin_List = 'Initial_Bin_List'
Binned_amp_sp = 'Binned_amp_sp'


binned_stats_min_amp = "BINNED_STATS_MIN_AMP"
binned_stats_max_amp = "binned_stats_max_amp"
binned_stats_max_pow = "BINNED_STATS_MAX_POW"  # MW  (we need to make sure if we get more
# power thna this the script does not crash)
binned_stats_min_pow = "BINNED_STATS_MIN_POW"   # MW
binned_stats_bin_width = "BINNED_STATS_BIN_WIDTH" # In amp-sets point units


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
                  max_sp_increase,
                  fwd_cav_pwr,
                  fwd_kly_pwr,
                  rev_kly_pwr,
                  rev_cav_pwr,
                  probe_pwr,
                  fwd_kly_pha,
                  rev_kly_pha,
                  rev_cav_pha,
                  fwd_cav_pha,
                  probe_pha,
                  pulse_length,
                  rfprot_state,
                  llrf_output,
                  elapsed_time,
                  llrf_ff_amp_locked,
                  llrf_ff_ph_locked,
                  pulse_count,
                  event_pulse_count,
                  duplicate_pulse_count,
                  water_temp,
                  vac_level,
                  cav_temp,
                  time_stamp,
                  log_pulse_count,
                  llrf_DAQ_rep_rate,
                  llrf_DAQ_rep_rate_status,
                  llrf_DAQ_rep_rate_status_previous,
                  llrf_DAQ_rep_rate_aim,
                  llrf_DAQ_rep_rate_max,
                  llrf_DAQ_rep_rate_min,
#                  log_breakdown_count,
                  vac_val_limit_status,
                  can_rf_output_OLD,
                  can_rf_output,
                  log_amp_set,
                  current_ramp_index,
                  power_aim,
                  pulse_length_aim,
                  pulse_length_aim_error,
                  pulse_length_min,
                  pulse_length_max,




                  #latest_ramp_up_sp,
                  last_sp_above_100,

                  amp_sp,
                  phi_sp,

                  last_106_bd_count,
                  log_pulse_length,

                  llrf_trigger,
                  llrf_trigger_status,
                  llrf_interlock_status,
                  llrf_interlock,
                  llrf_output_status,
                  llrf_ff_amp_locked_status,
                  llrf_ff_ph_locked_status,
                  pulse_length_status,

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
                  TOR_ACQM,
                  TOR_SCAN,
                  pulse_length_status,
                  Initial_Bin_List,
                  Binned_amp_sp
                  ]




class rf_condition_data_base(QObject):
    # whoami
    my_name = 'rf_condition_data'

    # initialise values for all the data,

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

    #latest_ramp_up_sp = 0


    values = {}
    [values.update({x: 0}) for x in all_value_keys]


    values[vac_valve_status] = VALVE_STATE.VALVE_ERROR
    #values[rev_power_spike_count] = STATE.UNKNOWN

    values[modulator_state] = GUN_MOD_STATE.UNKNOWN_STATE
    values[rfprot_state] = RF_PROT_STATUS.UNKNOWN

    values[vac_spike_status] = state.UNKNOWN
    values[DC_spike_status] = state.UNKNOWN
    values[breakdown_status] = state.UNKNOWN
    values[llrf_output_status] = state.UNKNOWN
    values[llrf_trigger_status] = state.UNKNOWN
    values[llrf_interlock_status] = state.UNKNOWN
    values[llrf_ff_amp_locked] = state.UNKNOWN
    values[llrf_ff_ph_locked] = state.UNKNOWN
    values[can_rf_output_OLD] = state.UNKNOWN

#sss

    values[last_sp_above_100] = 0
    #values[latest_ramp_up_sp] = 0

    values[vac_val_limit_status] = state.GOOD

    dummy_float = -999.0
    dummy_int = -999.0
    dummy_bool = -999.0



    values[cav_temp] = dummy_float
    values[water_temp] = dummy_float + 1



    values[pulse_length] = dummy_float + 2
    values[rev_kly_pwr] = dummy_float + 5
    values[rev_cav_pwr] = dummy_float + 6
    values[probe_pwr] = dummy_float + 7
    values[vac_level] = dummy_float
    values[breakdown_rate_aim] = dummy_int
    values[breakdown_rate_hi] = dummy_bool


    values[breakdown_rate] = dummy_int+ 11
    values[breakdown_count] = dummy_int +2
    values[pulse_count] = dummy_int + 13
    values[event_pulse_count] = dummy_int +14
    values[duplicate_pulse_count] = dummy_int +14
    values[elapsed_time] = dummy_int + 15
    values[DC_level] = dummy_float + 16
    values[rev_power_spike_count] = dummy_int
    values[next_power_increase] = -1
    values[phase_mask_by_power_trace_1_set] = False
    values[phase_mask_by_power_trace_2_set] = False
    values[phase_end_mask_by_power_trace_1_time] = -1.0
    values[phase_end_mask_by_power_trace_2_time] = -1.0




    values[old_x_min] = dummy_float
    values[old_y_min] = dummy_float
    values[old_x_max] = dummy_float
    values[old_y_max] = dummy_float
    values[old_m] = dummy_float
    values[old_c] = dummy_float
    values[x_min] = dummy_float
    values[x_max] = dummy_float
    values[y_min] = dummy_float
    values[x_max] = dummy_float
    values[m] = dummy_float
    values[c] = dummy_float

    amp_pwr_mean_data = {}
    amp_vs_kfpow_running_stat = {}

    amp_vs_kfpow_running_stat_binned = {}

    #logger
    logger = None
    _llrf_config = None
    _log_config = None

    last_fwd_kly_pwr = None
    last_amp = None

    #THERE ARE 2 COPIES OF THE last_million_log , FIX THIS !!!!!!!!!!!
    last_million_log = None

    def __init__(self):
        QObject.__init__(self)
        self.data_log_timer = QTimer()
        self.amp_pwr_log_timer = QTimer()
        #
        # previous entry in kfp running stat, so we don't duplicate too much in the file
        self.last_kfp_running_stat_entry = None
        #
        # This i sa counter to update the pulse_break_down log with the data.log (bunary)
        # its used to write the pulse_break_down less frequently than data.log
        self.counter_add_to_pulse_breakdown_log = 0




    @property
    def llrf_config(self):
        return rf_condition_data_base._llrf_config
    @llrf_config.setter
    def llrf_config(self,value):
        rf_condition_data_base._llrf_config = value

    def start_logging(self):
        self.logger.start_data_logging()
        self.data_log()
        self.data_log_timer.timeout.connect(self.data_log)
        self.data_log_timer.start(rf_condition_data_base.config.log_config['DATA_LOG_TIME'])
        self.amp_pwr_log_timer.timeout.connect(self.log_kly_fwd_power_vs_amp)
        self.amp_pwr_log_timer.start(rf_condition_data_base.config.log_config['AMP_PWR_LOG_TIME'])

    def timestamp(self):
        ts = datetime.datetime.now() - self.logger.log_start
        #print 'time = ' + str(ts.total_seconds())
        rf_condition_data_base.values[time_stamp] = ts.total_seconds()



    def update_break_down_count(self, count):
        # if all status are not bad then add to breakdown count
        if state.BAD not in [rf_condition_data_base.values[DC_spike_status],
                             rf_condition_data_base.values[vac_spike_status],
                             rf_condition_data_base.values[breakdown_status]
                             ]:
            self.force_update_breakdown_count(count)
        else:
            self.logger.message(
                self.my_name + ' NOT increasing breakdown count, already in cooldown, = ' + str(rf_condition_data_base.values[breakdown_count]),
                True)

    def force_update_breakdown_count(self, count):
        rf_condition_data_base.values[breakdown_count] += count

        self.logger.message(self.my_name + ' increasing breakdown count = ' + str(
                rf_condition_data_base.values[breakdown_count]) +  ', at pulse count = ' +
                            str(rf_condition_data_base.values[pulse_count]), True)
        self.beep(count)
        #self.add_to_pulse_breakdown_log(rf_condition_data_base.amp_sp_history[-1])

    def beep(self, count):
        winsound.Beep(2000,150)## MAGIC_NUMBER

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
        if self.counter_add_to_pulse_breakdown_log % 10 == 0: ## MAGIC_NUMBER
            self.add_to_pulse_breakdown_log(rf_condition_data_base.values[amp_sp])
            self.update_breakdown_stats()
        self.counter_add_to_pulse_breakdown_log += 1## MAGIC_NUMBER


    def DynamicBin(self,X, bin_mean, bedges, bin_pop, newdata, data_binned):
        for i in range(int(len(bin_mean))):
            if newdata[0] >= bedges[i] and newdata[0] < bedges[i + 1]:
                bin_pop[i] += 1
                bin_mean[i] = ((bin_mean[i] * bin_pop[i]) + newdata[1]) / (bin_pop[i] + 1.0)
                data_binned[i].append(newdata[1])
                #print('DynamicBin Working')
            else:
                continue

        return X, bin_mean, bedges, bin_pop, data_binned

    def log_kly_fwd_power_vs_amp(self):

        next_log_entry = self.last_kfp_running_stat_entry
        if rf_condition_data_base.values[amp_sp] in rf_condition_data_base.amp_vs_kfpow_running_stat.keys():
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
            if rf_condition_data_base.values[amp_sp] not in rf_condition_data_base.amp_sp_history:
                rf_condition_data_base.amp_sp_history.append(rf_condition_data_base.values[amp_sp])
                self.logger.message('New amp_sp_history value = ' + str(rf_condition_data_base.values[amp_sp]), True)



        print(next_log_entry)
        print("333")

        # newdata = [rf_condition_data_base.amp_vs_kfpow_running_stat[rf_condition_data_base.values[amp_sp]],
        #            rf_condition_data_base.amp_vs_kfpow_running_stat[rf_condition_data_base.values[amp_sp]][1]]

        newdata = [next_log_entry[0] , next_log_entry[2]]

        #print('newdata = ',[llrf_handler_base.data.amp_vs_kfpow_running_stat[llrf_handler_base.data.values[dat.amp_sp]]])

        X = rf_condition_data_base.values[Initial_Bin_List][0]
        bin_mean =rf_condition_data_base.values[Initial_Bin_List][1]
        bedges = rf_condition_data_base.values[Initial_Bin_List][2]
        bin_pop = rf_condition_data_base.values[Initial_Bin_List][3]
        data_binned = rf_condition_data_base.values[Initial_Bin_List][4]

        # print('X = ', X)
        # print('bin_mean = ', bin_mean)
        # print('bedges = ', bedges)
        # print('bin_pop = ', bin_pop)

        X, bin_mean, bedges, bin_pop, data_binned = self.DynamicBin(X, bin_mean, bedges, bin_pop,
                                                                    newdata, data_binned)

        rf_condition_data_base.values[Initial_Bin_List] =[ X, bin_mean, bedges, bin_pop, data_binned]

        # rf_condition_data_base.amp_vs_kfpow_running_stat[rf_condition_data_base.values[amp_sp]] =[X, bin_mean,
        # np.ones( len(X)) ]




    def kly_power_changed(self):
        r = False
        if rf_condition_data_base.last_fwd_kly_pwr != rf_condition_data_base.values[fwd_kly_pwr]:
            r = True
        rf_condition_data_base.last_fwd_kly_pwr = rf_condition_data_base.values[fwd_kly_pwr]
        return r

    def add_to_pulse_breakdown_log(self,amp):
        if amp > 100:#MAGIC_NUMBER
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





