import monitor
import pickle
import data.rf_condition_data_base as dat
import os
import datetime
#from VELA_CLARA_enums import STATE
from data.state import state


class outside_mask_trace_monitor(monitor.monitor):
    #whoami
    my_name = 'outside_mask_trace_monitor'
    outside_mask_trace_count = 0
    previous_outside_mask_trace_count = 0
    forward_power_data = {}
    reverse_power_data = {}
    probe_power_data = {}
    CFP = None
    CRP = None
    CPP = None

    def __init__(self,
                 llrf_controller,
                 data_dict,
                 llrf_param,
                 log_param,
                 breakdown_param
                ):
        # init base-class
        monitor.monitor.__init__(self,timed_cooldown=True)
        # output file info
        for trace in llrf_param['TRACES_TO_SAVE']:
            if "CAVITY_REVERSE_POWER" in trace:
                self.CRP = trace
                print(self.my_name + ' has ' + self.CRP)
            if "CAVITY_FORWARD_POWER" in trace:
                self.CFP = trace
                print(self.my_name + ' has ' + self.CFP)
            if "PROBE_POWER" in trace:
                self.CPP = trace
                print(self.my_name + ' has ' + self.CPP)
        try:
            log_start = datetime.datetime.now()
            time = str(log_start.year) + '-' + \
                   '{:02d}'.format(log_start.month) + '-' + \
                   '{:02d}'.format(log_start.day) + '-' + \
                   '{:02d}'.format(log_start.hour) + '-' + \
                   '{:02d}'.format(log_start.minute) + '-' + \
                   '{:02d}'.format(log_start.second)
            self.directory = log_param['OUTSIDE_MASK_DIRECTORY']+'\\' + time #MAGIC_STRING
            os.makedirs(self.directory)
            print 'DIRECTORY = ' + self.directory
        except:
            self.directory = None
        try:
            self.forward_file = self.directory +'\\' + log_param['OUTSIDE_MASK_FORWARD_FILENAME']#MAGIC_STRING
        except:
            self.forward_file = None
        try:
            self.reverse_file = self.directory +'\\' + log_param['OUTSIDE_MASK_REVERSE_FILENAME']#MAGIC_STRING
        except:
            self.reverse_file = None
        try:
            self.probe_file = self.directory +'\\' + log_param['OUTSIDE_MASK_PROBE_FILENAME']#MAGIC_STRING
        except:
            self.probe_file = None#add to attributes
        self.llrf = llrf_controller
        self.llrfObj = [self.llrf.getLLRFObjConstRef()]
        self.data_dict = data_dict
        self.timer.timeout.connect(self.update_value)
        self.timer.start(breakdown_param['OUTSIDE_MASK_CHECK_TIME'])
        self.data_dict[dat.breakdown_status] = state.GOOD

    def cooldown_function(self):
        print self.my_name + ' monitor function called, cool down ended'
        self.incool_down = False
        self.data_dict[dat.breakdown_status] = state.GOOD

    def update_value(self):
        self.data_dict[dat.breakdown_rate] = self.llrfObj[0].breakdown_rate
        self.data_dict[dat.pulse_count] = self.llrfObj[0].activePulseCount
        #~print ('pulse count  ', self.llrf.getActivePulseCount())
        self.data_dict[dat.elapsed_time] = self.llrf.elapsedTime()
        self.data_dict[dat.num_outside_mask_traces] = self.llrfObj[0].num_outside_mask_traces
        _count = self.llrfObj[0].num_outside_mask_traces
        #print(self.my_name + ' checking, cont = ' +str(_count))
        if _count > self.previous_outside_mask_trace_count:
            print(self.my_name +' NEW OUTSIDE MASK TRACE DETECTED, entering cooldown')
            self.data_dict[dat.breakdown_status] = state.BAD
            self.cooldown_timer.start(self.breakdown_param['OUTSIDE_MASK_COOLDOWN_TIME'])

            #THE BELOW HAS DISABLED DATA SAVING"!!!!!
            #self.get_new_outside_mask_traces(_count)
            self.previous_outside_mask_trace_count = _count

    def get_new_outside_mask_traces(self, _count):
        for i in range(self.previous_outside_mask_trace_count, _count):
            print(self.my_name + ' gettingoutside_mask_trace ' + str(i))
            new = self.llrf.getOutsideMaskData(i)
            print(self.my_name + ' new trace ' + new['trace_name'])
            if 'FORWARD' in new['trace_name']:
                self.forward_power_data.update(new)
                self.save(self.forward_file,new)
                print(self.my_name + ' forward trace outside mask!',len(self.forward_power_data))
            elif 'REVERSE' in new['trace_name']:
                self.reverse_power_data.update(new)
                self.save(self.reverse_file,new)
                print(self.my_name + ' reverse trace outside mask!', len(self.reverse_power_data))
            elif 'PROBE' in new['trace_name']:
                self.probe_power_data.update(new)
                self.save(self.probe_file,new)
                print(self.my_name + ' probe trace outside mask!', len(self.probe_power_data))

    def save_breakdown(self, obj, num):
        fn = self.log_directory + '/' + self.breakdown_file + '_' + str(num)
        self.save(fn, obj)

    def dump_breakdown_data(self):
        self.update_value()
        fn = self.log_directory + '/' + self.breakdown_file
        self.save(fn, self.breakdown_data)
    
    # noinspection PyMethodMayBeStatic
    def save(self, path, obj):
        with open(path + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
