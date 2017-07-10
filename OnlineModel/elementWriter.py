'''
classs of function to write specialize lines to a given .in file
'''
from epics import caget, caput
import numpy as np

#This is for a magnet
def isON(element):
	#print caget(element.object.pvRoot+'RPOWER')
	if caget(element.object.pvRoot+'RPOWER')==1:
		return True
	else:
		return False

def useDipole(dip):
	#print caget(dip.object.pvRoot+'GETSETI')
	if caget(dip.object.pvRoot+'GETSETI')!=0.0 and caget(dip.object.pvRoot+'GETSETI')!=-0.0:
		return True
	else:
		return False
#Find the first use of a given string and returns the line it is located
def find(string, infile):
	for i,line in enumerate(infile):
		if string in line:
			return i
	print ('A search in the current file could not find '+string)
def getPosition(lines,elementName):
	place = find('!'+elementName,lines)
	return  lines[place+1].split('=')[1]
def OFFSETWriter(lines):
		place = find('Xoff',lines)
		lines[place] = lines[place].split('=')[0]+'='+str(caget('VM-EBT-INJ-DIA-DUMMY-01:DDOUBLE8'))#+','
		place1 = find('Yoff',lines)
		lines[place1] = lines[place1].split('=')[0]+'='+str(caget('VM-EBT-INJ-DIA-DUMMY-01:DDOUBLE9'))#+','
		return lines
def ZSTARTWriter(lines,zstart):
	place = find('ZSTART',lines)
	lines[place] = lines[place].split('=')[0]+'='+str(zstart)#+','
	return lines
def ZSTOPWriter(lines,zstop):
	place = find('ZSTOP',lines)
	lines[place] = lines[place].split('=')[0]+'='+str(zstop)#+','
	return lines
def SPACEQWriter(lines,dimensiion):
	place = find('&CHARGE',lines)
	if dimensiion==3:
		lines.insert(place+2,'LSPCH3D=True')
	elif dimensiion==2:
		lines.insert(place+2,'LSPCH=True')
	else:
		lines.insert(place+2,'LSPCH=False')
	return lines
def QUADWriter(lines,quads):
	place = find('&QUADRUPOLE',lines)
	c=1
	for quad in quads:
		if isON(quad): #Check this Logic: trying to test if a quad is on or not'''
			#create text for quad
			if c==1:
				lines.insert(place+1, 'LQUAD=.T,')
			line1 = '!'+quad.name
			line2 = 'Q_pos('+str(c)+')='+str(quad.position)#+','
			line3 = 'Q_length('+str(c)+')='+str(quad.length)#+','
			line4 = 'Q_grad('+str(c)+')='+str(1000*np.copysign(np.polyval(quad.object.fieldIntegralCoefficients, abs(quad.object.siWithPol))/quad.object.magneticLength,quad.object.siWithPol))#+','				#NEEDS to be converted
			line5 = 'Q_bore('+str(c)+')='+str(quad.bore)#+','
			line6 = 'Q_smooth('+str(c)+')='+str(quad.smooth)#+','
			quadLines=[line1,line2,line3,line4,line5,line6]
			#insert quadlines to lines of .in file
			lines[place+2+(6*(c-1)):place+1+(6*(c-1))] = quadLines
			c+=1
	return lines
def SOLENOIDWriter(lines,sols):
	place = find('&SOLENOID',lines)
	c=1
	for sol in sols:
		if useDipole(sol):#Check this Logic: trying to test if a SOL is on or not THIS MIGHT NOT BE BEST WE MIGHT NEED THE CONTROLLER FUNCTION'''
			#create text for quad
			if c==1:
				lines.insert(place+1, 'Loop=F')
				lines.insert(place+2, 'LBfield=T')
			line1 = '!'+sol.name
			line2 = 'S_pos('+str(c)+')='+str(sol.position)#+','
			line3 = 'FILE_BFieLD('+str(c)+')=\''+str(sol.fieldMap)+'\''
			coeffs = sol.object.fieldIntegralCoefficients[-4:]
			line4 = 'MaxB('+str(c)+')='+str(np.polyval(coeffs, abs(sol.object.siWithPol)/sol.object.magneticLength))#+','#NEEDS to be converted
			line5 = 'S_xoff('+str(c)+')='+str(sol.xoff)#+','
			line6 = 'S_yoff('+str(c)+')='+str(sol.yoff)#+','
			line7 = 'S_smooth('+str(c)+')='+str(sol.smooth)#+','
			solLines=[line1,line2,line3,line4,line5,line6,line7]
			#insert quadlines to lines of .in file
			lines[place+3+(7*(c-1)):place+2+(7*(c-1))] = solLines
			c+=1
	return lines
