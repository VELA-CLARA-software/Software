# DJS Nov 2017
#
# DC monitor - basically a carbon copy of the vacuum_monitor BUT
# 1 difference: we do a level increase (i.e percentage from baseline)
#
# emits dc_signal giving the state of a dc pv,
# dc is bad  = false signal
# dc is good = true signal
#
# inherits from monitor base class
# This class runs in a separate Qthread
# so after instantiation you must call start on it (!)
# It relies on timers to automatically get new dc values
# process them, then emit signals when the state of the DC changes
# from 'good' to 'bad'
# these signals are always tied to the state of the cooldown through the
# property 'in_cooldown' and only emitted when the cooldown state changes
#
# Assuming connecting the interface to a DC pv works:
# it has a timer that gets and checks the DC signal
# a spike is defined as:
# self._latest_dc_value > self.dc_spike_delta_level * self._mean_dc_level
# if the dc has not spiked, it appends the new value to
# dc_value_history and sets _mean_dc_level
# if the dc spikes it emits dc_signal 'bad' and the
# class enters a cooldown state
# there are two cooldown states: 'timed' and 'level'
# 'timed' waits cooldown_time ms and then emits signal 'good'
# 'level' emits good when the dc returns
# to dc_spike_decay_level*_mean_dc_level then emits 'good'
# after cooldown the monitor returns to checking new dc values
# for a spike and updating the history buffer and mean
#
# base-class
from monitor import monitor
from numpy import mean
from PyQt4.QtCore import pyqtSignal


class dark_current_monitor(monitor):
    # a history of the values when not in cooldown
    # (beware: during startup, all values are added to this list!)
    _dc_value_history = []
    # the latest dc value
    _latest_dc_value = -1000000
    # a counter indexing each unique dc reading
    _dc_reading_counter = -1
    # the signal that's emitted on state-change, giving the new state
    # dc is bad  = false signal
    # dc is good = true signal
    dc_signal = pyqtSignal(bool)
    # is the monitor in cooldown or not?
    _in_cooldown = False
    # is the dc 'good'
    _dc_good = True
    # is the monitor connected to the passed PV ?
    _connected = False
    # the mean dc level, dummy init value that is very high
    _mean_dc_level = 9999999999

    def __init__(self,
                 gen_mon,
                 pv = '',
                 dc_spike_delta_level = 1.33,
                 dc_spike_decay_level = 1.1,
                 dc_num_samples_to_average = 10 ):
        # init base-class
        # super(monitor, self).__init__()
        monitor.__init__(self)
        # set default cool-down mode to timed
        self.set_timed_cooldown()
        # a general_monitor HWC
        self.gen_monitor = gen_mon
        # set up the connection to the passed PV
        self.connectPV(pv)
        # a timer to run check_dc automatically every self.update_time
        self.timer.timeout.connect(self.check_dc)
        # the amount above baseline (self._mean_dc_level) that triggers a dc spike event
        self.dc_spike_delta_level = dc_spike_delta_level
        # factor applied to _mean_dc_level to set the "recovered from spike" value
        # we're setting a recovery based on dc level not time here
        # this is for 'level' cool-down mode
        self.dc_spike_decay_level = dc_spike_decay_level
        # the number of dc values to keep in the history buffer
        self._dc_num_samples_to_average = dc_num_samples_to_average
        # now we're ready to start the timer, (could be called from a function)
        if self._connected:
            self.timer.start(self.update_time)

    def check_dc(self):
        # get a latest value and if it was a new value
        if self.update_value():
            #print 'value updated'
            # if in cooldown, check value against cooldown
            # method to see if we should stay in cooldown state
            if self._in_cooldown:
                self.check_has_cooled_down()
            # if not in cooldown check if new value is a dc spike
            else:
                self.check_for_spike()

    def check_has_cooled_down(self):
        if self.level_cooldown:
            if self._latest_dc_value < self.dc_spike_decay_level * self._mean_dc_level:
                print 'dc level _has_cooled_down'
                self.incool_down = False

    def check_for_spike(self):
        #print 'check_for_spike'
        print('DC monitor: ',self._latest_dc_value, self.dc_spike_delta_level + self._mean_dc_level)
        if self._latest_dc_value > self.dc_spike_delta_level * self._mean_dc_level:
            print('spike ',self._latest_dc_value, self.dc_spike_delta_level, self._mean_dc_level)
            # start the cooldown
            self.start_cooldown()
        else:
            # if not a spike
            # append self._latest_dc_value to history buffer (_dc_value_history)
            self._dc_value_history.append(self._latest_dc_value)
            # if buffer is too large, remove oldest value and calculate average
            if len(self._dc_value_history) > self._dc_num_samples_to_average:
                self._dc_value_history.pop(0)
                self._mean_dc_level = mean(self._dc_value_history)
                print('new mean = ',self._mean_dc_level)

    def start_cooldown(self):
        #print 'start_cooldown called'
        self.in_cooldown = True
        # if in timed_cooldown mode
        if self.timed_cooldown:
            # start the cooldown timer
            self.cooldown_timer.start(self.cool_down_time)

    # overloaded cooldown_function (better name?)
    # when the cooldown timer ends this function is called
    def cooldown_function(self):
        print 'dc cool down ended'
        # pass false to in_cooldown property
        self.in_cooldown = False

    @property
    def in_cooldown(self):
        return self._in_cooldown

    @in_cooldown.setter
    def in_cooldown(self,value):
        self._in_cooldown = value
        #  the state of the dc is inverse to the in_cooldown state
        self._dc_good = not self._in_cooldown
        # emit dc_state
        self.dc_signal.emit(self._dc_good)

    # get latest value from gen_monitor
    def update_value(self):
        #if self._connected:
        value = self.gen_monitor.getCounterAndValue(self.id)
        # test if value is a new value, i.e _dc_reading_counter has increased
        # (the gen_monitor will just pass back the latest va;ue it has)
        if value.keys()[0] != self._dc_reading_counter:
            # update _latest_dc_value
            self._latest_dc_value = value.values()[0]
            # set new _dc_reading_counter
            self._dc_reading_counter = value.keys()[0]
            print('new_value = ', self._latest_dc_value, 'counter  = ',self._dc_reading_counter)
            return True
        #else:
        #    self.connectPV(self.pv)
        return False

    # connect to process variable pv
    def connectPV(self, pv):
        if pv != '':
            self.id = self.gen_monitor.connectPV(pv)
            if self.id != 'FAILED':
                self._connected = True
                print('Connected to PV = ', pv,' with ID = ',self.id, ' acquiring data')
            else:
                print('Failed to connect to PV = ', pv, ' ID = ',self.id, ' NOT acquiring data')
        else:
            print('Cannot connect to Blank PV passed to dc_monitor')