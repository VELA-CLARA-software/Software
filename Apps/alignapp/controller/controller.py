from PyQt4 import QtGui, QtCore

import sys
import time
import numpy as np
import pyqtgraph as pg
from epics import caget,caput
#C:\Users\wln24624\Documents\SOFTWARE\Striptool
#sys.path.append('C:\\Users\\wln24624\\Documents\\SOFTWARE\\Striptool')
#sys.path.append('C:\\Users\\wln24624\\Documents\\SOFTWARE\\VELA-CLARA-Software\\Software\\Striptool\\')
sys.path.append('C:\\Users\\fj38.CLRC\\Documents\\work\\programs\\python\\githubstuff\\Software-master\\Software-master\\Striptool')
import striptool as st1
import striptool as st2
import striptool as st3

#def frankfn():
# return self.model.magnets.getRI('QUAD02')

class Controller():

	def __init__(self, view, model):
#                def frankfn():
#                 return self.model.magnets.getRI('QUAD02')
		self.view = view
		self.model = model
		vcsp = st1.stripPlot(self.view.groupBox)
#		vcsp = st1.stripPlot()
 #               self.view.groupBox.addWidget(vcsp)
		vcsp.setDecimateLength(10000)
		#vcsp.setGeometry(QtCore.QRect(5, 5, 600, 500))
		vcsp.addSignal(name='QUAD02',pen='r', timer=1.0/100.0, function=lambda: self.model.magnets.getRI('QUAD02'))
#                print "QUAD 02 value is." %  self.model.magnets.getRI('QUAD02') 
#                vcsp.addSignal(name='QUAD02',pen='r', timer=1.0/100.0, function=lambda: frankfn())
		vcsp.start()


                self.timer = QtCore.QTimer()
                self.timer.timeout.connect(self.updateDisplays)
                self.timer.start(500)

                self.view.Mag_PSU_State_Button_3.setText(str(self.model.laser.getHpos()))
                self.view.Mag_PSU_State_Button_3.clicked.connect(lambda: self.model.laser.setHpos(self.view.SIValue_3.value()))


                self.view.autopushButton.clicked.connect(self.model.correctorbit)

                self.plot1wt = pg.GraphicsLayoutWidget(self.view.groupBox_3)
                self.plot1 = self.plot1wt.addPlot()
                self.view.wlayout.addWidget(self.plot1wt)

                self.YAG01dist = self.plot1.plot(pen=None,symbol='o',symbolPen=None, symbolBrush=pg.mkBrush(255, 255, 255, 120))
#                self.YAG01dist.setData(caget('VM-EBT-INJ-DIA-CAM-02:CAM:DistribX'),caget('VM-EBT-INJ-DIA-CAM-02:CAM:DistribY'))

#                print 'Getting screen data', caget('VM-EBT-INJ-DIA-CAM-02:CAM:DistribX')

#		self.view.groupBox_3.addPlot(title="YAG-01")


#		self.YAG01Distrib =  self.viewYAG01.plot(pen=None,symbol='o',symbolPen=None, symbolBrush=pg.mkBrush(255, 255, 255, 120))
#               self.YAG01Distrib.setData(caget('VM-EBT-INJ-DIA-CAM-02:CAM:DistribX'),caget('VM-EBT-INJ-DIA-CAM-02:CAM:DistribY'))

#		self.viewYAG01 = self.view.glayoutOutput.addPlot(title="YAG-01")
#		self.YAG01Distrib =  self.viewYAG01.plot(pen=None,symbol='o',symbolPen=None, symbolBrush=pg.mkBrush(255, 255, 255, 120))
#                self.YAG01Distrib.setData(caget('VM-EBT-INJ-DIA-CAM-02:CAM:DistribX'),caget('VM-EBT-INJ-DIA-CAM-02:CAM:DistribY'))


		#vcsp.setPlotScale(50)

#		bpmsp = st2.stripPlot(self.view.groupBox_2)
#		bpmsp.setDecimateLength(10000)
#		#bpmsp.setGeometry(QtCore.QRect(5, 5, 600, 500))
#		#bpmsp.addSignal(name='QUAD01',pen='r', timer=1.0/100.0, function=lambda: self.model.magnets.getRI('QUAD01'))
#		bpmsp.start()
#		#bpmsp.setPlotScale(50)
#
#		yagsp = st3.stripPlot(self.view.groupBox_3)
#		yagsp.setDecimateLength(10000)
#		#yagsp.setGeometry(QtCore.QRect(5, 5, 600, 500))
#		#yagsp.addSignal(name='QUAD03',pen='r', timer=1.0/100.0, function=lambda: self.model.magnets.getRI('QUAD03'))
#		yagsp.start()
#		#yagsp.setPlotScale(50)
		print 'controller made'


        def updateDisplays(self):
                print "updating displays", self.model.laser.getHpos(), caget('VM-EBT-INJ-MAG-QUAD-02:RI')
                self.view.Mag_PSU_State_Button_3.setText(str(self.model.laser.getHpos()))
                self.YAG01dist.setData(caget('VM-EBT-INJ-DIA-CAM-02:CAM:DistribX'),caget('VM-EBT-INJ-DIA-CAM-02:CAM:DistribY'))

#        def addPlot(parent=None):
#                layout = QtGui.QVBoxLayout()
#                plotWidget = pg.GraphicsLayoutWidget(groupbox1)
#                plot = plotWidget.addPlot()
#                layout.addWidget(plotWidget)
#                parent.setLayout(layout)
#                return plot
