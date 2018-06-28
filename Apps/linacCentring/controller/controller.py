from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys,os
import time
import numpy as np
import pyqtgraph as pg
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget
from scipy.interpolate import Rbf
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

class machineReciever(QObject):
	def __init__(self, machine):
		super(machineReciever, self).__init__()
		self.machine = machine
		print 'self.machine = ', self.machine

	def set(self, function, *args, **kwargs):
		# print 'calling function ', getattr(self.machine, str(function))
		getattr(self.machine,str(function))(*args, **kwargs)

class machineSignaller(QObject):

	setMachine = pyqtSignal(str, 'PyQt_PyObject', 'PyQt_PyObject')

	def __init__(self, machine):
		super(machineSignaller, self).__init__()
		self.machine = machine
		print 'self.machine = ', self.machine

	def set(self, function, *args, **kwargs):
		# getattr(self.machine,function)(*args, **kwargs)
		self.setMachine.emit(function, *args, **kwargs)

	def get(self, function, *args, **kwargs):
		return getattr(self.machine,function)(*args, **kwargs)


from matplotlib.figure import Figure
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class noToolBarWidget(QWidget):

	def __init__(self, size=(5.0, 4.0), dpi=100):
		QWidget.__init__(self)
		self.fig = Figure(size, dpi=dpi)
		self.canvas = FigureCanvas(self.fig)
		self.canvas.setParent(self)

		self.vbox = QVBoxLayout()
		self.vbox.addWidget(self.canvas)

		self.setLayout(self.vbox)

	def getFigure(self):
		return self.fig

	def draw(self):
		self.canvas.draw()

