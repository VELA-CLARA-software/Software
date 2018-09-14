import sys,os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time
import numpy as np
import pyqtgraph as pg
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget
from scipy.interpolate import Rbf
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

class plotWidgets(QObject):

	actuators = ['approx', 'fine']

	def __init__(self, cavity, tab):
		super(plotWidgets, self).__init__()
		self.plotting = False
		self.cavity = cavity
		self.tab = tab
		self.mainPlot = {}
		self.subPlots = {}
		self.mainPlot['approx'] = {}
		self.mainPlot['approx']['x'] = noToolBarWidget()
		self.mainPlot['approx']['y'] = noToolBarWidget()
		self.tab.addTab(self.mainPlot['approx']['x'], 'Approx X')
		self.tab.addTab(self.mainPlot['approx']['y'], 'Approx Y')
		self.subPlots['approx'] = {}
		self.subPlots['approx']['x'] = self.mainPlot['approx']['x'].getFigure().add_subplot(111)
		self.subPlots['approx']['y'] = self.mainPlot['approx']['y'].getFigure().add_subplot(111)
		self.mainPlot['fine'] = {}
		self.mainPlot['fine']['x'] = noToolBarWidget()
		self.mainPlot['fine']['y'] = noToolBarWidget()
		self.tab.addTab(self.mainPlot['fine']['x'], 'Fine X')
		self.tab.addTab(self.mainPlot['fine']['y'], 'Fine Y')
		self.subPlots['fine'] = {}
		self.subPlots['fine']['x'] = self.mainPlot['fine']['x'].getFigure().add_subplot(111)
		self.subPlots['fine']['y'] = self.mainPlot['fine']['y'].getFigure().add_subplot(111)

	def plot(self, actuator, plane, data):
		plane = plane.lower()
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
					self.zi = rbf(xi, yi)
					plt = self.subPlots[a][plane]
					plt.clear()
					self.extent = [x.min(), x.max(), y.min(), y.max()]
					plt.imshow(self.zi, vmin=0, vmax=max(z), origin='lower',
	       					extent=self.extent)
					# plt.colorbar()
					self.mainPlot[a][plane].draw()
				except:
					pass
			self.plotting = False
		index = 0 if actuator == 'approx' else 2
		index += 1 if plane == 'y' else 0
		self.tab.setCurrentIndex(index)

class plotWidgetsBLM(QWidget):

	actuators = ['approx', 'fine']

	def __init__(self, cavity, tab):
		super(plotWidgetsBLM, self).__init__()
		self.plotting = False
		self.cavity = cavity
		self.tab = tab
		self.mainPlot = {}
		self.subPlots = {}
		self.subPlots['BPM1'] = {}
		self.mainPlot['BPM1'] = pg.PlotWidget(title='BPM 1')
		self.subPlots['BPM1']['High'] = self.mainPlot['BPM1'].getPlotItem().plot()
		self.subPlots['BPM1']['Low'] = self.mainPlot['BPM1'].getPlotItem().plot()
		self.mainPlot['BPM1'].showGrid(x=True, y=True)
		self.tab.addTab(self.mainPlot['BPM1'], 'BPM1')
		self.mainPlot['BPM2'] = pg.PlotWidget(title='BPM 2')
		self.subPlots['BPM2'] = {}
		self.subPlots['BPM2']['Low'] = self.mainPlot['BPM2'].getPlotItem().plot()
		self.subPlots['BPM2']['High'] = self.mainPlot['BPM2'].getPlotItem().plot()
		self.mainPlot['BPM2'].showGrid(x=True, y=True)
		self.tab.addTab(self.mainPlot['BPM2'], 'BPM 2')
		self.subPlots['X'] = {}
		self.mainPlot['X'] = pg.PlotWidget(title='X Plane')
		self.subPlots['X']['BPM1'] = self.mainPlot['X'].getPlotItem().plot()
		self.subPlots['X']['BPM2'] = self.mainPlot['X'].getPlotItem().plot()
		self.mainPlot['X'].showGrid(x=True, y=True)
		self.tab.addTab(self.mainPlot['X'], 'X')
		self.subPlots['Y'] = {}
		self.mainPlot['Y'] = pg.PlotWidget(title='Y Plane')
		self.subPlots['Y']['BPM1'] = self.mainPlot['Y'].getPlotItem().plot()
		self.subPlots['Y']['BPM2'] = self.mainPlot['Y'].getPlotItem().plot()
		self.mainPlot['Y'].showGrid(x=True, y=True)
		self.tab.addTab(self.mainPlot['Y'], 'Y')

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
