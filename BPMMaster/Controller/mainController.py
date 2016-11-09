from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
import threading
import sys, os

class Controller(QObject):

	def __init__(self, view):
		super(Controller, self).__init__()
		self.view = view
		self.threading = threading

		self.view.launchATTButton.clicked.connect(lambda: self.attCalThread())
		self.view.launchDLYButton.clicked.connect(lambda: self.dlyCalThread())
		self.view.launchTrajButton.clicked.connect(lambda: self.trajPlotThread())
		self.view.launchMonButton.clicked.connect(lambda: self.monPlotThread())

	def launchATTCal(self):
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
