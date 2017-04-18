from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys,os
import time
import numpy as np
import pyqtgraph as pg
from epics import caget,caput

sys.path.append('C:\\Users\\wln24624\\Documents\\SOFTWARE\\VELA-CLARA-Software\\Software\\loggerWidget')
import loggerWidget as lw

class Controller():

	def __init__(self, view, model):
		'''define model and view'''
		self.view = view
		self.model = model
		'''Plots'''
		pg.setConfigOption('background', 'w')
		graphs = pg.GraphicsView()
		layout = pg.GraphicsLayout(border=(100,100,100))
		graphs.setCentralItem(layout)

		self.ApproxPlot = layout.addPlot(title="Approximate Callibration")
		self.ApproxPlot.setLabel('left', text='Charge', units='nC')
		self.ApproxPlot.setLabel('bottom', text='Phase', units='Degrees')
		layout.nextRow()
		self.FinePlot = layout.addPlot(title=" Callibration")
		self.FinePlot.setLabel('left', text='X BPM Position', units='mm')
		self.FinePlot.setLabel('bottom', text='Phase', units='Degrees')
		self.view.plotLayout.addWidget(graphs)
		#Curves
		self.approxData = self.ApproxPlot.plot([1,2,3,4,5,6],[3,2,6,4,1,2],pen = 'b',width=50)
		self.approxFit = self.ApproxPlot.plot([1,2,3,4,5,6],[2,3,4,6,-2,1],pen = 'r',width=10)
		self.fineData = self.FinePlot.plot([1,2,3,4,5,6],[3,2,6,4,1,2],pen = 'b',width=10)
		self.fineFit = self.FinePlot.plot([1,2,3,4,5,6],[2,3,4,6,-2,1],pen = 'r',width=10)


		self.log = lw.loggerWidget()
		self.view.gridLayout.addWidget(self.log , 1,0,1,2)

		'''Threads for updating graphs and labels'''
		self.timer = QTimer()
		self.timer.timeout.connect(self.updateDisplays)
		self.timer.start(500)

		self.view.checkBox_all.stateChanged.connect(self.allMethod)
		self.view.pushButton_run.clicked.connect(self.model.run)

	def updateDisplays(self):
		self.approxData.setData(x=self.model.approxPhaseData,y=self.model.approxChargeData)
		self.approxFit.setData(x=self.model.approxPhaseFit,y=self.model.approxChargeFit)
		self.fineData.setData(x=self.model.finePhaseData,y=self.model.fineBPMData)
		self.fineFit.setData(x=self.model.finePhaseFit,y=self.model.fineBPMFit)
	def allMethod(self):
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
