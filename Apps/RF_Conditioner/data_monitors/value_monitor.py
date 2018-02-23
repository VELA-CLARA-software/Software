from monitor import monitor


class value_monitor(monitor):
    # whoami
    my_name = 'value_monitor'
    # the latest signal value
    _latest_value = -1
    # a counter indexing each unique signal reading
    _reading_counter = -1
    # successfully instantiated and 'working'
    set_success = False

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
        self.my_name = my_name
        self.gen_monitor = gen_mon
        #self.data_dict = monitor.data.values
        self.data_dict_key = data_dict_key
        self.id = id_key
        # a timer to run check_signal automatically every self.update_time
        self.timer.timeout.connect(self.update_value)
        self.timer.start(update_time)
        self.set_success = True

    def update_value(self):
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
