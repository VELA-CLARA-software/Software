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
from Software.Procedures.Machine.signaller import machineReciever, machineSignaller
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

from matplotlib.figure import Figure
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

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
					print 'ranges = ', [x.min(), x.max(), y.min(), y.max()]
					plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
	       					extent=[x.min(), x.max(), y.min(), y.max()])
					self.mainPlot[a].draw()
				except:
					pass
			self.plotting = False

class plotWidgetsBLM(QWidget):

	actuators = ['approx', 'fine']

	def __init__(self, cavity, approximateText='Charge', approximateUnits='pC'):
		super(plotWidgetsBLM, self).__init__()
		self.plotting = False
		self.cavity = cavity
		self.layout = QGridLayout()
		self.setLayout(self.layout)
		self.mainPlot = {}
		self.subPlots = {}
		self.subPlots['BPM1'] = {}
		self.mainPlot['BPM1'] = pg.PlotWidget(title='BPM 1')
		self.subPlots['BPM1']['High'] = self.mainPlot['BPM1'].getPlotItem().plot()
		self.subPlots['BPM1']['Low'] = self.mainPlot['BPM1'].getPlotItem().plot()
		self.mainPlot['BPM1'].showGrid(x=True, y=True)
		self.layout.addWidget(self.mainPlot['BPM1'],0,0)
		self.mainPlot['BPM2'] = pg.PlotWidget(title='BPM 2')
		self.subPlots['BPM2'] = {}
		self.subPlots['BPM2']['Low'] = self.mainPlot['BPM2'].getPlotItem().plot()
		self.subPlots['BPM2']['High'] = self.mainPlot['BPM2'].getPlotItem().plot()
		self.mainPlot['BPM2'].showGrid(x=True, y=True)
		self.layout.addWidget(self.mainPlot['BPM2'],0,1)
		self.subPlots['X'] = {}
		self.mainPlot['X'] = pg.PlotWidget(title='X Plane')
		self.subPlots['X']['BPM1'] = self.mainPlot['X'].getPlotItem().plot()
		self.subPlots['X']['BPM2'] = self.mainPlot['X'].getPlotItem().plot()
		self.mainPlot['X'].showGrid(x=True, y=True)
		self.line = QFrame()
		self.line.setFrameShape(QFrame.HLine);
		self.layout.addWidget(self.line,1,0,1,2)
		self.layout.addWidget(self.mainPlot['X'],2,0)
		self.subPlots['Y'] = {}
		self.mainPlot['Y'] = pg.PlotWidget(title='Y Plane')
		self.subPlots['Y']['BPM1'] = self.mainPlot['Y'].getPlotItem().plot()
		self.subPlots['Y']['BPM2'] = self.mainPlot['Y'].getPlotItem().plot()
		self.mainPlot['Y'].showGrid(x=True, y=True)
		self.layout.addWidget(self.mainPlot['Y'],2,1)

	def plot(self, alldata):
		if not self.plotting:
			xydata = {}
			corrdata = {}
			self.plotting = True
			for actuator in ['Low','High']:
				data = alldata[actuator]
				corrdata[actuator] = zip(data['x'], data['y'])
				# print 'corrdata[actuator] = ', corrdata[actuator]
				xydata[actuator] = zip(*[[[a[0], a[2]],[a[1],a[3]]] for a in data['z']])
				# print 'xydata[actuator] = ', xydata[actuator][0]
				if actuator == 'Low':
					symbol = 'o'
					color = 'b'
				else:
					symbol = 's'
					color = 'r'
				self.subPlots['BPM1'][actuator].setData(np.array(xydata[actuator][0]), symbol=symbol, pen=None, symbolPen=color, symbolBrush=color)
				self.subPlots['BPM2'][actuator].setData(np.array(xydata[actuator][1]), symbol=symbol, pen=None, symbolPen=color, symbolBrush=color)

			# print 'xydata[Low] = ', xydata['Low']
			xdata1 = [b[0] for a,b in zip(corrdata['Low'], xydata['Low'][0]) if a[1] == 0]
			xdata2 = [b[0] for a,b in zip(corrdata['High'], xydata['High'][0]) if a[1] == 0]
			self.subPlots['X']['BPM1'].setData(np.array(zip(xdata1,xdata2)), symbol='o', pen=None, symbolPen='b', symbolBrush='b')
			xdata1 = [b[0] for a,b in zip(corrdata['Low'], xydata['Low'][1]) if a[1] == 0]
			xdata2 = [b[0] for a,b in zip(corrdata['High'], xydata['High'][1]) if a[1] == 0]
			self.subPlots['X']['BPM2'].setData(np.array(zip(xdata1,xdata2)), symbol='s', pen=None, symbolPen='r', symbolBrush='r')

			ydata1 = [b[1] for a,b in zip(corrdata['Low'], xydata['Low'][0]) if a[0] == 0]
			ydata2 = [b[1] for a,b in zip(corrdata['High'], xydata['High'][0]) if a[0] == 0]
			self.subPlots['Y']['BPM1'].setData(np.array(zip(ydata1,ydata2)), symbol='o', pen=None, symbolPen='b', symbolBrush='b')
			ydata1 = [b[1] for a,b in zip(corrdata['Low'], xydata['Low'][1]) if a[0] == 0]
			ydata2 = [b[1] for a,b in zip(corrdata['High'], xydata['High'][1]) if a[0] == 0]
			self.subPlots['Y']['BPM2'].setData(np.array(zip(ydata1,ydata2)), symbol='s', pen=None, symbolPen='r', symbolBrush='r')

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
		self.plots['Linac1'] = plotWidgets('Linac1', approximateText='BPM X Position', approximateUnits='mm')
		self.view.plotLayoutLinac1.addWidget(self.plots['Linac1'])

		self.plots['Linac1BLM'] = plotWidgetsBLM('Linac1BLM', approximateText='BPM X Position', approximateUnits='mm')
		self.view.plotLayoutLinac1BLM.addWidget(self.plots['Linac1BLM'])

		self.plots['L01-SOL1'] = plotWidgets('L01-SOL1', approximateText='BPM X Position', approximateUnits='mm')
		self.view.plotLayoutSOL1.addWidget(self.plots['L01-SOL1'])

		self.plots['L01-SOL2'] = plotWidgets('L01-SOL2', approximateText='BPM X Position', approximateUnits='mm')
		self.view.plotLayoutSOL2.addWidget(self.plots['L01-SOL2'])

		self.buttons = [
		self.view.linac1StartRoughScanButton, self.view.linac1StartFineScanButton,
		self.view.linac1BLMStartRoughScanButton, self.view.linac1BLMStartFineScanButton,
		self.view.sol1StartRoughScanButton, self.view.sol1StartFineScanButton,
		self.view.sol2StartRoughScanButton, self.view.sol2StartFineScanButton
		]

		self.log = lw.loggerWidget()
		self.view.logTabLayout.addWidget(self.log)
		self.log.addLogger(logger)

		self.view.linac1StartRoughScanButton.clicked.connect(self.linac1RoughScan)
		self.view.linac1StartFineScanButton.clicked.connect(self.linac1FineScan)
		self.view.linac1BLMStartRoughScanButton.clicked.connect(self.linac1BLMRoughScan)
		self.view.linac1BLMStartFineScanButton.clicked.connect(self.linac1BLMFineScan)
		self.view.sol1StartRoughScanButton.clicked.connect(self.sol1RoughScan)
		self.view.sol1StartFineScanButton.clicked.connect(self.sol1FineScan)
		self.view.sol2StartRoughScanButton.clicked.connect(self.sol2RoughScan)
		self.view.sol2StartFineScanButton.clicked.connect(self.sol2FineScan)
		self.view.abortButton.hide()
		self.view.abortButton.clicked.connect(self.abortRunning)
		self.view.finishButton.hide()
		self.view.finishButton.clicked.connect(self.finishRunning)
		self.view.actionSave_Calibation_Data.triggered.connect(self.saveData)
		self.toggleVerbose(self.view.saveDataCheckbox.isChecked())
		self.view.saveDataCheckbox.toggled.connect(self.toggleVerbose)
		self.setLabel('MODE: '+self.model.machineType+' '+self.model.lineType+' with '+self.model.gunType+' gun')

	def toggleVerbose(self, state):
		print 'state = ', state
		self.model.verbose = state

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

	def solScan(self, scanfunction, stepsize):
		self.disableButtons()
		self.thread = GenericThread(scanfunction, self.plane,
			self.view.sol1LowerSet.value(), \
			self.view.sol1UpperSet.value(), \
			[self.view.Corr1_Min.value(), self.view.Corr1_Max.value()], \
			[self.view.Corr2_Min.value(), self.view.Corr2_Max.value()], \
			stepsize, \
			self.view.nSamples.value() \
		)
		self.thread.finished.connect(self.updatePlot)
		self.thread.finished.connect(self.enableButtons)
		self.thread.start()

	def sol1RoughScan(self):
		self.cavity = 'L01-SOL1'
		self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
		self.solScan(self.model.sol1Scan, self.view.roughStepSetCorrector.value())

	def sol2RoughScan(self):
		self.cavity = 'L01-SOL2'
		self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
		self.solScan(self.model.sol2Scan, self.view.roughStepSetCorrector.value())

	def sol1FineScan(self):
		self.cavity = 'L01-SOL1'
		self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
		self.solScan(self.model.sol1Scan, self.view.fineStepSetCorrector.value())

	def sol2FineScan(self):
		self.cavity = 'L01-SOL2'
		self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
		self.solScan(self.model.sol2Scan, self.view.fineStepSetCorrector.value())

	def linac1Scan(self, scanfunction, actuator, stepsize):
		self.disableButtons()
		self.cavity = 'Linac1'
		self.thread = GenericThread(scanfunction, actuator, self.plane, \
			self.view.linac1LowerSet.value(), \
			self.view.linac1UpperSet.value(), \
			[self.view.Corr1_Min.value(), self.view.Corr1_Max.value()], \
			[self.view.Corr2_Min.value(), self.view.Corr2_Max.value()], \
			stepsize, \
			self.view.nSamples.value() \
		)
		self.thread.finished.connect(self.updatePlot)
		self.thread.finished.connect(self.enableButtons)
		self.thread.start()

	def linac1RoughScan(self):
		self.cavity = 'Linac1'
		self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
		self.linac1Scan(self.model.linac1Scan, 'approx', self.view.roughStepSetCorrector.value())

	def linac1FineScan(self):
		self.cavity = 'Linac1'
		self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
		self.linac1Scan(self.model.linac1Scan, 'fine', self.view.fineStepSetCorrector.value())

	def updatePlotBLM(self):
		self.plots[self.cavity].plot(self.model.experimentalData[self.model.main])

	def linac1ScanBLM(self, scanfunction, actuator, stepsize):
		self.disableButtons()
		self.cavity = 'Linac1BLM'
		self.thread = GenericThread(scanfunction, actuator, \
			self.view.linac1LowerSet.value(), \
			self.view.linac1UpperSet.value(), \
			self.view.nSamples.value() \
		)
		self.thread.finished.connect(self.updatePlotBLM)
		self.thread.finished.connect(self.enableButtons)
		self.thread.start()

	def linac1BLMRoughScan(self):
		self.cavity = 'Linac1BLM'
		self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
		self.linac1ScanBLM(self.model.linac1BLMScan, 'approx', self.view.roughStepSetCorrector.value())

	def linac1BLMFineScan(self):
		self.cavity = 'Linac1BLM'
		self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
		self.linac1ScanBLM(self.model.linac1BLMScan, 'fine', self.view.fineStepSetCorrector.value())

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
