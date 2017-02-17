from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
import threading
import dlythreads
import VELA_CLARA_BPM_Control as vbpmc
import logging
logger = logging.getLogger(__name__)

class dlyController(QObject):

	def __init__(self, view, model, bpmCont):
		#Hardware controllers are piped in from the dlymainApp.py
		super(dlyController, self).__init__()
		self.view = view
		self.bpmCont = bpmCont
		self.model = model
		self.logger = logger
		self.threads = dlythreads
		self.thread = QtCore.QThread()
		self.threading = threading
		#This is a vector of strings - it is required for the monitorMultipleDataForNShots function in the dlymainModel.py
		#It is a c++ type that I couldn't get to match to a Python array of strings, and so have to import it. Suggestions for
		#doing this better?
		self.pvList = vbpmc.std_vector_string()
		self.plotTabs = []
		self.lowerList = []
		self.upperList = []

		self.view.addToListButton.clicked.connect(lambda: self.appendToList())
		self.view.clearPVListButton.clicked.connect(lambda: self.clearPVList())
		self.view.calibrateButton.clicked.connect(lambda: self.runDLYCalibration())

	def runDLYCalibration(self):
		#Disable the button while calibration is running
		self.view.calibrateButton.setEnabled(False)
		self.view.calibrateButton.setText("Calibrating......")
		#Update GUI
		QtGui.QApplication.processEvents()
		self.genPVList = []
		for i in self.pvList:
			self.genPVList.append(i)
		print self.genPVList
		self.logger.info('Delay calibration for '+str(self.genPVList)+' initiated!')
		self.numShots = int(self.view.numShots.toPlainText())
		self.sliderMin = int(self.view.lowerDLYBound.toPlainText())
		self.sliderMax = int(self.view.upperDLYBound.toPlainText())
		self.attValues = [[]] * len(self.pvList)
		#Add to QThreadPool
		self.pool = QtCore.QThreadPool()
		self.pool.setMaxThreadCount(len(self.pvList))
		self.thread = self.threads.dlyWorker(self.view, self.pvList, self.numShots, self.sliderMin, self.sliderMax, self.model)
		#Receives values from dlythreads.py with DLY calibration data and pipes into getValues function
		self.attValue = self.thread.signals.result.connect(self.getValues)
		self.pool.start(self.thread)
		self.pool.waitForDone()

	def getValues(self, sigList):
		self.numShots = int(self.view.numShots.toPlainText())
		self.att1Vals = []
		self.att2Vals = []
		self.RA1Vals = []
		self.RA2Vals = []
		#These are the values from dlymainModel.py
		self.sigList = sigList
		self.makestr = ""
		#Make plots for each measurement
		for i in self.pvList:
			#self.view.glayoutOutputs[i].clear()
			#self.view.glayoutOutputs_2[i].clear()
			self.plotDLY1 = self.view.glayoutOutputs[i].addPlot(title="DLY1")
			self.plotDLY1Distrib = self.plotDLY1.plot(pen=None,symbol='o')
			self.plotDLY1Distrib.setData(self.sigList[0][i].keys(), self.sigList[0][i].values())
			self.plotDLY2 = self.view.glayoutOutputs_2[i].addPlot(title="DLY2")
			self.plotDLY2Distrib = self.plotDLY2.plot(pen=None,symbol='o')
			self.plotDLY2Distrib.setData(self.sigList[1][i].keys(), self.sigList[1][i].values())
			self.makestr = self.makestr+("\nNew BPM DLY1 for "+i+" = "+str(self.model.getBPMReadDLY(str(i))[0]))
			self.makestr = self.makestr+("\nNew BPM DLY2 for "+i+" = "+str(self.model.getBPMReadDLY(str(i))[1]))
		self.view.newDLYVals.setText(self.view.newDLYVals.toPlainText()+"\n\n"+self.makestr)
		self.logger.info('Delay calibration for '+str(self.genPVList)+' complete!')
		self.logger.info(self.makestr)
		self.view.calibrateButton.setEnabled(True)
		self.view.calibrateButton.setText("Calibrate Delays")
		#return sigList

	def appendToList(self):
		print self.view.comboBox.currentText()
		self.pvName = str(self.view.comboBox.currentText())
		self.pvList.append(self.pvName)
		self.view.bpmPVList.insertPlainText(self.pvName+"\n")
		self.view.addPlotTab(self.view.TabWidget, self.pvName)
		return self.pvList

	def clearPVList(self):
		print len(self.pvList)
		self.i = len(self.pvList) + 2
		while self.i > 2:
			self.view.TabWidget.removeTab(self.i - 1)
			self.i = self.i - 1
			print self.i
		self.view.bpmPVList.clear()
		self.pvList = vbpmc.std_vector_string()
