import re

def convertLatticeFileToASTRAFile(latticeFile,astraFile,section):
	'''Read in lattice file'''
	lattice = open(latticeFile, 'r')
	latticeLines = lattice.read().split("\n")
	lattice.close()
	'''Read in skeleton astra file'''
	astra = open(astraFile, 'r')
	astraLines = astra.read().split("\n")
	astra.close()

	'''find  where LINE is in Lattice file'''
	linePlace  = find(section+':',latticeLines)
	Lstart = 0
	Length = runThroughAndWrite(latticeLines,astraLines,linePlace,Lstart)


def runThroughAndWrite(latticeLines,astraLines,linePlace,Lstart):
	L = Lstart
	lcell = 0.033333333

	'''get a list of all the element on that line'''
	elements = getLINEList(latticeLines,linePlace)
	print(elements)
	'''loop through list, adding to l and writing to astraLines'''
	for element in elements:
		'''find line for element info'''
		elementPlace = find(element+':',latticeLines)
		'''check if element is a line itself'''
		if ': LINE' in latticeLines[elementPlace]:
			L = runThroughAndWrite(latticeLines,astraLines,elementPlace,L)
		else:
			'''if not, continue writing to L and astra lines'''
			elementInfoString = getInfoString(latticeLines,elementPlace)

			if ' l =' in elementInfoString or '	l =' in elementInfoString:
				if '-CAV' in element[-4:]:
					'''Cavities are awkward!!'''
					n = getN_Kicks(elementInfoString)
					#print(n)
					l=n*lcell
				elif 'DIP-DRI' in element[-7:]:
					'''Cavities are awkward!!'''
					extra = getExtraDipoleDrift(elementInfoString)
					l=0.4+ extra#MAGIC Number
				else:
					'''find length of element'''
					l = getLength(elementInfoString)
			else:
				l = 0.0
			L+=l
		print(element+' is at '+str(L))
	return L



def find(string, lines):#retruns line a string is on
	for i,line in enumerate(lines):
		if string in line:
			return i
	print ('A search in the current file could not find '+string)


def getLINEList(lines,start):
	c=1
	info =lines[start]
	while(')' not in lines[start+c]):
		info+=lines[start+c]
		c+=1
	info+=lines[start+c]
	info = info.replace('\t','')
	info = info.replace(' ','')
	info = info.replace('&','')
	#print (info)
	'''split up line and remove useless characters'''
	#print(info)
	return info.split('=')[1].split('(')[1].split(')')[0].split(',')

def getInfoString(lines,place):
	c=1
	info=lines[place]
	while(':' not in lines[place+c]):
		info += lines[place+c]
		c+=1
	return info

def getLength(string):
	line = string.split('l = ')[1]
	c=0
	'''check if the next character is a digit and the end of a line'''
	'''start at 3+c to skip over any  decimal points or negative signs'''
	while(line.endswith(line[:3+c])==False and line[3+c].isdigit()):
		c+=1
	return float(line[:3+c])

def getN_Kicks(string):
	line = string.split('n_kicks = ')[1]
	c=1
	while(line.endswith(line[:c])==False and line[c].isdigit()):
		c+=1
	return float(line[:c])

def getExtraDipoleDrift(string):
	a = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", string)
#	print(a[-1])
	return float(a[-1])
