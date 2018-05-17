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
		self.timer.start(10)

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
		self.approxData.setData(x=self.model.approxPhaseData,y=self.model.approxChargeData)
		self.approxFit.setData(x=self.model.approxPhaseFit,y=self.model.approxChargeFit)
		self.fineData.setData(x=self.model.finePhaseData,y=self.model.fineBPMData)
		self.fineFit.setData(x=self.model.finePhaseFit,y=self.model.fineBPMFit)
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
