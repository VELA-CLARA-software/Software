'''
This Class is the one User's are to initialize in there code.
You need to pass in your controllers, specifying which element of the machine it is for
'''
import makeIn as mi
import elements as e
from PyQt4.QtCore import QThread
import os,sys

class ASTRA(QThread):
	#CONSTRUCTOR
	def __init__(self,V_MAG_Ctrl=None, C_S01_MAG_Ctrl=None, C_S02_MAG_Ctrl=None, C2V_MAG_Ctrl=None, V_RF_Ctrl=None, C_RF_Ctrl=None, L01_RF_Ctrl=None, messages=False):
		QThread.__init__(self)
		self.showMessages = messages
		self.VELA_MAG_Controller = V_MAG_Ctrl
		self.CLA_MAG_S01_Controller = C_S01_MAG_Ctrl
		self.CLA_MAG_S02_Controller = C_S02_MAG_Ctrl
		self.C2V_MAG_Controller = C2V_MAG_Ctrl
		self.VELA_LLRF_Controller = V_RF_Ctrl
		self.CLA_LLRF_Controller = C_RF_Ctrl
		self.CLA_L01_LLRF_Controller = L01_RF_Ctrl
		self.startElement = 'Null'
		self.stopElement = 'Null'
		self.initDistrib = 'Null'
	#DESTRUCTOR
	def __del__(self):
		self.wait()

	def createListOfINFilesToEdit(self):
		inFiles=[]
		if  self.stopElement[:2]== 'C1':
			inFiles=["C1.in"]

		elif self.stopElement[:2]=='CV':
			if self.startElement[:2]=='CV':
				inFiles=["CV.in"]
			elif self.startElement[:2]== 'C1':
				inFiles=["C1.in","CV.in"]
			else:
				print("ERROR: Start Element is not Correct")

		elif self.stopElement[:2]=='V2':
			if self.startElement[:2]== 'C1':
				inFiles=["C1.in","CV.in","V2.in"]
			elif self.startElement[:2]=='CV':
				inFiles=["CV.in","V2.in"]
			elif self.startElement[:2]=='V1':
				inFiles=["V1.in","V2.in"]
			elif self.startElement[:2]=='V2':
				inFiles=["V2.in"]
			else:
				print("ERROR: Start Element is not Correct")

		elif self.stopElement[:2]=='SP':
			if self.startElement[:2]== 'C1':
				inFiles=["C1.in","CV.in","SP.in"]
			elif self.startElement[:2]=='CV':
				inFiles=["CV.in","SP.in"]
			elif self.startElement[:2]=='V1':
				inFiles=["V1.in","SP.in"]
			elif self.startElement[:2]=='SP':
				inFiles=["SP.in"]
			else:
				print("ERROR: Start Element is not Correct")

		else:
			print("ERROR: Stop Element is not Correct")

		return inFiles
	def loadElements(self,section):
		#Depending of the certain section of the beam line your simulating load a ceratin group of elements
		if section[:2]=='C1':
			parts = e.C1_Line(self.CLA_MAG_S01_Controller,self.CLA_MAG_S02_Controller,self.C2V_MAG_Controller,self.CLA_LLRF_Controller,self.CLA_L01_LLRF_Controller)
		elif section[:2]=='V1':
			parts = e.V1_Line(self.VELA_MAG_Controller,self.C2V_MAG_Controller,self.VELA_LLRF_Controller)
		elif section[:2]=='V2':
			parts = e.V2_Line(self.VELA_MAG_Controller,self.C2V_MAG_Controller)
		elif section[:2]=='CV':
			parts = e.CV_Line(self.C2V_MAG_Controller)
		elif section[:2]=='SP':
			parts = e.SP_Line(self.VELA_MAG_Controller,self.C2V_MAG_Controller)
		else:
			print('Not selected a valid Section of Beam Line')
			parts = None
		return parts
	#Shell function to run AStra simulations in a thread is need. Using this 'shell' function alows me to pass in agurments
	def go(self,startElement,stopElement,initDistrib):
			self.startElement = startElement
			self.stopElement = stopElement
			self.initDistrib = initDistrib
			#Run in Thread
			self.start()
			#Don't run in thread
			#self.run()
	#Main functions (has to be called run if I want to use in a thread)
	def run(self):
		#Create a list of infiles to use in ASTRA simulations
		inFiles = self.createListOfINFilesToEdit()

		print('------------------------------')
		print('------NEW SIMULTAION RUN------')
		print('------------------------------')

		#Write .in files
		for i,section in enumerate(inFiles):
			#Determine which elements parts to use
			print('Writing temp-'+section)
			parts = self.loadElements(section)
			#Make .in file (z offset vary if beam in passing through a certain straight or going round a bend)
			if inFiles[0]!=section:
				if section=='SP.in' and inFiles[i - 1]=='V1.in':
					mi.makeIn(section, parts,self.startElement,self.stopElement, zStart_offset=-0.38845)#-0.38845)
				elif section=='SP.in' and inFiles[i - 1]=='CV.in':
					mi.makeIn(section, parts,self.startElement,self.stopElement, zStart_offset=-0.64)
				elif section=='V2.in' and inFiles[i - 1]=='V1.in':
					mi.makeIn(section, parts,self.startElement,self.stopElement, zStart_offset=-0.64)
				elif section=='V2.in' and inFiles[i - 1]=='CV.in':
					mi.makeIn(section, parts,self.startElement,self.stopElement, zStart_offset=-0.38845)
				elif section=='C2.in' and inFiles[i - 1]=='C1.in':
					mi.makeIn(section, parts,self.startElement,self.stopElement, zStart_offset=-0.64)#-0.54
				elif section=='CV.in' and inFiles[i - 1]=='C1.in':
					mi.makeIn(section, parts,self.startElement,self.stopElement, zStart_offset=-0.38845)#offset back by drift dipole and 2*D-Gap
			else:
				mi.makeIn(section, parts,self.startElement,self.stopElement,initialDistrib='/home/vmsim/Desktop/V2/ASTRA/'+self.initDistrib)
			#Once written copy the files to virtual Machine
			os.system('VBoxManage --nologo guestcontrol "VMSimulator" copyto --username "vmsim" --password "password" --target-directory "/home/vmsim/Desktop/V2/ASTRA/" "'+os.getcwd()+'\\temp-'+section+'"')
			os.system('VBoxManage --nologo guestcontrol "VMSimulator" copyto --username "vmsim" --password "password" --target-directory "/home/vmsim/Desktop/V2/ASTRA/" "'+os.getcwd()+'\\'+self.initDistrib+'"')

		#Now run Python script in Virtual Machine to run ASTRA
		if self.showMessages==True:
			os.system('VBoxManage --nologo guestcontrol "VMSimulator" run "usr/bin/python" --username "vmsim" --password "password" -- /home/vmsim/Desktop/V2/ASTRA/runASTRA.py %s' % (','.join(inFiles)))
		else:
			os.system('VBoxManage --nologo guestcontrol "VMSimulator" run "usr/bin/python" --username "vmsim" --password "password" -- /home/vmsim/Desktop/V2/ASTRA/runASTRA.py >> OverallSimMessages.txt %s' % (','.join(inFiles)))
