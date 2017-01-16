from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
import threading
import sys
import attCalthreads
sys.path.append('D:\\VELA-CLARA_software\\VELA-CLARA-Controllers-New-Structure-With-Magnets\\bin\\Release')
import VELA_CLARA_BPM_Control as vbpmc
import logging
logger = logging.getLogger(__name__)

class attCalController(QObject):

	def __init__(self, view, model, bpmCont, scopeCont):
		super(attCalController, self).__init__()
		self.view = view
		self.model = model
		self.logger = logger
		self.attCalthreads = attCalthreads
		self.threading = threading
		self.pvList = vbpmc.std_vector_string()
		self.lowerList = []
		self.upperList = []

		self.view.addToListButton.clicked.connect(lambda: self.appendToList())
		self.view.clearPVListButton.clicked.connect(lambda: self.clearPVList())
		self.view.calibrateButton.clicked.connect(lambda: self.runATTCalibration())

	def runATTCalibration(self):
		self.view.calibrateButton.setEnabled(False)
		self.view.calibrateButton.setText("Calibrating......")
		QtGui.QApplication.processEvents()
		self.genPVList = []
		for i in self.pvList:
			self.genPVList.append(i)
		print self.genPVList
		self.logger.info('Attenuation calibration for '+str(self.genPVList)+' initiated!')
		self.numShots = int(self.view.numShots.toPlainText())
		self.sliderMin = int(self.view.lowerATTBound.toPlainText())
		self.sliderMax = int(self.view.upperATTBound.toPlainText())
		self.attValues = [[]] * len(self.pvList)
		self.pool = QtCore.QThreadPool()
		self.pool.setMaxThreadCount(len(self.pvList))

		print self.pvList
		self.thread = self.attCalthreads.attCalWorker(self.view, self.pvList, self.numShots, self.sliderMin, self.sliderMax, self.model)
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
		self.sigList = sigList
		self.makestr = "Charge at WCM = "+str(self.model.getWCMQ())
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
		#return sigList

	def appendToList(self):
		#del self.pvList[:]
		self.pvName = str(self.view.comboBox.currentText())
		self.pvList.append(self.pvName)
		self.view.bpmPVList.insertPlainText(self.pvName+"\n")
		#self.view.plainTextEdit.setPlainText(self.pvName)
		self.view.addPlotTab(self.view.TabWidget, self.pvName)
		return self.pvList
		#self.tab = QtGui.QWidget()
		#self.tab.setObjectName(str(self.pvName))
		#self.newTab = self.view.Ui_TabWidget.addPlotTab(self.tab, self.pvName)
		#self.newTab.setObjectName(_fromUtf8(str(self.pvName)))
