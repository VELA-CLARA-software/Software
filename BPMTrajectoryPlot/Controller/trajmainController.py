from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
import random
import threading

class trajController(QObject):

	def __init__(self, view, model, bpmCont, scopeCont):
		super(trajController, self).__init__()
		self.view = view
		self.model = model
		self.threading = threading
		self.pvList = []
		self.view.trajectoryButton.clicked.connect(lambda: self.view.setComboBox(self.view.tab))
		self.view.individualButton.clicked.connect(lambda: self.view.setComboBox(self.view.tab))
		self.view.pushButton_2.clicked.connect(lambda: self.appendToList())
		self.view.pushButton_3.clicked.connect(lambda: self.clearPVList())
		self.view.pushButton.clicked.connect(lambda: self.startPlots())

	def getPVList(self):
		if self.view.trajectoryButton.isChecked():
			self.trajectory = str(self.view.comboBox.currentText())
			if self.trajectory == "VELA INJ":
				self.pvList = self.model.velaInjList
			elif self.trajectory == "VELA Spectrometer":
				self.pvList = self.model.velaSP1List
			elif self.trajectory == "VELA BA1":
				self.pvList = self.model.velaBA1List
			elif self.trajectory == "VELA BA2":
				self.pvList = self.model.velaBA2List
			elif self.trajectory == "CLARA":
				self.pvList = self.model.claraList
			elif self.trajectory == "C2V":
				self.pvList = self.model.c2vList
		else:
			pass
		return self.pvList

	def clearPVList(self):
		self.view.plainTextEdit.clear()
		self.pvList = []

	def startPlots(self):
		self.getPVList()
		self.plotUpdate = QtCore.QTimer()
		self.plotUpdate.timeout.connect(self.onTimer)
		self.plotUpdate.start(100)

	def onTimer(self):
		self.trajectory = str(self.view.comboBox.currentText())
		#self.numShots = int(self.view.getNumShots.toPlainText())
		self.numShots = 1
		self.bpmData = self.model.monitorBPMs(self.pvList, self.numShots)
		self.bpmXData = self.bpmData[0]
		self.bpmYData = self.bpmData[1]
		self.bpmQData = self.bpmData[2]
		self.autoScale = self.view.autoscaleCheckBox.checkState()
		self.view.xPlot.update_figure(self.bpmXData, self.autoScale, "X")
		self.view.yPlot.update_figure(self.bpmYData, self.autoScale, "Y")
		self.view.qPlot.update_figure(self.bpmYData, self.autoScale, "Q")

	def getData1(self):
		self.data = [random.randint(-10, 10) for i in range(5)]
		print self.data
		return self.data

	def appendToList(self):
		if self.view.individualButton.isChecked():
			self.pvName = str(self.view.comboBox.currentText())
			self.pvList.append(self.pvName)
			self.view.plainTextEdit.insertPlainText(self.pvName+"\n")
		return self.pvList
