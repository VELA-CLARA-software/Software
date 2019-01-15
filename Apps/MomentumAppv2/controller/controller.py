from PyQt4 import QtGui, QtCore
import sys,os
import time
import numpy as np
import pyqtgraph as pg
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\..\\..\\..\\Widgets\\loggerWidget\\')
#import loggerWidget as lw
import random as r
import cv2
from epics import caget,caput
class Controller():

	def __init__(self, view, model):
		'''define model and view'''
		self.view = view
		self.model = model
		#print 'HERE WE ARE(controller)!!!!: BPM readout =', str(model.Cbpms.getXFromPV('C2V-BPM01'))
		'''1 Create Momentum Graphs'''
		monitor = pg.GraphicsView()
		layout = pg.GraphicsLayout(border=(100,100,100))
		monitor.setCentralItem(layout)
		'''1.1 create graph for BPM Y and Y position monitoring'''
		self.xdict = {0:'X', 1:'Y'}
		#self.positionGraph_1 = layout.addPlot(title="S02-BPM-01")
		self.positionGraph_2 = layout.addPlot(title="S02-YAG02", labels = {'left': '&Delta; x [mm]'})
		self.positionGraph_3 = layout.addPlot(title="S02-BPM02", labels = {'left': '&Delta; x  [mm]'})
		self.positionGraph_4 = layout.addPlot(title="C2V-BPM01", labels = {'left': '&Delta; x  [mm]'})
		#self.positionGraph_1.axes['bottom']['item'].setTicks([self.xdict.items()])
		self.positionGraph_2.axes['bottom']['item'].setTicks([self.xdict.items()])
		self.positionGraph_3.axes['bottom']['item'].setTicks([self.xdict.items()])
		self.positionGraph_4.axes['bottom']['item'].setTicks([self.xdict.items()])
		#self.positionGraph_1.setMouseEnabled(x=False, y=True)
		self.positionGraph_2.setMouseEnabled(x=False, y=True)
		self.positionGraph_3.setMouseEnabled(x=False, y=True)
		self.positionGraph_4.setMouseEnabled(x=False, y=True)
		self.bgMin = -15
		self.bgMax = 15
		#self.positionGraph_1.setYRange(self.bgMin,self.bgMax)
		#self.positionGraph_2.setYRange(self.bgMin,self.bgMax)
		self.positionGraph_2.setYRange(self.bgMin,self.bgMax)
		self.positionGraph_3.setYRange(self.bgMin,self.bgMax)
		self.positionGraph_4.setYRange(self.bgMin,self.bgMax)
		#barcolour1=(30,255,80)
		#barcolour2=(5,40,12)
		barcolour1=(30,80,255)
		barcolour2=(5,40,12)
		barcolourt=(255,80,30)
		barwidth = 0.85
		barwidth2 = 1.0
		#self.bg1 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=1)
		self.bg2 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour1, brush=barcolour1)
		#self.bg2_target = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth2, pen=barcolourt, brush=barcolourt)
		self.bg2_y = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour2, brush=barcolour2)
		self.bg3 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour1, brush=barcolour1)
		#self.bg3_target = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth2, pen=barcolourt, brush=barcolourt)
		self.bg3_y = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour2, brush=barcolour2)
		self.bg4 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour1, brush=barcolour1)
		#self.bg4_target = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth2, pen=barcolourt, brush=barcolourt)
		self.bg4_y = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour2, brush=barcolour2)
		#self.positionGraph_1.setYRange(-1,1)
		#self.positionGraph_2.setYRange(-1,1)
		#self.positionGraph_3.setYRange(-1,1)
		#self.positionGraph_1.addItem(self.bg1)
		#self.positionGraph_2.addItem(self.bg2_target)
		self.positionGraph_2.addItem(self.bg2)
		self.positionGraph_2.addItem(self.bg2_y)

		#self.positionGraph_3.addItem(self.bg3_target)
		self.positionGraph_3.addItem(self.bg3)
		self.positionGraph_3.addItem(self.bg3_y)

		#self.positionGraph_4.addItem(self.bg4_target)
		self.positionGraph_4.addItem(self.bg4)
		self.positionGraph_4.addItem(self.bg4_y)
		layout.nextRow()
		#'''1.2 Create place to diplay an image of a YAG screen'''
		# yagImageBox = layout.addViewBox(lockAspect=True, colspan=3)
		# self.YAGImage = pg.ImageItem(np.random.normal(size=(2560,2160)))
		# yagImageBox.addItem(self.YAGImage)

		self.scanGraph = layout.addPlot(title = 'Rough dipole scan', colspan=3, labels = {'left': 'BPM x pos. [mm]', 'bottom': 'Dipole current [A]'})
		#x1=[0, 1, 2, 3]
		#y1=[0, 1, 4, 9]
		#self.sp = pg.ScatterPlotItem()
		self.sp = pg.PlotDataItem()
		#n=30
		#pos = np.random.normal(size=(2,n), scale=1e-5)
		#spots = [{'pos': pos[:,i], 'data': 1} for i in range(n)] + [{'pos': [0,0], 'data': 1}]
		x=[0,1,2]
		y=[0,0,0]
		self.sp.setData(x,y)
		self.scanGraph.addItem(self.sp)

		layout.nextRow()
		self.scanGraph2 = layout.addPlot(title = 'Scan to find signal on S02-BPM-02', colspan=3, labels = {'left': 'BPM x pos. [mm]', 'bottom': 'Corrector current [A]'})
		self.sp2 = pg.PlotDataItem()
		x=[]
		y=[]
		self.sp2.setData(x,y)
		self.scanGraph2.addItem(self.sp2)

		layout.nextRow()
		self.scanGraph3 = layout.addPlot(title = 'Fine dipole scan (no plotting yet)', colspan=3, labels = {'left': 'BPM x pos. [mm]', 'bottom': 'Dipole current [A]'})
		self.sp3 = pg.PlotDataItem()
		x=[]
		y=[]
		self.sp3.setData(x,y)
		self.scanGraph3.addItem(self.sp3)

		layout.nextRow()
		self.displayMom = layout.addLabel('MOMENTUM = MeV/c', colspan=3)

		self.view.horizontalLayout_4.addWidget(monitor)

		'''2. Create Momentum Spread Graphs'''
		monitor_s = pg.GraphicsView()
		layout_s = pg.GraphicsLayout(border=(100,100,100))
		monitor_s.setCentralItem(layout_s)
		self.dispersionGraph  = layout_s.addPlot(title="Dispersion")
		self.dCurve = self.dispersionGraph.plot(pen = 'y')
		self.fCurve = self.dispersionGraph.plot(pen = 'r')
		self.displayDisp = layout_s.addLabel('DISPERSION = pixels per Ampere')
		layout_s.nextRow()
		self.profileGraph  = layout_s.addPlot(title="Fit to YAG Profile")
		self.displayMom_S = layout_s.addLabel('Momentum Spread =  MeV/c')
		self.view.horizontalLayout_5.addWidget(monitor_s)

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
		self.view.comboBox_selectRF.currentIndexChanged.connect(self.model.selectRF)
		self.view.comboBox_selectRF.activated.connect(self.model.selectRF)
		#self.view.lineEdit_selectCurrent.editingFinished.connect(self.model.selectCurrent)
		self.view.doubleSpinBox_I.valueChanged.connect(self.model.selectCurrent)
		self.view.pushButton_useCurrent.clicked.connect(self.model.useCurrent)
		#self.view.lineEdit_selectMom.editingFinished.connect(self.model.selectMom)
		self.view.doubleSpinBox_I.valueChanged.connect(self.model.selectMom)
		self.view.pushButton_useRF.clicked.connect(self.model.useRF)

		self.view.pushButton_Prelim_1.clicked.connect(self.model.measureMomentumPrelim_1)
		#self.view.pushButton_Prelim_2.clicked.connect(self.model.measureMomentumPrelim_2)
		self.view.pushButton_Prelim_3.clicked.connect(self.model.measureMomentumPrelim_3)
		#self.view.pushButton_Prelim_4.clicked.connect(self.model.measureMomentumPrelim_4)#
		#self.view.pushButton_Prelim_5.clicked.connect(self.model.measureMomentumPrelim_5)

		self.view.pushButton_Align_1a.clicked.connect(self.model.measureMomentumAlign_1_A)
		self.view.pushButton_Align_1.clicked.connect(self.model.measureMomentumAlign_1)
		self.view.pushButton_Align_2_A.clicked.connect(self.model.measureMomentumAlign_2_A)
		self.view.pushButton_Align_2.clicked.connect(self.model.measureMomentumAlign_2)
		self.view.pushButton_Align_2_B.clicked.connect(self.model.measureMomentumAlign_2_B)
		self.view.pushButton_Align_3.clicked.connect(self.model.measureMomentumAlign_3)
		self.view.pushButton_Align_4.clicked.connect(self.model.measureMomentumAlign_4)

		self.view.pushButton_roughGetCurrentRange.clicked.connect(self.model.roughGetCurrentRange)
		self.view.pushButton_roughGetRFRange.clicked.connect(self.model.roughGetRFRange)
		#self.view.pushButton_fineGetCurrentRange.clicked.connect(self.model.fineGetCurrentRange)
		#self.view.pushButton_fineGetRFRange.clicked.connect(self.model.fineGetRFRange)
		self.view.pushButton_fineGetCurrentRange_2.clicked.connect(self.model.fineGetCurrentRange_2)
		self.view.pushButton_fineGetRFRange_2.clicked.connect(self.model.fineGetRFRange_2)

		self.view.lineEdit_roughCurrentMin.editingFinished.connect(self.model.setRoughMinI)
		self.view.lineEdit_roughCurrentMax.editingFinished.connect(self.model.setRoughMaxI)
		self.view.lineEdit_roughRFMin.editingFinished.connect(self.model.setRoughMinRF)
		self.view.lineEdit_roughRFMax.editingFinished.connect(self.model.setRoughMaxRF)
		self.view.lineEdit_fineCurrentMin.editingFinished.connect(self.model.setFineMinI)
		self.view.lineEdit_fineCurrentMax.editingFinished.connect(self.model.setFineMaxI)
		#self.view.lineEdit_fineRFMin.editingFinished.connect(self.model.setFineMinRF)
		#self.view.lineEdit_fineRFMax.editingFinished.connect(self.model.setFineMaxRF)

		self.view.pushButton_roughCentreC2VCurrent.clicked.connect(self.model.measureMomentumCentreC2VApprox)
		self.view.pushButton_fineCentreC2VCurrent.clicked.connect(self.model.measureMomentumCentreC2V)
		# self.view.pushButton_fineCentreC2VCurrent_2.clicked.connect(self.model.measureMomentumCentreC2V_2)


		# self.view.pushButton_degaussC2V.clicked.connect(self.model.degaussC2V)
		# self.view.pushButton_camState2C2V.clicked.connect(self.model.camState2C2V)
		# self.view.pushButton_insertC2VScreen.clicked.connect(self.model.insertC2VScreen)
		# self.view.pushButton_retractC2VScreen.clicked.connect(self.model.retractC2VScreen)
		#
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
		#print 'updateDisplays'
		#print os.system('caget CLA-S01-DIA-CAM-01:ANA:X_RBV')
		#print 'uD1'
		#print self.model.Cbpms.getXFromPV('S02-BPM01')
		#print 'uD2'
		#print 'HERE WE ARE(updateDisplays)!!!!: BPM readout =', str(self.model.Cbpms.getXFromPV('C2V-BPM01'))
		#self.view.label_predictMom_2.setText('S02-DIP-01 = '+str(self.model.Cmagnets.getSI('S02-DIP01'))+' A')
		#self.view.label_predictMom.setText(str(self.model.predictedMomentum))
		#self.view.label_predictI.setText(str(self.model.predictedI))
		#self.view.doubleSpinBox_p.setValue(float(self.model.predictedMomentum))
		#self.view.doubleSpinBox_I.setValue(float(self.model.predictedI))
		self.view.label_I.setText('('+self.model.dipole+' = '+str(self.model.Cmagnets.getSI(self.model.dipole))+' A)')
		self.view.label_I_2.setText(self.model.dipole+' = '+str(self.model.Cmagnets.getSI(self.model.dipole))+' A')
		self.view.label_RF.setText('(show relevant RF settings...)')

		#self.displayMom.setText('Approx. Momentum<br> Current: '+str(self.model.approxI)+' A<br>'+str(self.model.approx_p)+' = MeV/c<br><br>MOMENTUM<br> Current: '+str(self.model.I)+' A<br>'+str(self.model.p)+' = MeV/c')
		self.displayMom.setText('APPROX: Current: '+str(self.model.approxI)+' A, Momentum = '+str(self.model.approx_p)+' MeV/c<br>FINE: Current: '+str(self.model.I)+' A, Momentum = '+str(self.model.p)+' MeV/c')
