import threading
import time
import threading
import random
import numpy as np
import epics
from epics import caget,caput


class setRandomPV():

	def __init__(self):
		self.threading = threading
		#self.pool = QtCore.QThreadPool()
		self.arrayList = []
		self.numList = []

	def setPV(self, pvName, rangeStart, rangeEnd, numShots, repRate, pvType):
		self.pvList = self.arrayList + self.numList
		# for i in self.pvList:
		self.thread = self.threading.Thread(target = Worker(pvName, rangeStart, rangeEnd, numShots, repRate, pvType).run)
		self.thread.start()
		print "thread " + pvName + " started"


	def caputRanPV(self, pvName, rangeSta, rangeEnd, numShots, repRate, pvType):
		self.pvName = pvName
		self.repRate = repRate
		self.numShots = numShots
		self.gotAValue = 0
		#self.start = time.clock()
		self.which = self.isAnArray(self.pvName)

		while self.gotAValue <= self.numShots:
			self.start = time.clock()
			self.num = random.uniform(rangeSta, rangeEnd)
			while time.clock() < (self.start + 1/(self.repRate)):
				#print "sleep"
				time.sleep(0.001)
			if pvType == "array":# and time.clock() < (self.start + 1/(self.repRate)):
				self.arrayNum = []
				i = 0
				while i < 10:
					#print i
					self.arrayNum.append(random.uniform(rangeSta, rangeEnd))
					i = i + 1
					if i == 9:
						break
				epics.caput(str(self.pvName), self.arrayNum)
				self.gotAValue = self.gotAValue + 1
			elif pvType == "num":# and time.clock() < (self.start + 1/(self.repRate)):
				epics.caput(str(self.pvName), self.num)
				#print str(self.pvName),"   ",self.num
				self.gotAValue = self.gotAValue + 1
			else:
				print "not valid pvType"
			#print self.gotAValue

	def addToArrayList(self, pvName):
		self.arrayList.append(pvName)

	def addToNumList(self, pvName):
		self.numList.append(pvName)

	def isAnArray(self, pvName):
		if pvName in self.arrayList:
			return True
		else:
			return False

class Worker(threading.Thread):
	def __init__(self, pvName, rangeSta, rangeEnd, numShots, repRate, pvType):
		self.pvName = pvName
		self.rangeSta = rangeSta
		self.rangeEnd = rangeEnd
		self.numShots = numShots
		self.repRate = repRate
		self.pvType = pvType
		self.setRandomPV = setRandomPV()
	#def __del__(self):
	#	self.wait()

	def run(self):
		self.setRandomPV.caputRanPV(self.pvName, self.rangeSta, self.rangeEnd, self.numShots, self.repRate, self.pvType)
