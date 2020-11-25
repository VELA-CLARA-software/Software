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

	fromMachine = pyqtSignal(int, 'PyQt_PyObject')

	def __init__(self, machine):
		super(machineReciever, self).__init__()
		self.machine = machine

	def toMachine(self, id, function, args, kwargs):
		ans = getattr(self.machine,str(function))(*args, **kwargs)
		self.fromMachine.emit(id, ans)

class machineSignaller(QObject):

	toMachine = pyqtSignal(int, str, tuple, dict)

	def __init__(self, machine):
		super(machineSignaller, self).__init__()
		self.machine = machine
		self.recievedSignal = {}
		self.signalRecieved = {}
		self.id = -1

	def get(self, function, *args, **kwargs):
		id = int(self.id) + 1
		self.signalRecieved[id] = False
		self.toMachine.emit(id, function, args, kwargs)
		self.id += 1
		while not all([self.signalRecieved[i] for i in range(id+1)]):
			time.sleep(0.01)
		return self.recievedSignal[id]

	def fromMachine(self, id, response):
		self.signalRecieved[id] = True
		self.recievedSignal[id] = response

	def __getattr__(self, attr):
		return getattr(self.machine, attr)

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

	actuators = ['data', 'fit']

	def __init__(self, quad):
		super(plotWidgets, self).__init__()
		self.plotting = False
		self.quad = quad
		self.layout = QGridLayout()
		self.setLayout(self.layout)
		self.mainPlot = {}
		self.subPlots = {}
		self.subPlots['BPM1'] = {}
		self.mainPlot['BPM1'] = pg.PlotWidget(title='BPM 1')
		self.subPlots['BPM1']['X'] = self.mainPlot['BPM1'].getPlotItem().plot(pen='r', sumbol='s')
		self.subPlots['BPM1']['Y'] = self.mainPlot['BPM1'].getPlotItem().plot(pen='b', sumbol='o')
		self.mainPlot['BPM1'].showGrid(x=True, y=True)
		self.layout.addWidget(self.mainPlot['BPM1'],0,0)
		self.mainPlot['BPM2'] = pg.PlotWidget(title='BPM 2')
		self.subPlots['BPM2'] = {}
		self.subPlots['BPM2']['X'] = self.mainPlot['BPM2'].getPlotItem().plot(pen='r', sumbol='s')
		self.subPlots['BPM2']['Y'] = self.mainPlot['BPM2'].getPlotItem().plot(pen='b', sumbol='o')
		self.mainPlot['BPM2'].showGrid(x=True, y=True)
		self.layout.addWidget(self.mainPlot['BPM2'],0,1)

	def plot(self, sub, alldata):
		if not self.plotting:
			self.plotting = True
			data = alldata['y'][1:]
			data0 = alldata['y'][0]
			data = [d - data0 for d in data]
			bpm1x,bpm1y,bpm2x,bpm2y = zip(*data)
			qValues = alldata['x'][1:]
			self.subPlots['BPM1']['X'].setData(np.array(zip(qValues,bpm1x)))
			self.subPlots['BPM1']['Y'].setData(np.array(zip(qValues,bpm1y)))
			self.subPlots['BPM2']['X'].setData(np.array(zip(qValues,bpm2x)))
			self.subPlots['BPM2']['Y'].setData(np.array(zip(qValues,bpm2y)))
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
		self.machineSignaller.toMachine.connect(self.machineReciever.toMachine)
		self.machineReciever.fromMachine.connect(self.machineSignaller.fromMachine)
		self.loggerSignal.connect(self.setLabel)
		self.plots = {}

		'''Plots'''
		pg.setConfigOption('background', 'w')
		# Gun
		# LINAC1
		self.plots['S02-QUAD1'] = plotWidgets('S02-QUAD1')
		self.view.plotLayoutS2Q1.addWidget(self.plots['S02-QUAD1'])

		self.plots['S02-QUAD2'] = plotWidgets('S02-QUAD2')
		self.view.plotLayoutS2Q2.addWidget(self.plots['S02-QUAD2'])

		self.plots['S02-QUAD3'] = plotWidgets('S02-QUAD3')
		self.view.plotLayoutS2Q3.addWidget(self.plots['S02-QUAD3'])

		self.plots['S02-QUAD4'] = plotWidgets('S02-QUAD4')
		self.view.plotLayoutS2Q4.addWidget(self.plots['S02-QUAD4'])

		self.buttons = [
		self.view.S2Q1StartButton, self.view.S2Q2StartButton,
		self.view.S2Q3StartButton, self.view.S2Q4StartButton,
		self.view.TurnOffQuadsButton, self.view.DegaussButton,
		]

		self.log = lw.loggerWidget()
		self.view.logTabLayout.addWidget(self.log)
		self.log.addLogger(logger)

		self.view.TurnOffQuadsButton.clicked.connect(self.TurnOffQuadsCorrs)
		self.view.DegaussButton.clicked.connect(self.Degauss)

		self.view.S2Q1StartButton.clicked.connect(self.S2Q1Start)
		self.view.S2Q2StartButton.clicked.connect(self.S2Q2Start)
		self.view.S2Q3StartButton.clicked.connect(self.S2Q3Start)
		self.view.S2Q4StartButton.clicked.connect(self.S2Q4Start)

		self.view.abortButton.hide()
		self.view.abortButton.clicked.connect(self.abortRunning)
		self.view.finishButton.hide()
		self.view.finishButton.clicked.connect(self.finishRunning)
		self.view.actionSave_Calibation_Data.triggered.connect(self.saveData)

	def setButtonState(self, state=True):
		for b in self.buttons:
			b.setEnabled(state)

	def enableButtons(self):
		self.setButtonState(True)
		try:
			self.view.finishButton.clicked.disconnect(self.finishRunning)
			self.view.finishButton.hide()
		except:
			pass
		try:
			self.view.abortButton.clicked.disconnect(self.abortRunning)
			self.view.abortButton.hide()
		except:
			pass

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
		self.plots[self.cavity].plot(self.model.sub, self.model.experimentalData[self.model.main][self.model.sub])

