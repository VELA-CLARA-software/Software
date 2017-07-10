'''
This class class containing lists of element in each section of a simulation function
the data for each element is splitt up into two parts: ASTRA info and Controller info

Positions of elements are with respect to the the Cathod of that line or the exiting face of a Dipole.

'''
#GENERIC CLASSES
class cavity():
		def __init__(self,name,controllerObject,fieldMap,position,nue,numb=1):
			self.name = name
			#controller info
			self.object = controllerObject
			#ASTRA info
			self.fieldMap = fieldMap
			self.maxE = 0.0
			self.position = position
			self.smooth = 10
			self.nue = nue
			self.phi = 0.0
			self.numb = numb
class solenoid():
	def __init__(self,name,controllerObject,fieldMap,position):
		self.name = name
		#controller info
		self.object = controllerObject
		#ASTRA info
		self.fieldMap = fieldMap
		self.maxB = 0.0
		self.position = position
		self.smooth = 10
		self.xoff = 0.0
		self.yoff = 0.0
class quad():
	def __init__(self,name,controllerObject,length,position,bore):
		self.name = name
		#controller data
		self.object = controllerObject
		#ASTRA info
		self.length = length
		self.position = position
		self.bore = bore
		self.strength = 0.0
		self.smooth = 3.0
class dipole():
	def __init__(self, name, controllerObject,D1,D2,D3,D4,Gap1,Gap2):
		self.name = name
		#controller data
		self.object = controllerObject
		#ASTRA info
		self.strength = 0.0
		self.D1 = D1
		self.D2 = D2
		self.D3 = D3
		self.D4 = D4
		self.Gap1 = Gap1
		self.Gap2 = Gap2
class corrector():
	def __init__(self, name, controllerObject,position,Gap1,Gap2):
		self.name = name
		#controller data
		self.object = controllerObject
		#ASTRA info
		self.strength = 0.0
		self.position = position
		self.D1 = [0.1,position-(self.object.magneticLength/1000)]
		self.D2 = [-0.1,position-(self.object.magneticLength/1000)]
		self.D3 = [0.1,position]
		self.D4 = [-0.1,position]
		self.Gap1 = Gap1
		self.Gap2 = Gap2

