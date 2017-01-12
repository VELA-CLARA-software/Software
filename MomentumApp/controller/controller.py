from PyQt4 import QtGui, QtCore
import sys,os
import time
import numpy as np
import pyqtgraph as pg
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\..\\..\\loggerWidget\\')
import loggerWidget as lw
import random as r

class Controller():

	def __init__(self, view, model):
		'''define model and view'''
		self.view = view
		self.model = model
		'''1 Create Momentum Graphs'''
		monitor = pg.GraphicsView()
		layout = pg.GraphicsLayout(border=(100,100,100))
		monitor.setCentralItem(layout)
		'''1.1 create graph for BPM Y and Y position monitoring'''
		self.xdict = {0:'X', 1:'Y'}
		self.positionGraph_1 = layout.addPlot(title="BPM XX")
		self.positionGraph_2 = layout.addPlot(title="BPM XX")
		self.positionGraph_3 = layout.addPlot(title="BPM XX")
		self.positionGraph_1.axes['bottom']['item'].setTicks([self.xdict.items()])
		self.positionGraph_2.axes['bottom']['item'].setTicks([self.xdict.items()])
		self.positionGraph_3.axes['bottom']['item'].setTicks([self.xdict.items()])
		self.bg1 = pg.BarGraphItem(x=self.xdict.keys(), height=[-0.3,0.2], width=1)
		self.bg2 = pg.BarGraphItem(x=self.xdict.keys(), height=[-0.3,0.2], width=1)
		self.bg3 = pg.BarGraphItem(x=self.xdict.keys(), height=[-0.3,0.2], width=1)
		self.positionGraph_1.setYRange(-1,1)
		self.positionGraph_2.setYRange(-1,1)
		self.positionGraph_3.setYRange(-1,1)
		self.positionGraph_1.addItem(self.bg1)
		self.positionGraph_2.addItem(self.bg2)
		self.positionGraph_3.addItem(self.bg3)
		layout.nextRow()
		'''1.2 Create plave to diplay and image of a YAG screen'''
		yagImageBox = layout.addViewBox(lockAspect=True, colspan=2)
		self.YAGImage = pg.ImageItem(np.random.normal(size=(1392,1040)))
		yagImageBox.addItem(self.YAGImage)
		self.displayMom = layout.addLabel('MOMENTUM = MeV/c')
		self.view.horizontalLayout_4.addWidget(monitor)

		'''2. Create Momentum Spread Graphs'''
		monitor_s = pg.GraphicsView()
		layout_s = pg.GraphicsLayout(border=(100,100,100))
		monitor_s.setCentralItem(layout_s)
		self.dispersionGraph  = layout_s.addPlot(title="Dispersion")
		self.displayDisp = layout_s.addLabel('DISPERSION = pixels per Ampere')
		layout_s.nextRow()
		self.profileGraph  = layout_s.addPlot(title="Fit to YAG Profile")
		self.displayMom_S = layout_s.addLabel('Momentum Spread =  MeV/c')
		self.view.horizontalLayout_5.addWidget(monitor_s)

		'''Create logs for each procedure (and combined on log Tab)'''
		self.FullLog = lw.loggerWidget([self.model.PL,self.model.PSL,self.model.deets])
		self.FullLog.setLogColours(debugcolour='blue',infocolour='green',warningcolour='orange',errorcolour='red',criticalcolour='purple')
		self.pLog = lw.loggerWidget(self.model.PL)
		self.pLog.setColumnWidths(155,40,80)
		self.pLog.setLogColours(debugcolour='blue',infocolour='green',warningcolour='orange',errorcolour='red',criticalcolour='purple')
		self.psLog = lw.loggerWidget(self.model.PSL)
		self.psLog.setColumnWidths(155,40,80)
		self.psLog.setLogColours(debugcolour='blue',infocolour='green',warningcolour='orange',errorcolour='red',criticalcolour='purple')
		self.view.gridLayout_3.addWidget(self.FullLog)
		self.view.gridLayout_2.addWidget(self.psLog , 9,0,1,2)
		self.view.gridLayout.addWidget(self.pLog , 8,0,1,2)


		'''Threads for updating graphs and labels'''
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.updateDisplays)
		self.timer.start(500)

		'''Connections to GUI Buttons'''
		self.view.pushButton.clicked.connect(self.model.measureMomentum)
		self.view.pushButton_s.clicked.connect(self.model.measureMomentumSpread)
		self.view.checkBox_all.stateChanged.connect(self.setChecks_mom)
		self.view.checkBox_all_s.stateChanged.connect(self.setChecks_mom_s)
		self.view.pushButton_refreshImage.clicked.connect(self.refreshImage)


	def updateDisplays(self):
		self.displayMom.setText('MOMENTUM<br> Current: '+str(self.model.I)+' A<br>'+str(self.model.p)+' = MeV/c')
		self.bg1.setOpts(x=self.xdict.keys(), height=[r.uniform(-1,1),r.uniform(-1,1)], width=1)# replace the random generators with  bpm x read offs
		self.bg2.setOpts(x=self.xdict.keys(), height=[r.uniform(-1,1),r.uniform(-1,1)], width=1)
		self.bg3.setOpts(x=self.xdict.keys(), height=[r.uniform(-1,1),r.uniform(-1,1)], width=1)

	def refreshImage(self):
		self.YAGImage.setImage(np.random.normal(size=(1392,1040)))

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