###############################################################################

	def TurnOffQuadsCorrs(self):
		self.disableButtons()
		self.thread = GenericThread(self.model.turnOffQuadsCorrs)
		self.thread.finished.connect(self.enableButtons)
		self.thread.start()

	def Degauss(self):
		self.disableButtons()
		self.thread = GenericThread(self.model.degaussQuads)
		self.thread.finished.connect(self.enableButtons)
		self.thread.start()

	def quadScan(self, lower, upper, stepsize):
		self.disableButtons()
		self.thread = GenericThread(self.model.quadScan,
			self.cavity,
			lower,
			upper,
			stepsize, \
			self.view.nSamples.value() \
		)
		self.thread.finished.connect(self.updatePlot)
		self.thread.finished.connect(self.enableButtons)
		self.thread.start()

	def S2Q1Start(self):
		self.cavity = 'S02-QUAD1'
		self.quadScan(self.view.S2Q1LowerSet.value(),self.view.S2Q1UpperSet.value(),self.view.S2Q1StepSet.value())

	def S2Q2Start(self):
		self.cavity = 'S02-QUAD2'
		self.quadScan(self.view.S2Q2LowerSet.value(),self.view.S2Q2UpperSet.value(),self.view.S2Q2StepSet.value())

	def S2Q3Start(self):
		self.cavity = 'S02-QUAD3'
		self.quadScan(self.view.S2Q3LowerSet.value(),self.view.S2Q3UpperSet.value(),self.view.S2Q3StepSet.value())

	def S2Q4Start(self):
		self.cavity = 'S02-QUAD4'
		self.quadScan(self.view.S2Q4LowerSet.value(),self.view.S2Q4UpperSet.value(),self.view.S2Q4StepSet.value())

###############################################################################


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
