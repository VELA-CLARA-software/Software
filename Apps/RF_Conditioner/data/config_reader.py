# DJS Sept 2017
#
# read in config files
# generic, following similar style to hwc config
#
# this class needs to know:
#       all possible keywords
#       what part of the app they are needed for
#       the type of their value, (string, int, float, bool)
# once the config file is parsed functions can be called
# to retrieve processed data for as particular item (i.e vacuum monitoring)
from VELA_CLARA_enums import MACHINE_AREA
from VELA_CLARA_LLRF_Control import LLRF_TYPE


class config_reader(object):
    # whoami
    name = 'config_reader'
    # config file special characters
    comment = '#'
    end_of_entry = ';'
    string_literal = '"'
    equals = '='
    # parsed config data
    _config_dict = {}

    def __init__(self, filename = ""):
        self._filename = filename
        self.llrf_type = LLRF_TYPE.UNKNOWN_TYPE

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self,value):
        self._filename = value

    # parse the text file and create config_dict
    def get_config(self):
        # type: () -> object
        # clear existing data
        self._config_dict = {}
        with open(self._filename) as f:
            content = f.readlines()
            # remove whitespace characters like `\n` at the end of each line
            content = [self.stripWS(x) for x in content]
            # select non-empty strings
            content = [s for s in content if s]
            # remove comment lines
            content = [x for x in content if x[0]!= self.comment ]
            # strip to end of entry
            content = [x.split(self.end_of_entry, 1)[0] for x in content]
            # select key value pairs
            content = [x for x in content if self.equals in x]
            # split on equals
            content = [x.split(self.equals) for x in content]
            # select non-empty pairs
            content = [s for s in content if s[0] and s[1]]
            print content
            [self._config_dict.update({x[0]: x[1]}) for x in content]
        # at  minimum the  config needs to give a llf_type
        try:
            self.llrf_type = self.get_llrf_type(self._config_dict['RF_STRUCTURE'])
        except:
            return False
        return self.sanity_checks()

    def sanity_checks(self):
        if self.llrf_type == LLRF_TYPE.UNKNOWN_TYPE:
            return False

        return True

    # strip whitespace except in string literal
    def stripWS(self,txt):
        a = self.string_literal.join(it if i % 2 else ''.join(it.split())for i, it in enumerate(txt.split(self.string_literal)))
        return a.replace("\"", "")

    # check _config dict for keys and put hits in a new dict
    def get_part_dict(self,keys):
        r = {}
        [r.update({key:self._config_dict[key]}) for key in keys if key in self._config_dict ]
        return r
    #//mfw Cancer below\\
    #//we must assume value type\\
    def get_param_dict(self,string_param=[],float_param=[],int_param=[],area_param=[],type_param=[],bool_param=[],monitor_param=[]):
        r = {}
        for item in string_param:
            try:
                r.update({item: self._config_dict[item]})
            except:
                print(self.name," FAILED to Find, ",item)
        for item in int_param:
            try:
                r.update({item: int(self._config_dict[item])})
            except:
                print(self.name," FAILED to Find, ",item)
        for item in float_param:
            try:
                r.update({item: float(self._config_dict[item])})
            except:
                print(self.name," FAILED to Find, ",item)
        for item in area_param:
            try:
                r.update({item: self.get_machine_area(self._config_dict[item])})
            except:
                print(self.name," FAILED to Find, ",item)
        for item in type_param:
            try:
                r.update({item: self.get_llrf_type(self._config_dict[item])})
                self.llrf_type = r[item]
            except:
                print(self.name," FAILED to Find, ",item)
        for item in bool_param:
            try:
                r.update({item: self.get_bool(self._config_dict[item])})
            except:
                print(self.name," FAILED to Find, ",item)
        for item in monitor_param:
            try:
                r.update({item: self.get_traces_to_monitor(self._config_dict[item])})
            except:
                print(self.name, " FAILED to Find, ", item)
        # for k, v in r.iteritems():
        #     print k, v
        return r
    # neater but not type for values
    def get_vac_parameter_NO_TYPE(self):
        vac_keys = ['VAC_PV','VAC_SPIKE_DELTA','VAC_DECAY_MODE','VAC_SPIKE_DECAY_LEVEL','VAC_SPIKE_DECAY_LEVEL'
                    ,'VAC_SPIKE_DECAY_TIME','VAC_NUM_SAMPLES_TO_AVERAGE']
        vac_param = self.get_part_dict(vac_keys)
        for k, v in vac_param.iteritems():
            print k, v
        return vac_param

    def vac_parameter(self):
        string_param = ['VAC_PV', 'VAC_DECAY_MODE']
        float_param = ['VAC_SPIKE_DECAY_LEVEL', 'VAC_SPIKE_DELTA']
        int_param = ['VAC_NUM_SAMPLES_TO_AVERAGE','VAC_SPIKE_DECAY_TIME','VAC_CHECK_TIME']
        return self.get_param_dict(string_param=string_param,float_param=float_param,int_param=int_param)

    def DC_parameter(self):
        string_param = ['DC_PV', 'DC_DECAY_MODE']
        float_param = ['DC_SPIKE_DECAY_LEVEL', 'DC_SPIKE_DELTA']
        int_param = ['DC_NUM_SAMPLES_TO_AVERAGE','DC_SPIKE_DECAY_TIME','DC_CHECK_TIME']
        return self.get_param_dict(string_param=string_param,float_param=float_param,int_param=int_param)

    def log_param(self):
        string_param = ['LOG_FILENAME','LOG_DIRECTORY','DATA_LOG_FILENAME','DATA_LOG_DIRECTORY',
                        'OUTSIDE_MASK_FORWARD_FILENAME','OUTSIDE_MASK_REVERSE_FILENAME','OUTSIDE_MASK_DIRECTORY','OUTSIDE_MASK_PROBE_FILENAME']
        int_param = ['DATA_LOG_TIME']
        return self.get_param_dict(string_param=string_param,int_param=int_param)

    def vac_valve_parameter(self):
        string_param = ['VAC_VALVE']
        area_param = ['VAC_VALVE_AREA']
        int_param = ['VAC_VALVE_CHECK_TIME']
        return self.get_param_dict(string_param=string_param,area_param=area_param,int_param=int_param)

    def water_temp_parameter(self):
        string_param=['WATER_TEMPERATURE_PV']
        int_param=['WATER_TEMPERATURE_CHECK_TIME']
        return self.get_param_dict(string_param=string_param,int_param=int_param)

    def cavity_temp_parameter(self):
        string_param=['CAVITY_TEMPERATURE_PV']
        int_param=['CAVITY_TEMPERATURE_CHECK_TIME']
        return self.get_param_dict(string_param=string_param,int_param=int_param)

    def llrf_param(self):
        type_param=['RF_STRUCTURE']
        int_param=['TIME_BETWEEN_RF_INCREASES','DEFAULT_RF_INCREASE_LEVEL','RF_REPETITION_RATE','BREAKDOWN_RATE_AIM',
                   'LLRF_CHECK_TIME']
        string_param=['CRP_MASK_TYPE','CFP_MASK_TYPE','BREAKDOWN_FILENAME','BREAKDOWN_DIRECTORY']
        monitor_param=['TRACES_TO_SAVE']
        float_param=['MEAN_TIME_TO_AVERAGE','RF_INCREASE_LEVEL']
        return self.get_param_dict(string_param=string_param,int_param=int_param,
                                   type_param=type_param,monitor_param=monitor_param,
                                   float_param=float_param
                                   )



    def breakdown_param(self):
        bool_param=['CRP_AUTO_SET','CFP_AUTO_SET','CPP_AUTO_SET','CRP_AMP_DROP','CFP_AMP_DROP','CPP_AMP_DROP']
        monitor_param = ['BREAKDOWN_TRACES']
        int_param=[
            'CRP_S1','CRP_S2','CRP_S3','CRP_S4','CRP_MASK_LEVEL','CRP_CHECK_STREAK','CRP_MASK_FLOOR','CRP_NUM_AVERAGE_TRACES',
            'CFP_S1','CFP_S2','CFP_S3','CFP_S4','CFP_MASK_LEVEL','CFP_CHECK_STREAK','CFP_MASK_FLOOR','CFP_NUM_AVERAGE_TRACES',
            'CPP_S1','CPP_S2','CPP_S3','CPP_S4','CPP_MASK_LEVEL','CPP_CHECK_STREAK','CPP_MASK_FLOOR','CPP_NUM_AVERAGE_TRACES',
            'CRP_AMP_DROP_VAL','CFP_AMP_DROP_VAL','CPP_AMP_DROP_VAL','OUTSIDE_MASK_CHECK_TIME'
            ]
        float_param = ['CRP_MASK_END','CFP_MASK_END','CPP_MASK_END']
        string_param=['CRP_MASK_TYPE','CFP_MASK_TYPE','CPP_MASK_TYPE']
        return self.get_param_dict(int_param=int_param,bool_param=bool_param,monitor_param=monitor_param,float_param=float_param,string_param=string_param)

    def mod_param(self):
        int_param=['MOD_CHECK_TIME']
        return self.get_param_dict(int_param=int_param)

    def rfprot_param(self):
        int_param=['RF_PROT_CHECK_TIME']
        string_param=['RF_STRUCTURE']
        return self.get_param_dict(string_param=string_param,int_param=int_param)

    def gui_param(self):
        int_param=['GUI_UPDATE_TIME']
        return self.get_param_dict(int_param=int_param)


    def settings(self):
        r ={}
        return r


    def get_llrf_type(self,text):
        if text == "CLARA_HRRG":
            return LLRF_TYPE.CLARA_HRRG
        elif text == 'CLARA_LRRG':
            return LLRF_TYPE.CLARA_LRRG
        elif text == 'VELA_HRRG':
            return LLRF_TYPE.VELA_HRRG
        elif text == 'VELA_LRRG':
            return LLRF_TYPE.VELA_LRRG
        elif text == 'L01':
            return LLRF_TYPE.L01
        else:
            return LLRF_TYPE.UNKNOWN_TYPE

    def get_bool(self,text):
        if text == 'TRUE':
            return True
        elif text == 'FALSE':
            return False

    def get_machine_area(self,text):
        if text == 'S01':
            return MACHINE_AREA.CLARA_S01
        elif text == 'INJ':
            return MACHINE_AREA.VELA_INJ
        else:
            return MACHINE_AREA.UNKNOWN_AREA

    # this is prtobably not needed for guns!!!!
    def which_cavity(self,trace):
        if self.llrf_type == LLRF_TYPE.CLARA_HRRG:
            return trace.replace("CAVITY","CAVITY")
        elif  self.llrf_type == LLRF_TYPE.CLARA_LRRG:
            return trace.replace("CAVITY","CAVITY")
        elif  self.llrf_type == LLRF_TYPE.L01:
            return trace.replace("CAVITY", "L01_CAVITY")
        else:
            return "error"

    def get_traces_to_monitor(self,traces_to_monitor):
        #print 'get_traces_to_monitor'
        traces = []
        for trace in traces_to_monitor.split(','):
            if "CAVITY" in trace and "PROBE" not in trace:#MAGIC_STRING
                traces.append(self.which_cavity(trace))
            else:
                traces.append(trace)
            #print('NEW TRACE To Monitor',traces[-1])
        return traces