import epics
import random
from epics import caget,caput
import os,sys
import time

class Model():
	def __init__(self, view):
		self.view = view
		self.arrayList = ["VM-EBT-INJ-DIA-BPMC-02:X",
						  "VM-EBT-INJ-DIA-BPMC-04:X",
						  "VM-EBT-INJ-DIA-BPMC-06:X",
						  "VM-EBT-INJ-DIA-BPMC-10:X",
						  "VM-EBT-INJ-DIA-BPMC-12:X",
						  "VM-EBT-INJ-DIA-BPMC-02:Y",
						  "VM-EBT-INJ-DIA-BPMC-04:Y",
						  "VM-EBT-INJ-DIA-BPMC-06:Y",
						  "VM-EBT-INJ-DIA-BPMC-10:Y",
						  "VM-EBT-INJ-DIA-BPMC-12:Y",
						  "VM-EBT-INJ-SCOPE-01:TR1",
						  "VM-EBT-INJ-SCOPE-01:TR2",
						  "VM-EBT-INJ-SCOPE-01:TR3",
						  "VM-EBT-INJ-SCOPE-01:TR4",
						  "VM-EBT-INJ-DIA-BPMC-02:DATA:B2V.VALA",
						  "VM-EBT-INJ-DIA-BPMC-04:DATA:B2V.VALA",
						  "VM-EBT-INJ-DIA-BPMC-06:DATA:B2V.VALA",
						  "VM-EBT-INJ-DIA-BPMC-10:DATA:B2V.VALA",
						  "VM-EBT-INJ-DIA-BPMC-12:DATA:B2V.VALA"]

		self.numList = ["VM-EBT-INJ-SCOPE-01:P1",
						"VM-EBT-INJ-SCOPE-01:P2",
						"VM-EBT-INJ-SCOPE-01:P3",
						"VM-EBT-INJ-SCOPE-01:P4"]

	def setRanPV(self, pvName, rangeSta, rangeEnd, numShots, repRate):
		self.pvName = pvName
		self.repRate = repRate
		self.numShots = numShots
		self.gotAValue = 0
		self.which = self.isAnArray(self.pvName)
		#self.arrayNum = []
		while self.gotAValue != self.numShots:
			if self.gotAValue > 1000:
				self.gotAValue = 0
			self.start = time.clock()
			self.num = random.uniform(rangeSta, rangeEnd)
			while time.clock() < (self.start + 1/(self.repRate)):
				time.sleep(0.001)
			if self.isAnArray(self.pvName) == True:# and time.clock() < (self.start + 1/(self.repRate)):
				self.arrayNum = []
				for i in epics.caget(str(self.pvName)):
					self.arrayNum.append(random.uniform(rangeSta, rangeEnd))
					i = i + 1
					if i == 9:
						break
				epics.caput(str(self.pvName), self.arrayNum)
				self.gotAValue = self.gotAValue + 1
			elif self.which == False:# and time.clock() < (self.start + 1/(self.repRate)):
				epics.caput(str(self.pvName), self.num)
				self.gotAValue = self.gotAValue + 1
			#else:
				#print "not valid"

	def isAnArray(self, pvName):
		if pvName in self.arrayList:
			return True
		else:
			return False
