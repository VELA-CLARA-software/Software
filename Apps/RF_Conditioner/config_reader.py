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

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self,value):
        self._filename = value

    # parse the text file and create config_dict
    def get_config(self):
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
        return False

    # strip whitespace except in string literal
    def stripWS(self,txt):
        return self.string_literal.join(it if i % 2 else ''.join(it.split())for i, it in enumerate(txt.split(self.string_literal)))

    # check _config dict for keys and put hits in a new dict
    def get_part_dict(self,keys):
        r = {}
        [r.update({key:self._config_dict[key]}) for key in keys if key in self._config_dict ]
        return r
    #//mfw Cancer below\\
    #//we must assume value type\\
    def get_param_dict(self,string_param,float_param,int_param):
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
        for k, v in r.iteritems():
            print k, v
        return r
    # neater but not type for values
    def get_vac_parameter_NO_TYPE(self):
        vac_keys = ['VAC_PV','VAC_SPIKE_DELTA','VAC_DECAY_MODE','VAC_SPIKE_DECAY_LEVEL','VAC_SPIKE_DECAY_LEVEL'
                    ,'VAC_SPIKE_DECAY_TIME','VAC_NUM_SAMPLES_TO_AVERAGE']
        vac_param = self.get_part_dict(vac_keys)
        for k, v in vac_param.iteritems():
            print k, v
        return vac_param


    def get_vac_parameter(self):
        string_param = ['VAC_PV', 'VAC_DECAY_MODE',]
        float_param = ['VAC_SPIKE_DECAY_LEVEL', 'VAC_SPIKE_DELTA']
        int_param = ['VAC_NUM_SAMPLES_TO_AVERAGE','VAC_SPIKE_DECAY_TIME']
        return self.get_param_dict(string_param=string_param,float_param=float_param,int_param=int_param)

    def get_log_files(self):
        keys = ['LOG_FILE','BREAK_DOWN_LOG','DATA_LOG']
        return self.get_param_dict(string_param=keys)
