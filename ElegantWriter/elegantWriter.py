class command(dict):

    allowedKeyWords = {}

    def __init__(self, **kwargs):
        super(command, self).__init__()
        for key, value in kwargs.iteritems():
            if key.lower() in self.allowedKeyWords:
                try:
                    self[key.lower()] = value
                    print 'hello?',self.allowedKeyWords[key.lower()]
                except:
                    pass

    def long(self, value):
        return int(value)

    def double(self, value):
        return float(value)

    def string(self, value):
        return '"'+value+'"'

    def write(self):
        string = '&'+type(self).__name__+'\n'
        for key, value in self.iteritems():
            string+='\t'+key+' = '+str(value)+'\n'
        string+='&end\n'
        print string

class alterElements(command):

    allowedKeyWords = {'name':'string',
    'item':'string',
    'type':'string',
    'exclude':'string',
    'value':'double',
    'string_value':'string',
    'differential':'long',
    'multiplicative':'long',
    'alter_at_each_step':'long',
    'alter_before_load_parameters':'long',
    'verbose':'long',
    'allow_missing_elements':'long',
    'allow_missing_parameters':'long',
    'start_occurence':'long',
    'end_occurence':'long',
    's_start':'double',
    's_end':'double',
    'before':'string',
    'after':'string'}

    def __init__(self, **kwargs):
        super(alterElements, self).__init__(**kwargs)
