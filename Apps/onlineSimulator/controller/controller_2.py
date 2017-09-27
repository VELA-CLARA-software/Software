from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys,os
import time
import numpy as np
import pyqtgraph as pg
from epics import caget,caput
class Controller():

	def __init__(self, view, model):
		'''define model and view'''
		self.view = view
		self.model = model
		'''1 Sky Line V1 Monitors'''
		V1Monitor = pg.GraphicsView()
		V1Layout = pg.GraphicsLayout(border=(100,100,100))
		V1Monitor.setCentralItem(V1Layout)
		self.V1Title = V1Layout.addLabel('V1 Line')
		V1Layout.nextRow()
		self.V1_xdict = {0:'BPM01', 1:'YAG01', 2:'YAG02', 3:'YAG03', 4:'BPM02'}
		self.V1_SL_x = V1Layout.addPlot(title="X (mm)")
		self.V1_SL_x.axes['bottom']['item'].setTicks([self.V1_xdict.items()])
		self.V1_x = pg.BarGraphItem(x=self.V1_xdict.keys(), height=[0,0,0,0,0], width=1)
		self.V1_SL_x.addItem(self.V1_x)
		V1Layout.nextRow()
		self.V1_SL_y = V1Layout.addPlot(title="Y (mm)")
		self.V1_SL_y.axes['bottom']['item'].setTicks([self.V1_xdict.items()])
		self.V1_y = pg.BarGraphItem(x=self.V1_xdict.keys(), height=[0,0,0,0,0], width=1)
		self.V1_SL_y.addItem(self.V1_y)
		V1Layout.nextRow()
		self.V1_SL_sx= V1Layout.addPlot(title="Sigma X (mm)")
		self.V1_SL_sx.axes['bottom']['item'].setTicks([self.V1_xdict.items()])
		self.V1_sx = pg.BarGraphItem(x=self.V1_xdict.keys(), height=[0,0,0,0,0], width=1)
		self.V1_SL_sx.addItem(self.V1_sx)
		V1Layout.nextRow()
		self.V1_SL_sy= V1Layout.addPlot(title="Sigma Y (mm)")
		self.V1_SL_sy.axes['bottom']['item'].setTicks([self.V1_xdict.items()])
		self.V1_sy = pg.BarGraphItem(x=self.V1_xdict.keys(), height=[0,0,0,0,0], width=1)
		self.V1_SL_sy.addItem(self.V1_sy)

		'''2 Sky Line V2 Monitors'''
		V2Monitor = pg.GraphicsView()
		V2Layout = pg.GraphicsLayout(border=(100,100,100))
		V2Monitor.setCentralItem(V2Layout)
		self.V2Title = V2Layout.addLabel('V2 Line')
		V2Layout.nextRow()
		self.V2_xdict = {0:'YAG05', 1:'YAG06', 2:'BPM04', 3:'YAG07', 4:'BPM05', 5:'YAG08'}
		self.V2_SL_x = V2Layout.addPlot(title="X (mm)")
		self.V2_SL_x.axes['bottom']['item'].setTicks([self.V2_xdict.items()])
		self.V2_x = pg.BarGraphItem(x=self.V2_xdict.keys(), height=[0,0,0,0,0,0], width=1)
		self.V2_SL_x.addItem(self.V2_x)
		V2Layout.nextRow()
		self.V2_SL_y = V2Layout.addPlot(title="Y (mm)")
		self.V2_SL_y.axes['bottom']['item'].setTicks([self.V2_xdict.items()])
		self.V2_y = pg.BarGraphItem(x=self.V2_xdict.keys(), height=[0,0,0,0,0,0], width=1)
		self.V2_SL_y.addItem(self.V2_y)
		V2Layout.nextRow()
		self.V2_SL_sx= V2Layout.addPlot(title="Sigma X (mm)")
		self.V2_SL_sx.axes['bottom']['item'].setTicks([self.V2_xdict.items()])
		self.V2_sx = pg.BarGraphItem(x=self.V2_xdict.keys(), height=[0,0,0,0,0,0], width=1)
		self.V2_SL_sx.addItem(self.V2_sx)
		V2Layout.nextRow()
		self.V2_SL_sy= V2Layout.addPlot(title="Sigma Y (mm)")
		self.V2_SL_sy.axes['bottom']['item'].setTicks([self.V2_xdict.items()])
		self.V2_sy = pg.BarGraphItem(x=self.V2_xdict.keys(), height=[0,0,0,0,0,0], width=1)
		self.V2_SL_sy.addItem(self.V2_sy)

		'''3 Sky Line SP Monitors'''
		SPMonitor = pg.GraphicsView()
		SPLayout = pg.GraphicsLayout(border=(100,100,100))
		SPMonitor.setCentralItem(SPLayout)
		self.SPTitle = SPLayout.addLabel('SP Line')
		SPLayout.nextRow()
		self.SP_xdict = {0:'BPM03', 1:'YAG04'}
		self.SP_SL_x = SPLayout.addPlot(title="X (mm)")
		self.SP_SL_x.axes['bottom']['item'].setTicks([self.SP_xdict.items()])
		self.SP_x = pg.BarGraphItem(x=self.SP_xdict.keys(), height=[0,0], width=1)
		self.SP_SL_x.addItem(self.SP_x)
		SPLayout.nextRow()
		self.SP_SL_y = SPLayout.addPlot(title="Y (mm)")
		self.SP_SL_y.axes['bottom']['item'].setTicks([self.SP_xdict.items()])
		self.SP_y = pg.BarGraphItem(x=self.SP_xdict.keys(), height=[0,0], width=1)
		self.SP_SL_y.addItem(self.SP_y)
		SPLayout.nextRow()
		self.SP_SL_sx= SPLayout.addPlot(title="Sigma X (mm)")
		self.SP_SL_sx.axes['bottom']['item'].setTicks([self.SP_xdict.items()])
		self.SP_sx = pg.BarGraphItem(x=self.SP_xdict.keys(), height=[0,0], width=1)
		self.SP_SL_sx.addItem(self.SP_sx)
		SPLayout.nextRow()
		self.SP_SL_sy= SPLayout.addPlot(title="Sigma Y (mm)")
		self.SP_SL_sy.axes['bottom']['item'].setTicks([self.SP_xdict.items()])
		self.SP_sy = pg.BarGraphItem(x=self.SP_xdict.keys(), height=[0,0], width=1)
		self.SP_SL_sy.addItem(self.SP_sy)

		'''4 Sky Line CV Monitors'''
		CVMonitor = pg.GraphicsView()
		CVLayout = pg.GraphicsLayout(border=(100,100,100))
		CVMonitor.setCentralItem(CVLayout)
		self.CVTitle = CVLayout.addLabel('CV Line')
		CVLayout.nextRow()
		self.CV_xdict = {0:'CV-BPM01', 1:'CV-YAG01'}
		self.CV_SL_x = CVLayout.addPlot(title="X (mm)")
		self.CV_SL_x.axes['bottom']['item'].setTicks([self.CV_xdict.items()])
		self.CV_x = pg.BarGraphItem(x=self.CV_xdict.keys(), height=[0,0], width=1)
		self.CV_SL_x.addItem(self.CV_x)
		CVLayout.nextRow()
		self.CV_SL_y = CVLayout.addPlot(title="Y (mm)")
		self.CV_SL_y.axes['bottom']['item'].setTicks([self.SP_xdict.items()])
		self.CV_y = pg.BarGraphItem(x=self.CV_xdict.keys(), height=[0,0], width=1)
		self.CV_SL_y.addItem(self.CV_y)
		CVLayout.nextRow()
		self.CV_SL_sx= CVLayout.addPlot(title="Sigma X (mm)")
		self.CV_SL_sx.axes['bottom']['item'].setTicks([self.CV_xdict.items()])
		self.CV_sx = pg.BarGraphItem(x=self.CV_xdict.keys(), height=[0,0], width=1)
		self.CV_SL_sx.addItem(self.CV_sx)
		CVLayout.nextRow()
		self.CV_SL_sy= CVLayout.addPlot(title="Sigma Y (mm)")
		self.CV_SL_sy.axes['bottom']['item'].setTicks([self.CV_xdict.items()])
		self.CV_sy = pg.BarGraphItem(x=self.CV_xdict.keys(), height=[0,0], width=1)
		self.CV_SL_sy.addItem(self.CV_sy)

		'''5 Sky Line C1 Monitors'''
		C1Monitor = pg.GraphicsView()
		C1Layout = pg.GraphicsLayout(border=(100,100,100))
		C1Monitor.setCentralItem(C1Layout)
		self.C1Title = C1Layout.addLabel('C1 Line')
		C1Layout.nextRow()
		self.C1_xdict = {0:'S01-BPM01', 1:'S01-YAG01', 2:'S02-BPM01', 3:'S02-YAG01', 4:'S02-YAG02'}#, 5:'C1-S02-BPM02', 6:'C1-S02-YAG03'}
		self.C1_SL_x = C1Layout.addPlot(title="X (mm)")
		self.C1_SL_x.axes['bottom']['item'].setTicks([self.C1_xdict.items()])
		self.C1_x = pg.BarGraphItem(x=self.C1_xdict.keys(), height=[0,0,0,0,0], width=1)
		self.C1_SL_x.addItem(self.C1_x)
		C1Layout.nextRow()
		self.C1_SL_y = C1Layout.addPlot(title="Y (mm)")
		self.C1_SL_y.axes['bottom']['item'].setTicks([self.C1_xdict.items()])
		self.C1_y = pg.BarGraphItem(x=self.C1_xdict.keys(), height=[0,0,0,0,0], width=1)
		self.C1_SL_y.addItem(self.C1_y)
		C1Layout.nextRow()
		self.C1_SL_sx= C1Layout.addPlot(title="Sigma X (mm)")
		self.C1_SL_sx.axes['bottom']['item'].setTicks([self.C1_xdict.items()])
		self.C1_sx = pg.BarGraphItem(x=self.C1_xdict.keys(), height=[0,0,0,0,0], width=1)
		self.C1_SL_sx.addItem(self.C1_sx)
		C1Layout.nextRow()
		self.C1_SL_sy= C1Layout.addPlot(title="Sigma Y (mm)")
		self.C1_SL_sy.axes['bottom']['item'].setTicks([self.C1_xdict.items()])
		self.C1_sy = pg.BarGraphItem(x=self.C1_xdict.keys(), height=[0,0,0,0,0], width=1)
		self.C1_SL_sy.addItem(self.C1_sy)

		self.view.gridLayout_sky.addWidget(C1Monitor,0,0,1,2)
		self.view.gridLayout_sky.addWidget(CVMonitor,0,2,1,1)
		self.view.gridLayout_sky.addWidget(V1Monitor,1,0,1,1)
		self.view.gridLayout_sky.addWidget(V2Monitor,1,2,1,1)
		self.view.gridLayout_sky.addWidget(SPMonitor,1,1,1,1)
		'''Threads for updating graphs and labels'''
		self.timer = QTimer()
		self.timer.timeout.connect(self.updateDisplays)
		self.timer.start(500)

		self.view.pushButton.clicked.connect(self.model.run)

	def updateDisplays(self):
		if self.model.ASTRA.isRunning():
			self.view.label_95.setText('Status: Running...')
		else:
			self.view.label_95.setText('Status: Ready')
		self.V1_x.setOpts(x=self.V1_xdict.keys(), height=[1000*self.model.bpms.getXFromPV('BPM01'),
													1000*caget('VM-EBT-INJ-DIA-CAM-02:CAM:X'),
													1000*caget('VM-EBT-INJ-DIA-CAM-03:CAM:X'),
													1000*caget('VM-EBT-INJ-DIA-CAM-04:CAM:X'),
													1000*self.model.bpms.getXFromPV('BPM02')], width=1)# replace the random generators with  bpm x read offs
		self.V1_y.setOpts(x=self.V1_xdict.keys(), height=[1000*self.model.bpms.getYFromPV('BPM01'),
													1000*caget('VM-EBT-INJ-DIA-CAM-02:CAM:Y'),
													1000*caget('VM-EBT-INJ-DIA-CAM-03:CAM:Y'),
													1000*caget('VM-EBT-INJ-DIA-CAM-04:CAM:Y'),
													1000*self.model.bpms.getYFromPV('BPM02')], width=1)
		self.V1_sx.setOpts(x=self.V1_xdict.keys(), height=[0,
													1000*caget('VM-EBT-INJ-DIA-CAM-02:CAM:SigmaX'),
													1000*caget('VM-EBT-INJ-DIA-CAM-03:CAM:SigmaX'),
													1000*caget('VM-EBT-INJ-DIA-CAM-04:CAM:SigmaX'),
													0], width=1)
		self.V1_sy.setOpts(x=self.V1_xdict.keys(), height=[0,
													1000*caget('VM-EBT-INJ-DIA-CAM-02:CAM:SigmaY'),
													1000*caget('VM-EBT-INJ-DIA-CAM-03:CAM:SigmaY'),
													1000*caget('VM-EBT-INJ-DIA-CAM-04:CAM:SigmaY'),
													0], width=1)

		self.V2_x.setOpts(x=self.V2_xdict.keys(), height=[1000*caget('VM-EBT-INJ-DIA-CAM-06:CAM:X'),
														1000*caget('VM-EBT-INJ-DIA-CAM-07:CAM:X'),
														1000*self.model.bpms.getXFromPV('BPM04'),
														1000*caget('VM-EBT-INJ-DIA-CAM-08:CAM:X'),
														1000*self.model.bpms.getXFromPV('BPM05'),
														1000*caget('VM-EBT-INJ-DIA-CAM-09:CAM:X')], width=1)

		self.V2_y.setOpts(x=self.V2_xdict.keys(), height=[1000*caget('VM-EBT-INJ-DIA-CAM-06:CAM:Y'),
														1000*caget('VM-EBT-INJ-DIA-CAM-07:CAM:Y'),
														1000*self.model.bpms.getYFromPV('BPM04'),
														1000*caget('VM-EBT-INJ-DIA-CAM-08:CAM:Y'),
														1000*self.model.bpms.getYFromPV('BPM05'),
														1000*caget('VM-EBT-INJ-DIA-CAM-09:CAM:Y')], width=1)

		self.V2_sx.setOpts(x=self.V2_xdict.keys(), height=[1000*caget('VM-EBT-INJ-DIA-CAM-06:CAM:SigmaX'),
														1000*caget('VM-EBT-INJ-DIA-CAM-07:CAM:SigmaX'),
														0,
														1000*caget('VM-EBT-INJ-DIA-CAM-08:CAM:SigmaX'),
														0,
														1000*caget('VM-EBT-INJ-DIA-CAM-09:CAM:SigmaX')], width=1)

		self.V2_sy.setOpts(x=self.V2_xdict.keys(), height=[1000*caget('VM-EBT-INJ-DIA-CAM-06:CAM:SigmaY'),
														1000*caget('VM-EBT-INJ-DIA-CAM-07:CAM:SigmaY'),
														0,
														1000*caget('VM-EBT-INJ-DIA-CAM-08:CAM:SigmaY'),
														0,
														1000*caget('VM-EBT-INJ-DIA-CAM-09:CAM:SigmaY')], width=1)

		self.SP_x.setOpts(x=self.SP_xdict.keys(), height=[1000*self.model.bpms.getXFromPV('BPM03'),
														1000*caget('VM-EBT-INJ-DIA-CAM-05:CAM:X')], width=1)
		self.SP_y.setOpts(x=self.SP_xdict.keys(), height=[1000*self.model.bpms.getYFromPV('BPM03'),
														1000*caget('VM-EBT-INJ-DIA-CAM-05:CAM:Y')], width=1)
		self.SP_sx.setOpts(x=self.SP_xdict.keys(), height=[0,
														1000*caget('VM-EBT-INJ-DIA-CAM-05:CAM:SigmaX')], width=1)
		self.SP_sy.setOpts(x=self.SP_xdict.keys(), height=[0,
														1000*caget('VM-EBT-INJ-DIA-CAM-05:CAM:SigmaY')], width=1)

		self.CV_x.setOpts(x=self.SP_xdict.keys(), height=[1000*caget('VM-CLA-C2V-DIA-BPM-01:X'),
														1000*caget('VM-CLA-C2V-DIA-CAM-01:X')], width=1)
		self.CV_y.setOpts(x=self.SP_xdict.keys(), height=[1000*caget('VM-CLA-C2V-DIA-BPM-01:Y'),
														1000*caget('VM-CLA-C2V-DIA-CAM-01:Y')], width=1)
		self.CV_sx.setOpts(x=self.SP_xdict.keys(), height=[0,
														1000*caget('VM-CLA-C2V-DIA-CAM-01:SigmaX')], width=1)
		self.CV_sy.setOpts(x=self.SP_xdict.keys(), height=[0,
														1000*caget('VM-CLA-C2V-DIA-CAM-01:SigmaY')], width=1)

		self.C1_x.setOpts(x=self.C1_xdict.keys(), height=[1000*caget('VM-CLA-S01-DIA-BPM-01:X'),
														1000*caget('VM-CLA-S01-DIA-CAM-01:X'),
														1000*caget('VM-CLA-S02-DIA-BPM-01:X'),
														1000*caget('VM-CLA-S02-DIA-CAM-01:X'),
														1000*caget('VM-CLA-S02-DIA-CAM-02:X')], width=1)
		self.C1_y.setOpts(x=self.C1_xdict.keys(), height=[1000*caget('VM-CLA-S01-DIA-BPM-01:Y'),
														1000*caget('VM-CLA-S01-DIA-CAM-01:Y'),
														1000*caget('VM-CLA-S02-DIA-BPM-01:Y'),
														1000*caget('VM-CLA-S02-DIA-CAM-01:Y'),
														1000*caget('VM-CLA-S02-DIA-CAM-02:Y')], width=1)
		self.C1_sx.setOpts(x=self.C1_xdict.keys(), height=[0,
														1000*caget('VM-CLA-S01-DIA-CAM-01:SigmaX'),
														0,
														1000*caget('VM-CLA-S02-DIA-CAM-01:SigmaX'),
														1000*caget('VM-CLA-S02-DIA-CAM-02:SigmaX')], width=1)
		self.C1_sy.setOpts(x=self.C1_xdict.keys(), height=[0,
														1000*caget('VM-CLA-S01-DIA-CAM-01:SigmaY'),
														0,
														1000*caget('VM-CLA-S02-DIA-CAM-01:SigmaY'),
														1000*caget('VM-CLA-S02-DIA-CAM-02:SigmaY')], width=1)