def CAVITYWriter(lines,cavs):
	place = find('&CAVITY',lines)
	lines.insert(place+1, 'Loop=F')
	lines.insert(place+2, 'LEFieLD=T')

	c=1
	for cav in cavs:
		#if isON(cav):#OR IF STARTING AT THE BEGIN'''
		if True:
			#create text for quad
			line1 = '!'+cav.name
			line2 = 'C_pos('+str(c)+')='+str(cav.position)#+','
			line3 = 'FILE_EFieLD('+str(c)+')=\''+str(cav.fieldMap)+'\''
			line4 = 'MaxE('+str(c)+')='+str(cav.object.amp_MVM)#+','
			line5 = 'Phi('+str(c)+')='+str(cav.object.phi_DEG)#+','
			line6 = 'Nue('+str(c)+')='+str(cav.nue)#+','
			line7 = 'C_smooth('+str(c)+')='+str(cav.smooth)#+','
			line8 = 'C_numb('+str(c)+')='+str(cav.numb)#+','
			cavLines=[line1,line2,line3,line4,line5,line6,line7,line8]
			#insert quadlines to lines of .in file
			lines[place+3+(7*(c-1)):place+2+(7*(c-1))] = cavLines
			c+=1
	return lines
def DIPOLEWriter(lines,dips,corrs):
	place = find('&DIPOLE',lines)
	lines.insert(place+1, 'Loop=.F,')
	lines.insert(place+2, 'LDipole=.T')

	c=1
	for dip in dips:
		if useDipole(dip):#define this function later on:it will check if end element is on another line and whether it use the dipole to get there'''
			#create text for quad
			line1 = '!'+dip.name
			line2 = 'D_Type('+str(c)+')=\'horizontal\''
			line3 = 'D_Gap(1,'+str(c)+')='+str(dip.Gap1)+','				#NEEDS to be converted
			line4 = 'D_Gap(2,'+str(c)+')='+str(dip.Gap2)+','
			line5 = 'D1('+str(c)+')=('+str(dip.D1[0])+','+str(dip.D1[1])+')'
			line6 = 'D2('+str(c)+')=('+str(dip.D2[0])+','+str(dip.D2[1])+')'
			line7 = 'D3('+str(c)+')=('+str(dip.D3[0])+','+str(dip.D3[1])+')'
			line8 = 'D4('+str(c)+')=('+str(dip.D4[0])+','+str(dip.D4[1])+')'
			dip.strength = np.copysign(np.polyval(dip.object.fieldIntegralCoefficients, abs(dip.object.siWithPol))/dip.object.magneticLength,dip.object.siWithPol)
			#print dip.strength
			line9 = 'D_strength('+str(c)+')='+str(dip.strength)#+','
			dipLines=[line1,line2,line3,line4,line5,line6,line7,line8,line9]
			#insert quadlines to lines of .in file
			lines[place+3+(9*(c-1)):place+2+(9*(c-1))] = dipLines
			c+=1
		#now add correctors
		for corr in corrs:
			if useDipole(corr):#define this function later on:it will check if end element is on another line and whether it use the dipole to get there'''

				line1 = '!'+corr.name
				if 'H' in corr.name:
					line2 = 'D_Type('+str(c)+')=\'horizontal\''
				elif 'V' in corr.name:
					line2 = 'D_Type('+str(c)+')=\'vertical\''
				else:
					print('Not entered a valid corrector name')
				line3 = 'D_Gap(1,'+str(c)+')='+str(corr.Gap1)#+','				#NEEDS to be converted
				line4 = 'D_Gap(2,'+str(c)+')='+str(corr.Gap2)#+','
				line5 = 'D1('+str(c)+')=('+str(corr.D1[0])+','+str(corr.D1[1])+')'
				line6 = 'D2('+str(c)+')=('+str(corr.D2[0])+','+str(corr.D2[1])+')'
				line7 = 'D3('+str(c)+')=('+str(corr.D3[0])+','+str(corr.D3[1])+')'
				line8 = 'D4('+str(c)+')=('+str(corr.D4[0])+','+str(corr.D4[1])+')'
				corr.strength = 1000*np.copysign(np.polyval(corr.object.fieldIntegralCoefficients, abs(corr.object.siWithPol))/corr.object.magneticLength,corr.object.siWithPol)
				line9 = 'D_strength('+str(c)+')='+str(corr.strength)#+','
				print corr.strength
				corrLines=[line1,line2,line3,line4,line5,line6,line7,line8,line9]
				#insert quadlines to lines of .in file
				lines[place+3+(9*(c-1)):place+2+(9*(c-1))] = corrLines
				c+=1
	return lines
def DISTRIBWriter(lines,distibFile):
	place = find('Distribution',lines)
	lines[place] = lines[place].split('=')[0]+'=\''+distibFile+'\','
	return lines
def QBUNCHWriter(lines,bunchCharge):
	place = find('Qbunch',lines)
	lines[place] = lines[place].split('=')[0]+'='+str(bunchCharge)+','
	return lines
