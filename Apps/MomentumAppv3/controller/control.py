from PyQt4 import QtCore
import pyqtgraph as pg
#from functools import partial
#import time
#from PyQt4.QtGui import QApplication

class Controller():
    def __init__(self, view, model, data):
        self.view = view
        self.model = model
        self.data = data
        self.C2Vbpm = self.model.C2Vbpm

        # Converter
        self.view.doubleSpinBox_I.valueChanged[float].connect(self.model.changeBox_p)
        self.view.doubleSpinBox_p.valueChanged[float].connect(self.model.changeBox_I)

        # Prediction
        self.view.pushButton_useCurrent.clicked.connect(self.model.useCurrent)
        self.view.pushButton_useRF.clicked.connect(self.model.useRF)
        self.view.doubleSpinBox_I_predict.valueChanged[float].connect(self.model.changeBox_p_predict)
        self.view.doubleSpinBox_p_predict.valueChanged[float].connect(self.model.changeBox_I_predict)

        # Rough measure
        self.data.values['rough_step'] = 0.1
        self.view.doubleSpinBox_step_1.setValue(self.data.values['rough_step'])
        self.view.doubleSpinBox_step_1.valueChanged[float].connect(self.model.setRoughStep)

        self.view.pushButton_get_p_rough.clicked.connect(self.model.get_p_rough)
        self.view.pushButton_roughGetCurrentRange.clicked.connect(self.model.roughGetCurrentRange)

        # Rough set
        self.view.doubleSpinBox_p_rough_set.valueChanged[float].connect(self.model.p_rough_set)

        self.data.values['rough_set_step'] = 100.0
        self.view.doubleSpinBox_step_2.setValue(self.data.values['rough_set_step'])
        self.view.doubleSpinBox_step_2.valueChanged[float].connect(self.model.setRoughSetStep)

        self.view.pushButton_select_gun.clicked.connect(self.model.select_gun)
        self.view.pushButton_select_linac.clicked.connect(self.model.select_linac)
        # Align
        self.view.pushButton_Align_2.clicked.connect(self.model.measureMomentumAlign_2)

        # Fine set
        self.view.doubleSpinBox_p_fine_set.valueChanged[float].connect(self.model.p_fine_set)

        self.data.values['fine_set_step'] = 100.0
        self.view.doubleSpinBox_step_3.setValue(self.data.values['fine_set_step'])
        self.view.doubleSpinBox_step_3.valueChanged[float].connect(self.model.setFineSetStep)

        self.view.pushButton_select_gun_2.clicked.connect(self.model.select_gun_fine)
        self.view.pushButton_select_linac_2.clicked.connect(self.model.select_linac_fine)

        '''Threads for updating graphs and labels'''
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateDisplays)
        self.timer.start(100)

        '''rough measure - C2V BPM plot'''
        monitor = pg.GraphicsView()
        layout = pg.GraphicsLayout()#border=(100,100,100))
        monitor.setCentralItem(layout)
        '''1.1 create graph for BPM Y and Y position monitoring'''
        self.xdict = {0:'X', 1:'Y'}
        #self.positionGraph_2 = layout.addPlot(title="S02-YAG02", labels = {'left': '&Delta; x [mm]'})
        self.positionGraph_1 = layout.addPlot(labels = {'left': '&Delta; x [mm]'})
        self.positionGraph_1.axes['bottom']['item'].setTicks([self.xdict.items()])
        self.positionGraph_1.setMouseEnabled(x=False, y=True)
        self.bgMin = -10
        self.bgMax = 10
        self.positionGraph_1.setYRange(self.bgMin,self.bgMax)
        barcolour1=(30,80,255)
        barcolour2=(5,40,12)
        barcolourt=(255,80,30)
        barwidth = 0.85
        barwidth2 = 1.0
        self.bg1 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour1, brush=barcolour1)
        self.bg1_y = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour2, brush=barcolour2)
        self.positionGraph_1.addItem(self.bg1)
        self.positionGraph_1.addItem(self.bg1_y)
        self.view.horizontalLayout.addWidget(monitor)

        '''rough set - C2V BPM plot'''
        monitor_2 = pg.GraphicsView()
        layout_2 = pg.GraphicsLayout()#border=(100,100,100))
        monitor_2.setCentralItem(layout_2)
        self.positionGraph_2 = layout_2.addPlot(labels = {'left': '&Delta; x [mm]'})
        self.positionGraph_2.axes['bottom']['item'].setTicks([self.xdict.items()])
        self.positionGraph_2.setMouseEnabled(x=False, y=True)
        self.positionGraph_2.setYRange(self.bgMin,self.bgMax)
        self.bg2 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour1, brush=barcolour1)
        self.bg2_y = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour2, brush=barcolour2)
        self.positionGraph_2.addItem(self.bg2)
        self.positionGraph_2.addItem(self.bg2_y)
        self.view.horizontalLayout_2.addWidget(monitor_2)

        '''rough measure - dipole scan plot'''
        monitor_3 = pg.GraphicsView()
        layout_3 = pg.GraphicsLayout()#border=(100,100,100))
        monitor_3.setCentralItem(layout_3)
        self.scanGraph = layout_3.addPlot(title = 'Rough dipole scan', colspan=3, labels = {'left': 'BPM x pos. [mm]', 'bottom': 'Dipole current [A]'})
        self.sp = pg.PlotDataItem()
        x=[0,1,2]
        y=[0,0,0]
        self.sp.setData(x,y)
        self.scanGraph.addItem(self.sp)
        self.view.horizontalLayout_3.addWidget(monitor_3)


        '''fine measure align - S02 BPM plot'''
        monitor_3 = pg.GraphicsView()
        layout_3 = pg.GraphicsLayout()#border=(100,100,100))
        monitor_3.setCentralItem(layout_3)
        self.positionGraph_3 = layout_3.addPlot(labels = {'left': '&Delta; x [mm]'})
        self.positionGraph_3.axes['bottom']['item'].setTicks([self.xdict.items()])
        self.positionGraph_3.setMouseEnabled(x=False, y=True)
        self.positionGraph_3.setYRange(self.bgMin,self.bgMax)
        self.bg3 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour1, brush=barcolour1)
        self.bg3_y = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour2, brush=barcolour2)
        self.positionGraph_3.addItem(self.bg3)
        self.positionGraph_3.addItem(self.bg3_y)
        self.view.horizontalLayout_4.addWidget(monitor_3)

        '''fine measure align - S02 YAG plot'''
        monitor_4 = pg.GraphicsView()
        layout_4 = pg.GraphicsLayout()#border=(100,100,100))
        monitor_4.setCentralItem(layout_4)
        self.positionGraph_4 = layout_4.addPlot(labels = {'left': '&Delta; x [mm]'})
        self.positionGraph_4.axes['bottom']['item'].setTicks([self.xdict.items()])
        self.positionGraph_4.setMouseEnabled(x=False, y=True)
        self.positionGraph_4.setYRange(self.bgMin,self.bgMax)
        self.bg4 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour1, brush=barcolour1)
        self.bg4_y = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour2, brush=barcolour2)
        self.positionGraph_4.addItem(self.bg4)
        self.positionGraph_4.addItem(self.bg4_y)
        self.view.horizontalLayout_5.addWidget(monitor_4)

        '''fine measure - C2V BPM plot'''
        monitor_5 = pg.GraphicsView()
        layout_5 = pg.GraphicsLayout()#border=(100,100,100))
        monitor_5.setCentralItem(layout_5)
        self.positionGraph_5 = layout_5.addPlot(labels = {'left': '&Delta; x [mm]'})
        self.positionGraph_5.axes['bottom']['item'].setTicks([self.xdict.items()])
        self.positionGraph_5.setMouseEnabled(x=False, y=True)
        self.positionGraph_5.setYRange(self.bgMin,self.bgMax)
        self.bg5 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour1, brush=barcolour1)
        self.bg5_y = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour2, brush=barcolour2)
        self.positionGraph_5.addItem(self.bg5)
        self.positionGraph_5.addItem(self.bg5_y)
        self.view.horizontalLayout_10.addWidget(monitor_5)

        '''fine set - C2V BPM plot'''
        monitor_6 = pg.GraphicsView()
        layout_6 = pg.GraphicsLayout()#border=(100,100,100))
        monitor_6.setCentralItem(layout_6)
        self.positionGraph_6 = layout_6.addPlot(labels = {'left': '&Delta; x [mm]'})
        self.positionGraph_6.axes['bottom']['item'].setTicks([self.xdict.items()])
        self.positionGraph_6.setMouseEnabled(x=False, y=True)
        self.positionGraph_6.setYRange(self.bgMin,self.bgMax)
        self.bg6 = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour1, brush=barcolour1)
        self.bg6_y = pg.BarGraphItem(x=self.xdict.keys(), height=[0.0,0.0], width=barwidth, pen=barcolour2, brush=barcolour2)
        self.positionGraph_6.addItem(self.bg6)
        self.positionGraph_6.addItem(self.bg6_y)
        self.view.horizontalLayout_11.addWidget(monitor_6)


    def updateDisplays(self):
        self.view.label_I.setText(
            self.model.dipole+'current = '+str(self.model.Cmagnets.getSI(self.model.dipole))+' A'
            +'\nC2V BPM x-position = '+str(self.model.Cbpms.getXFromPV(self.C2Vbpm))+' mm'
            +'\nGun set point = '+str(self.model.gun.getAmpSP())
            +'\nLinac set point = '+str(self.model.linac1.getAmpSP())
            +'\nIs linac timing set to on? = '+str(self.model.Linac01Timing.isLinacOn())
            )

        self.view.label_dipole_set.setText(str(self.model.Cmagnets.getSI(self.model.dipole)))

        # rough set
        self.view.label_I_rough.setText(str(self.model.Cmagnets.getSI(self.model.dipole)))

        try:
            if self.data.values['RFmode_rough'] == 'Gun':
                self.view.label_RF_rough.setText(str(self.model.gun.getAmpSP()))
            elif self.data.values['RFmode_rough'] == 'Linac':
                self.view.label_RF_rough.setText(str(self.model.linac1.getAmpSP()))
        except:
            self.view.label_RF_rough.setText('Mode not set')

        # fine set
        self.view.label_I_fine.setText(str(self.model.Cmagnets.getSI(self.model.dipole)))

        try:
            if self.data.values['RFmode_fine'] == 'Gun':
                self.view.label_RF_fine.setText(str(self.model.gun.getAmpSP()))
            elif self.data.values['RFmode_fine'] == 'Linac':
                self.view.label_RF_fine.setText(str(self.model.linac1.getAmpSP()))
        except:
            self.view.label_RF_rough.setText('Mode not set')


        # plots
        self.bg1.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV(self.C2Vbpm),0])
        self.bg1_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.Cbpms.getYFromPV(self.C2Vbpm)])
        self.bg2.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV(self.C2Vbpm),0])
        self.bg2_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.Cbpms.getYFromPV(self.C2Vbpm)])
        self.bg3.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV(self.C2Vbpm),0])
        self.bg3_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.Cbpms.getYFromPV(self.C2Vbpm)])
        self.bg4.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV(self.C2Vbpm),0])
        self.bg4_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.Cbpms.getYFromPV(self.C2Vbpm)])
        self.bg5.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV(self.C2Vbpm),0])
        self.bg5_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.Cbpms.getYFromPV(self.C2Vbpm)])
        self.bg6.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV(self.C2Vbpm),0])
        self.bg6_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.Cbpms.getYFromPV(self.C2Vbpm)])