#MACHINE SECTION CLASSES
class V1_Line():
	def __init__(self,magnetController,magnetController2,LLRFController):
		self.cavities = []
		self.solenoids = []
		self.quadrupoles = []
		self.dipoles = []
		self.correctors = []
		self.mag = magnetController
		self.C2Vmag = magnetController2
		self.llrf = LLRFController

		self.cavities.append(cavity('V1-GUN',self.llrf.getLLRFObjConstRef(),'/home/vmsim/Desktop/V2/ASTRA/Field_Maps/bas_gun.txt',0.0,2.9974431))

		self.solenoids.append(solenoid('V1-LRRG-SOL',self.mag.getMagObjConstRef("SOL"),'/home/vmsim/Desktop/V2/ASTRA/Field_Maps/bas_sol.txt',0.0))

		self.quadrupoles.append(quad('V1-QUAD01',self.mag.getMagObjConstRef("QUAD01"),0.1,1.285,0.01))
		self.quadrupoles.append(quad('V1-QUAD02',self.mag.getMagObjConstRef("QUAD02"),0.1,1.495,0.01))
		self.quadrupoles.append(quad('V1-QUAD03',self.mag.getMagObjConstRef("QUAD03"),0.1,1.705,0.01))
		self.quadrupoles.append(quad('V1-QUAD04',self.mag.getMagObjConstRef("QUAD04"),0.1,1.915,0.01))
		self.quadrupoles.append(quad('V1-QUAD07',self.mag.getMagObjConstRef("QUAD07"),0.1,4.923,0.01))
		self.quadrupoles.append(quad('V1-QUAD08',self.mag.getMagObjConstRef("QUAD08"),0.1,5.193,0.01))
		self.quadrupoles.append(quad('V1-QUAD09',self.mag.getMagObjConstRef("QUAD09"),0.1,6.872,0.01))
		self.quadrupoles.append(quad('V1-QUAD10',self.mag.getMagObjConstRef("QUAD10"),0.1,9.548,0.01))
		self.quadrupoles.append(quad('V1-QUAD11',self.mag.getMagObjConstRef("QUAD11"),0.1,12.224,0.01))
		self.quadrupoles.append(quad('V1-QUAD15',self.mag.getMagObjConstRef("QUAD15"),0.1,14.90,0.01))

		self.dipoles.append(dipole('INJ-DIP01',self.C2Vmag.getMagObjConstRef("DIP02"),[0.0800007,3.83958],[-0.0800007,3.83958],[-0.0926015,4.25628],[-0.20574,4.143140],0.02,0.02))
		#self.dipoles.append(dipole('INJ-DIP01',self.mag.getMagObjConstRef("DIP01"),[0.0800007,3.83958],[-0.0800007,3.83958],[-0.0926015,4.25628],[-0.20574,4.143140],0.04,0.04))
		#self.dipoles.append(dipole('INJ-DIP02',self.mag.getMagObjConstRef("DIP02"),[-1.04426,7.19523],[-1.1574,7.08209],[-1.17,7.49879],[-1.33,7.49879],0.02,0.02))
		#Positions fro the front of the magnet
		self.correctors.append(corrector('V1-HCOR01', self.mag.getMagObjConstRef("HCOR01"),0.3,0.0,0.0))#guess!!!
		self.correctors.append(corrector('V1-HCOR02', self.mag.getMagObjConstRef("HCOR02"),0.9075,0.0,0.0))
		self.correctors.append(corrector('V1-HCOR03', self.mag.getMagObjConstRef("HCOR03"),2.420,0.0,0.0))
		self.correctors.append(corrector('V1-HCOR04', self.mag.getMagObjConstRef("HCOR04"),3.030,0.0,0.0))
		self.correctors.append(corrector('V1-HCOR06', self.mag.getMagObjConstRef("HCOR06"),4.789,0.0,0.0))
		self.correctors.append(corrector('V1-HCOR07', self.mag.getMagObjConstRef("HCOR07"),7.022,0.0,0.0))
		self.correctors.append(corrector('V1-HCOR08', self.mag.getMagObjConstRef("HCOR08"),9.070,0.0,0.0))
		self.correctors.append(corrector('V1-HCOR09', self.mag.getMagObjConstRef("HCOR09"),12.670,0.0,0.0))
		self.correctors.append(corrector('V1-VCOR01', self.mag.getMagObjConstRef("VCOR01"),0.3,0.0,0.0))#guess!!!
		self.correctors.append(corrector('V1-VCOR02', self.mag.getMagObjConstRef("VCOR02"),0.9075,0.0,0.0))
		self.correctors.append(corrector('V1-VCOR03', self.mag.getMagObjConstRef("VCOR03"),2.420,0.0,0.0))
		self.correctors.append(corrector('V1-VCOR04', self.mag.getMagObjConstRef("VCOR04"),3.030,0.0,0.0))
		self.correctors.append(corrector('V1-VCOR06', self.mag.getMagObjConstRef("VCOR06"),4.789,0.0,0.0))
		self.correctors.append(corrector('V1-VCOR07', self.mag.getMagObjConstRef("VCOR07"),7.022,0.0,0.0))
		self.correctors.append(corrector('V1-VCOR08', self.mag.getMagObjConstRef("VCOR08"),9.070,0.0,0.0))
		self.correctors.append(corrector('V1-VCOR09', self.mag.getMagObjConstRef("VCOR09"),12.670,0.0,0.0))
