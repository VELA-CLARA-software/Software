import yaml

stream = file('keywords.yaml', 'r')
settings = yaml.load(stream)
stream.close()

class command(dict):

    def __init__(self, commandname, **kwargs):
        super(command, self).__init__()
        self.commandname = commandname
        self.allowedKeyWords = settings[self.commandname]
        for key, value in kwargs.iteritems():
            if key.lower() in self.allowedKeyWords:
                try:
                    self[key.lower()] = getattr(self,self.allowedKeyWords[key.lower()])(value)
                except:
                    pass

    def long(self, value):
        return int(value)

    def double(self, value):
        return float(value)

    def string(self, value):
        return '"'+value+'"'

    def write(self):
        string = '&'+self.commandname+'\n'
        for key, value in self.iteritems():
            string+='\t'+key+' = '+str(value)+'\n'
        string+='&end\n'
        return string
