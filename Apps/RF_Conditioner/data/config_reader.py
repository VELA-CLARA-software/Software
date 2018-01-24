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
    my_name = 'config_reader'
    # config file special characters
    comment = '#'
    end_of_entry = ';'
    string_literal = '"'
    equals = '='
    # parsed config data
    config = {}

    #
    logger = None

    have_config = False
    _config_file = None

    all_config_data = None

    vac_config= None
    DC_config = None
    log_config = None
    vac_valve_config= None
    water_temp_config= None
    cavity_temp_config = None
    llrf_config = None
    breakdown_config = None
    mod_config = None
    rfprot_config = None
    gui_config = None

    #
    llrf_type = LLRF_TYPE.UNKNOWN_TYPE

    def __init__(self):
        dummyy = 0

    @property
    def config_file(self):
        return config_reader._config_file
    @config_file.setter
    def config_file(self,value):
        config_reader._config_file = value

    # parse the text file and create config_dict
    def get_config(self):
        # clear existing data
        config_reader.config = {}
        with open(config_reader._config_file) as f:
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
            [config_reader.config.update({x[0]: x[1]}) for x in content]
        # at  minimum the  config needs to give a llf_type
        try:
            config_reader.llrf_type = self.get_llrf_type(config_reader.config['RF_STRUCTURE'])
        except:
            return False
        self.vac_parameter()
        self.DC_parameter()
        self.log_param()
        self.vac_valve_parameter()
        self.water_temp_parameter()
        self.cavity_temp_parameter()
        self.llrf_param()
        self.breakdown_param()
        self.mod_param()
        self.rfprot_param()
        self.gui_param()
        print(config_reader.my_name + ' read input from ' + str(config_reader.config_file) )

        config_reader.all_config_data = [config_reader.vac_config,
                                         config_reader.DC_config,
                                         config_reader.log_config,
                                         config_reader.vac_valve_config,
                                         config_reader.water_temp_config,
                                         config_reader.cavity_temp_config,
                                         config_reader.llrf_config,
                                         config_reader.breakdown_config,
                                         config_reader.mod_config,
                                         config_reader.rfprot_config,
                                         config_reader.gui_config]
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
        [r.update({key:config_reader.config[key]}) for key in keys if key in config_reader.config ]
        return r
    #//mfw Cancer below\\
    #//we must assume value type\\
    def get_param_dict(self,string_param=[],float_param=[],int_param=[],area_param=[],type_param=[],bool_param=[],monitor_param=[]):
        r = {}
        for item in string_param:
            try:
                r.update({item: config_reader.config[item]})
            except:
                print(self.my_name," FAILED to Find, ",item)
        for item in int_param:
            try:
                r.update({item: int(config_reader.config[item])})
            except:
                print(self.my_name," FAILED to Find, ",item)
        for item in float_param:
            try:
                r.update({item: float(config_reader.config[item])})
            except:
                print(self.my_name," FAILED to Find, ",item)
        for item in area_param:
            try:
                r.update({item: self.get_machine_area(config_reader.config[item])})
            except:
                print(self.my_name," FAILED to Find, ",item)
        for item in type_param:
            try:
                r.update({item: self.get_llrf_type(config_reader.config[item])})
                self.llrf_type = r[item]
            except:
                print(self.my_name," FAILED to Find, ",item)
        for item in bool_param:
            try:
                r.update({item: self.get_bool(config_reader.config[item])})
            except:
                print(self.my_name," FAILED to Find, ",item)
        for item in monitor_param:
            try:
                r.update({item: self.get_traces_to_monitor(config_reader.config[item])})
            except:
                print(self.my_name, " FAILED to Find, ", item)
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
        return config_reader.vac_param

    def vac_parameter(self):
        string_param = ['VAC_PV', 'VAC_DECAY_MODE']
        float_param = ['VAC_SPIKE_DECAY_LEVEL', 'VAC_SPIKE_DELTA','VAC_SPIKE_AMP_DROP']
        int_param = ['VAC_NUM_SAMPLES_TO_AVERAGE','VAC_SPIKE_DECAY_TIME','VAC_CHECK_TIME','OUTSIDE_MASK_COOLDOWN_TIME']
        bool_param = ['VAC_SHOULD_DROP_AMP']
        config_reader.vac_config = self.get_param_dict(string_param=string_param,float_param=float_param,
                                                    int_param=int_param,bool_param=bool_param)
        return config_reader.vac_config

    def DC_parameter(self):
        string_param = ['DC_PV', 'DC_DECAY_MODE']
        float_param = ['DC_SPIKE_DECAY_LEVEL', 'DC_SPIKE_DELTA','DC_SPIKE_AMP_DROP']
        int_param = ['DC_NUM_SAMPLES_TO_AVERAGE','DC_SPIKE_DECAY_TIME','DC_CHECK_TIME','OUTSIDE_MASK_COOLDOWN_TIME']
        bool_param = ['DC_SHOULD_DROP_AMP']
        config_reader.DC_config = self.get_param_dict(string_param=string_param,float_param=float_param,
                                                    int_param=int_param,bool_param=bool_param)
        return config_reader.DC_config


    def log_param(self):
        string_param = ['LOG_FILENAME','LOG_DIRECTORY','DATA_LOG_FILENAME',
                        'OUTSIDE_MASK_FORWARD_FILENAME','OUTSIDE_MASK_REVERSE_FILENAME',
                        'OUTSIDE_MASK_PROBE_FILENAME','PULSE_COUNT_BREAKDOWN_LOG_FILENAME'
                        ]
        int_param = ['DATA_LOG_TIME','AMP_PWR_LOG_TIME']
        config_reader.log_config = self.get_param_dict(string_param=string_param,int_param=int_param)
        return config_reader.log_config

    def vac_valve_parameter(self):
        string_param = ['VAC_VALVE']
        area_param = ['VAC_VALVE_AREA']
        int_param = ['VAC_VALVE_CHECK_TIME']
        config_reader.vac_valve_config = self.get_param_dict(string_param=string_param,area_param=area_param,
                                                       int_param=int_param)
        return config_reader.vac_valve_config

    def water_temp_parameter(self):
        string_param=['WATER_TEMPERATURE_PV']
        int_param=['WATER_TEMPERATURE_CHECK_TIME']
        config_reader.water_temp_config = self.get_param_dict(string_param=string_param,int_param=int_param)
        return config_reader.water_temp_config

    def cavity_temp_parameter(self):
        string_param=['CAVITY_TEMPERATURE_PV']
        int_param=['CAVITY_TEMPERATURE_CHECK_TIME']
        config_reader.cavity_temp_config = self.get_param_dict(string_param=string_param,int_param=int_param)
        return config_reader.cavity_temp_config

    def llrf_param(self):
        type_param=['RF_STRUCTURE']
        int_param=['TIME_BETWEEN_RF_INCREASES','DEFAULT_RF_INCREASE_LEVEL','RF_REPETITION_RATE','BREAKDOWN_RATE_AIM',
                   'LLRF_CHECK_TIME','NORMAL_POWER_INCREASE','LOW_POWER_INCREASE','LOW_POWER_INCREASE_RATE_LIMIT'
                   ,'NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY'
                   ]
        string_param=[]
        monitor_param=['TRACES_TO_SAVE']
        float_param = ['MEAN_TIME_TO_AVERAGE','RF_INCREASE_LEVEL','RF_INCREASE_RATE','POWER_AIM','PULSE_LENGTH_AIM',
                      'PULSE_LENGTH_STEP','PULSE_LENGTH_START']
        config_reader.llrf_config = self.get_param_dict(string_param=string_param,int_param=int_param,
                                   type_param=type_param,monitor_param=monitor_param,
                                   float_param=float_param
                                   )
        return config_reader.llrf_config

    def breakdown_param(self):
        bool_param=['CRP_AUTO_SET','CFP_AUTO_SET','CPP_AUTO_SET','CRP_AMP_DROP','CFP_AMP_DROP','CPP_AMP_DROP']
        monitor_param = ['BREAKDOWN_TRACES']
        int_param=[
            'CRP_S1','CRP_S2','CRP_S3','CRP_S4','CRP_MASK_LEVEL','CRP_CHECK_STREAK','CRP_MASK_FLOOR','CRP_NUM_AVERAGE_TRACES',
            'CFP_S1','CFP_S2','CFP_S3','CFP_S4','CFP_MASK_LEVEL','CFP_CHECK_STREAK','CFP_MASK_FLOOR','CFP_NUM_AVERAGE_TRACES',
            'CPP_S1','CPP_S2','CPP_S3','CPP_S4','CPP_MASK_LEVEL','CPP_CHECK_STREAK','CPP_MASK_FLOOR','CPP_NUM_AVERAGE_TRACES',
            'CRP_AMP_DROP_VAL','CFP_AMP_DROP_VAL','CPP_AMP_DROP_VAL','OUTSIDE_MASK_CHECK_TIME','OUTSIDE_MASK_COOLDOWN_TIME'
            ]
        float_param = ['CRP_MASK_END','CFP_MASK_END','CPP_MASK_END']
        string_param=['CRP_MASK_TYPE','CFP_MASK_TYPE','CPP_MASK_TYPE']
        config_reader.breakdown_config = self.get_param_dict(int_param=int_param, bool_param=bool_param, monitor_param=monitor_param,float_param=float_param, string_param=string_param)
        return config_reader.breakdown_config

    def mod_param(self):
        int_param=['MOD_CHECK_TIME']
        config_reader.mod_config = self.get_param_dict(int_param=int_param)
        return config_reader.mod_config

    def rfprot_param(self):
        int_param=['RF_PROT_CHECK_TIME']
        string_param=['RF_STRUCTURE']
        config_reader.rfprot_config = self.get_param_dict(string_param=string_param,int_param=int_param)
        return config_reader.rfprot_config

    def gui_param(self):
        int_param=['GUI_UPDATE_TIME']
        config_reader.gui_config = self.get_param_dict(int_param=int_param)
        return config_reader.gui_config

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
        elif text == 'VELA_INJ':
            print('VELA_INJ AREA')
            return MACHINE_AREA.VELA_INJ
        else:
            return MACHINE_AREA.UNKNOWN_AREA

    # this is prtobably not needed for guns!!!!
    def which_cavity(self,trace):
        if self.llrf_type == LLRF_TYPE.CLARA_HRRG:
            return trace.replace("CAVITY","CAVITY")
        elif  self.llrf_type == LLRF_TYPE.CLARA_LRRG:
            return trace.replace("CAVITY","CAVITY")
        elif  self.llrf_type == LLRF_TYPE.VELA_LRRG:
            return trace.replace("CAVITY","CAVITY")
        elif  self.llrf_type == LLRF_TYPE.VELA_HRRG:
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