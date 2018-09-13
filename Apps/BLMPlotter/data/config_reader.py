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

    blm_config = None
    log_config = None
    charge_config = None
    machine_mode = None
    gui_config = None

    def __init__(self):
        dummyy = 0

    # parse the text file and create config_dict
    def get_config(self):
        # clear existing data
        config_reader.config = {}
        self.blm_parameter()
        self.log_param()
        self.charge_parameter()

        config_reader.all_config_data = [config_reader.blm_config,
                                         config_reader.log_config,
                                         config_reader.charge_config]

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
        for item in bool_param:
            try:
                r.update({item: self.get_bool(config_reader.config[item])})
            except:
                print(self.my_name, " FAILED to Find, ", item)
        # for k, v in r.iteritems():
        #     print k, v
        return r

    def blm_parameter(self):
        string_param = ['BLM_NAMES']
        config_reader.blm_config = self.get_param_dict(string_param=string_param)
        return config_reader.blm_config

    def charge_parameter(self):
        string_param = ['CHARGE_NAME','CHARGE_DIAG_TYPE']
        config_reader.charge_config = self.get_param_dict(string_param=string_param)
        return config_reader.charge_config

    def log_param(self):
        string_param = ['LOG_FILENAME', 'LOG_DIRECTORY', 'DATA_LOG_FILENAME']
        int_param = ['DATA_LOG_TIME']
        config_reader.log_config = self.get_param_dict(string_param=string_param, int_param=int_param)
        return config_reader.log_config

    def settings(self):
        r = {}
        return r

    def get_bool(self, text):
        if text == 'TRUE':
            return True
        elif text == 'FALSE':
            return False