from monitor import monitor


class value_monitor(monitor):
    # whoami
    my_name = 'value_monitor'
    # get latest value from gen_monitor
    def __init__(self,
                 gen_mon=None,
                 id_key='',
                 data_dict_key='',
                 my_name ='value_monitor',
                 update_time=1000
                 ):
        # init base-class
        # super(monitor, self).__init__()
        monitor.__init__(self,update_time=1000)

        # the latest signal value
        self._latest_value = -1
        # a counter indexing each unique signal reading
        self._reading_counter = -1
        # successfully instantiated and 'working'
        self.set_success = False

        self.my_name = my_name
        self.gen_monitor = gen_mon
        #self.data_dict = monitor.data.values
        self.data_dict_key = data_dict_key
        self.id = id_key
        # a timer to run check_signal automatically every self.update_time
        if isinstance(self.id, basestring):
            monitor.logger.message(self.my_name + ' got single gen_mon ID', True)
            self.timer.timeout.connect(self.update_value)
            self.timer.start(update_time)
            self.set_success = True

        elif isinstance(self.id, list):
            monitor.logger.message(self.my_name + ' got list of gen_mon IDs', True)
            self._latest_value = [-1]*len(self.id)
            self._reading_counter = [-1]*len(self.id)
            self.timer.timeout.connect(self.update_values)
            self.timer.start(update_time)
            self.set_success = True

    def update_value(self):
        #monitor.logger.message(self.my_name + ' gen_mon update_value', True)
        # if self._connected:
        value = self.gen_monitor.getCounterAndValue(self.id)
        # test if value is a new value, i.e _reading_counter has increased
        # (the gen_monitor will just pass back the latest value it has)
        if value.keys()[0] != self._reading_counter:
            # update _latest_value
            self._latest_value = value.values()[0]
            monitor.data.values[self.data_dict_key] = self._latest_value
            # set new _reading_counter
            self._reading_counter = value.keys()[0]
            #print(self.my_name, ' new_value = ', self._latest_value, 'counter  = ',self._reading_counter)

    def update_values(self):
        for i, id in enumerate(self.id):
            value = self.gen_monitor.getCounterAndValue(id)
            # if self._connected:
            if value.keys()[0] != self._reading_counter[i]:
                # update _latest_value
                monitor.data.values[self.data_dict_key[i]] = value.values()[0]
                # set new _reading_counter
                self._reading_counter[i] = value.keys()[0]
                # print(self.my_name, ' new_value = ', self._latest_value, 'counter  = ',self._reading_counter)