class V2_Line():
	def __init__(self,magnetController,magnetController2):
		self.cavities = []
		self.solenoids = []
		self.quadrupoles = []
		self.dipoles = []
		self.correctors = []
		self.mag = magnetController
		self.C2Vmag = magnetController2

		self.quadrupoles.append(quad('V2-QUAD07',self.mag.getMagObjConstRef("QUAD07"),0.1,0.614,0.01))
		self.quadrupoles.append(quad('V2-QUAD08',self.mag.getMagObjConstRef("QUAD08"),0.1,2.766,0.01))
		self.quadrupoles.append(quad('V2-QUAD09',self.mag.getMagObjConstRef("QUAD09"),0.1,6.872,0.01))
		self.quadrupoles.append(quad('V2-QUAD10',self.mag.getMagObjConstRef("QUAD10"),0.1,4.918,0.01))
		self.quadrupoles.append(quad('V2-QUAD11',self.mag.getMagObjConstRef("QUAD11"),0.1,7.066,0.01))
		self.quadrupoles.append(quad('V2-QUAD15',self.mag.getMagObjConstRef("QUAD15"),0.1,14.90,0.01))

		self.dipoles.append(dipole('CV-DIP02',self.C2Vmag.getMagObjConstRef("DIP02"),[0.20574,-0.30356],[0.0926015,-0.4167],[0.0800007,0],[-0.0800007,0],0.02,0.02))
		#long straight dipole (rectangluar)
		self.correctors.append(corrector('V2-HCOR06', self.mag.getMagObjConstRef("HCOR06"),0.564,0.0,0.0))
		self.correctors.append(corrector('V2-HCOR07', self.mag.getMagObjConstRef("HCOR07"),2.741,0.0,0.0))
		self.correctors.append(corrector('V2-HCOR08', self.mag.getMagObjConstRef("HCOR08"),4.961,0.0,0.0))
		self.correctors.append(corrector('V2-HCOR09', self.mag.getMagObjConstRef("HCOR09"),8.1585,0.0,0.0))
		self.correctors.append(corrector('V2-VCOR06', self.mag.getMagObjConstRef("VCOR06"),0.564,0.0,0.0))
		self.correctors.append(corrector('V2-VCOR07', self.mag.getMagObjConstRef("VCOR07"),2.741,0.0,0.0))
		self.correctors.append(corrector('V2-VCOR08', self.mag.getMagObjConstRef("VCOR08"),4.961,0.0,0.0))
		self.correctors.append(corrector('V2-VCOR09', self.mag.getMagObjConstRef("VCOR09"),8.1585,0.0,0.0))
