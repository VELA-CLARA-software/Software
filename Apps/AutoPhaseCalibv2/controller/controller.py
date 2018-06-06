from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys,os
import time
import numpy as np
import pyqtgraph as pg
import csv
from  functools import partial
sys.path.append("../../../")
import Software.Widgets.loggerWidget.loggerWidget as lw
import logging
logger = logging.getLogger(__name__)

class GenericThread(QThread):
	def __init__(self, function, *args, **kwargs):
		QThread.__init__(self)
		self.function = function
		self.args = args
		self.kwargs = kwargs

	def run(self):
		self.object = self.function(*self.args,**self.kwargs)
		print 'finished!'

class plotWidgets(pg.GraphicsView):

	actuators = ['approx', 'dipole', 'fine']

	def __init__(self, cavity, approximateText='Charge', approximateUnits='pC'):
		super(plotWidgets, self).__init__()
		self.cavity = cavity
		self.layout = pg.GraphicsLayout(border=(100,100,100))
		self.setCentralItem(self.layout)
		self.mainPlot = {}
		self.subPlots = {}
		self.mainPlot['approx'] = self.layout.addPlot(title="Approximate Callibration")
		self.mainPlot['approx'].setLabel('left', approximateText, approximateUnits)
		self.mainPlot['approx'].setLabel('bottom', text='Phase', units='Degrees')
		self.subPlots['approx'] = {}
		self.layout.nextRow()
		self.mainPlot['dipole'] = self.layout.addPlot(title="Dipole Current Set")
		self.mainPlot['dipole'].setLabel('left', text='X BPM Position', units='mm')
		self.mainPlot['dipole'].setLabel('bottom', text='Dipole Current', units='Amps')
		self.subPlots['dipole'] = {}
		self.layout.nextRow()
		self.mainPlot['fine'] = self.layout.addPlot(title="Callibration")
		self.mainPlot['fine'].setLabel('left', text='X BPM Position', units='mm')
		self.mainPlot['fine'].setLabel('bottom', text='Phase', units='Degrees')
		self.subPlots['fine'] = {}

		for a in self.actuators:
			self.subPlots[a]['data'] = self.mainPlot[a].plot(symbolPen = 'b', symbol='o', width=0, symbolSize=1, pen=None)
			self.subPlots[a]['fit'] = self.mainPlot[a].plot(pen = 'r', width=50)
			self.subPlots[a]['std'] = pg.ErrorBarItem(x=np.array([]), y=np.array([]), height=np.array([]), beam=None, pen={'color':'b', 'width':2})
			self.mainPlot[a].addItem(self.subPlots[a]['std'])

	def newData(self, cavity, actuator, data):
		actuator = str(actuator)
		try:
			if str(cavity) == self.cavity:
				if 'xData' in data and 'yData' in data and 'yStd' in data:
					self.subPlots[actuator]['data'].setData(x=data['xData'], y=data['yData'])
					self.subPlots[actuator]['std'].setData(x=data['xData'], y=data['yData'], height=np.array(data['yStd']))
				if 'xFit' in data and 'yFit' in data:
					self.subPlots[actuator]['fit'].setData(x=data['xFit'], y=data['yFit'])
		except:
			pass

