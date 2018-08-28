from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
import sys,os
import time
import numpy as np
import pyqtgraph as pg
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\..\\..\\..\\Widgets\\loggerWidget\\')
#import loggerWidget as lw
import random as r
import cv2
from epics import caget,caput
from functools import partial
class Controller():
	#userinput=True
	def __init__(self, view, model):
		#global userinput
		#userinput = False
		'''define model and view'''
		self.view = view
		self.model = model
		#userinput = True
		#global userinput
		#print 'HERE WE ARE(controller)!!!!: BPM readout =', str(model.Cbpms.getXFromPV('C2V-BPM01'))
		self.bpm_list = self.model.bpm_list#['S01-BPM01', 'S02-BPM01', 'S02-BPM02', 'C2V-BPM01', \
		#'INJ-BPM04', 'INJ-BPM05', 'BA1-BPM01', 'BA1-BPM02', 'BA1-BPM03', 'BA1-BPM04']

		'''1 Create Momentum Graphs'''
		monitor = pg.GraphicsView()
		#text = pg.TextItem('Some text')
		#layout = pg.GraphicsLayout(border=(100,100,100))
		layout = pg.GraphicsLayout()
		monitor.setCentralItem(layout)

		for r, bpm_name in enumerate(self.bpm_list):
			row = str(r+1)
			setattr(self, 'label_'+row, layout.addLabel(bpm_name))
		layout.nextRow()

		#self.label_1 = layout.addLabel('')
		#self.label_2 = layout.addLabel('')
		#self.label_3 = layout.addLabel('')
		#self.label_4 = layout.addLabel('')		#monitor.addItem(text)


		'''1.1 create graph for BPM Y and Y position monitoring'''
		self.xdict = {0:'X', 1:'Y'}
		self.xdict_Q = {0:'Q'}
		#print self.xdict.keys()

		self.width1=0.9
		self.width2=1
		self.barcolour1_live=(60,100,255)
		self.barcolour1_notLive=(20,30,90)
		#self.barcolour1_live=self.barcolour1_notLive
		#self.barcolour2='r'
		self.barcolour2_live=(255,100,60)
		self.barcolour2_notLive=(90,30,20)
		self.barcolour3_live=(140,140,140)
		self.barcolour3_notLive=(50,50,50)
		for r, bpm_name in enumerate(self.bpm_list):
			row = str(r+1)
			setattr(self, 'positionGraph_'+row, layout.addPlot())
			getattr(self, 'positionGraph_'+row).axes['bottom']['item'].setTicks([self.xdict.items()])
			getattr(self, 'positionGraph_'+row).setMouseEnabled(x=False, y=True)
			getattr(self, 'positionGraph_'+row).setXRange(-0.7,1.7)
			getattr(self, 'positionGraph_'+row).setYRange(-15,15)
			setattr(self, 'bg'+row, pg.BarGraphItem(x=self.xdict.keys(), height=[0.0, 0.0], width=self.width1, pen=self.barcolour1_live, brush=self.barcolour1_live))
			setattr(self, 'bg'+row+'_target', pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=self.width2, pen=self.barcolour2_live, brush=self.barcolour2_live))
			getattr(self, 'positionGraph_'+row).addItem(getattr(self, 'bg'+row+'_target'))
			getattr(self, 'positionGraph_'+row).addItem(getattr(self, 'bg'+row))
		# self.positionGraph_1 = layout.addPlot(title="S01-BPM01")
		# self.positionGraph_2 = layout.addPlot(title="S02-BPM01")
		# self.positionGraph_3 = layout.addPlot(title="S02-BPM02")
		# self.positionGraph_4 = layout.addPlot(title="C2V-BPM01")
		# self.positionGraph_5 = layout.addPlot(title="INJ-BPM04")
		# self.positionGraph_6 = layout.addPlot(title="INJ-BPM05")


		# self.positionGraph_1.axes['bottom']['item'].setTicks([self.xdict.items()])
		# self.positionGraph_2.axes['bottom']['item'].setTicks([self.xdict.items()])
		# self.positionGraph_3.axes['bottom']['item'].setTicks([self.xdict.items()])
		# self.positionGraph_4.axes['bottom']['item'].setTicks([self.xdict.items()])
		# self.positionGraph_5.axes['bottom']['item'].setTicks([self.xdict.items()])
		# self.positionGraph_6.axes['bottom']['item'].setTicks([self.xdict.items()])



		# self.positionGraph_1.setMouseEnabled(x=False, y=True)
		# self.positionGraph_2.setMouseEnabled(x=False, y=True)
		# self.positionGraph_3.setMouseEnabled(x=False, y=True)
		# self.positionGraph_4.setMouseEnabled(x=False, y=True)
		# self.positionGraph_5.setMouseEnabled(x=False, y=True)
		# self.positionGraph_6.setMouseEnabled(x=False, y=True)


		# self.positionGraph_1.setYRange(-15,15)
		# self.positionGraph_2.setYRange(-15,15)
		# self.positionGraph_3.setYRange(-15,15)
		# self.positionGraph_4.setYRange(-15,15)
		# self.positionGraph_5.setYRange(-15,15)
		# self.positionGraph_6.setYRange(-15,15)
		# width=0.9
		# barcolour1=(30,80,255)
		# barcolour2='r'
		# self.bg1 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=width, pen=barcolour1, brush=barcolour1)
		# self.bg1_target = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=1, pen=barcolour2, brush=barcolour2)
		# self.bg2 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=width, pen=barcolour1, brush=barcolour1)
		# self.bg2_target = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=1, pen=barcolour2, brush=barcolour2)
		# self.bg3 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=width, pen=barcolour1, brush=barcolour1)
		# self.bg3_target = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=1, pen=barcolour2, brush=barcolour2)
		# self.bg4 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=width, pen=barcolour1, brush=barcolour1)
		# self.bg4_target = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=1, pen=barcolour2, brush=barcolour2)
		# self.bg5 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=width, pen=barcolour1, brush=barcolour1)
		# self.bg5_target = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=1, pen=barcolour2, brush=barcolour2)
		# self.bg6 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=width, pen=barcolour1, brush=barcolour1)
		# self.bg6_target = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=1, pen=barcolour2, brush=barcolour2)




		# self.positionGraph_1.addItem(self.bg1_target)
		# self.positionGraph_2.addItem(self.bg2_target)
		# self.positionGraph_3.addItem(self.bg3_target)
		# #layout.nextRow()
		# self.positionGraph_4.addItem(self.bg4_target)
		# self.positionGraph_5.addItem(self.bg5_target)
		# self.positionGraph_6.addItem(self.bg6_target)
		# self.positionGraph_1.addItem(self.bg1)
		# self.positionGraph_2.addItem(self.bg2)
		# self.positionGraph_3.addItem(self.bg3)
		# self.positionGraph_4.addItem(self.bg4)
		# self.positionGraph_5.addItem(self.bg5)
		# self.positionGraph_6.addItem(self.bg6)

		layout.nextRow()

		#self.label_1 = layout.addLabel('')
		#self.label_2 = layout.addLabel('')
		#self.label_3 = layout.addLabel('')
		#self.label_4 = layout.addLabel('')

		#self.bpm_list = ['S01-BPM01', 'S02-BPM01', 'S02-BPM02', 'C2V-BPM01', 'INJ-BPM04', 'INJ-BPM05']
		for r, bpm_name in enumerate(self.bpm_list):
			row = str(r+1)
			setattr(self, 'positionGraph_'+row+'_Q', layout.addPlot())
			getattr(self, 'positionGraph_'+row+'_Q').axes['bottom']['item'].setTicks([self.xdict_Q.items()])
			getattr(self, 'positionGraph_'+row+'_Q').setMouseEnabled(x=False, y=True)
			getattr(self, 'positionGraph_'+row+'_Q').setXRange(-0.7,0.7)
			getattr(self, 'positionGraph_'+row+'_Q').setYRange(0,135)
			setattr(self, 'bg'+row+'_Q', pg.BarGraphItem(x=self.xdict_Q.keys(), height=[0.0], width=0.5))
			getattr(self, 'positionGraph_'+row+'_Q').addItem(getattr(self, 'bg'+row+'_Q'))
		#self.positionGraph_1_Q = layout.addPlot(title="S01-BPM-01")
		#self.positionGraph_1_Q.axes['bottom']['item'].setTicks([self.xdict_Q.items()])
		#self.positionGraph_1_Q.setMouseEnabled(x=False, y=True)
		#self.bg1_Q = pg.BarGraphItem(x=self.xdict_Q.keys(), height=[0.0], width=1)
		#self.positionGraph_1_Q.addItem(self.bg1_Q)
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
		self.view.pushButton_Align_x_5.clicked.connect(partial(self.model.Align_x, 5))
		self.view.pushButton_Align_y_5.clicked.connect(partial(self.model.Align_y, 5))
		self.view.pushButton_Align_both_5.clicked.connect(partial(self.model.Align_both, 5))
		self.view.pushButton_Align_x_6.clicked.connect(partial(self.model.Align_x, 6))
		self.view.pushButton_Align_y_6.clicked.connect(partial(self.model.Align_y, 6))
		self.view.pushButton_Align_both_6.clicked.connect(partial(self.model.Align_both, 6))

		self.view.lineEdit_HC_1.editingFinished.connect(partial(self.model.steer_H, 1, 1))
		self.view.lineEdit_VC_1.editingFinished.connect(partial(self.model.steer_V, 1, 1))
		self.view.lineEdit_HC_2.editingFinished.connect(partial(self.model.steer_H, 2, 1))
		self.view.lineEdit_VC_2.editingFinished.connect(partial(self.model.steer_V, 2, 1))
		self.view.lineEdit_HC_3.editingFinished.connect(partial(self.model.steer_H, 3, 1))
		self.view.lineEdit_VC_3.editingFinished.connect(partial(self.model.steer_V, 3, 1))
		self.view.lineEdit_HC_4.editingFinished.connect(partial(self.model.steer_H, 4, 1))
		self.view.lineEdit_VC_4.editingFinished.connect(partial(self.model.steer_V, 4, 1))
		self.view.lineEdit_HC_5.editingFinished.connect(partial(self.model.steer_H, 5, 1))
		self.view.lineEdit_VC_5.editingFinished.connect(partial(self.model.steer_V, 5, 1))
		self.view.lineEdit_HC_6.editingFinished.connect(partial(self.model.steer_H, 6, 1))
		self.view.lineEdit_VC_6.editingFinished.connect(partial(self.model.steer_V, 6, 1))

		self.view.lineEdit_posAxisBounds.editingFinished.connect(self.model.setPosAxisBounds)
		self.view.lineEdit_qAxisMax.editingFinished.connect(self.model.setQAxisMax)
		# self.view.doubleSpinBox_H_1.setValue(self.model.get_H(1))
		# self.view.doubleSpinBox_V_1.setValue(self.model.get_V(1))
		# self.view.doubleSpinBox_H_2.setValue(self.model.get_H(2))
		# self.view.doubleSpinBox_V_2.setValue(self.model.get_V(2))
		# self.view.doubleSpinBox_H_3.setValue(self.model.get_H(3))
		# self.view.doubleSpinBox_V_3.setValue(self.model.get_V(3))
		# self.view.doubleSpinBox_H_4.setValue(self.model.get_H(4))
		# self.view.doubleSpinBox_V_4.setValue(self.model.get_V(4))

		# userinput = True
		#
		# self.view.doubleSpinBox_H_1.valueChanged.connect(partial(self.model.steer_H, 1, userinput))
		# self.view.doubleSpinBox_V_1.valueChanged.connect(partial(self.model.steer_V, 1, userinput))
		# self.view.doubleSpinBox_H_2.valueChanged.connect(partial(self.model.steer_H, 2, userinput))
		# self.view.doubleSpinBox_V_2.valueChanged.connect(partial(self.model.steer_V, 2, userinput))
		# self.view.doubleSpinBox_H_3.valueChanged.connect(partial(self.model.steer_H, 3, userinput))
		# self.view.doubleSpinBox_V_3.valueChanged.connect(partial(self.model.steer_V, 3, userinput))
		# self.view.doubleSpinBox_H_4.valueChanged.connect(partial(self.model.steer_H, 4, userinput))
		# self.view.doubleSpinBox_V_4.valueChanged.connect(partial(self.model.steer_V, 4, userinput))
		# self.view.doubleSpinBox_H_5.valueChanged.connect(partial(self.model.steer_H, 5, userinput))
		# self.view.doubleSpinBox_V_5.valueChanged.connect(partial(self.model.steer_V, 5, userinput))
		# self.view.doubleSpinBox_H_6.valueChanged.connect(partial(self.model.steer_H, 6, userinput))
		# self.view.doubleSpinBox_V_6.valueChanged.connect(partial(self.model.steer_V, 6, userinput))

		self.view.pushButton_set.clicked.connect(self.model.set)
		self.view.pushButton_set_0.clicked.connect(self.model.set_0)
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
		#self.view.pushButton_Checks.clicked.connect(self.model.measureMomentumSpreadChecks)
		#self.view.pushButton_MinBeta.clicked.connect(self.model.measureMomentumSpreadMinBeta)
		#self.view.pushButton_SetDispSize.clicked.connect(self.model.measureMomentumSpreadSetDispSize)
		#self.view.pushButton_CalcDisp.clicked.connect(self.model.measureMomentumSpreadCalcDisp)
		#self.view.pushButton_Calc.clicked.connect(self.model.measureMomentumSpreadCalc)

	def updateDisplays(self):
		#print os.system('caget CLA-S01-DIA-CAM-01:ANA:X_RBV')
		#time.sleep(0.2)
		#global userinput
		# if userinput == False:
		# 	print 'HEREREREERE'
		# 	print userinput
		# 	self.view.doubleSpinBox_H_3.setValue(self.model.get_H(3))
		# 	print userinput
		#print 'HERE WE ARE(updateDisplays)!!!!: BPM readout =', str(self.model.Cbpms.getXFromPV('C2V-BPM01'))

		# SAMPL
		#self.model.func.simulate.run()
		#time.sleep(0.1)
		#QApplication.processEvents()

		#self.displayMom.setText('MOMENTUM<br> Current: '+str(self.model.I)+' A<br>'+str(self.model.p)+' = MeV/c')
		#self.bg1.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV('S01-BPM01'), getattr(self.view, 'doubleSpinBox_x_'+str(1)).value(), \
		#1*self.model.Cbpms.getYFromPV('S01-BPM01'), getattr(self.view, 'doubleSpinBox_y_'+str(1)).value()])# replace the random generators with  bpm x read offs

		# Update BPM postion bar charts:
		for r, bpm_name in enumerate(self.bpm_list):
			row = str(r+1)
			getattr(self, 'bg'+row).setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV(bpm_name),1*self.model.Cbpms.getYFromPV(bpm_name)])
			getattr(self, 'bg'+row+'_target').setOpts(x=self.xdict.keys(), height=[getattr(self.view, 'doubleSpinBox_x_'+row).value(), getattr(self.view, 'doubleSpinBox_y_'+row).value()])
			liveTarget = getattr(self.model, 'liveTarget'+row)
			getattr(self, 'positionGraph_'+row).setYRange(-self.model.posAxisBounds,self.model.posAxisBounds)
			getattr(self, 'positionGraph_'+row+'_Q').setYRange(0,self.model.qAxisMax)
			#print row, liveTarget, bpm_name
			#time.sleep(0.5)
			if str(liveTarget) == 'GOOD':
				#print 'yes it\'s good'
				getattr(self, 'bg'+row+'_target').setOpts(pen=self.barcolour2_live, brush=self.barcolour2_live)
			else:
				getattr(self, 'bg'+row+'_target').setOpts(pen=self.barcolour2_notLive, brush=self.barcolour2_notLive)
		# self.bg1.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV('S01-BPM01'),1*self.model.Cbpms.getYFromPV('S01-BPM01')])
		# self.bg1_target.setOpts(x=self.xdict.keys(), height=[getattr(self.view, 'doubleSpinBox_x_'+str(1)).value(), getattr(self.view, 'doubleSpinBox_y_'+str(1)).value()])
		# self.bg2.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV('S02-BPM01'),1*self.model.Cbpms.getYFromPV('S02-BPM01')])
		# self.bg2_target.setOpts(x=self.xdict.keys(), height=[getattr(self.view, 'doubleSpinBox_x_'+str(2)).value(), getattr(self.view, 'doubleSpinBox_y_'+str(2)).value()])
		# self.bg3.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV('S02-BPM02'),1*self.model.Cbpms.getYFromPV('S02-BPM02')])
		# self.bg3_target.setOpts(x=self.xdict.keys(), height=[getattr(self.view, 'doubleSpinBox_x_'+str(3)).value(), getattr(self.view, 'doubleSpinBox_y_'+str(3)).value()])
		# self.bg4.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV('C2V-BPM01'),1*self.model.Cbpms.getYFromPV('C2V-BPM01')])
		# self.bg4_target.setOpts(x=self.xdict.keys(), height=[getattr(self.view, 'doubleSpinBox_x_'+str(4)).value(), getattr(self.view, 'doubleSpinBox_y_'+str(4)).value()])
		# self.bg5.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV('INJ-BPM04'),1*self.model.Cbpms.getYFromPV('INJ-BPM04')])
		# self.bg5_target.setOpts(x=self.xdict.keys(), height=[getattr(self.view, 'doubleSpinBox_x_'+str(5)).value(), getattr(self.view, 'doubleSpinBox_y_'+str(5)).value()])
		# self.bg6.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV('INJ-BPM05'),1*self.model.Cbpms.getYFromPV('INJ-BPM05')])
		# self.bg6_target.setOpts(x=self.xdict.keys(), height=[getattr(self.view, 'doubleSpinBox_x_'+str(6)).value(), getattr(self.view, 'doubleSpinBox_y_'+str(6)).value()])

		# Update BPM charge bar charts
		for r, bpm_name in enumerate(self.bpm_list):
			row = str(r+1)
			#print row, self.model.Cbpms.getBPMQBuffer(bpm_name), bpm_name
			#time.sleep(1)
			#if len(self.model.Cbpms.getBPMQBuffer(bpm_name)) > 0:
			#print row, self.model.Cbpms.getBPMQBuffer(bpm_name), len(self.model.Cbpms.getBPMQBuffer(bpm_name)), bpm_name

			#time.sleep(0.5)
			if len(self.model.Cbpms.getBPMQBuffer(bpm_name)) > 0 and str(self.model.Cbpms.getStatusBuffer(bpm_name)[-1]) == 'GOOD':
				#print 'yes'
				getattr(self, 'bg'+row+'_Q').setOpts(x=self.xdict_Q.keys(), height=[np.mean(self.model.Cbpms.getBPMQBuffer(bpm_name))], pen=self.barcolour3_live, brush=self.barcolour3_live)
				getattr(self, 'bg'+row).setOpts(pen=self.barcolour1_live, brush=self.barcolour1_live)
			else:
				#print 'no'
				getattr(self, 'bg'+row+'_Q').setOpts(x=self.xdict_Q.keys(), height=[0], pen=self.barcolour3_live, brush=self.barcolour3_live)
				getattr(self, 'bg'+row).setOpts(pen=self.barcolour1_notLive, brush=self.barcolour1_notLive)

						# self.bg1_Q.setOpts(x=self.xdict_Q.keys(), height=[np.mean(self.model.Cbpms.getBPMQBuffer('S01-BPM01'))])
		# self.bg2_Q.setOpts(x=self.xdict_Q.keys(), height=[np.mean(self.model.Cbpms.getBPMQBuffer('S02-BPM01'))])
		# self.bg3_Q.setOpts(x=self.xdict_Q.keys(), height=[np.mean(self.model.Cbpms.getBPMQBuffer('S02-BPM02'))])
		# self.bg4_Q.setOpts(x=self.xdict_Q.keys(), height=[np.mean(self.model.Cbpms.getBPMQBuffer('C2V-BPM01'))])
		#chargebufferfromfunc = bpmctrl.getBPMQBuffer(bpm_name)

		#self.view.label_H_1.setNum(1*self.model.Cbpms.getXFromPV('S01-BPM01'))
		#self.view.label_V_1.setNum(1*self.model.Cbpms.getYFromPV('S01-BPM01'))

		# Update BPM readout boxes
		for r, bpm_name in enumerate(self.bpm_list):
			row = str(r+1)
			getattr(self.view, 'label_H_'+row).setNum(1*self.model.Cbpms.getXFromPV(str(getattr(self.view, 'comboBox_'+row).currentText())))
			getattr(self.view, 'label_V_'+row).setNum(1*self.model.Cbpms.getYFromPV(str(getattr(self.view, 'comboBox_'+row).currentText())))
			if len(self.model.Cbpms.getBPMQBuffer(bpm_name)) > 0 and str(self.model.Cbpms.getStatusBuffer(bpm_name)[-1]) == 'GOOD':
				getattr(self.view, 'label_V_av_'+row).setNum(np.mean(1*self.model.Cbpms.getBPMYBuffer(str(getattr(self.view, 'comboBox_'+row).currentText()))))
				getattr(self.view, 'label_H_av_'+row).setNum(np.mean(1*self.model.Cbpms.getBPMXBuffer(str(getattr(self.view, 'comboBox_'+row).currentText()))))
			else:
				getattr(self.view, 'label_V_av_'+row).setText('')
				getattr(self.view, 'label_V_av_'+row).setText('')
		for r, bpm_name in enumerate(self.bpm_list):
			row = str(r+1)
			getattr(self.view, 'label_HC_'+row).setNum(self.model.get_H(row))
			getattr(self.view, 'label_VC_'+row).setNum(self.model.get_V(row))
