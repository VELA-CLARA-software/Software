# DJS Sept 2017
#
# spike monitor
#
#
# inherits from monitor base class
# It relies on timers to automatically get new signal values
# process them, then sets a flag in the passed stat_dict
# when the state of the signal changes
# from 'good' to 'bad'
# these states are always tied to the state of the cooldown through the
# property 'in_cooldown' and only emitted when the cooldown state changes
#
# Assuming connecting the interface to a pv has worked:
# it has a timer that gets and checks the signal signal
# a spike is defined as:
# self._latest_value > self.spike_delta + self._mean_level
# if the signal has not spiked, it appends the new value to
# value_history and sets _mean_level
# if the signal 'spikes'  it sets 'bad' and the
# object enters a cooldown state
# there are two cooldown states: 'timed' and 'level'
# 'timed' waits cooldown_time ms and then sets 'good'
# 'level' emits good when the vacuum returns
# to spike_decay_level*_mean_level then sets 'good'
# after cooldown the monitor returns to checking new signal values
# for a spike and updating the history buffer and mean
#
# base-class
from monitor import monitor
from VELA_CLARA_enums import STATE
from PyQt4.QtCore import QTimer
import src.data.rf_condition_data_base as dat
from numpy import mean
#from data.state import state


class spike_monitor(monitor):
    # whoami
    my_name = 'spike_monitor'
    # a history of the values when not in cooldown
    # (beware: during startup, all values are added to this list!)
    #_value_history = []
    # the latest signal value
    #_latest_value = -1
    # a counter indexing each unique signal reading
    #_reading_counter = -1
    # is the monitor in cooldown or not?
    #_in_cooldown = False
    # is the signal 'good'
    #_good = True
    # is the monitor connected to the passed PV ?
    #_connected = False
    # the mean signal  level, dummy init value that is very high
    #_mean_level = 1

    def __init__(self,
                 # the general monitor, acquires data
                 gen_mon,
                 # id to acquire data from gen_mon
                 id_key,
                 # mode fo decay after spike, 'level' or 'timed'
                 decay_mode,
                 # change in signal value to eb a spike
                 spike_delta,
                 # level to return to for state to go good again
                 spike_decay_level,
                 #m time taken
                 spike_decay_time,
                 # number of samples to average
                 num_samples_to_average,
                 # tim eto acquire next data
                 update_time,
                 # where to write current value
                 data_dict_val_key,
                 # where to write current state
                 data_dict_state_key,
                 # drop LLRF amp on spike?
                 should_drop_amp,
                 # amp setting to ddrop to on spike
                 amp_drop_value,
                 # object name
                 my_name = 'spike_monitor',
                 # minimum cooldown time for level decay
                 min_cooldown_time = 7000,
                 # max_level above which cool down
                 max_level = 1,
                 max_drop_amp = 7
                 ):
        # init base-class
        monitor.__init__(self)
        # local copies of passed variables
        self.my_name = my_name
        self.amp_drop_value = amp_drop_value
        self.data_dict_val_key = data_dict_val_key
        self.data_dict_state_key = data_dict_state_key
        self.id = id_key
        self.should_drop_amp = should_drop_amp
        # a general_monitor HWC
        self.gen_monitor = gen_mon
        # how many spikes have there been?
        self.spike_count = 0
        # see config_reader and.or config file for keys / values
        self.max_level = max_level
        self.max_drop_amp = max_drop_amp

        self._reading_counter = -1
        self._latest_value = None # ???
        self._mean_level   = None # ???
        self._value_history = []

        if self.should_drop_amp:
            monitor.logger.message(self.my_name + ' will drop amp on spike detection',True)
        else:
            monitor.logger.message(self.my_name + ' will NOT drop amp on spike detection',True)
        # set cool-down mode based on config, default will be LEVEL
        self.set_cooldown_mode(decay_mode)
        # a timer to run check_signal automatically every self.update_time
        self.timer.timeout.connect(self.check_signal)
        self.min_cooldown_timer = QTimer()
        self.min_cooldown_timer.setSingleShot(True)
        self.min_cooldown_time = min_cooldown_time
        self.min_cooldown_timer.timeout.connect(self.min_cooldown_finished)
        self.min_time_good = True
        # the amount above baseline (self._mean_level) that triggers a vacuum spike event
        # noinspection PyBroadException
        try:
            self.spike_delta = spike_delta
        except:
            self.spike_delta = None
        # factor applied to _mean_level to set the "recovered from spike" value
        # we're setting a recovery based on vacuum level not time here
        # this is for 'level' cool-down mode
        try:
            self.spike_decay_level = spike_decay_level
        except:
            self.spike_decay_level = 1.1

        try:
            self.cool_down_time = spike_decay_time
        except:
            # set a default value???
            self.cool_down_time = 5000
        try:
            self.update_time = update_time
        except:
            # set a default value???
            self.update_time = 1000
        # the number of signal values to keep in the history buffer
        try:
            self._num_samples_to_average = num_samples_to_average
        except:
            self._num_samples_to_average = None

        # initialise data to state unknown
        monitor.data.values[self.data_dict_state_key] = STATE.UNKNOWN
        # now we're ready to start
        self.run()

    def run(self):
        # now we're ready to start the timer, (could be called from a function)
        item = [self.spike_delta, self.spike_decay_level, self.cool_down_time]
        if self.sanity_checks(item):
            self.timer.start(self.update_time)
            monitor.logger.message(self.my_name + ' STARTED running',True)
            monitor.logger.message(self.my_name + ' ' + self.data_dict_state_key + ' ' + str(
                    monitor.data.values[self.data_dict_state_key]) ,
                                   True)
            self.set_good()

            monitor.logger.message(self.my_name + ' ' + self.data_dict_state_key + ' ' + str(
                    monitor.data.values[self.data_dict_state_key]) ,
                                   True)

        else:
            monitor.logger.message(self.my_name + ' NOT STARTED running',True)


    def check_signal(self):
        # get a latest value and if it was a new value
        if self.update_value():
            #print 'value updated'
            # if in cooldown, check value against cooldown
            # method to see if we should stay in cooldown state
            if self._in_cooldown:
                self.check_has_cooled_down()
            # if not in cooldown check if new value is a vacuum spike
            else:
                self.check_for_spike()

    def check_has_cooled_down(self):
        if self.level_cooldown:
            if self._latest_value < self.spike_decay_level * self._mean_level:
                if self.min_time_good:
                    monitor.logger.message(self.my_name, ' has_cooled_down')
                    self.in_cooldown = False

    def check_for_spike(self):
        #print 'check_for_spike'
        #print(self.my_name,' ',self._latest_value, self.spike_delta + self._mean_level)
        if self._mean_level != None:
            if self._latest_value > self.spike_delta + self._mean_level:
                print( self.my_name + ' spike ',self._latest_value, " ", self.spike_delta, " ", self._latest_value-self._mean_level)
                # this is the first place we can detect a spike, so drop amp here
                if self.should_drop_amp:
                    if monitor.data.values[dat.breakdown_status] == STATE.GOOD:
                        monitor.llrf_control.setAmpHP(self.amp_drop_value)
                # dump_data
                self.dump_data()
                # start the cooldown
                self.start_cooldown()
                monitor.logger.header(self.my_name + ' new spike: ')
                monitor.logger.message(str(self._latest_value) + ' > ' + str(self.spike_delta + self._mean_level) + ', mean = ' +str(self._mean_level),True)
                self.alarm('spike')

        self._value_history.append(self._latest_value)
        # if buffer is too large, remove oldest value and calculate average
        if len(self._value_history) > self._num_samples_to_average:
            self._value_history.pop(0)
            self._mean_level = sum(self._value_history)/self._num_samples_to_average

            # print(self.my_name, ' new_value = ', self._latest_value, 'counter  = ',self._reading_counter,', new-mean = ',
            #       self._latest_value - self._mean_level)

        # if self.max_level < self._latest_value:
        #     if monitor.data.values[dat.breakdown_status] == state.GOOD:
        #         monitor.llrf_control.setAmpHP(self.max_drop_value)
        #         monitor.logger.message(self.my_name, ' level too high has_cooled_down')

    def min_cooldown_finished(self):
        self.min_time_good = True

    def start_cooldown(self):
        monitor.data.update_break_down_count(1)
        #print 'start_cooldown called'
        self.in_cooldown = True
        self.min_time_good = False
        self.min_cooldown_timer.start(self.min_cooldown_time)
        # if in timed_cooldown mode
        if self.timed_cooldown:
            # start the cooldown timer
            self.cooldown_timer.start(self.cool_down_time)

    # overloaded cooldown_function (better name?)
    # when the cooldown timer ends this function is called
    def cooldown_function(self):
        #print(self.my_name,' cool down ended')
        # pass false to in_cooldown property
        self.in_cooldown = False

    @property
    def in_cooldown(self):
        return self._in_cooldown

    @property
    def latest_value(self):
        return self._latest_value

    @in_cooldown.setter
    def in_cooldown(self,value):
        self._in_cooldown = value
        #  the state  is inverse to the in_cooldown state
        #self._good = not self._in_cooldown
        # set state good
        if value:
            self.set_bad()
        else:
            self.set_good()

    # get latest value from gen_monitor
    def update_value(self):
        #if self._connected:
        value = self.gen_monitor.getCounterAndValue(self.id)
        # test if value is a new value, i.e _reading_counter has increased
        # (the gen_monitor will just pass back the latest value it has)
        if value.keys()[0] != self._reading_counter:
            # update _latest_value
            self._latest_value = value.values()[0]
            monitor.data.values[self.data_dict_val_key] = self._latest_value
            # set new _reading_counter
            self._reading_counter = value.keys()[0]
            return True
        #else:
        #    self.connectPV(self.pv)
        return False

    def set_bad(self):
        monitor.data.values[self.data_dict_state_key] = STATE.BAD

    def set_good(self):
        monitor.data.values[self.data_dict_state_key] = STATE.GOOD

    def dump_data(self):
        # increase count:
        self.spike_count += 1
        #trace_dump = monitor.llrf_control.getOneTraceData()
        new = monitor.llrf_control.getOneTraceData()
        new.update({'vacuum': monitor.data.values[dat.vac_level]})
        new.update({'DC': monitor.data.values[dat.DC_level]})
        new.update({'SOL': monitor.data.values[dat.sol_value]})
        monitor.logger.pickle_file(self.my_name + '_' + str(self.spike_count), new)
        print 'def dump_data(self): FIN'


