'''
This class helps make a .in  file of your choice. SHould work for any .in whter independant of in a chain on them

1.identify which .in file you are making
2. get the skeleton version of it
3. get/write the inital distribution
4. get/write the rest of NEWRUN info
5. insert Charge info
5. insert Cavity info
6. insert solenoid info
7. insert quad info
8. insert Dipole info

'''
import elementWriter as w
import elements
import os

def makeIn(fileName, elementLine, startElement, stopElement, initialDistrib='/home/vmsim/Desktop/V2/ASTRA/temp-start.ini' , zStart_offset=0.0):
	#open, read in, and close the original/skeleton file
	dir_path = os.path.dirname(os.path.realpath(__file__))
	original = open(dir_path+ '\\' +fileName, 'r')
	lines = original.read().split("\n")
	original.close()
	parts = elementLine
	#Write in Elements
	lines = w.QUADWriter(lines, parts.quadrupoles)
	lines = w.CAVITYWriter(lines, parts.cavities)
	lines = w.SOLENOIDWriter(lines, parts.solenoids)
	lines = w.DIPOLEWriter(lines, parts.dipoles,parts.correctors)
	lines = w.DISTRIBWriter(lines,initialDistrib)
	lines = w.SPACEQWriter(lines, 1)#for now always have it off
	lines = w.QBUNCHWriter(lines,0.25)

	#Start Position
	#If we are writing the first .in  of a simulation
	if fileName[:2] == startElement[:2]:
		#Find start position
		if startElement[-3:]=='GUN':
			lines = w.ZSTARTWriter(lines,0.0)
			#lines = w.DISTRIBWriter(lines, '/home/vmsim/Desktop/V2/ASTRA-SAND/temp-start-gun.ini')
			lines = w.OFFSETWriter(lines)
		else:
			#Strat at a given element
			startPos =	stopPos = w.getPosition(lines, startElement)
			lines = w.ZSTARTWriter(lines,startPos)
	else:
		# if this isn't the first section of simulation beam need to traverse a dipole.
		#As all element positions are defined by exiting face of a dipole, z-start offest are needed
		lines = w.ZSTARTWriter(lines,zStart_offset)

	#Stop Position
	#If we are writing the last .in  of a simulation
	if fileName[:2] == stopElement[:2]:
		stopPos = w.getPosition(lines, stopElement)
	else:
		#find stop position for the dipole to take you onto the correct bend
		place = w.find('!'+stopElement[:2],lines)
		stopPos = lines[place].split('=')[1]
	lines = w.ZSTOPWriter(lines,stopPos)

	temp=open('temp-'+fileName,'w')
	s='\n'.join(lines)
	temp.write(s)
	temp.close()