class C1_Line():
	def __init__(self,magnetController1,magnetController2,magnetControllerC2V,LLRFController1,LLRFController2):
		self.cavities = []
		self.solenoids = []
		self.quadrupoles = []
		self.dipoles = []
		self.correctors = []
		self.magS01 = magnetController1
		self.magS02 = magnetController2
		self.magC2V = magnetControllerC2V
		self.llrfGUN = LLRFController1
		self.llrfL01 = LLRFController2
		self.cavities.append(cavity('C1-GUN',self.llrfGUN.getLLRFObjConstRef(),'/home/vmsim/Desktop/V2/ASTRA/Field_Maps/bas_gun.txt',0.0,2.9974431))
		self.cavities.append(cavity('C1-LINA01',self.llrfL01.getLLRFObjConstRef(),'/home/vmsim/Desktop/V2/ASTRA/Field_Maps/TWS_S-DL.dat',1.19357,2.9985,numb=60))

		self.solenoids.append(solenoid('C1-LRRG-SOL',self.magS01.getMagObjConstRef("LRG-SOL"),'/home/vmsim/Desktop/V2/ASTRA/Field_Maps/bas_sol.txt',0.0))
		self.solenoids.append(solenoid('C1-LINA01-SOL01',self.magS01.getMagObjConstRef("L01-SOL1"),'/home/vmsim/Desktop/V2/ASTRA/Field_Maps/SwissFEL_linac_sols.dat',1.7)) #(does this do both SOL01 and SOL02)
		self.solenoids.append(solenoid('C1-LINA01-SOL02',self.magS01.getMagObjConstRef("L01-SOL2"),'/home/vmsim/Desktop/V2/ASTRA/Field_Maps/SwissFEL_linac_sols.dat',2.7))

		self.quadrupoles.append(quad('C1-S02-QUAD01',self.magS02.getMagObjConstRef("S02-QUAD1"),0.1007,3.57750031299999,0.003))
		self.quadrupoles.append(quad('C1-S02-QUAD02',self.magS02.getMagObjConstRef("S02-QUAD2"),0.1007,3.97750031299999,0.003))
		self.quadrupoles.append(quad('C1-S02-QUAD03',self.magS02.getMagObjConstRef("S02-QUAD3"),0.1007,5.27750031299999,0.003))
		self.quadrupoles.append(quad('C1-S02-QUAD04',self.magS02.getMagObjConstRef("S02-QUAD4"),0.1007,5.67750031299999,0.003))
		self.quadrupoles.append(quad('C1-S02-QUAD05',self.magS02.getMagObjConstRef("S02-QUAD5"),0.1007,6.440300313,0.003))

		self.dipoles.append(dipole('CV-DIP01',self.magC2V.getMagObjConstRef("DIP01"),[0.0800007,5.72687],[-0.0800007,5.72687],[-0.0926015,6.14357],[-0.20574,6.03043],0.02,0.02))

	 	self.correctors.append(corrector('C1-S01-HCOR01', self.magS01.getMagObjConstRef("S01-HCOR1"),0.35482,0.0,0.0))
		self.correctors.append(corrector('C1-S01-HCOR02', self.magS01.getMagObjConstRef("S01-HCOR2"),0.9377,0.0,0.0))
	 	self.correctors.append(corrector('C1-S01-VCOR01', self.magS01.getMagObjConstRef("S01-VCOR1"),0.35482,0.0,0.0))
		self.correctors.append(corrector('C1-S01-VCOR02', self.magS01.getMagObjConstRef("S01-VCOR2"),0.9377,0.0,0.0))

	 	self.correctors.append(corrector('C1-S02-HCOR01', self.magS02.getMagObjConstRef("S02-HCOR1"),3.448080313,0.0,0.0))
		self.correctors.append(corrector('C1-S02-HCOR02', self.magS02.getMagObjConstRef("S02-HCOR2"),4.26807031299999,0.0,0.0))
		#self.correctors.append(corrector('C1-S02-HCOR03', self.magS02.getMagObjConstRef("S02-HCOR3"),4.84556031299999,0.0,0.0))
	 	self.correctors.append(corrector('C1-S02-VCOR01', self.magS02.getMagObjConstRef("S02-VCOR1"),3.448080313,0.0,0.0))
		self.correctors.append(corrector('C1-S02-VCOR02', self.magS02.getMagObjConstRef("S02-VCOR2"),4.26807031299999,0.0,0.0))
		#self.correctors.append(corrector('C1-S02-VCOR03', self.magS02.getMagObjConstRef("S02-HCOR3"),4.84556031299999,0.0,0.0))

	 	#self.correctors.append(corrector('C1-S02-HCOR01', self.magS02.getMagObjConstRef("HCOR01"),4.2004,0.0,0.0))
		#self.correctors.append(corrector('C1-S02-HCOR02', self.magS02.getMagObjConstRef("HCOR02"),4.86304,0.0,0.0))
	 	#self.correctors.append(corrector('C1-S02-HCOR03', self.magS02.getMagObjConstRef("HCOR03"),0.35482,0.0,0.0))
		#self.correctors.append(corrector('C1-S02-HCOR04', self.magS02.getMagObjConstRef("HCOR04"),0.832,0.0,0.0))
	 	#self.correctors.append(corrector('C1-S02-VCOR01', self.magS02.getMagObjConstRef("VCOR01"),4.2004,0.0,0.0))
		#self.correctors.append(corrector('C1-S02-VCOR02', self.magS02.getMagObjConstRef("VCOR02"),4.86304,0.0,0.0))
	 	#self.correctors.append(corrector('C1-S02-VCOR03', self.magS02.getMagObjConstRef("VCOR03"),0.35482,0.0,0.0))
		#self.correctors.append(corrector('C1-S02-VCOR04', self.magS02.getMagObjConstRef("VCOR04"),0.832,0.0,0.0))
