from PyQt4 import QtGui, QtCore

import sys
import time
import threads
import numpy as np
import pyqtgraph as pg
import epics
from epics import caget,caput


class Controller():

	def __init__(self, view, model):
		self.view = view
		self.model = model
		self.threads = threads
		#MONITOR SET UP FOR ALL DATA STREAMS ON MONITOR
		self.MONITOR = self.view.glayoutMonitor.addPlot()
		self.quad01Curve = self.MONITOR.plot(pen='c')
		self.text1 = pg.TextItem('QUAD 01', border='c')
		self.quad02Curve = self.MONITOR.plot(pen='g')
		self.text2 = pg.TextItem('QUAD 02', border='g')
		self.quad03Curve = self.MONITOR.plot(pen='w')
		self.text3 = pg.TextItem('QUAD 03', border='w')
		self.quad04Curve = self.MONITOR.plot(pen='m')
		self.text4 = pg.TextItem('QUAD 04', border='m')
		self.quad07Curve = self.MONITOR.plot(pen='b')
		self.text7 = pg.TextItem('QUAD 07', border='b')
		self.quad08Curve = self.MONITOR.plot(pen='r')
		self.text8 = pg.TextItem('QUAD 08', border='r')
		self.quad09Curve = self.MONITOR.plot(pen='y')
		self.text9 = pg.TextItem('QUAD 09', border='y')

		self.text10 = pg.TextItem('BPM1', border='w')
		self.text11 = pg.TextItem('BPM2', border='w')
		self.text12 = pg.TextItem('BPM4', border='w')
		self.text13 = pg.TextItem('BPM5', border='w')
		#ADD LINES AND TEXT TO PLOT
		self.MONITOR.addItem(self.quad01Curve)
		self.MONITOR.addItem(self.quad02Curve)
		self.MONITOR.addItem(self.quad03Curve)
		self.MONITOR.addItem(self.quad04Curve)
		self.MONITOR.addItem(self.quad07Curve)
		self.MONITOR.addItem(self.quad08Curve)
		self.MONITOR.addItem(self.quad09Curve)
		self.MONITOR.addItem(self.text1)
		self.MONITOR.addItem(self.text2)
		self.MONITOR.addItem(self.text3)
		self.MONITOR.addItem(self.text4)
		self.MONITOR.addItem(self.text7)
		self.MONITOR.addItem(self.text8)
		self.MONITOR.addItem(self.text9)
		#ARRAYS FOR DATA STREAMS
		self.q1Monitor = []
		self.q2Monitor = []
		self.q3Monitor = []
		self.q4Monitor = []
		self.q7Monitor = []
		self.q8Monitor = []
		self.q9Monitor = []
		#INITATE MONITOR
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.updateMonitor)
		self.timer.timeout.connect(self.updateOutput)
		self.timer.start(10)

		#OUTPUT MONITOR
		pg.setConfigOptions(antialias=True)
		self.viewYAG01 = self.view.glayoutOutput.addPlot(title="YAG-01")
		self.YAG01Distrib =  self.viewYAG01.plot(pen=None,symbol='o',symbolPen=None, symbolBrush=pg.mkBrush(255, 255, 255, 120))
		#pen=None,brush=pg.mkBrush(255, 255, 255, 120)
		self.viewYAG02 = self.view.glayoutOutput.addPlot(title="YAG-02")
		self.YAG02Distrib = self.viewYAG02.plot(pen=None,symbol='o',symbolPen=None, symbolBrush=pg.mkBrush(255, 255, 255, 120))
		self.viewYAG03 = self.view.glayoutOutput.addPlot(title="YAG-03")
		self.YAG03Distrib = self.viewYAG03.plot(pen=None,symbol='o',symbolPen=None, symbolBrush=pg.mkBrush(255, 255, 255, 120))
		self.viewYAG05 = self.view.glayoutOutput.addPlot(title="YAG-05")
		self.YAG05Distrib = self.viewYAG05.plot(pen=None,symbol='o',symbolPen=None, symbolBrush=pg.mkBrush(255, 255, 255, 120))
		self.view.glayoutOutput.nextRow()
		self.viewYAG06 = self.view.glayoutOutput.addPlot(title="YAG-06")
		self.YAG06Distrib = self.viewYAG06.plot(pen=None,symbol='o',symbolPen=None, symbolBrush=pg.mkBrush(255, 255, 255, 120))
		self.viewYAG07 = self.view.glayoutOutput.addPlot(title="YAG-07")
		self.YAG07Distrib = self.viewYAG07.plot(pen=None,symbol='o',symbolPen=None, symbolBrush=pg.mkBrush(255, 255, 255, 120))
		self.viewYAG08 = self.view.glayoutOutput.addPlot(title="YAG-08")
		self.YAG08Distrib = self.viewYAG08.plot(pen=None,symbol='o',symbolPen=None, symbolBrush=pg.mkBrush(255, 255, 255, 120))
		self.viewBPMS = self.view.glayoutOutput.addPlot(title="BPMs")
		self.BPM1marker = self.viewBPMS.plot(pen=None,symbol='+',symbolPen=None, symbolBrush=pg.mkBrush(255, 255, 255, 120))
		self.viewBPMS.addItem(self.text10)
		self.viewBPMS.addItem(self.text11)
		self.viewBPMS.addItem(self.text12)
		self.viewBPMS.addItem(self.text13)
		#QtGui.QApplication.instance().exec_()

		self.thread = self.threads.runASTRAThread(self.view, self.model)
		#connecttions
		self.view.runASTRA_Btn.clicked.connect(self.startSimulation)
		self.view.setVirtualMachine_Btn.clicked.connect(self.model.setVM)

	def startSimulation(self):

		self.thread.start()

	def updateOutput(self):
		if self.model.updateOutput==1:
			x=[]
			y=[]
			x.append(self.model.bpms.getXFromPV('BPM01'))
			y.append(self.model.bpms.getYFromPV('BPM01'))
			x.append(self.model.bpms.getXFromPV('BPM02'))
			y.append(self.model.bpms.getYFromPV('BPM02'))
			x.append(self.model.bpms.getXFromPV('BPM04'))
			y.append(self.model.bpms.getYFromPV('BPM04'))
			x.append(self.model.bpms.getXFromPV('BPM05'))
			y.append(self.model.bpms.getYFromPV('BPM05'))

			self.text10.setPos(x[0], y[0])
			self.text11.setPos(x[1], y[1])
			self.text12.setPos(x[2], y[2])
			self.text13.setPos(x[3], y[3])

			self.BPM1marker.setData(x,y)
			#self.viewBPMS.setXRange(3*min(x),3*max(x))
			#self.viewBPMS.setYRange(3*min(y),3*max(y))
			#print(caget('VM-EBT-INJ-DIA-CAM-02:CAM:DistribX'))
			#print(caget('VM-EBT-INJ-DIA-CAM-02:CAM:DistribY'))


			min_rot = 3*min(caget('VM-EBT-INJ-DIA-CAM-02:CAM:DistribX'))
			max_rot = 3*max(caget('VM-EBT-INJ-DIA-CAM-02:CAM:DistribX'))
			self.YAG01Distrib.setData(caget('VM-EBT-INJ-DIA-CAM-02:CAM:DistribX'),caget('VM-EBT-INJ-DIA-CAM-02:CAM:DistribY'))
			self.YAG02Distrib.setData(caget('VM-EBT-INJ-DIA-CAM-03:CAM:DistribX'),caget('VM-EBT-INJ-DIA-CAM-03:CAM:DistribY'))
			self.YAG03Distrib.setData(caget('VM-EBT-INJ-DIA-CAM-04:CAM:DistribX'),caget('VM-EBT-INJ-DIA-CAM-04:CAM:DistribY'))
			self.YAG05Distrib.setData(caget('VM-EBT-INJ-DIA-CAM-06:CAM:DistribX'),caget('VM-EBT-INJ-DIA-CAM-06:CAM:DistribY'))
			self.YAG06Distrib.setData(caget('VM-EBT-INJ-DIA-CAM-07:CAM:DistribX'),caget('VM-EBT-INJ-DIA-CAM-07:CAM:DistribY'))
			self.YAG07Distrib.setData(caget('VM-EBT-INJ-DIA-CAM-08:CAM:DistribX'),caget('VM-EBT-INJ-DIA-CAM-08:CAM:DistribY'))
			self.YAG08Distrib.setData(caget('VM-EBT-INJ-DIA-CAM-10:CAM:DistribX'),caget('VM-EBT-INJ-DIA-CAM-10:CAM:DistribY'))
			self.viewYAG01.setXRange(min_rot,max_rot)
			self.viewYAG01.setYRange(min_rot,max_rot)
			self.viewYAG02.setXRange(min_rot,max_rot)
			self.viewYAG02.setYRange(min_rot,max_rot)
			self.viewYAG03.setXRange(min_rot,max_rot)
			self.viewYAG03.setYRange(min_rot,max_rot)
			self.viewYAG05.setXRange(min_rot,max_rot)
			self.viewYAG05.setYRange(min_rot,max_rot)
			self.viewYAG06.setXRange(min_rot,max_rot)
			self.viewYAG06.setYRange(min_rot,max_rot)
			self.viewYAG07.setXRange(min_rot,max_rot)
			self.viewYAG07.setYRange(min_rot,max_rot)
			self.viewYAG08.setXRange(min_rot,max_rot)
			self.viewYAG08.setYRange(min_rot,max_rot)


	def updateMonitor(self):
		#ADD DATA HERE
		self.q1Monitor.append(self.model.magnets.getRI('QUAD01'))
		self.q2Monitor.append(self.model.magnets.getRI('QUAD02'))
		self.q3Monitor.append(self.model.magnets.getRI('QUAD03'))
		self.q4Monitor.append(self.model.magnets.getRI('QUAD04'))
		self.q7Monitor.append(self.model.magnets.getRI('QUAD07'))
		self.q8Monitor.append(self.model.magnets.getRI('QUAD08'))
		self.q9Monitor.append(self.model.magnets.getRI('QUAD09'))
		if len(self.q1Monitor)==1001:#REMOVE DATA IF GETTING TOO BIG ( > 1000 point)
			self.text1.setPos(100, max(self.q1Monitor))
			self.text2.setPos(200, max(self.q2Monitor))
			self.text3.setPos(300, max(self.q3Monitor))
			self.text4.setPos(400, max(self.q4Monitor))
			self.text7.setPos(500, max(self.q7Monitor))
			self.text8.setPos(600, max(self.q8Monitor))
			self.text9.setPos(700, max(self.q9Monitor))

			self.q1Monitor.pop(0)
			self.q2Monitor.pop(0)
			self.q3Monitor.pop(0)
			self.q4Monitor.pop(0)
			self.q7Monitor.pop(0)
			self.q8Monitor.pop(0)
			self.q9Monitor.pop(0)

		self.quad01Curve.setData(self.q1Monitor)
		self.quad02Curve.setData(self.q2Monitor)
		self.quad03Curve.setData(self.q3Monitor)
		self.quad04Curve.setData(self.q4Monitor)
		self.quad07Curve.setData(self.q7Monitor)
		self.quad08Curve.setData(self.q8Monitor)
		self.quad09Curve.setData(self.q9Monitor)

		self.MONITOR.enableAutoRange('xy', True)  ## stop auto-scaling after the first data set is plotted
