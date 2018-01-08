import monitor


class value_monitor(monitor.monitor):
    # whoami
    my_name = 'value_monitor'
    # the latest signal value
    _latest_value = -1
    # a counter indexing each unique signal reading
    _reading_counter = -1
    def __init__(self,
                 gen_mon,
                 settings_dict,
                 id_key,
                 gui_dict,
                 gui_dict_key,
                 update_time
                 ):
        # init base-class
        # super(monitor, self).__init__()
        monitor.monitor.__init__(self)
        self.gen_monitor = gen_mon
        self.gui_dict = [gui_dict]
        self.gui_dict_key = gui_dict_key
        self.id = settings_dict[id_key]
        # a timer to run check_signal automatically every self.update_time
        self.timer.timeout.connect(self.update_value)
        self.timer.start(self.update_time)

    # get latest value from gen_monitor
    def update_value(self):
        # if self._connected:
        value = self.gen_monitor.getCounterAndValue(self.id)
        # test if value is a new value, i.e _reading_counter has increased
        # (the gen_monitor will just pass back the latest value it has)
        if value.keys()[0] != self._reading_counter:
            # update _latest_value
            self._latest_value = value.values()[0]
            self.gui_dict[0][self.gui_dict_key] = self._latest_value
            # set new _reading_counter
            self._reading_counter = value.keys()[0]
            print(self.my_name, 'new_value = ', self._latest_value, 'counter  = ',self._reading_counter)
            #      self._latest_value-self._mean_level)
            return True
        # else:
        #    self.connectPV(self.pv)
        return False