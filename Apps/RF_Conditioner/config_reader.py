# DJS Sept 2017
#
# read in config files
# generic, following similar style to hwc config


class config_reader(object):
    comment = '#'
    end_of_entry = ';'
    string_literal = '"'
    equals = '='
    _config_dict = {}

    def __init__(self, filename = ""):
        self._filename = filename


    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self,value):
        self._filename = value


    def get_config(self):
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
    # neater but not type fot values
    def get_vac_parameter_NO_TYPE(self):
        vac_keys = ['VAC_PV','VAC_SPIKE_DELTA','VAC_DECAY_MODE','VAC_SPIKE_DECAY_LEVEL','VAC_SPIKE_DECAY_LEVEL'
                    ,'VAC_SPIKE_DECAY_TIME','VAC_NUM_SAMPLES_TO_AVERAGE']
        vac_param = self.get_part_dict(vac_keys)
        for k, v in vac_param.iteritems():
            print k, v
        return vac_param

    #//Pure Cancer below\\
    #//we must assume value type\\
    #//mfw\\
    def get_vac_parameter(self):
        vac_param = {}
        if 'VAC_PV' in self._config_dict:
            vac_param.update({'VAC_PV'               : self._config_dict['VAC_PV']} )
        if 'VAC_SPIKE_DELTA' in self._config_dict:
            vac_param.update({ 'VAC_SPIKE_DELTA'      : float(self._config_dict['VAC_SPIKE_DELTA'])} )
        if 'VAC_DECAY_MODE' in self._config_dict:
            vac_param.update({ 'VAC_DECAY_MODE'       : self._config_dict['VAC_DECAY_MODE']} )
        if 'VAC_SPIKE_DECAY_LEVEL' in self._config_dict:
            vac_param.update({ 'VAC_SPIKE_DECAY_LEVEL': float(self._config_dict['VAC_SPIKE_DECAY_LEVEL'])} )
        if 'VAC_SPIKE_DECAY_TIME' in self._config_dict:
            vac_param.update({'VAC_SPIKE_DECAY_TIME' : float(self._config_dict['VAC_SPIKE_DECAY_TIME'])})
        if 'VAC_NUM_SAMPLES_TO_AVERAGE' in self._config_dict:
            vac_param.update({'VAC_NUM_SAMPLES_TO_AVERAGE' :int(self._config_dict['VAC_NUM_SAMPLES_TO_AVERAGE'])} )
        for k, v in vac_param.iteritems():
            print k, v
        return vac_param

    def get_log_files(self):
        keys = ['LOG_FILE','BREAK_DOWN_LOG','DATA_LOG']
        r = self.get_part_dict(keys)
        for k, v in r.iteritems():
            print k, v
        return r