class Controller(QObject):

	newDataSignal = pyqtSignal()
	loggerSignal = pyqtSignal(str)

	def __init__(self, view, model):
		super(Controller, self).__init__()
		'''define model and view'''
		self.view = view
		self.model = model
		self.model.logger = self.loggerSignal
		self.model.newData = self.newDataSignal
		self.loggerSignal.connect(self.setLabel)
		self.plots = {}

		'''Plots'''
		pg.setConfigOption('background', 'w')
		# Gun
		self.plots['Gun'] = plotWidgets('Gun', approximateText='Charge', approximateUnits='pC')
		self.view.plotLayoutGun.addWidget(self.plots['Gun'])
		# LINAC1
		self.plots['Linac1'] = plotWidgets('Linac1', approximateText='BPM X Position', approximateUnits='mm')
		self.view.plotLayoutLinac1.addWidget(self.plots['Linac1'])

		self.log = lw.loggerWidget()
		self.view.logTabLayout.addWidget(self.log)
		self.log.addLogger(logger)

		self.buttons = [self.view.setupMagnetsButton, self.view.crestGunWCMButton, self.view.crestGunBPM, self.view.setGunPhaseButton,
							self.view.crestLinac1Button, self.view.setLinac1PhaseButton, self.view.crestLinac1RoughButton, self.view.turnOnGunButton,
							self.view.setGunDipoleButton, self.view.setLinac1DipoleButton, self.view.turnOnLinac1Button]

		# self.view.setupMagnetsButton.clicked.connect(self.model.magnetDegausser)
		self.view.crestGunWCMButton.clicked.connect(self.gunWCMCrester)
		self.view.crestGunBPM.clicked.connect(self.gunBPMCrester)
		self.view.setGunPhaseButton.clicked.connect(lambda : self.model.gunPhaser(gunPhaseSet=float(self.view.gunPhaseSet.text()), offset=True))
		self.view.crestLinac1Button.clicked.connect(self.linac1BPMCrester)
		self.view.setLinac1PhaseButton.clicked.connect(lambda : self.model.linac1Phaser(linac1PhaseSet=float(self.view.linac1PhaseSet.text()), offset=True))
		self.view.crestLinac1RoughButton.clicked.connect(self.linac1CresterQuick)
		self.view.abortButton.hide()
		self.view.abortButton.clicked.connect(self.abortRunning)
		self.view.finishButton.hide()
		self.view.finishButton.clicked.connect(self.finishRunning)
		self.view.actionSave_Calibation_Data.triggered.connect(self.saveData)
		# self.view.turnOnGunButton.clicked.connect(self.model.turnOnGun)
		self.view.setGunDipoleButton.clicked.connect(self.setDipoleCurrentForGun)
		self.view.setLinac1DipoleButton.clicked.connect(self.setDipoleCurrentForLinac1)

		self.setLabel('MODE: '+self.model.machineType+' '+self.model.lineType+' with '+self.model.gunType+' gun')

	def setButtonState(self, state=True):
		for b in self.buttons:
			b.setEnabled(state)

	def enableButtons(self):
		self.setButtonState(True)
		self.view.finishButton.clicked.disconnect(self.finishRunning)
		self.view.finishButton.hide()
		self.view.abortButton.clicked.disconnect(self.abortRunning)
		self.view.abortButton.hide()

	def disableButtons(self):
		self.setButtonState(False)
		self.view.finishButton.clicked.connect(self.finishRunning)
		self.view.finishButton.show()
		self.view.abortButton.clicked.connect(self.abortRunning)
		self.view.abortButton.show()

	def abortRunning(self):
		if hasattr(self,'crester'):
			self.crester.crester.abort()
			self.crester.quit()
			self.enableButtons()

	def finishRunning(self):
		if hasattr(self,'crester'):
			self.crester.crester.finish()

	def updatePlot(self):
		self.plots[self.cavity].newData(self.model.cavity, self.model.actuator, self.model.crestingData[self.model.cavity][self.model.actuator])

	def gunWCMCrester(self):
		self.cavity = 'Gun'
		self.thread = GenericThread(self.model.gunWCMCrester)
		self.newDataSignal.connect(self.updatePlot)
		self.thread.start()

	def linac1CresterQuick(self):
		self.cavity = 'Linac1'
		self.thread = GenericThread(self.model.linac1CresterQuick)
		self.newDataSignal.connect(self.updatePlot)
		self.thread.start()

	def gunBPMCrester(self):
		self.cavity = 'Gun'
		self.thread = GenericThread(self.model.gunCresterFine, int(self.view.rangeSetGun.text()), int(self.view.nScanningSetGun.text()), int(self.view.nShotsSetGun.text()))
		self.newDataSignal.connect(self.updatePlot)
		self.thread.start()

	def linac1BPMCrester(self):
		self.cavity = 'Linac1'
		self.thread = GenericThread(self.model.linac1CresterFine, int(self.view.rangeSetLinac1.text()), int(self.view.nScanningSetLinac1.text()), int(self.view.nShotsSetLinac1.text()))
		self.newDataSignal.connect(self.updatePlot)
		self.thread.start()

	def setDipoleCurrentForGun(self):
		self.cavity = 'Gun'
		self.thread = GenericThread(self.model.gunDipoleSet)
		self.newDataSignal.connect(self.updatePlot)
		self.thread.start()

	def setDipoleCurrentForLinac1(self):
		self.cavity = 'Linac1'
		self.thread = GenericThread(self.model.linac1DipoleSet)
		self.newDataSignal.connect(self.updatePlot)
		self.thread.start()

	def setLabel(self, string):
		logger.info(string)
		self.view.label_MODE.setText('Status: <font color="red">' + string + '</font>')

	def saveData(self):
		for cavity in ['Gun', 'Linac1']:
			my_dict = {}
			for name in ['approxPhaseData', 'approxChargeData', 'approxPhaseFit', 'approxChargeFit', 'approxChargeStd']:
				my_dict[name] = self.model.crestingData[cavity][name]
			with open(cavity+'_approx_CrestingData.csv', 'wb') as f:  # Just use 'w' mode in 3.x
			    w = csv.DictWriter(f, my_dict.keys())
			    w.writeheader()
			    w.writerow(my_dict)
			my_dict = {}
			for name in ['finePhaseFit', 'fineBPMFit', 'finePhaseData', 'fineBPMData', 'fineBPMStd']:
				my_dict[name] = self.model.crestingData[cavity][name]
			with open(cavity+'_fine_CrestingData.csv', 'wb') as f:  # Just use 'w' mode in 3.x
			    w = csv.DictWriter(f, my_dict.keys())
			    w.writeheader()
			    w.writerow(my_dict)
