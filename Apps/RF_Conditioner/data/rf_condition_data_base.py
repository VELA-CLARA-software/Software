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

breakdown_rate_limit = 'breakdown_rate_limit'
breakdown_count = 'breakdown_count'
elapsed_time = 'elapsed_time'
breakdown_rate = 'breakdown_rate'
pulse_count = 'pulse_count'
modulator_state = 'modulator_state'
rfprot_state = 'rfprot_state'
llrf_output = 'llrf_output'
llrf_ff_amp_locked = 'llrf_ff_amp_locked'
llrf_ff_ph_locked = 'llrf_ff_ph_locked'
amp_ff = 'amp_ff'
amp_sp = 'amp_sp'
all_value_keys = [rev_power_spike_status,
                  num_outside_mask_traces,
                  breakdown_rate_limit,
                  vac_spike_status,
                  vac_valve_status,
                  DC_spike_status,
                  DC_level,
                  modulator_state,
                  breakdown_count,
                  breakdown_status,
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
                  water_temp,
                  vac_level,
                  cav_temp,
                  time_stamp
                  ]

class rf_condition_data_base(QObject):
    # whoami
    my_name = 'rf_condition_data'
    # we know there will be some LLRF involved
    llrf_type = LLRF_TYPE.UNKNOWN_TYPE

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
    [values.update({x: -999}) for x in all_value_keys]
    def __init__(self,
                 logger=None):
        QObject.__init__(self)
        self.llrf = None

        self.logger = logger

        self.values[vac_valve_status] = VALVE_STATE.VALVE_ERROR
        self.values[vac_spike_status] = STATE.UNKNOWN
        self.values[DC_spike_status] = STATE.UNKNOWN
        self.values[breakdown_status ] = STATE.UNKNOWN
        self.values[rev_power_spike_status] = STATE.UNKNOWN
        self.values[modulator_state] = GUN_MOD_STATE.UNKNOWN1
        self.values[rfprot_state] = RF_GUN_PROT_STATUS.UNKNOWN
        self.values[llrf_output] = STATE.UNKNOWN
        self.values[llrf_ff_amp_locked] = STATE.UNKNOWN

        dummy = -999.0
        self.values[cav_temp] = dummy
        self.values[water_temp] = dummy + 1
        self.values[pulse_length] = dummy + 2
        self.values[fwd_cav_pwr] = dummy + 3
        self.values[fwd_kly_pwr] = dummy + 4
        self.values[rev_kly_pwr] = dummy + 5
        self.values[rev_cav_pwr] = dummy + 6
        self.values[probe_pwr] = dummy + 7
        self.values[vac_level] = dummy + 8
        self.values[breakdown_rate_limit] = dummy + 10
        self.values[breakdown_rate] = dummy + 11
        self.values[pulse_count] = dummy + 12
        self.values[breakdown_count] = dummy + 14
        self.values[elapsed_time] = dummy + 15
        self.values[amp_ff] = dummy + 16
        self.values[amp_sp] = dummy + 17
        self.values[DC_level] = dummy + 18
        self.timer = QTimer()
        # matplot lib bplot set-up, plotting needs improving for speed...
        plt.ion()
        plt.show()


    def start_logging(self, log_param):
        self.log_start = self.logger.start_data_logging()
        self.timer.timeout.connect(self.log)
        self.timer.start(log_param['DATA_LOG_TIME'])

    def timestamp(self):
        ts = datetime.datetime.now() - self.log_start
        #print 'time = ' + str(ts.total_seconds())
        self.values[time_stamp] = ts.total_seconds()



    # the main logging data file is binary(!)
    # With the amount of data etc. i think this is the only practical way
    # to save it, the header fo reach file with give types and names
    def log(self):
        self.log_kly_fwd_power_vs_amp()
        self.timestamp()
        if self.should_write_header:
            self.logger.write_data_log_header(self.values)
            self.should_write_header = False
        self.logger.write_data(self.values)

    def log_kly_fwd_power_vs_amp(self):
        self.kly_fwd_power_history.append(self.values[fwd_kly_pwr ])
        self.amp_sp_history.append(self.values[amp_sp ])
        self.sp_pwr_hist.append( [self.values[amp_sp ],self.values[fwd_kly_pwr]] )
        #self.max_sp = [i[0] for i in self.sp_pwr_hist]






