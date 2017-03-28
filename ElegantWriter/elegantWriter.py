import yaml
import traceback

stream = file('commands.yaml', 'r')
commandkeywords = yaml.load(stream)
stream.close()

stream = file('elements.yaml', 'r')
elementkeywords = yaml.load(stream)
stream.close()

class command(dict):

    def __init__(self, commandname, **kwargs):
        super(command, self).__init__()
        self.commandname = commandname
        self.allowedKeyWords = commandkeywords[self.commandname]
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
        wholestring=''
        string = '&'+self.commandname+'\n'
        for key, value in self.iteritems():
            string+='\t'+key+' = '+str(value)+'\n'
        string+='&end\n'
        return string

class element(dict):

    def __init__(self, commandname=None, **kwargs):
        super(element, self).__init__()
        if not commandname in elementkeywords:
            raise NameError('Element \'%s\' does not exist' % commandname)
        (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
        self.name = text[:text.find('=')].strip()
        self.commandname = commandname
        self.allowedKeyWords = elementkeywords[self.commandname]
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
        wholestring=''
        string = self.name+': '+self.commandname
        for key, value in self.iteritems():
            tmpstring = ', '+key+' = '+str(value)
            if len(string+tmpstring) > 78:
                wholestring+=string+', &\n'
                string=''
            string+= tmpstring
        wholestring+=string+';\n'
        return wholestring

class elementLine(object):

    def __init__(self, name="line", line=[]):
        super(elementLine, self).__init__()
        (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
        self.name = text[:text.find('=')].strip()
        self.line = line

    def writeElements(self):
        unique = reduce(lambda l, x: l if x in l else l+[x], self.line, [])
        for element in unique:
            print element.write()

    def write(self):
        wholestring=''
        string = self.name+': Line=('
        for element in self.line:
            if string[-1] == '(':
                tmpstring = element.name
            else:
                tmpstring = ', '+element.name
            if len(string+tmpstring) > 78:
                wholestring+=string+', &\n'
                string=''
                string+=tmpstring[2::]
            else:
                string+= tmpstring
        wholestring+=string+');\n'
        return wholestring
