from VELA_CLARA_LLRF_Control import MACHINE_AREA, MACHINE_MODE, LLRF_TYPE

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

    pil_config = None
    llrf_config = None
    mag_config = None
    log_config = None
    machine_mode = None
    gui_config = None

    def __init__(self):
        dummyy = 0

    @property
    def config_file(self):
        return config_reader._config_file

    @config_file.setter
    def config_file(self, value):
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
            content = [x for x in content if x[0] != self.comment]
            # strip to end of entry
            content = [x.split(self.end_of_entry, 1)[0] for x in content]
            # select key value pairs
            content = [x for x in content if self.equals in x]
            # split on equals
            content = [x.split(self.equals) for x in content]
            # select non-empty pairs
            content = [s for s in content if s[0] and s[1]]
            print(content)
            [config_reader.config.update({x[0]: x[1]}) for x in content]
        # try:
        #     config_reader.machine_mode = self.get_machine_mode(config_reader.config['MACHINE_MODE'])
        # except:
        #     return False
        self.pil_parameter()
        self.llrf_parameter()
        self.mag_parameter()
        self.log_param()
        self.gui_param()
        print(config_reader.my_name + ' read input from ' + str(config_reader.config_file))

        config_reader.all_config_data = [config_reader.pil_config,
                                         config_reader.llrf_config,
                                         config_reader.mag_config,
                                         config_reader.log_config,
                                         config_reader.gui_config]

        return self.sanity_checks()

    def sanity_checks(self):
        return True

    # strip whitespace except in string literal
    def stripWS(self, txt):
        a = self.string_literal.join(
            it if i % 2 else ''.join(it.split()) for i, it in enumerate(txt.split(self.string_literal)))
        return a.replace("\"", "")

    # check _config dict for keys and put hits in a new dict
    def get_part_dict(self, keys):
        r = {}
        [r.update({key: config_reader.config[key]}) for key in keys if key in config_reader.config]
        return r

    # //mfw Cancer below\\
    # //we must assume value type\\
    def get_param_dict(self, string_param=[], float_param=[], int_param=[], area_param=[], type_param=[], bool_param=[],
                       monitor_param=[],channel_param=[],diag_param=[],mode_param=[]):
        r = {}
        for item in string_param:
            try:
                r.update({item: config_reader.config[item]})
            except:
                print(self.my_name, " FAILED to Find, ", item)
        for item in int_param:
            try:
                r.update({item: int(config_reader.config[item])})
            except:
                print(self.my_name, " FAILED to Find, ", item)
        for item in float_param:
            try:
                r.update({item: float(config_reader.config[item])})
            except:
                print(self.my_name, " FAILED to Find, ", item)
        for item in area_param:
            try:
                r.update({item: self.get_machine_area(config_reader.config[item])})
            except:
                print(self.my_name, " FAILED to Find, ", item)
        for item in diag_param:
            try:
                r.update({item: self.get_diag_type(config_reader.config[item])})
            except:
                print(self.my_name, " FAILED to Find, ", item)
        for item in mode_param:
            try:
                r.update({item: self.get_machine_mode(config_reader.config[item])})
            except:
                print(self.my_name, " FAILED to Find, ", item)
        for item in type_param:
            try:
                r.update({item: self.get_llrf_type(config_reader.config[item])})
            except:
                print(self.my_name, " FAILED to Find, ", item)
        for item in bool_param:
            try:
                r.update({item: self.get_bool(config_reader.config[item])})
            except:
                print(self.my_name, " FAILED to Find, ", item)
        # for k, v in r.iteritems():
        #     print k, v
        return r

    def pil_parameter(self):
        string_param = ['PIL_NAME','LAS_EM_NAME','HWP_NAME']
        area_param = ['PIL_AREA']
        mode_param = ['PIL_MODE']
        int_param = ['PIL_CHECK_TIME']
        config_reader.pil_config = self.get_param_dict(string_param=string_param, area_param=area_param,
                                                       int_param=int_param,mode_param=mode_param)
        return config_reader.pil_config

    def llrf_parameter(self):
        string_param = ['LLRF_NAME']
        area_param = ['LLRF_AREA']
        int_param = ['LLRF_CHECK_TIME']
        mode_param = ['LLRF_MODE','MACHINE_MODE']
        type_param = ['LLRF_TYPE']
        config_reader.llrf_config = self.get_param_dict(string_param=string_param, area_param=area_param,
                                                        int_param=int_param, mode_param=mode_param, type_param=type_param)
        return config_reader.llrf_config

    def mag_parameter(self):
        string_param = ['BSOL_NAME','SOL_NAME']
        area_param = ['MACHINE_AREA']
        int_param = ['MAG_CHECK_TIME']
        mode_param = ['MACHINE_MODE']
        config_reader.mag_config = self.get_param_dict(string_param=string_param, area_param=area_param,
                                                         int_param=int_param,mode_param=mode_param)
        return config_reader.mag_config

    def log_param(self):
        string_param = ['LOG_FILENAME', 'LOG_DIRECTORY', 'DATA_LOG_FILENAME', 'FILE_DIRECTORY', 'SUMMARY_FILE']
        int_param = ['DATA_LOG_TIME']
        config_reader.log_config = self.get_param_dict(string_param=string_param, int_param=int_param)
        return config_reader.log_config


    def gui_param(self):
        int_param = ['GUI_UPDATE_TIME']
        config_reader.gui_config = self.get_param_dict(int_param=int_param)
        return config_reader.gui_config

    def settings(self):
        r = {}
        return r

    def get_bool(self, text):
        if text == 'TRUE':
            return True
        elif text == 'FALSE':
            return False

    def get_machine_area(self, text):
        if text == 'S01':
            return MACHINE_AREA.CLARA_S01
        elif text == 'VELA_INJ':
            return MACHINE_AREA.VELA_INJ
        elif text == 'CLARA_PH1':
            return MACHINE_AREA.CLARA_PH1
        elif text == 'C2B':
            return MACHINE_AREA.CLARA_2_BA1_BA2
        else:
            return MACHINE_AREA.UNKNOWN_AREA

    def get_machine_mode(self, text):
        if text == 'PHYSICAL':
            return MACHINE_MODE.PHYSICAL
        elif text == 'VIRTUAL':
            return MACHINE_MODE.VIRTUAL
        elif text == 'OFFLINE':
            return MACHINE_MODE.OFFLINE

    def get_llrf_type(self, text):
        if text == 'CLARA_LRRG':
            return LLRF_TYPE.CLARA_LRRG
        else:
            return LLRF_TYPE.UNKNOWN_TYPE