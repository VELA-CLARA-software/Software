from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
import threading
import sys
import attCalthreads
import VELA_CLARA_BPM_Control as vbpmc
import logging
logger = logging.getLogger(__name__)

class attCalController(QObject):

	def __init__(self, view, model, bpmCont, scopeCont):
		#Hardware controllers are piped in from the attCalmainApp.py
		super(attCalController, self).__init__()
		self.view = view
		self.model = model
		self.logger = logger
		self.attCalthreads = attCalthreads
		self.threading = threading
		#This is a vector of strings - it is required for the monitorMultipleDataForNShots function in the attCalmainModel.py
		#It is a c++ type that I couldn't get to match to a Python array of strings, and so have to import it. Suggestions for
		#doing this better?
		self.pvList = vbpmc.std_vector_string()
		self.lowerList = []
		self.upperList = []

		self.view.addToListButton.clicked.connect(lambda: self.appendToList())
		self.view.clearPVListButton.clicked.connect(lambda: self.clearPVList())
		self.view.calibrateButton.clicked.connect(lambda: self.runATTCalibration())

	def runATTCalibration(self):
		#Disable the button while calibration is running
		self.view.calibrateButton.setEnabled(False)
		self.view.calibrateButton.setText("Calibrating......")
		#Update GUI
		QtGui.QApplication.processEvents()
		self.genPVList = []
		for i in self.pvList:
			self.genPVList.append(i)
		print self.genPVList
		self.logger.info('Attenuation calibration for '+str(self.genPVList)+' initiated!')
		#Get ranges and numshots from GUI
		self.numShots = int(self.view.numShots.toPlainText())
		self.sliderMin = int(self.view.lowerATTBound.toPlainText())
		self.sliderMax = int(self.view.upperATTBound.toPlainText())
		self.attValues = [[]] * len(self.pvList)
		#Add to QThreadPool
		self.pool = QtCore.QThreadPool()
		self.pool.setMaxThreadCount(len(self.pvList))

		print self.pvList
		#Run threads for ATT calibration
		self.thread = self.attCalthreads.attCalWorker(self.view, self.pvList, self.numShots, self.sliderMin, self.sliderMax, self.model)
		#Receives values from attCalthreads.py with ATT calibration data and pipes into getValues function
		self.attValue = self.thread.signals.result.connect(self.getValues)
		self.pool.start(self.thread)
		self.pool.waitForDone()

	def clearPVList(self):
		self.view.bpmPVList.clear()
		self.i = 2
		while self.i <= len(self.pvList) + 1:
			self.view.TabWidget.removeTab(self.i)
			self.i = self.i + 1
		self.pvList = vbpmc.std_vector_string()

	def getValues(self, sigList):
		self.numShots = int(self.view.numShots.toPlainText())
		self.att1Vals = []
		self.att2Vals = []
		self.RA1Vals = []
		self.RA2Vals = []
		#These are the values from attCalmainModel.py
		self.sigList = sigList
		self.makestr = "Charge at WCM = "+str(self.model.getWCMQ())
		#Make plots for each measurement
		for i in range(len(self.pvList)):
			self.view.glayoutOutputs[i].clear()
			self.view.glayoutOutputs_2[i].clear()
			self.plotatt1 = self.view.glayoutOutputs[i].addPlot(title="ATT1")
			self.plotatt1Distrib = self.plotatt1.plot(pen=None,symbol='o')
			self.plotatt1Distrib.setData(self.sigList[0].values()[i].keys(), self.sigList[0].values()[i].values())
			self.plotatt2 = self.view.glayoutOutputs_2[i].addPlot(title="ATT2")
			self.plotatt2Distrib = self.plotatt2.plot(pen=None,symbol='o')
			self.plotatt2Distrib.setData(self.sigList[1].values()[i].keys(), self.sigList[1].values()[i].values())
			self.makestr = self.makestr+("\nNew BPM ATT1 for "+self.pvList[i]+" = "+str(self.model.getBPMReadAttenuation(str(self.pvList[i]))[0]))
			self.makestr = self.makestr+("\nNew BPM ATT2 for "+self.pvList[i]+" = "+str(self.model.getBPMReadAttenuation(str(self.pvList[i]))[1]))
		print self.makestr
		self.view.newATTVals.setText(self.makestr)
		self.logger.info('Attenuation calibration for '+str(self.genPVList)+' complete!')
		self.logger.info(self.makestr)
		self.view.calibrateButton.setEnabled(True)
		self.view.calibrateButton.setText("Calibrate Attenuations")

	def appendToList(self):
		self.pvName = str(self.view.comboBox.currentText())
		self.pvList.append(self.pvName)
		self.view.bpmPVList.insertPlainText(self.pvName+"\n")
		self.view.addPlotTab(self.view.TabWidget, self.pvName)
		return self.pvList