#self.bg1.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV('S02-BPM01'),1*self.model.Cbpms.getYFromPV('S02-BPM01')], width=1)# replace the random generators with  bpm x read offs
		#self.bg2.setOpts(x=self.xdict.keys(), height=[1*self.model.camerasIA.getSelectedIARef().IA.x,1*self.model.camerasIA.getSelectedIARef().IA.y], width=1)
		#print self.model.cam.getX('S02-CAM-02')
		self.bg2.setOpts(x=self.xdict.keys(), height=[1*self.model.cam.getX('S02-CAM-02')-self.view.doubleSpinBox_x_2.value(),0])
		#self.bg2_target.setOpts(x=self.xdict.keys(), height=[self.view.doubleSpinBox_x_2.value(),0])

		# not certain y-centre=15 mm?
		self.bg2_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.cam.getY('S02-CAM-02')-15])
		self.bg3.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV('S02-BPM02')-self.view.doubleSpinBox_x_1.value(),0])
		#self.bg3_target.setOpts(x=self.xdict.keys(), height=[self.view.doubleSpinBox_x_1.value(),0])
		self.bg3_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.Cbpms.getYFromPV('S02-BPM02')])
		self.bg4.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV('C2V-BPM01')-self.view.doubleSpinBox_x_3.value(),0])
		#self.bg4_target.setOpts(x=self.xdict.keys(), height=[self.view.doubleSpinBox_x_3.value(),0])
		self.bg4_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.Cbpms.getYFromPV('C2V-BPM01')])

		self.sp.setData(self.model.dipCurrent, self.model.BPMPosition)
		self.sp2.setData(self.model.dipCurrent2, self.model.BPMPosition2)
		self.sp3.setData(self.model.dipCurrent3, self.model.BPMPosition3)

		#self.sp.setData(x,y)
		self.dCurve.setData(x=self.model.dCurrents,y=self.model.dPositions)
		self.fCurve.setData(x=self.model.fCurrents,y=self.model.fPositions)
		self.displayDisp.setText('DISPERSION:<br>'+str(self.model.Dispersion)+' m/A')
		self.displayMom_S.setText('MOMENTUM SPREAD:<br>'+str(self.model.pSpread)+' MeV/c')

		#self.view.label_H_1.setNum(self.model.Cbpms.getXFromPV('S02-BPM02')-self.view.doubleSpinBox_x_1.value())
		if len(self.model.Cbpms.getBPMXPVBuffer('S02-BPM02')) > 0:
			self.view.label_H_1.setNum(np.mean(self.model.Cbpms.getBPMXPVBuffer('S02-BPM02'))-self.view.doubleSpinBox_x_1.value())
		else:
			self.view.label_H_1.setNum(self.model.Cbpms.getXFromPV('S02-BPM02')-self.view.doubleSpinBox_x_1.value())

		self.view.label_H_2.setNum(self.model.cam.getX('S02-CAM-02')-self.view.doubleSpinBox_x_2.value())
		#if (self.cam.getX('S02-CAM-02')-self.view.doubleSpinBox_x_2.value()) < self.view.doubleSpinBox_tol_2.value():
		#	self.view.label_H_2.setOpt()

		#self.view.label_H_3.setNum(self.model.Cbpms.getXFromPV('C2V-BPM01')-self.view.doubleSpinBox_x_3.value())
		if len(self.model.Cbpms.getBPMXPVBuffer('C2V-BPM01')) > 0:
			self.view.label_H_3.setNum(np.mean(self.model.Cbpms.getBPMXPVBuffer('C2V-BPM01'))-self.view.doubleSpinBox_x_3.value())
		else:
			self.view.label_H_3.setNum(self.model.Cbpms.getXFromPV('C2V-BPM01')-self.view.doubleSpinBox_x_3.value())

		if len(self.model.Cbpms.getBPMXPVBuffer('C2V-BPM01')) > 0:
			self.view.label_H_4.setNum(np.mean(self.model.Cbpms.getBPMXPVBuffer('C2V-BPM01'))-self.view.doubleSpinBox_x_4.value())
		else:
			self.view.label_H_4.setNum(self.model.Cbpms.getXFromPV('C2V-BPM01')-self.view.doubleSpinBox_x_4.value())
	# def refreshImage(self):
	# 	 #image = np.random.normal(size=(2560,2160))
	# 	 cap = cv2.VideoCapture("http://192.168.83.31:7080/MJPG1.mjpg")
	# 	 #print cap
	# 	 _,frame = cap.read()
	# 	 self.YAGImage.setImage(np.flip(np.transpose(frame[:,:,0]),1))

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