class plotWidgets(QWidget):

	actuators = ['approx', 'fine']

	def __init__(self, cavity, approximateText='Charge', approximateUnits='pC'):
		super(plotWidgets, self).__init__()
		self.plotting = False
		self.cavity = cavity
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		self.mainPlot = {}
		self.subPlots = {}
		self.mainPlot['approx'] = noToolBarWidget()
		self.layout.addWidget(self.mainPlot['approx'])
		self.subPlots['approx'] = self.mainPlot['approx'].getFigure().add_subplot(111)
		self.mainPlot['fine'] = noToolBarWidget()
		self.layout.addWidget(self.mainPlot['fine'])
		self.subPlots['fine'] = self.mainPlot['fine'].getFigure().add_subplot(111)

	def plot(self, actuator, data):
		if not self.plotting:
			self.plotting = True
			a = str(actuator)
			x, y, z = map(lambda x: np.array(x), [data['x'], data['y'], data['z']])
			if True:#len(np.unique(x)) > 2 and len(np.unique(y)) > 2:
				try:
					xi, yi = np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100)
					xi, yi = np.meshgrid(xi, yi)

					# Interpolate
					rbf = Rbf(x, y, z, function='linear')
					zi = rbf(xi, yi)
					plt = self.subPlots[a]
					plt.clear()
					plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
	       					extent=[x.min(), x.max(), y.min(), y.max()])
					self.mainPlot[a].draw()
				except:
					pass
			self.plotting = False

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
		self.machineSignaller = machineSignaller(self.model.baseMachine)
		self.machineReciever = machineReciever(self.model.baseMachine)
		self.model.machine = self.machineSignaller
		self.machineSignaller.setMachine.connect(self.machineReciever.set)
		self.loggerSignal.connect(self.setLabel)
		self.plots = {}

		'''Plots'''
		pg.setConfigOption('background', 'w')
		# Gun
		# LINAC1
		self.plots['Linac1'] = plotWidgets('Linac1', approximateText='BPM X Position', approximateUnits='mm')
		self.view.plotLayoutLinac1.addWidget(self.plots['Linac1'])

		self.plots['L01-SOL1'] = plotWidgets('L01-SOL1', approximateText='BPM X Position', approximateUnits='mm')
		self.view.plotLayoutSOL1.addWidget(self.plots['L01-SOL1'])

		self.plots['L01-SOL2'] = plotWidgets('L01-SOL2', approximateText='BPM X Position', approximateUnits='mm')
		self.view.plotLayoutSOL2.addWidget(self.plots['L01-SOL2'])

		self.buttons = [self.view.linac1StartRoughScanButton, self.view.linac1StartFineScanButton,
		self.view.sol1XStartRoughScanButton, self.view.sol1YStartRoughScanButton,
		self.view.sol2XStartRoughScanButton, self.view.sol2YStartRoughScanButton
		]

		self.log = lw.loggerWidget()
		self.view.logTabLayout.addWidget(self.log)
		self.log.addLogger(logger)

		self.view.linac1StartRoughScanButton.clicked.connect(self.linac1RoughScan)
		self.view.linac1StartFineScanButton.clicked.connect(self.linac1FineScan)
		self.view.sol1XStartRoughScanButton.clicked.connect(self.sol1XRoughScan)
		self.view.sol2XStartRoughScanButton.clicked.connect(self.sol2XRoughScan)
		self.view.sol1YStartRoughScanButton.clicked.connect(self.sol1YRoughScan)
		self.view.sol2YStartRoughScanButton.clicked.connect(self.sol2YRoughScan)
		self.view.abortButton.hide()
		self.view.abortButton.clicked.connect(self.abortRunning)
		self.view.finishButton.hide()
		self.view.finishButton.clicked.connect(self.finishRunning)
		self.view.actionSave_Calibation_Data.triggered.connect(self.saveData)

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
		if hasattr(self,'thread'):
			self.model.abort()
			self.thread.quit()
			self.enableButtons()

	def finishRunning(self):
		if hasattr(self,'thread'):
			self.thread.function.finish()

	def updatePlot(self):
		self.plots[self.cavity].plot(self.model.actuator, self.model.experimentalData[self.model.cavity][self.model.actuator])

	def sol1XRoughScan(self):
		self.disableButtons()
		self.cavity = 'L01-SOL1'
		self.thread = GenericThread(self.model.sol1RoughScan, 'X', float(self.view.sol1LowerSet.text()), \
			float(self.view.sol1UpperSet.text()), \
			float(self.view.rangeSetCorrector.text()), \
			float(self.view.approxStepSetCorrector.text()), \
			float(self.view.nSamples.text()) \
		)
		self.thread.finished.connect(self.updatePlot)
		self.thread.finished.connect(self.enableButtons)
		self.thread.start()

	def sol2XRoughScan(self):
		self.disableButtons()
		self.cavity = 'L01-SOL2'
		self.thread = GenericThread(self.model.sol2RoughScan, 'X', float(self.view.sol2LowerSet.text()), \
			float(self.view.sol2UpperSet.text()), \
			float(self.view.rangeSetCorrector.text()), \
			float(self.view.approxStepSetCorrector.text()), \
			float(self.view.nSamples.text()) \
		)
		self.thread.finished.connect(self.updatePlot)
		self.thread.finished.connect(self.enableButtons)
		self.thread.start()

	def sol1YRoughScan(self):
		self.disableButtons()
		self.cavity = 'L01-SOL1'
		self.thread = GenericThread(self.model.sol1RoughScan, 'Y', float(self.view.sol1LowerSet.text()), \
			float(self.view.sol1UpperSet.text()), \
			float(self.view.rangeSetCorrector.text()), \
			float(self.view.approxStepSetCorrector.text()), \
			float(self.view.nSamples.text()) \
		)
		self.thread.finished.connect(self.updatePlot)
		self.thread.finished.connect(self.enableButtons)
		self.thread.start()

	def sol2YRoughScan(self):
		self.disableButtons()
		self.cavity = 'L01-SOL2'
		self.thread = GenericThread(self.model.sol2RoughScan, 'Y', float(self.view.sol1LowerSet.text()), \
			float(self.view.sol1UpperSet.text()), \
			float(self.view.rangeSetCorrector.text()), \
			float(self.view.approxStepSetCorrector.text()), \
			float(self.view.nSamples.text()) \
		)
		self.thread.finished.connect(self.updatePlot)
		self.thread.finished.connect(self.enableButtons)
		self.thread.start()

	def linac1RoughScan(self):
		self.cavity = 'Linac1'
		self.thread = GenericThread(self.model.linac1RoughScan, float(self.view.linac1LowerSet.text()), \
			float(self.view.linac1UpperSet.text()), \
			float(self.view.rangeSetCorrector.text()), \
			float(self.view.approxStepSetCorrector.text()), \
			float(self.view.nSamples.text()) \
		)
		self.model.newData.connect(self.updatePlot)
		self.thread.finished.connect(self.enableButtons)
		self.thread.start()

	def linac1FineScan(self):
		self.cavity = 'Linac1'
		self.thread = GenericThread(self.model.linac1FineScan, float(self.view.linac1LowerSet.text()), \
			float(self.view.linac1UpperSet.text()), \
			float(self.view.rangeSetCorrector.text()), \
			float(self.view.fineStepSetCorrector.text()), \
			float(self.view.nSamples.text()) \
		)
		self.model.newData.connect(self.updatePlot)
		self.thread.finished.connect(self.enableButtons)
		self.thread.start()

	def setLabel(self, string):
		logger.info(string)
		self.view.label_MODE.setText('Status: <font color="red">' + string + '</font>')

	def saveData(self):
		for cavity in ['Linac1', 'L01-SOL1',  'L01-SOL2']:
			if cavity in self.model.experimentalData:
				print cavity
				my_dict = {}
				for name in ['x', 'y', 'z']:
					my_dict[name] = self.model.experimentalData[cavity]['approx'][name]
				print my_dict
				with open(cavity+'_approx_experimentalData.csv', 'wb') as f:  # Just use 'w' mode in 3.x
				    w = csv.DictWriter(f, my_dict.keys())
				    w.writeheader()
				    w.writerow(my_dict)
				my_dict = {}
				for name in ['x', 'y', 'z']:
					my_dict[name] = self.model.experimentalData[cavity]['fine'][name]
				with open(cavity+'_fine_experimentalData.csv', 'wb') as f:  # Just use 'w' mode in 3.x
				    w = csv.DictWriter(f, my_dict.keys())
				    w.writeheader()
				    w.writerow(my_dict)
