from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys,os
import time
import numpy as np
import pyqtgraph as pg
import threads
# from epics import caget,caput
from  functools import partial
sys.path.append("../../../")
import Software.Widgets.loggerWidget.loggerWidget as lw
import logging
logger = logging.getLogger(__name__)

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
		if str(cavity) == self.cavity:
			if 'xData' in data and 'yData' in data and 'yStd' in data:
				self.subPlots[actuator]['data'].setData(x=data['xData'], y=data['yData'])
				self.subPlots[actuator]['std'].setData(x=data['xData'], y=data['yData'], height=np.array(data['yStd']))
			if 'xFit' in data and 'yFit' in data:
				self.subPlots[actuator]['fit'].setData(x=data['xFit'], y=data['yFit'])

class Controller():

	def __init__(self, view, model):
		'''define model and view'''
		self.view = view
		self.model = model
		self.plots = {}

		'''Plots'''
		pg.setConfigOption('background', 'w')
		# Gun
		self.plots['Gun'] = plotWidgets('Gun', approximateText='Charge', approximateUnits='pC')
		self.view.plotLayoutGun.addWidget(self.plots['Gun'])
		self.model.crestingData.newDataSignal.connect(self.plots['Gun'].newData)
		# LINAC1
		self.plots['Linac1'] = plotWidgets('Linac1', approximateText='BPM X Position', approximateUnits='mm')
		self.view.plotLayoutLinac1.addWidget(self.plots['Linac1'])
		self.model.crestingData.newDataSignal.connect(self.plots['Linac1'].newData)

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
		self.view.actionSave_Calibation_Data.triggered.connect(self.model.saveData)
		self.view.turnOnGunButton.clicked.connect(self.model.turnOnGun)
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

	class crestingThread:

		def __init__(self, parent, crester):
			parent.disableButtons()
			self.crester = crester()
			parent.crester = self.crester
			self.crester.crester.finished.connect(parent.enableButtons)
			self.crester.crester.setLabel.connect(parent.setLabel)
			self.crester.start()

	def gunWCMCrester(self):
		thread = self.crestingThread(self, self.model.gunWCMCrester)

	def linac1CresterQuick(self):
		thread = self.crestingThread(self, self.model.linac1CresterQuick)

	def gunBPMCrester(self):
		func = partial(self.model.gunBPMCrester, int(self.view.rangeSetGun.text()), int(self.view.nScanningSetGun.text()), int(self.view.nShotsSetGun.text()))
		thread = self.crestingThread(self, func)

	def linac1BPMCrester(self):
		func = partial(self.model.linac1BPMCrester, int(self.view.rangeSetLinac1.text()), int(self.view.nScanningSetLinac1.text()), int(self.view.nShotsSetLinac1.text()))
		thread = self.crestingThread(self, func)

	def setDipoleCurrentForGun(self):
		thread = self.crestingThread(self, self.model.setDipoleCurrentForGun)

	def setDipoleCurrentForLinac1(self):
		thread = self.crestingThread(self, self.model.setDipoleCurrentForLinac1)

	def setLabel(self, string):
		logger.info(string)
		self.view.label_MODE.setText('Status: <font color="red">' + string + '</font>')
