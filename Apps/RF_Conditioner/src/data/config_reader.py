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
    sol_config = None
    mon_config = None

    #
    llrf_type = LLRF_TYPE.UNKNOWN_TYPE

    def __init__(self):
        dummy = 0

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
        self.sol_parameter()
        self.mon_parameter()
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
                                         config_reader.gui_config,
                                         config_reader.sol_config,
                                         config_reader.mon_config]
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
    # def get_vac_parameter_NO_TYPE(self):
    #     vac_keys = ['VAC_PV','VAC_SPIKE_DELTA','VAC_DECAY_MODE','VAC_SPIKE_DECAY_LEVEL','VAC_SPIKE_DECAY_LEVEL'
    #                 ,'VAC_SPIKE_DECAY_TIME','VAC_NUM_SAMPLES_TO_AVERAGE']
    #     vac_param = self.get_part_dict(vac_keys)
    #     for k, v in vac_param.iteritems():
    #         print k, v
    #     return config_reader.vac_param

    def vac_parameter(self):
        string_param = ['VAC_PV', 'VAC_DECAY_MODE']
        float_param = ['VAC_SPIKE_DECAY_LEVEL', 'VAC_SPIKE_DELTA','VAC_SPIKE_AMP_DROP','VAC_MAX_LEVEL','VAC_MAX_AMP_DROP']
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
                        'OUTSIDE_MASK_PROBE_FILENAME','PULSE_COUNT_BREAKDOWN_LOG_FILENAME',
                        'PULSE_COUNT_BREAKDOWN_LOG_FILENAME',
                        'AMP_POWER_LOG_FILENAME'
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

    def sol_parameter(self):
        string_param=['SOL_PV']
        int_param=['SOL_CHECK_TIME']
        config_reader.sol_config = self.get_param_dict(string_param=string_param,int_param=int_param)
        return config_reader.sol_config

    def llrf_param(self):
        type_param=['RF_STRUCTURE']
        int_param=['TIME_BETWEEN_RF_INCREASES','DEFAULT_RF_INCREASE_LEVEL','RF_REPETITION_RATE','BREAKDOWN_RATE_AIM',
                   'LLRF_CHECK_TIME','NORMAL_POWER_INCREASE','LOW_POWER_INCREASE','LOW_POWER_INCREASE_RATE_LIMIT'
                   ,'NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY','EXTRA_TRACES_ON_BREAKDOWN','NUM_BUFFER_TRACES',
                   'DEFAULT_PULSE_COUNT','MAX_DELTA_AMP_SP'
                   ]
        string_param = []
        monitor_param=['TRACES_TO_SAVE','MEAN_TRACES']
        float_param = ['MEAN_TIME_TO_AVERAGE','RF_INCREASE_LEVEL','RF_INCREASE_RATE','POWER_AIM','PULSE_LENGTH_AIM',
                       'PULSE_LENGTH_STEP','PULSE_LENGTH_START','KLY_PWR_FOR_ACTIVE_PULSE',
                       '1_MEAN_START','1_MEAN_END',
                       '2_MEAN_START','2_MEAN_END',
                       '3_MEAN_START','3_MEAN_END',
                       '4_MEAN_START','4_MEAN_END',
                       '5_MEAN_START','5_MEAN_END',
                       '6_MEAN_START','6_MEAN_END',
                       '7_MEAN_START','7_MEAN_END',
                       '8_MEAN_START','8_MEAN_END',
                       '9_MEAN_START','9_MEAN_END',
                       '10_MEAN_START','10_MEAN_END',
                       '11_MEAN_START','11_MEAN_END',
                       '12_MEAN_START','12_MEAN_END'
                       ]

        config_reader.llrf_config = self.get_param_dict(string_param=string_param,int_param=int_param,
                                   type_param=type_param,monitor_param=monitor_param,
                                   float_param=float_param
                                   )
        return config_reader.llrf_config

    def breakdown_param(self):
        bool_param=['CFPOW_AUTO_SET',
                    'CRPOW_AUTO_SET',
                    'CPPOW_AUTO_SET',
                    'KFPOW_AUTO_SET',
                    'KRPOW_AUTO_SET',
                    'CFPHA_AUTO_SET',
                    'CRPHA_AUTO_SET',
                    'CPPHA_AUTO_SET',
                    'KFPHA_AUTO_SET',
                    'KRPHA_AUTO_SET',

                    'CFPOW_DROP_AMP',
                    'CRPOW_DROP_AMP',
                    'CPPOW_DROP_AMP',
                    'KFPOW_DROP_AMP',
                    'KRPOW_DROP_AMP',
                    'CFPHA_DROP_AMP',
                    'CRPHA_DROP_AMP',
                    'CPPHA_DROP_AMP',
                    'KFPHA_DROP_AMP',
                    'KRPHA_DROP_AMP'

                    ]

        monitor_param = ['BREAKDOWN_TRACES']
        int_param=[
            'CFPOW_MASK_ABS_MIN',
            'CRPOW_MASK_ABS_MIN',
            'CPPOW_MASK_ABS_MIN',
            'KFPOW_MASK_ABS_MIN',
            'KRPOW_MASK_ABS_MIN',
            'CFPHA_MASK_ABS_MIN',
            'CRPHA_MASK_ABS_MIN',
            'CPPHA_MASK_ABS_MIN',
            'KFPHA_MASK_ABS_MIN',
            'KRPHA_MASK_ABS_MIN',

            'CFPOW_MASK_LEVEL',
            'CRPOW_MASK_LEVEL',
            'CPPOW_MASK_LEVEL',
            'KFPOW_MASK_LEVEL',
            'KRPOW_MASK_LEVEL',
            'CFPHA_MASK_LEVEL',
            'CRPHA_MASK_LEVEL',
            'CPPHA_MASK_LEVEL',
            'KFPHA_MASK_LEVEL',
            'KRPHA_MASK_LEVEL',

            'CFPOW_CHECK_STREAK',
            'CRPOW_CHECK_STREAK',
            'CPPOW_CHECK_STREAK',
            'KFPOW_CHECK_STREAK',
            'KRPOW_CHECK_STREAK',
            'CFPHA_CHECK_STREAK',
            'CRPHA_CHECK_STREAK',
            'CPPHA_CHECK_STREAK',
            'KFPHA_CHECK_STREAK',
            'KRPHA_CHECK_STREAK',

            'CFPOW_MASK_FLOOR',
            'CRPOW_MASK_FLOOR',
            'CPPOW_MASK_FLOOR',
            'KFPOW_MASK_FLOOR',
            'KRPOW_MASK_FLOOR',
            'CFPHA_MASK_FLOOR',
            'CRPHA_MASK_FLOOR',
            'CPPHA_MASK_FLOOR',
            'KFPHA_MASK_FLOOR',
            'KRPHA_MASK_FLOOR',

            'CFPOW_NUM_AVERAGE_TRACES',
            'CRPOW_NUM_AVERAGE_TRACES',
            'CPPOW_NUM_AVERAGE_TRACES',
            'KFPOW_NUM_AVERAGE_TRACES',
            'KRPOW_NUM_AVERAGE_TRACES',
            'CFPHA_NUM_AVERAGE_TRACES',
            'CRPHA_NUM_AVERAGE_TRACES',
            'CPPHA_NUM_AVERAGE_TRACES',
            'KFPHA_NUM_AVERAGE_TRACES',
            'KRPHA_NUM_AVERAGE_TRACES',

            'CRPOW_AMP_DROP_VALUE',
            'CPPOW_AMP_DROP_VALUE',
            'KFPOW_AMP_DROP_VALUE',
            'KRPOW_AMP_DROP_VALUE',
            'CFPHA_AMP_DROP_VALUE',
            'CRPHA_AMP_DROP_VALUE',
            'CPPHA_AMP_DROP_VALUE',
            'CFPOW_AMP_DROP_VALUE',
            'KFPHA_AMP_DROP_VALUE',
            'KRPHA_AMP_DROP_VALUE',

            'OUTSIDE_MASK_CHECK_TIME','OUTSIDE_MASK_COOLDOWN_TIME'
            ]



        float_param = ['CFPOW_MASK_START',
                       'CRPOW_MASK_START',
                       'CPPOW_MASK_START',
                       'KFPOW_MASK_START',
                       'KRPOW_MASK_START',
                       'CRPHA_MASK_START',
                       'CPPHA_MASK_START',
                       'CFPHA_MASK_START',
                       'KFPHA_MASK_START',
                       'KRPHA_MASK_START',

                       'CFPOW_MASK_END',
                       'CRPOW_MASK_END',
                       'CPPOW_MASK_END',
                       'KFPOW_MASK_END',
                       'KRPOW_MASK_END',
                       'CFPHA_MASK_END',
                       'CRPHA_MASK_END',
                       'CPPHA_MASK_END',
                       'KFPHA_MASK_END',
                       'KRPHA_MASK_END',

                       'CFPOW_MASK_WINDOW_START',
                       'CRPOW_MASK_WINDOW_START',
                       'CPPOW_MASK_WINDOW_START',
                       'KFPOW_MASK_WINDOW_START',
                       'KRPOW_MASK_WINDOW_START',
                       'CFPHA_MASK_WINDOW_START',
                       'CRPHA_MASK_WINDOW_START',
                       'CPPHA_MASK_WINDOW_START',
                       'KFPHA_MASK_WINDOW_START',
                       'KRPHA_MASK_WINDOW_START',

                       'CFPOW_MASK_WINDOW_END',
                       'CRPOW_MASK_WINDOW_END',
                       'CPPOW_MASK_WINDOW_END',
                       'KFPOW_MASK_WINDOW_END',
                       'KRPOW_MASK_WINDOW_END',
                       'CFPHA_MASK_WINDOW_END',
                       'CRPHA_MASK_WINDOW_END',
                       'CPPHA_MASK_WINDOW_END',
                       'KFPHA_MASK_WINDOW_END',
                       'KRPHA_MASK_WINDOW_END',
                       'PHASE_MASK_BY_POWER_LEVEL_1',
                       'PHASE_MASK_BY_POWER_LEVEL_2']


        string_param=['CFPOW_MASK_TYPE',
                      'CRPOW_MASK_TYPE',
                      'CPPOW_MASK_TYPE',
                      'KFPOW_MASK_TYPE',
                      'KRPOW_MASK_TYPE',
                      'CFPHA_MASK_TYPE',
                      'CRPHA_MASK_TYPE',
                      'CPPHA_MASK_TYPE',
                      'KFPHA_MASK_TYPE',
                      'KRPHA_MASK_TYPE',

                      'CFPOW_MASK_SET_TYPE',
                      'CRPOW_MASK_SET_TYPE',
                      'CPPOW_MASK_SET_TYPE',
                      'KFPOW_MASK_SET_TYPE',
                      'KRPOW_MASK_SET_TYPE',
                      'CRPHA_MASK_SET_TYPE',
                      'CFPHA_MASK_SET_TYPE',
                      'CPPHA_MASK_SET_TYPE',
                      'KFPHA_MASK_SET_TYPE',
                      'KRPHA_MASK_SET_TYPE',
                      'PHASE_MASK_BY_POWER_PHASE_TRACE_1','PHASE_MASK_BY_POWER_POWER_TRACE_1',
                      'PHASE_MASK_BY_POWER_PHASE_TRACE_2','PHASE_MASK_BY_POWER_POWER_TRACE_2'
                      ]
        config_reader.breakdown_config = self.get_param_dict(int_param=int_param,
                                                             bool_param=bool_param,
                                                             monitor_param=monitor_param,
                                                             float_param=float_param,
                                                             string_param=string_param)

        # we do some more manual processing here:
        #cancer


        print 'all breakdown_config keys'
        for key in config_reader.breakdown_config.keys():
            print key


        # this si re-casting the type to int for these paramters if CRP_MASK_SET_TYPE = INDEX
        for key,value in config_reader.breakdown_config.iteritems():
            if '_MASK_SET_TYPE' in key:
                if value == 'INDEX':
                    k = key[:5] + '_MASK_START'
                    config_reader.breakdown_config[k] = int(config_reader.breakdown_config[k])
                    k = key[:5] + '_MASK_END'
                    config_reader.breakdown_config[k] = int(config_reader.breakdown_config[k])
                    k = key[:5] + '_MASK_WINDOW_END'
                    config_reader.breakdown_config[k] = int(config_reader.breakdown_config[k])
                    k = key[:5] + '_MASK_WINDOW_START'
                    config_reader.breakdown_config[k] = int(config_reader.breakdown_config[k])
                if value == 'TIME':
                    k = key[:5] + '_MASK_START'
                    config_reader.breakdown_config[k] = float(config_reader.breakdown_config[k])
                    k = key[:5] + '_MASK_END'
                    config_reader.breakdown_config[k] = float(config_reader.breakdown_config[k])
                    k = key[:5] + '_MASK_WINDOW_END'
                    config_reader.breakdown_config[k] = float(config_reader.breakdown_config[k])
                    k = key[:5] + '_MASK_WINDOW_START'
                    config_reader.breakdown_config[k] = float(config_reader.breakdown_config[k])



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


    def mon_parameter(self):
        ## this picks up any extra PVs that are logged to file, but NOT disdplayed to the GUI
        ## its going to look fo rany keys that have the suffix '_GMON'
        #
        # Loop over each key in config_reader.config looking for _GMON
        #
        for key, value in config_reader.config.iteritems():
            if key[-5:] == '_GMON':
                if config_reader.mon_config == None:
                    config_reader.mon_config = {}
                config_reader.mon_config[ key[:-5] ] = value
                print key[:-5]
                print value
        return config_reader.mon_config

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
            return MACHINE_AREA.VELA_INJ
        elif text == 'ALL_VELA_CLARA':
            return MACHINE_AREA.ALL_VELA_CLARA
        elif text == 'CLARA_PH1':
            return MACHINE_AREA.CLARA_PH1
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