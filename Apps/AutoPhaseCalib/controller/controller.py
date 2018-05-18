from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys,os
import time
import numpy as np
import pyqtgraph as pg
import threads
# from epics import caget,caput

sys.path.append("../../../")
import Software.Widgets.loggerWidget.loggerWidget as lw

class Controller():

	def __init__(self, view, model):
		'''define model and view'''
		self.view = view
		self.model = model

		'''Plots'''
		pg.setConfigOption('background', 'w')
		self.ApproxPlot = {}
		self.FinePlot = {}
		self.approxData = {}
		self.approxFit = {}
		self.approxStd = {}
		self.fineData = {}
		self.fineFit = {}
		self.fineStd = {}
		# Gun
		graphs = pg.GraphicsView()
		layout = pg.GraphicsLayout(border=(100,100,100))
		graphs.setCentralItem(layout)

		self.ApproxPlot['Gun'] = layout.addPlot(title="Approximate Callibration")
		self.ApproxPlot['Gun'].setLabel('left', text='Charge', units='pC')
		self.ApproxPlot['Gun'].setLabel('bottom', text='Phase', units='Degrees')
		layout.nextRow()
		self.FinePlot['Gun'] = layout.addPlot(title=" Callibration")
		self.FinePlot['Gun'].setLabel('left', text='X BPM Position', units='mm')
		self.FinePlot['Gun'].setLabel('bottom', text='Phase', units='Degrees')
		self.view.plotLayoutGun.addWidget(graphs)

		# LINAC1
		graphs = pg.GraphicsView()
		layout = pg.GraphicsLayout(border=(100,100,100))
		graphs.setCentralItem(layout)

		self.ApproxPlot['Linac1'] = layout.addPlot(title="Approximate Callibration")
		self.ApproxPlot['Linac1'].setLabel('left', text='X BPM Position', units='mm')
		self.ApproxPlot['Linac1'].setLabel('bottom', text='Phase', units='Degrees')
		layout.nextRow()
		self.FinePlot['Linac1'] = layout.addPlot(title=" Callibration")
		self.FinePlot['Linac1'].setLabel('left', text='X BPM Position', units='mm')
		self.FinePlot['Linac1'].setLabel('bottom', text='Phase', units='Degrees')
		self.view.plotLayoutLinac1.addWidget(graphs)

		#Curves
		for cavity in ['Gun', 'Linac1']:
			self.approxData[cavity] = self.ApproxPlot[cavity].plot([],[], symbolPen = 'b', symbol='o', width=0, symbolSize=1, pen=None)
			self.approxStd[cavity] = pg.ErrorBarItem(x=[1,2,3,4,5,6], y=[2,3,4,6,-2,1], height=np.array([1,1,1,1,1,1]), beam=None, pen={'color':'b', 'width':2})
			self.ApproxPlot[cavity].addItem(self.approxStd[cavity])
			self.approxFit[cavity] = self.ApproxPlot[cavity].plot([1,2,3,4,5,6],[2,3,4,6,-2,1], pen = 'r', width=50)
			# self.approxStd[cavity] = self.ApproxPlot[cavity].plot([1,2,3,4,5,6],[2,3,4,6,-2,1], symbolPen = 'k', symbol='+', width=1)
			self.fineData[cavity] = self.FinePlot[cavity].plot([1,2,3,4,5,6],[3,2,6,4,1,2], symbolPen = 'b', symbol='o', width=1, symbolSize=1)
			self.fineFit[cavity] = self.FinePlot[cavity].plot([1,2,3,4,5,6],[2,3,4,6,-2,1], pen = 'r', width=50)
			self.fineStd[cavity] = pg.ErrorBarItem(x=[1,2,3,4,5,6], y=[2,3,4,6,-2,1], height=np.array([1,1,1,1,1,1]), beam=None, pen={'color':'b', 'width':2})
			self.FinePlot[cavity].addItem(self.fineStd[cavity])


		self.log = lw.loggerWidget()
		self.view.logTabLayout.addWidget(self.log)

		'''Threads for updating graphs and labels'''
		self.timer = QTimer()
		self.timer.timeout.connect(self.updateDisplays)
		self.timer.start(100)

		self.view.setupMagnetsButton.clicked.connect(self.model.magnetDegausser)
		self.view.crestGunWCMButton.clicked.connect(self.model.gunWCMCrester)
		self.view.crestGunBPM.clicked.connect(self.model.gunBPMCrester)
		self.view.setGunPhaseButton.clicked.connect(lambda : self.model.gunPhaser(True))
		self.view.crestLinacButton.clicked.connect(self.model.linacBPMCrester)
		self.view.setLinacPhaseButton.clicked.connect(lambda : self.model.linac1Phaser(True))
		self.view.crestLinacRoughButton.clicked.connect(self.model.linacCresterQuick)
		self.view.abortButton.hide()
		self.view.abortButton.clicked.connect(self.model.abortRunning)
		self.view.actionSave_Calibation_Data.triggered.connect(self.model.saveData)


	def updateDisplays(self):
		for cavity in ['Gun', 'Linac1']:
			self.approxData[cavity].setData(x=self.model.crestingData[cavity]['approxPhaseData'],y=self.model.crestingData[cavity]['approxChargeData'])
			self.approxFit[cavity].setData(x=self.model.crestingData[cavity]['approxPhaseFit'],y=self.model.crestingData[cavity]['approxChargeFit'])
			try:
				self.approxStd[cavity].setData(x=self.model.crestingData[cavity]['approxPhaseData'],y=self.model.crestingData[cavity]['approxChargeData'],
				height=np.array(self.model.crestingData[cavity]['approxChargeStd']))
			except:
				pass
			self.fineData[cavity].setData(x=self.model.crestingData[cavity]['finePhaseData'],y=self.model.crestingData[cavity]['fineBPMData'])
			self.fineFit[cavity].setData(x=self.model.crestingData[cavity]['finePhaseFit'],y=self.model.crestingData[cavity]['fineBPMFit'])
			try:
				self.fineStd[cavity].setData(x=self.model.crestingData[cavity]['finePhaseData'],y=self.model.crestingData[cavity]['fineBPMData'],
				height=np.array(self.model.crestingData[cavity]['fineBPMStd']))
			except:
				pass
	# def allMethod(self):
	# 	if self.view.checkBox_all.isChecked()==True:
	# 		self.view.checkBox_1.setChecked (True)
	# 		self.view.checkBox_2.setChecked (True)
	# 		self.view.checkBox_3.setChecked (True)
	# 		self.view.checkBox_4.setChecked (True)
	# 	elif self.view.checkBox_all.isChecked()==False:
	# 		self.view.checkBox_1.setChecked (False)
	# 		self.view.checkBox_2.setChecked (False)
	# 		self.view.checkBox_3.setChecked (False)
	# 		self.view.checkBox_4.setChecked (False)
