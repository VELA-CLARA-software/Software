from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
import threading
import mainThreads
import sys, os

class Controller(QObject):

	def __init__(self, view):
		super(Controller, self).__init__()
		self.view = view
		self.threading = threading
		self.mainThreads = mainThreads
		self.fullPVList = ["VM-EBT-INJ-DIA-BPMC-02:DATA:B2V.VALA",
						  "VM-EBT-INJ-DIA-BPMC-04:DATA:B2V.VALA",
						  "VM-EBT-INJ-DIA-BPMC-06:DATA:B2V.VALA",
						  "VM-EBT-INJ-DIA-BPMC-10:DATA:B2V.VALA",
						  "VM-EBT-INJ-DIA-BPMC-12:DATA:B2V.VALA",
						  "VM-EBT-INJ-DIA-BPMC-14:DATA:B2V.VALA"]

		#Each time you click one of the buttons, a separate application is launched. This means that the individual apps
		#are not owned by the Master app. This is a design choice, but it should mean that they are not talking to each
		#other. If this proves problematic, then let ADB know.
		self.view.randomVariableButton.clicked.connect(lambda: self.setRandomPVs())
		self.view.launchATTButton.clicked.connect(lambda: self.attCalThread())
		self.view.launchDLYButton.clicked.connect(lambda: self.dlyCalThread())
		self.view.launchTrajButton.clicked.connect(lambda: self.trajPlotThread())
		self.view.launchMonButton.clicked.connect(lambda: self.monPlotThread())

	def setRandomPVs(self):
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.setPVTimer)
		self.timer.start(1000)

	def setPVTimer(self):
		#This is where the random PVs for the virtual machine are set. See mainThreads.py
		self.repRate = QtCore.QString.toFloat(self.view.repRateValue.toPlainText())[0]
		if not self.view.randomVariableCheckBox.isChecked():
			self.view.randomVariableButton.setEnabled(True)
		else:
			self.pool = QtCore.QThreadPool()
			self.pool.setMaxThreadCount(len(self.fullPVList))
			if self.view.randomVariableCheckBox.isChecked():
				self.view.randomVariableButton.setEnabled(False)
				for i in self.fullPVList:
					QtGui.QApplication.processEvents()
					self.th1 = self.mainThreads.ranPVs(i, -5, 5, 1, self.repRate, "array")
					self.pool.start(self.th1)
				self.pool.waitForDone()

	def launchATTCal(self):
		#The method of launching each app is a bit messy, and will probably be tidied up in the future.
		self.view.dialogBox.setText("Launching BPM attenuation calibration")
		if self.view.velaINJButton.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMAttenuationCalibration\\attCalmainApp.py VELA_INJ Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMAttenuationCalibration\\attCalmainApp.py VELA_INJ Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMAttenuationCalibration\\attCalmainApp.py VELA_INJ Offline")
		elif self.view.velaBA1Button.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMAttenuationCalibration\\attCalmainApp.py VELA_BA1 Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMAttenuationCalibration\\attCalmainApp.py VELA_BA1 Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMAttenuationCalibration\\attCalmainApp.py VELA_BA1 Offline")
		elif self.view.velaBA2Button.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMAttenuationCalibration\\attCalmainApp.py VELA_BA2 Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMAttenuationCalibration\\attCalmainApp.py VELA_BA2 Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMAttenuationCalibration\\attCalmainApp.py VELA_BA2 Offline")
		elif self.view.claraButton.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMAttenuationCalibration\\attCalmainApp.py CLARA Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMAttenuationCalibration\\attCalmainApp.py CLARA Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMAttenuationCalibration\\attCalmainApp.py CLARA Offline")
		elif self.view.c2vButton.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMAttenuationCalibration\\attCalmainApp.py C2V Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMAttenuationCalibration\\attCalmainApp.py C2V Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMAttenuationCalibration\\attCalmainApp.py C2V Offline")

	def attCalThread(self):
		self.attThread = threading.Thread(target = self.launchATTCal)
		self.attThread.daemon = True
		self.attThread.start()

	def launchDLYCal(self):
		self.view.dialogBox.setText("Launching BPM delay calibration")
		if self.view.velaINJButton.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMDelayCalibration\\dlymainApp.py VELA_INJ Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMDelayCalibration\\dlymainApp.py VELA_INJ Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMDelayCalibration\\dlymainApp.py VELA_INJ Offline")
		elif self.view.velaBA1Button.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMDelayCalibration\\dlymainApp.py VELA_BA1 Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMDelayCalibration\\dlymainApp.py VELA_BA1 Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMDelayCalibration\\dlymainApp.py VELA_BA1 Offline")
		elif self.view.velaBA2Button.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMDelayCalibration\\dlymainApp.py VELA_BA2 Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMDelayCalibration\\dlymainApp.py VELA_BA2 Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMDelayCalibration\\dlymainApp.py VELA_BA2 Offline")
		elif self.view.claraButton.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMDelayCalibration\\dlymainApp.py CLARA Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMDelayCalibration\\dlymainApp.py CLARA Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMDelayCalibration\\dlymainApp.py CLARA Offline")
		elif self.view.c2vButton.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMDelayCalibration\\dlymainApp.py C2V Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMDelayCalibration\\dlymainApp.py C2V Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMDelayCalibration\\dlymainApp.py C2V Offline")

	def dlyCalThread(self):
		self.dlyThread = threading.Thread(target = self.launchDLYCal)
		self.dlyThread.daemon = True
		self.dlyThread.start()

	def launchTrajPlot(self):
		self.view.dialogBox.setText("Launching BPM trajectory plotter")
		if self.view.velaINJButton.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMTrajectoryPlot\\trajmainApp.py VELA_INJ Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMTrajectoryPlot\\trajmainApp.py VELA_INJ Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMTrajectoryPlot\\trajmainApp.py VELA_INJ Offline")
		elif self.view.velaBA1Button.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMTrajectoryPlot\\trajmainApp.py VELA_BA1 Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMTrajectoryPlot\\trajmainApp.py VELA_BA1 Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMTrajectoryPlot\\trajmainApp.py VELA_BA1 Offline")
		elif self.view.velaBA2Button.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMTrajectoryPlot\\trajmainApp.py VELA_BA2 Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMTrajectoryPlot\\trajmainApp.py VELA_BA2 Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMTrajectoryPlot\\trajmainApp.py VELA_BA2 Offline")
		elif self.view.claraButton.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMTrajectoryPlot\\trajmainApp.py CLARA Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMTrajectoryPlot\\trajmainApp.py CLARA Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMTrajectoryPlot\\trajmainApp.py CLARA Offline")
		elif self.view.c2vButton.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMTrajectoryPlot\\trajmainApp.py C2V Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMTrajectoryPlot\\trajmainApp.py C2V Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMTrajectoryPlot\\trajmainApp.py C2V Offline")

	def trajPlotThread(self):
		self.trajThread = threading.Thread(target = self.launchTrajPlot)
		self.trajThread.daemon = True
		self.trajThread.start()

	def launchMonPlot(self):
		self.view.dialogBox.setText("Launching BPM monitor GUI")
		if self.view.velaINJButton.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMMonitor\\monmainApp.py VELA_INJ Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMMonitor\\monmainApp.py VELA_INJ Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMMonitor\\monmainApp.py VELA_INJ Offline")
		elif self.view.velaBA1Button.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMMonitor\\monmainApp.py VELA_BA1 Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMMonitor\\monmainApp.py VELA_BA1 Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMMonitor\\monmainApp.py VELA_BA1 Offline")
		elif self.view.velaBA2Button.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMMonitor\\monmainApp.py VELA_BA2 Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMMonitor\\monmainApp.py VELA_BA2 Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMMonitor\\monmainApp.py VELA_BA2 Offline")
		elif self.view.claraButton.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMMonitor\\monmainApp.py CLARA Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMMonitor\\monmainApp.py CLARA Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMMonitor\\monmainApp.py CLARA Offline")
		elif self.view.c2vButton.isChecked():
			if self.view.virtualButton.isChecked():
				os.system("python ..\BPMMonitor\\monmainApp.py C2V Virtual")
			elif self.view.physicalButton.isChecked():
				os.system("python ..\BPMMonitor\\monmainApp.py C2V Physical")
			elif self.view.offlineButton.isChecked():
				os.system("python ..\BPMMonitor\\monmainApp.py C2V Offline")

	def monPlotThread(self):
		self.monThread = threading.Thread(target = self.launchMonPlot)
		self.monThread.daemon = True
		self.monThread.start()
