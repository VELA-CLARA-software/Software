# DJS Sept 2017
#
# vacuum monitor
# emits vac_signal giving the state of a vacuum pv,
# vacuum is bad  = false
# vacuum is good = true
#
#
# inherits from monitor base class
# This class runs in a separate Qthread
# so after instantiation you must call start on it (!)
# It relies on timers to automatically get new vacuum values
# process them, then sets a flag in the passed stat_dict
# when the state of the vacuum changes
# from 'good' to 'bad'
# these states are always tied to the state of the cooldown through the
# property 'in_cooldown' and only emitted when the cooldown state changes
#
# Assuming connecting the interface to a vacuum pv works:
# it has a timer that gets and checks the vacuum signal
# a spike is defined as:
# self._latest_vac_value > self.vac_spike_delta + self._mean_vac_level
# if the vacuum has not spiked, it appends the new value to 
# vac_value_history and sets _mean_vac_level
# if the vacuum spikes it sets 'bad' and the
# class enters a cooldown state
# there are two cooldown states: 'timed' and 'level'
# 'timed' waits cooldown_time ms and then emits signal 'good'
# 'level' emits good when the vacuum returns
# to vac_spike_decay_level*_mean_vac_level then emits 'good'
# after cooldown the monitor returns to checking new vacuum values
# for a spike and updating the history buffer and mean
#
# base-class
from monitor import monitor
from numpy import mean
from state import state

class vacuum_monitor(monitor):
    # whoami
    my_name = 'vacuum_monitor'
    # a history of the values when not in cooldown
    # (beware: during startup, all values are added to this list!)
    _vac_value_history = []
    # the latest vacuum value
    _latest_vac_value = -1
    # a counter indexing each unique vacuum reading
    _vac_reading_counter = -1
    # the signal that's emitted on state-change, giving the new state
    # is the monitor in cooldown or not?
    _in_cooldown = False
    # is the vacuum 'good'
    _vacum_good = True
    # is the monitor connected to the passed PV ?
    _connected = False
    # the mean vacuum level, dummy init value that is very high
    _mean_vac_level = 1

    def __init__(self,
                 gen_mon,
                 vac_param,
                 state_dict,
                 gui_dict
                 # pv = '',
                 # vac_spike_delta = 1e-9,
                 # vac_spike_decay_level = 1.1,
                 # vac_num_samples_to_average = 3
                 ):
        # init base-class
        # super(monitor, self).__init__()
        monitor.__init__(self)
        # see config_reader and.or config file for keys / values
        # vac_keys = ['VAC_PV','VAC_SPIKE_DELTA','VAC_DECAY_MODE','VAC_SPIKE_DECAY_LEVEL','VAC_SPIKE_DECAY_LEVEL'
        #            ,'VAC_SPIKE_DECAY_TIME','VAC_NUM_SAMPLES_TO_AVERAGE', 'VAC_ID']
        self.state_dict = [state_dict]
        self.gui_dict   = [gui_dict]
        self.id = vac_param['VAC_ID']
        # set cool-down mode based on config, default will be LEVEL
        self.set_cooldown_mode(vac_param.get('VAC_DECAY_MODE'))
        # a general_monitor HWC
        self.gen_monitor = gen_mon
        # a timer to run check_vacuum automatically every self.update_time
        self.timer.timeout.connect(self.check_vacuum)
        # the amount above baseline (self._mean_vac_level) that triggers a vacuum spike event
        try:
            self.vac_spike_delta = vac_param['VAC_SPIKE_DELTA']
        except:
            self.vac_spike_delta = None
        # factor applied to _mean_vac_level to set the "recovered from spike" value
        # we're setting a recovery based on vacuum level not time here
        # this is for 'level' cool-down mode
        if self.level_cooldown:
            try:
                self.vac_spike_decay_level = vac_param['VAC_SPIKE_DECAY_LEVEL']
            except:
                self.vac_spike_decay_level = 1.1
        elif self.timed_cooldown:
            try:
                self.cool_down_time = vac_param['VAC_SPIKE_DECAY_TIME']
            except:
                # set a default value???
                self.cool_down_time = 5000
        # the number of vacuum values to keep in the history buffer
        try:
            self._vac_num_samples_to_average = vac_param['VAC_NUM_SAMPLES_TO_AVERAGE']
        except:
            self._vac_num_samples_to_average = None
        # now we're ready to start the timer, (could be called from a function)
        item = [self.vac_spike_delta, self.vac_spike_decay_level, self.cool_down_time]
        if self.sanity_checks(item):
            self.timer.start(self.update_time)

    def check_vacuum(self):
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
            if self._latest_vac_value < self.vac_spike_decay_level * self._mean_vac_level:
                print 'vacuum level _has_cooled_down'
                self.incool_down = False

    def check_for_spike(self):
        #print 'check_for_spike'
        print('Vac monitor: ',self._latest_vac_value, self.vac_spike_delta + self._mean_vac_level)
        if self._latest_vac_value > self.vac_spike_delta + self._mean_vac_level:
            print('spike ',self._latest_vac_value, self.vac_spike_delta, self._mean_vac_level)
            # start the cooldown
            self.state_dict[0]['vacuum_state'] = state.BAD
            self.start_cooldown()
        else:
            # if not a spike
            self.state_dict[0]['vacuum_state'] = state.GOOD
            # append self._latest_vac_value to history buffer (_vac_value_history)
            self._vac_value_history.append(self._latest_vac_value)
            # if buffer is too large, remove oldest value and calculate average
            if len(self._vac_value_history) > self._vac_num_samples_to_average:
                self._vac_value_history.pop(0)
                self._mean_vac_level = mean(self._vac_value_history)
                print('new mean = ',self._mean_vac_level)

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
        print 'vacuum cool down ended'
        # pass false to in_cooldown property
        self.in_cooldown = False

    @property
    def in_cooldown(self):
        return self._in_cooldown

    @property
    def latest_value(self):
        return self._latest_vac_value

    @in_cooldown.setter
    def in_cooldown(self,value):
        self._in_cooldown = value
        #  the state of the vacuum is inverse to the in_cooldown state
        self._vacum_good = not self._in_cooldown
        # emit vacuum_state
        #self.vac_signal.emit(self._vacum_good)
        self.state_dict[0]['vacuum_state'] = state.GOOD

    # get latest value from gen_monitor
    def update_value(self):
        #if self._connected:
        value = self.gen_monitor.getCounterAndValue(self.id)
        # test if value is a new value, i.e _vac_reading_counter has increased
        # (the gen_monitor will just pass back the latest va;ue it has)
        if value.keys()[0] != self._vac_reading_counter:
            # update _latest_vac_value
            self._latest_vac_value = value.values()[0]
            self.gui_dict[0]['vacuum_level'] = self._latest_vac_value
            # set new _vac_reading_counter
            self._vac_reading_counter = value.keys()[0]
            print('new_value = ', self._latest_vac_value, 'counter  = ',self._vac_reading_counter)
            return True
        #else:
        #    self.connectPV(self.pv)
        return False