class C2_Line():
	def __init__(self,magnetController1,magnetController2,magnetControllerC2V):
		self.cavities = []
		self.solenoids = []
		self.quadrupoles = []
		self.dipoles = []
		self.correctors = []
		self.magS01 = magnetController1
		self.magS02 = magnetController2

		self.quadrupoles.append(quad('C1-S02-QUAD05',self.magS02.getMagObjConstRef("QUAD05"),0.1007,0.26378,0.003))

		self.dipoles.append(dipole('CV-DIP01',self.magS02.magnetControllerC2V("DIP01"),[0.0800007,-0.5],[-0.0800007,-0.5],[-0.0926015,-0.0833],[-0.20574,-0.19644],0.02,0.02))
class CV_Line():
	def __init__(self,magnetController1):
		self.cavities = []
		self.solenoids = []
		self.quadrupoles = []
		self.dipoles = []
		self.correctors = []
		self.mag = magnetController1


		self.quadrupoles.append(quad('CV-QUAD01',self.mag.getMagObjConstRef('C2V-QUAD1'),0.1007,0.3332745323,0.01))
		self.quadrupoles.append(quad('CV-QUAD02',self.mag.getMagObjConstRef('C2V-QUAD2'),0.1007,0.6232745323,0.01))
		self.quadrupoles.append(quad('CV-QUAD03',self.mag.getMagObjConstRef('C2V-QUAD3'),0.1007,0.9132745323,0.01))


		#self.dipoles.append(dipole('CV-DIP01',self.mag.getMagObjConstRef('DIP01'),[-0.0926015,-0.4167],[-0.20574,-0.30356],[0.0800007,0],[-0.0800007,0],0.02,0.02))# not much cahnge!!!

		self.dipoles.append(dipole('CV-DIP01',self.mag.getMagObjConstRef('DIP01'),[0.0849-0.1775,-0.0283-0.38845],[-0.0283-0.1775,0.0849-0.38845],[0.2575-0.1775,0],[0.097-0.1775,0],0.02,0.02))
		self.dipoles.append(dipole('CV-DIP02',self.mag.getMagObjConstRef('DIP02'),[0.0800007,1.2458490646],[-0.0800007,1.2458490646],[0.20574,1.5494090646],[0.0926015,1.6625490646],0.02,0.02))

	 	self.correctors.append(corrector('CV-HCOR01', self.mag.getMagObjConstRef("C2V-HCOR1"),0.2100545323,0.0,0.0))
		self.correctors.append(corrector('CV-VCOR01', self.mag.getMagObjConstRef("C2V-VCOR1"),0.2100545323,0.0,0.0))
class SP_Line():
	def __init__(self,magnetController,magnetController2):
		self.cavities = []
		self.solenoids = []
		self.quadrupoles = []
		self.dipoles = []
		self.correctors = []
		self.mag = magnetController
		self.C2Vmag = magnetController2

		self.quadrupoles.append(quad('SP-QUAD05',self.mag.getMagObjConstRef("QUAD05"),0.1,0.4213,0.01))
		self.quadrupoles.append(quad('SP-QUAD06',self.mag.getMagObjConstRef("QUAD06"),0.1,0.8213,0.01))


		self.dipoles.append(dipole('V1-DIP01',self.C2Vmag.getMagObjConstRef("DIP02"),[0.0849-0.1775,-0.0283-0.38845],[-0.0283-0.1775,0.0849-0.38845],[0.2575-0.1775,0],[0.097-0.1775,0],0.02,0.02))
		#self.dipoles.append(dipole('V1-DIP01',self.mag.getMagObjConstRef("DIP01"),[0.0849-0.1775,-0.0283],[-0.0283-0.1775,0.0849],[0.2575-0.1775,0.38845],[0.097-0.1775,0.38845],0.04,0.04))
	 	self.correctors.append(corrector('SP-HCOR05', self.mag.getMagObjConstRef("HCOR05"),0.2453,0.0,0.0))
		self.correctors.append(corrector('SP-VCOR05', self.mag.getMagObjConstRef("VCOR05"),0.2453,0.0,0.0))
