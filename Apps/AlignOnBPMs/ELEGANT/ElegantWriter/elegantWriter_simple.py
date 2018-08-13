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

    def addElement(self, name=None, **kwargs):
        if name == None:
            raise NameError('Element does not have a name')
        self['elements'][name] = elegentElement(name, **kwargs)
        setattr(self,name,self['elements'][name])
        return self['elements'][name]

    def addLine(self, name=None, line=[]):
        if name == None:
            raise NameError('Line does not have a name')
        self['lines'][name] = elegantLine(name, line)
        setattr(self,name,self['lines'][name])
        return self['lines'][name]

    def addCommand(self, name=None, **kwargs):
        if name == None:
            raise NameError('Element does not have a name')
        self['commands'][name] = elegantCommand(name, **kwargs)
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
            line = getattr(self,line[0])['line']
            for lineelem in line:
                for elem in self['elements']:
                    if '*'+elem in lineelem or elem+'*' in lineelem:
                        lineelem = lineelem.replace(elem,'self.'+elem)
                        elements += eval(lineelem)
                    elif elem == lineelem:
                        elements += [eval('self.'+lineelem)]
                    elif '-'+elem == lineelem:
                        elements += [eval('self.'+lineelem.replace('-',''))]
        elements = reduce(lambda l, x: l if x in l else l+[x], elements, [])
        # print elements
        for element in elements:
            file.write(getattr(self,element['name']).write())

    def writeLines(self,file):
        for line in self['lines'].iteritems():
            file.write(getattr(self,line[0],'name').write())

class elegantCommand(dict):

    def __init__(self, name=None, type=None, **kwargs):
        super(elegantCommand, self).__init__()
        if not type in commandkeywords:
            raise NameError('Command \'%s\' does not exist' % commandname)
        if name == None:
            raise NameError('Command does not have a name')
        if type == None:
            raise NameError('Command does not have a type')
        self['name'] = name
        self['type'] = type
        self['commandtype'] = 'command'
        self.allowedKeyWords = commandkeywords[self['type']]
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
        string = '&'+self['type']+'\n'
        for key, value in self.iteritems():
            string+='\t'+key+' = '+str(value)+'\n'
        string+='&end\n\n'
        return string

class elegentElement(dict):

    def __init__(self, name=None, type=None, **kwargs):
        super(elegentElement, self).__init__()
        if not type in elementkeywords:
            raise NameError('Element \'%s\' does not exist' % commandname)
        if name == None:
            raise NameError('Element does not have a name')
        if type == None:
            raise NameError('Element does not have a type')
        self['name'] = name
        self['type'] = type
        self['commandtype'] = 'element'
        self.allowedKeyWords = elementkeywords[self['type']]
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
        if 'bend' in self['type']:
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
        string = self['name']+': '+self['type']
        for key, value in self.iteritems():
            if not key is 'name' and not key is 'type' and not key is 'commandtype':
                tmpstring = ', '+key+' = '+str(value)
                if len(string+tmpstring) > 78:
                    wholestring+=string+', &\n'
                    string=''
                string+= tmpstring
        wholestring+=string+';\n'
        return wholestring

class elegantLine(dict):

    def __init__(self, name=None, line=[]):
        super(elegantLine, self).__init__()
        if name == None:
            raise NameError('Line does not have a name')
        self['name'] = name
        self['commandtype'] = 'line'
        self['line'] = line

    def __mul__(self, other):
        return [self for x in range(other)]

    def __rmul__(self, other):
        return [self for x in range(other)]

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
        for element in self['line']:
            if string[-1] == '(':
                tmpstring = element
            else:
                tmpstring = ', '+element
            if len(string+tmpstring) > 78:
                wholestring+=string+', &\n'
                string=''
                string+=tmpstring[2::]
            else:
                string+= tmpstring
        wholestring+=string+');\n'
        return wholestring
