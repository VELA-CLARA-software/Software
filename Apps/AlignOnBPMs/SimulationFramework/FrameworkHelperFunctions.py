from collections import OrderedDict
import numpy as np

def readFile(fname):
    with open(fname) as f:
        content = f.readlines()
    return content

def saveFile(filename, lines=[]):
    stream = file(filename, 'w')
    for line in lines:
        stream.write(line)
    stream.close()

def findSetting(setting, value, dictionary={}):
    """Looks for a 'value' in 'setting' in dict 'dictionary'"""
    settings = []
    for l, e in dictionary.items():
        if isinstance(e,(dict)) and setting in e.keys() and value == e[setting]:
            settings.append([l,e])
    return settings

def findSettingValue(setting, dictionary={}):
    """Finds the value of a setting in dict 'dictionary'"""
    return [k[setting] for k in findSetting(setting, '', dictionary)]

def lineReplaceFunction(line, findString, replaceString, i=None):
    """Searches for, and replaces, the string 'findString' with 'replaceString' in 'line'"""
    global lineIterator
    if findString in line:
        if not i is None:
            lineIterator += 1
            return line.replace('$'+findString+'$', str(replaceString[i]))
        else:
            return line.replace('$'+findString+'$', str(replaceString))
    else:
        return line

def replaceString(lines=[], findString=None, replaceString=None):
    """Iterates over lines and replaces 'findString' with 'replaceString' which can be a list"""
    global lineIterator
    if isinstance(replaceString,list):
        lineIterator = 0
        return [lineReplaceFunction(line, findString, replaceString, lineIterator) for line in lines]
    else:
        return [lineReplaceFunction(line, findString, replaceString) for line in lines]

#
def chop(expr, delta=1e-8):
    """Performs a chop on small numbers"""
    if isinstance(expr, (int, float, complex)):
        return 0 if -delta <= expr <= delta else expr
    else:
        return [chop(x, delta) for x in expr]

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def sortByPositionFunction(element):
    """Sort function for element positions"""
    return float(element[1]['position_start'][2])

def rotationMatrix(theta):
    """Simple 3D rotation matrix"""
    c, s = np.cos(theta), np.sin(theta)
    return np.matrix([[c, 0, -s], [0, 1, 0], [s, 0, c]])

def getParameter(dicts, param, default=0):
    """Returns the values of 'param' in dict 'dict' if it exists, else returns default value. dict can be a list, the most important last."""
    param = param.lower()
    if isinstance(dicts,list) or isinstance(dicts, tuple):
        val = default
        for d in dicts:
            if isinstance(d, dict) or isinstance(d, OrderedDict):
                dset = {k.lower():v for k,v in d.items()}
                if param in dset:
                    val = dset[param]
        return val
    elif isinstance(dicts, dict) or isinstance(dicts, OrderedDict):
        dset = {k.lower():v for k,v in dicts.items()}
        # val = dset[param] if param in dset else default
        if param in dset:
            return dset[param]
        else:
            # print 'not here! returning ', default
            return default
    else:
        # print 'not here! returning ', default
        return default

def formatOptionalString(parameter, string, n=None):
    """String for optional parameters"""
    if n is None:
        return ' '+string+'='+parameter+'\n' if parameter != 'None' else ''
    else:
        return ' '+string+'('+str(n)+')='+parameter+'\n' if parameter != 'None' else ''

def createOptionalString(paramaterdict, parameter, n=None):
    """Formats ASTRA strings for optional ASTRA parameters"""
    val = str(getParameter(paramaterdict,parameter,default=None))
    return formatOptionalString(val,parameter,n)
