import yaml
import traceback
import itertools

stream = file('commands.yaml', 'r')
commandkeywords = yaml.load(stream)
stream.close()

stream = file('elements.yaml', 'r')
elementkeywords = yaml.load(stream)
stream.close()

class elegantLattice(dict):

    def __init__(self):
        super(elegantLattice, self).__init__()
        self['elements'] = {}
        self['lines'] = {}
        self['commands'] = {}

    def addElement(self, **kwargs):
        if not 'name' in kwargs:
            (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
            name = text[:text.find('=')].strip()
        else:
            name = kwargs['name']
        commandname = kwargs['type']
        del kwargs['type']
        del kwargs['name']
        # print 'kwargs = ',kwargs
        self['elements'][name] = elegentElement(name=name, commandname=commandname, **kwargs)
        setattr(self,name,self['elements'][name])
        # print self['elements'][name]
        return self['elements'][name]

    def addLine(self, line=[]):
        (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
        name = text[:text.find('=')].strip()
        print 'line name = ', name
        self['lines'][name] = elegantLine(name, line)
        setattr(self,name,self['lines'][name])
        return self['lines'][name]

    def addCommand(self, command=None, **kwargs):
        (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
        name = text[:text.find('=')].strip()
        self['commands'][name] = elegantCommand(name, command, **kwargs)
        setattr(self,name,self['commands'][name])
        return self['commands'][name]

    def writeCommandFile(self,filename='lattice.lte'):
        file = open(filename,'w')
        for command in self['commands'].iteritems():
            file.write(getattr(self,command[0]).write())
        file.close()

    def writeLatticeFile(self,filename='lattice.lte'):
        file = open(filename,'w')
        self.writeElements(file)
        self.writeLines(file)
        file.close()

    def writeElements(self,file):
        elements = []
        for line in self['lines'].iteritems():
            elements+=getattr(self,line[0]).getElements()
        elements = [x for x in elements if x['commandtype'] is 'element']
        unique = reduce(lambda l, x: l if x in l else l+[x], elements, [])
        for element in unique:
            file.write(getattr(self,element['name']).write())

    def writeLines(self,file):
        elements = []
        for line in self['lines'].iteritems():
            elements+=getattr(self,line[0]).getElements()
        elements = [x for x in elements if x['commandtype'] is 'line']
        for line in self['lines'].iteritems():
            elements+=[line[1]]
        unique = reduce(lambda l, x: l if x in l else l+[x], elements, [])
        for element in unique:
            if not '-' in element['name']:
                file.write(getattr(self,element['name']).write())

class elegantCommand(dict):

    def __init__(self, name=None, commandname=None, **kwargs):
        super(elegantCommand, self).__init__()
        self['name'] = name
        self['commandname'] = commandname
        self['commandtype'] = 'command'
        self.allowedKeyWords = commandkeywords[self['commandname']]
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
        string = '&'+self['commandname']+'\n'
        for key, value in self.iteritems():
            string+='\t'+key+' = '+str(value)+'\n'
        string+='&end\n\n'
        return string

class elegentElement(dict):

    def __init__(self, name, commandname=None, **kwargs):
        super(elegentElement, self).__init__()
        if not commandname in elementkeywords:
            raise NameError('Element \'%s\' does not exist' % commandname)
        # (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
        # self.name = text[:text.find('=')].strip()
        # print 'elegentElement name = ', name
        self['name'] = name
        self['commandname'] = commandname
        self['commandtype'] = 'element'
        self.allowedKeyWords = elementkeywords[self['commandname']]
        for key, value in kwargs.iteritems():
            if key.lower() in self.allowedKeyWords:
                try:
                    self[key.lower()] = getattr(self,self.allowedKeyWords[key.lower()])(value)
                except:
                    pass

    def __mul__(self, other):
        return [self for x in range(other)]

    def __rmul__(self, other):
        return [self for x in range(other)]

    def __neg__(self):
        if 'bend' in self['commandname']:
            newself = self.copy()
            if 'e1' in newself and 'e2' in newself:
                e1 = newself['e1']
                e2 = newself['e2']
                newself['e1'] = e2
                newself['e2'] = e1
            elif 'e1' in newself:
                newself['e2'] = newself['e1']
                del newself['e1']
            elif 'e2' in newself:
                newself['e1'] = newself['e2']
                del newself['e2']
            if 'edge1_effects' in newself and 'edge2_effects' in newself:
                e1 = newself['edge1_effects']
                e2 = newself['edge2_effects']
                newself['edge1_effects'] = e2
                newself['edge2_effects'] = e1
            elif 'edge1_effects' in newself:
                newself['edge2_effects'] = newself['edge1_effects']
                del newself['edge1_effects']
            elif 'edge2_effects' in newself:
                newself['edge1_effects'] = newself['edge2_effects']
                del newself['edge2_effects']
            newself['name'] = '-'+newself['name']
            return newself
        else:
            return self

    def long(self, value):
        return int(value)

    def double(self, value):
        return float(value)

    def string(self, value):
        return '"'+value+'"'

    def write(self):
        wholestring=''
        string = self['name']+': '+self['commandname']
        for key, value in self.iteritems():
            if not key is 'name' and not key is 'commandname' and not key is 'commandtype':
                tmpstring = ', '+key+' = '+str(value)
                if len(string+tmpstring) > 78:
                    wholestring+=string+', &\n'
                    string=''
                string+= tmpstring
        wholestring+=string+';\n'
        return wholestring

class elegantLine(dict):

    def __init__(self, name="line", line=[]):
        super(elegantLine, self).__init__()
        self.line = []
        print 'name = ', name
        self['name'] = name
        self['commandtype'] = 'line'
        self.expandLine(line)
        self['line'] = [x['name'] for x in self.line]

    def __mul__(self, other):
        return [self for x in range(other)]

    def __rmul__(self, other):
        return [self for x in range(other)]

    def __neg__(self):
        newself = self.copy()
        newself['line'] = newself['line'][::-1]
        newself['name'] = '-'+newself['name']
        return newself

    def expandLine(self, line):
        for e in line:
            if isinstance(e, (list, tuple)):
                self.expandLine(e)
            else:
                self.line.append(e)

    def writeElements(self):
        unique = reduce(lambda l, x: l if x in l else l+[x], self.line, [])
        return [element.write() for element in unique]

    def getElements(self):
        unique = reduce(lambda l, x: l if x in l else l+[x], self.line, [])
        return unique


    def write(self):
        wholestring=''
        string = self['name']+': Line=('
        for element in self.line:
            if string[-1] == '(':
                tmpstring = element['name']
            else:
                tmpstring = ', '+element['name']
            if len(string+tmpstring) > 78:
                wholestring+=string+', &\n'
                string=''
                string+=tmpstring[2::]
            else:
                string+= tmpstring
        wholestring+=string+');\n'
        return wholestring
