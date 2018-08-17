from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
import sys,os
import time
import numpy as np
import pyqtgraph as pg
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\..\\..\\..\\Widgets\\loggerWidget\\')
import loggerWidget as lw
import random as r
import cv2
from epics import caget,caput
from functools import partial
class Controller():

	def __init__(self, view, model):
		'''define model and view'''
		self.view = view
		self.model = model
		print 'HERE WE ARE(controller)!!!!: BPM readout =', str(model.Cbpms.getXFromPV('C2V-BPM01'))
		'''1 Create Momentum Graphs'''
		monitor = pg.GraphicsView()
		layout = pg.GraphicsLayout(border=(100,100,100))
		monitor.setCentralItem(layout)
		'''1.1 create graph for BPM Y and Y position monitoring'''
		self.xdict = {0:'X', 1:'Y'}
		self.positionGraph_1 = layout.addPlot(title="S01-BPM-01")
		self.positionGraph_2 = layout.addPlot(title="S02-BPM-01")
		self.positionGraph_3 = layout.addPlot(title="S02-BPM-02")
		self.positionGraph_4 = layout.addPlot(title="C2V-BPM-01")
		self.positionGraph_1.axes['bottom']['item'].setTicks([self.xdict.items()])
		self.positionGraph_2.axes['bottom']['item'].setTicks([self.xdict.items()])
		self.positionGraph_3.axes['bottom']['item'].setTicks([self.xdict.items()])
		self.positionGraph_4.axes['bottom']['item'].setTicks([self.xdict.items()])
		self.positionGraph_1.setYRange(-1,1)
		self.positionGraph_2.setYRange(-1,1)
		self.positionGraph_3.setYRange(-1,1)
		self.positionGraph_4.setYRange(-1,1)
		self.bg1 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=1)
		self.bg2 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=1)
		self.bg3 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=1)
		self.bg4 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=1)
		self.positionGraph_1.addItem(self.bg1)
		self.positionGraph_2.addItem(self.bg2)
		self.positionGraph_3.addItem(self.bg3)
		self.positionGraph_4.addItem(self.bg4)
		layout.nextRow()
		self.label_1 = layout.addLabel('')
		self.label_2 = layout.addLabel('')
		self.label_3 = layout.addLabel('')
		self.label_4 = layout.addLabel('')
		'''1.2 Create place to diplay an image of a YAG screen'''
		# yagImageBox = layout.addViewBox(lockAspect=True, colspan=2)
		# self.YAGImage = pg.ImageItem(np.random.normal(size=(2560,2160)))
		# yagImageBox.addItem(self.YAGImage)
		# self.displayMom = layout.addLabel('MOMENTUM = MeV/c')
		self.view.horizontalLayout_4.addWidget(monitor)

		'''2. Create Momentum Spread Graphs'''
		# monitor_s = pg.GraphicsView()
		# layout_s = pg.GraphicsLayout(border=(100,100,100))
		# monitor_s.setCentralItem(layout_s)
		# self.dispersionGraph  = layout_s.addPlot(title="Dispersion")
		# self.dCurve = self.dispersionGraph.plot(pen = 'y')
		# self.fCurve = self.dispersionGraph.plot(pen = 'r')
		# self.displayDisp = layout_s.addLabel('DISPERSION = pixels per Ampere')
		# layout_s.nextRow()
		# self.profileGraph  = layout_s.addPlot(title="Fit to YAG Profile")
		# self.displayMom_S = layout_s.addLabel('Momentum Spread =  MeV/c')
		# self.view.horizontalLayout_5.addWidget(monitor_s)

		'''Create logs for each procedure (and combined on log Tab)'''
		'''self.FullLog = lw.loggerWidget([self.model.PL,self.model.PSL,self.model.deets])
		self.FullLog.setLogColours(debugcolour='blue',infocolour='green',warningcolour='orange',errorcolour='red',criticalcolour='purple')
		self.pLog = lw.loggerWidget(self.model.PL)
		self.pLog.setColumnWidths(155,40,80)
		self.pLog.setLogColours(debugcolour='blue',infocolour='green',warningcolour='orange',errorcolour='red',criticalcolour='purple')
		self.psLog = lw.loggerWidget(self.model.PSL)
		self.psLog.setColumnWidths(155,40,80)
		self.psLog.setLogColours(debugcolour='blue',infocolour='green',warningcolour='orange',errorcolour='red',criticalcolour='purple')
		self.view.gridLayout_3.addWidget(self.FullLog)
		self.view.gridLayout_2.addWidget(self.psLog , 9,0,1,2)
		self.view.gridLayout.addWidget(self.pLog , 8,0,1,2)'''


		'''Threads for updating graphs and labels'''
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.updateDisplays)
		self.timer.start(100)

		'''Connections to GUI Buttons'''
		#self.view.pushButton_Prelim.clicked.connect(self.model.measureMomentumPrelim)
		#self.view.pushButton_Align.clicked.connect(self.model.measureMomentumAlign)
		#self.view.pushButton_Align_2.clicked.connect(self.model.measureMomentumAlign_2)
		self.view.pushButton_Align_x_1.clicked.connect(partial(self.model.Align_x, 1))
		self.view.pushButton_Align_y_1.clicked.connect(partial(self.model.Align_y, 1))
		self.view.pushButton_Align_both_1.clicked.connect(partial(self.model.Align_both, 1))
		self.view.pushButton_Align_x_2.clicked.connect(partial(self.model.Align_x, 2))
		self.view.pushButton_Align_y_2.clicked.connect(partial(self.model.Align_y, 2))
		self.view.pushButton_Align_both_2.clicked.connect(partial(self.model.Align_both, 2))
		self.view.pushButton_Align_x_3.clicked.connect(partial(self.model.Align_x, 3))
		self.view.pushButton_Align_y_3.clicked.connect(partial(self.model.Align_y, 3))
		self.view.pushButton_Align_both_3.clicked.connect(partial(self.model.Align_both, 3))
		self.view.pushButton_Align_x_4.clicked.connect(partial(self.model.Align_x, 4))
		self.view.pushButton_Align_y_4.clicked.connect(partial(self.model.Align_y, 4))
		self.view.pushButton_Align_both_4.clicked.connect(partial(self.model.Align_both, 4))


		self.view.doubleSpinBox_H_1.valueChanged.connect(partial(self.model.steer_H,1))
		self.view.doubleSpinBox_V_1.valueChanged.connect(partial(self.model.steer_V,1))
		self.view.doubleSpinBox_H_2.valueChanged.connect(partial(self.model.steer_H,2))
		self.view.doubleSpinBox_V_2.valueChanged.connect(partial(self.model.steer_V,2))
		self.view.doubleSpinBox_H_3.valueChanged.connect(partial(self.model.steer_H,3))
		self.view.doubleSpinBox_V_3.valueChanged.connect(partial(self.model.steer_V,3))
		self.view.doubleSpinBox_H_4.valueChanged.connect(partial(self.model.steer_H,4))
		self.view.doubleSpinBox_V_4.valueChanged.connect(partial(self.model.steer_V,4))

		self.view.pushButton_save.clicked.connect(self.model.save)
		self.view.pushButton_save_2.clicked.connect(self.model.save_positions)
		self.view.pushButton_load.clicked.connect(self.model.load)
		#self.view.comboBox_1.currentIndexChanged.connect(self.model.combobox_bpm)
		#self.view.doubleSpinBox.

		#self.view.pushButton_CentreC2V.clicked.connect(self.model.measureMomentumCentreC2V)
		#self.view.pushButton_CalcMom.clicked.connect(self.model.measureMomentumCalcMom)

		#self.view.pushButton_s.clicked.connect(self.model.measureMomentumSpread)
		#self.view.checkBox_all.stateChanged.connect(self.setChecks_mom)
		#self.view.checkBox_all_s.stateChanged.connect(self.setChecks_mom_s)
		#self.view.pushButton_refreshImage.clicked.connect(self.refreshImage)
		self.view.pushButton_Checks.clicked.connect(self.model.measureMomentumSpreadChecks)
		self.view.pushButton_MinBeta.clicked.connect(self.model.measureMomentumSpreadMinBeta)
		self.view.pushButton_SetDispSize.clicked.connect(self.model.measureMomentumSpreadSetDispSize)
		self.view.pushButton_CalcDisp.clicked.connect(self.model.measureMomentumSpreadCalcDisp)
		self.view.pushButton_Calc.clicked.connect(self.model.measureMomentumSpreadCalc)

	def updateDisplays(self):
		#print 'HERE WE ARE(updateDisplays)!!!!: BPM readout =', str(self.model.Cbpms.getXFromPV('C2V-BPM01'))

		# SAMPL
		self.model.func.simulate.run()
		time.sleep(0.1)
		QApplication.processEvents()

		#self.displayMom.setText('MOMENTUM<br> Current: '+str(self.model.I)+' A<br>'+str(self.model.p)+' = MeV/c')
		self.bg1.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV('S01-BPM01'),1*self.model.Cbpms.getYFromPV('S01-BPM01')], width=1)# replace the random generators with  bpm x read offs
		self.bg2.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV('S02-BPM01'),1*self.model.Cbpms.getYFromPV('S02-BPM01')], width=1)
		self.bg3.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV('S02-BPM02'),1*self.model.Cbpms.getYFromPV('S02-BPM02')], width=1)
		self.bg4.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV('C2V-BPM01'),1*self.model.Cbpms.getYFromPV('C2V-BPM01')], width=1)
		self.label_1.setText('x='+str(1*self.model.Cbpms.getXFromPV('S01-BPM01'))+' y='+str(1*self.model.Cbpms.getYFromPV('S01-BPM01')))
		self.label_2.setText('x='+str(1*self.model.Cbpms.getXFromPV('S02-BPM01'))+' y='+str(1*self.model.Cbpms.getYFromPV('S02-BPM01')))
		self.label_3.setText('x='+str(1*self.model.Cbpms.getXFromPV('S02-BPM02'))+' y='+str(1*self.model.Cbpms.getYFromPV('S02-BPM02')))
		self.label_4.setText('x='+str(1*self.model.Cbpms.getXFromPV('C2V-BPM01'))+' y='+str(1*self.model.Cbpms.getYFromPV('C2V-BPM01')))
		self.view.doubleSpinBox_H_1.setValue(self.model.get_H(1))
		self.view.doubleSpinBox_V_1.setValue(self.model.get_V(1))
		self.view.doubleSpinBox_H_2.setValue(self.model.get_H(2))
		self.view.doubleSpinBox_V_2.setValue(self.model.get_V(2))
		self.view.doubleSpinBox_H_3.setValue(self.model.get_H(3))
		self.view.doubleSpinBox_V_3.setValue(self.model.get_V(3))
		self.view.doubleSpinBox_H_4.setValue(self.model.get_H(4))
		self.view.doubleSpinBox_V_4.setValue(self.model.get_V(4))
		# self.dCurve.setData(x=self.model.dCurrents,y=self.model.dPositions)
		# self.fCurve.setData(x=self.model.fCurrents,y=self.model.fPositions)
		# self.displayDisp.setText('DISPERSION:<br>'+str(self.model.Dispersion)+' m/A')
		# self.displayMom_S.setText('MOMENTUM SPREAD:<br>'+str(self.model.pSpread)+' MeV/c')
	def refreshImage(self):
		 #image = np.random.normal(size=(2560,2160))
		 cap = cv2.VideoCapture("http://192.168.83.31:7080/MJPG1.mjpg")
		 #print cap
		 _,frame = cap.read()
		 self.YAGImage.setImage(np.flip(np.transpose(frame[:,:,0]),1))

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