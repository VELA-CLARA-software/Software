from PyQt4 import QtGui, QtCore
import sys
import time
import numpy as np
import pyqtgraph as pg
import pyqtgraph.console as con
from epics import caget,caput
sys.path.append('C:\\Users\\wln24624\\Documents\\SOFTWARE\\VELA-CLARA-Software\\Software\\Striptool\\')
import striptool

class Controller():

	def __init__(self, view, model):
		self.view = view
		self.model = model
		#Set up grpahin areas
		print 'controller made'
		self.view.pushButton.clicked.connect(self.model.hello)
		self.view.checkBox_all.stateChanged.connect(self.setChecks_mom)
		self.view.checkBox_all_s.stateChanged.connect(self.setChecks_mom_s)

		monitor = pg.GraphicsView()
		layout = pg.GraphicsLayout(border=(100,100,100))
		monitor.setCentralItem(layout)

		xdict = {0:'X', 1:'Y'}
		stringaxis = pg.AxisItem(orientation='bottom')
		stringaxis.setTicks([xdict.items()])
		self.positionGraph_1 = layout.addPlot(title="BPM XX")
		self.positionGraph_2 = layout.addPlot(title="BPM XX")
		self.positionGraph_3 = layout.addPlot(title="BPM XX")
		self.positionGraph_1.axes['bottom']['item'].setTicks([xdict.items()])
		self.positionGraph_2.axes['bottom']['item'].setTicks([xdict.items()])
		self.positionGraph_3.axes['bottom']['item'].setTicks([xdict.items()])
		self.positionGraph_1.addItem(pg.BarGraphItem(x=xdict.keys(), height=[-0.3,0.2], width=1))
		self.positionGraph_2.addItem(pg.BarGraphItem(x=xdict.keys(), height=[0.1,-0.4], width=1))
		self.positionGraph_3.addItem(pg.BarGraphItem(x=xdict.keys(), height=[0.1,-0.2], width=1))
		layout.nextRow()
		yagImageBox = layout.addViewBox(lockAspect=True, colspan=2)
		self.YAGImage = pg.ImageItem(np.random.normal(size=(1392,1040)))
		yagImageBox.addItem(self.YAGImage)
		self.displayMom = layout.addLabel('MOMENTUM = MeV/c')
		yagImageBox.autoRange()
		self.view.horizontalLayout_4.addWidget(monitor)


		monitor_s = pg.GraphicsView()
		layout_s = pg.GraphicsLayout(border=(100,100,100))
		monitor_s.setCentralItem(layout_s)
		self.dispersionGraph  = layout_s.addPlot(title="Dispersion")
		self.displayDisp = layout_s.addLabel('DISPERSION = pixels per Ampere')
		layout_s.nextRow()
		self.profileGraph  = layout_s.addPlot(title="Fit to YAG Profile")
		self.displayMom_S = layout_s.addLabel('Momentum Spread =  MeV/c')
		self.view.horizontalLayout_5.addWidget(monitor_s)

		#self.view.gridLayout.addWidget(con.ConsoleWidget(namespace= {'pg': pg, 'np': np}, text='Hellow Llamas!!'),8,0,1,2 )

	def setChecks_mom(self):
		if self.view.checkBox_all.isChecked()==True:
			self.view.checkBox_1.setChecked (True)
			self.view.checkBox_2.setChecked (True)
			self.view.checkBox_3.setChecked (True)
			self.view.checkBox_4.setChecked (True)
		elif self.view.checkBox_all.isChecked()==False:
			self.view.checkBox_1.setChecked (False)
			self.view.checkBox_2.setChecked (False)
			self.view.checkBox_3.setChecked (False)
			self.view.checkBox_4.setChecked (False)

	def setChecks_mom_s(self):
		if self.view.checkBox_all_s.isChecked()==True:
			self.view.checkBox_1_s.setChecked (True)
			self.view.checkBox_2_s.setChecked (True)
			self.view.checkBox_3_s.setChecked (True)
			self.view.checkBox_4_s.setChecked (True)
		elif self.view.checkBox_all_s.isChecked()==False:
			self.view.checkBox_1_s.setChecked (False)
			self.view.checkBox_2_s.setChecked (False)
			self.view.checkBox_3_s.setChecked (False)
			self.view.checkBox_4_s.setChecked (False)
