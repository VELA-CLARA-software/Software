from PyQt4 import QtCore
import pyqtgraph as pg
import time
#from functools import partial
#import time
#from PyQt4.QtGui import QApplication

class Controller():
    def __init__(self, view, model, data):
        self.view = view
        self.model = model
        self.data = data
        self.C2Vbpm = self.model.C2Vbpm
        self.S02bpm = self.model.S02bpm
        self.S02cam = self.model.S02cam

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

        self.view.pushButton_x_up_1.clicked.connect(self.model.dipole_current_up)
        self.view.pushButton_x_down_1.clicked.connect(self.model.dipole_current_down)

        self.view.doubleSpinBox_roughIMin.valueChanged[float].connect(self.model.roughIMin)
        self.view.doubleSpinBox_roughIMax.valueChanged[float].connect(self.model.roughIMax)
        self.view.doubleSpinBox_roughIStep.valueChanged[float].connect(self.model.roughIStep)

        self.view.pushButton_roughCentreC2VCurrent.clicked.connect(self.model.measureMomentumCentreC2VApprox)

        # Rough set
        self.view.doubleSpinBox_p_rough_set.valueChanged[float].connect(self.model.p_rough_set)

        self.data.values['rough_set_step'] = 100.0
        self.view.doubleSpinBox_step_2.setValue(self.data.values['rough_set_step'])
        self.view.doubleSpinBox_step_2.valueChanged[float].connect(self.model.setRoughSetStep)

        self.view.pushButton_set_I_rough.clicked.connect(self.model.set_I_rough)

        self.view.pushButton_select_gun.clicked.connect(self.model.select_gun)
        self.view.pushButton_select_linac.clicked.connect(self.model.select_linac)

        self.view.pushButton_x_up_2.clicked.connect(self.model.RF_amplitude_up)
        self.view.pushButton_x_down_2.clicked.connect(self.model.RF_amplitude_down)

        # Align
        self.view.pushButton_degauss.clicked.connect(self.model.degauss)
        self.view.pushButton_degauss_2.clicked.connect(self.model.degauss_2)
        self.view.pushButton_Align_1.clicked.connect(self.model.measureMomentumAlign_1)
        self.view.pushButton_InsertYAG.clicked.connect(self.model.insertYAG)

        self.data.values['fine_step2'] = 0.1
        self.view.doubleSpinBox_step_4.setValue(self.data.values['fine_step2'])
        self.view.doubleSpinBox_step_4.valueChanged[float].connect(self.model.setFineStep2)
        self.view.pushButton_x_up_6.clicked.connect(self.model.cor2_current_up)
        self.view.pushButton_x_down_6.clicked.connect(self.model.cor2_current_down)

        self.data.values['target1'] = 0.0
        self.data.values['target1_y'] = 0.0
        self.view.doubleSpinBox_x_1.setValue(self.data.values['target1'])
        self.data.values['tol1'] = 0.5
        self.view.doubleSpinBox_tol_1.setValue(self.data.values['tol1'])

        self.data.values['target2'] = 13.0#6.4
        self.data.values['target2_y'] = 15.0
        self.view.doubleSpinBox_x_2.setValue(self.data.values['target2'])
        self.data.values['tol2'] = 0.5
        self.view.doubleSpinBox_tol_2.setValue(self.data.values['tol2'])

        self.view.pushButton_Align_3.clicked.connect(self.model.measureMomentumAlign_3)
        self.view.pushButton_Align_4.clicked.connect(self.model.retractYAG)


        self.data.values['fine_step1'] = 0.1
        self.view.doubleSpinBox_step_5.setValue(self.data.values['fine_step1'])
        self.view.doubleSpinBox_step_5.valueChanged[float].connect(self.model.setFineStep1)
        self.view.pushButton_x_up_7.clicked.connect(self.model.cor1_current_up)
        self.view.pushButton_x_down_7.clicked.connect(self.model.cor1_current_down)

        # Fine measure
        self.view.pushButton_fineGetCurrentRange_2.clicked.connect(self.model.fineGetCurrentRange_2)
        self.view.pushButton_fineCentreC2VCurrent.clicked.connect(self.model.measureMomentumCentreC2V)

        self.data.values['target3'] = 0.0
        self.data.values['target3_y'] = 0.0
        self.view.doubleSpinBox_x_3.setValue(self.data.values['target3'])
        self.data.values['tol3'] = 0.5
        self.view.doubleSpinBox_tol_3.setValue(self.data.values['tol3'])

        # Fine set
        self.view.doubleSpinBox_p_fine_set.valueChanged[float].connect(self.model.p_fine_set)

        self.data.values['fine_set_step'] = 100.0
        self.view.doubleSpinBox_step_3.setValue(self.data.values['fine_set_step'])
        self.view.doubleSpinBox_step_3.valueChanged[float].connect(self.model.setFineSetStep)

        self.view.pushButton_set_I_fine.clicked.connect(self.model.set_I_fine)

        self.view.pushButton_select_gun_2.clicked.connect(self.model.select_gun_fine)
        self.view.pushButton_select_linac_2.clicked.connect(self.model.select_linac_fine)

        self.view.pushButton_x_up_3.clicked.connect(self.model.RF_amplitude_up_fine)
        self.view.pushButton_x_down_3.clicked.connect(self.model.RF_amplitude_down_fine)

        # Momentum spread
        self.view.pushButton_CalcDisp.clicked.connect(self.model.measureMomentumSpreadCalcDisp)
        self.view.pushButton_Calc.clicked.connect(self.model.measureMomentumSpreadCalc)

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
        self.view.horizontalLayout_5.addWidget(monitor_3)

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
        self.view.horizontalLayout_4.addWidget(monitor_4)

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
        self.view.horizontalLayout_15.addWidget(monitor_s)


    def updateDisplays(self):
        self.view.label_I.setText(
            self.model.dipole+'current = '+str(self.model.Cmagnets.getSI(self.model.dipole))+' A'
            +'\nC2V BPM x-position = '+str(self.model.Cbpms.getXFromPV(self.C2Vbpm))+' mm'
            +'\nGun set point = '+str(self.model.gun.getAmpSP())
            +'\nLinac set point = '+str(self.model.linac1.getAmpSP())
            +'\nIs linac timing set to on? = '+str(self.model.Linac01Timing.isLinacOn())
            )

        self.view.label_dipole_set.setText(str(self.model.Cmagnets.getSI(self.model.dipole)))
        self.view.label_dipole_set_2.setText(str(self.model.Cmagnets.getSI(self.model.dipole)))
        # rough set
        self.view.label_I_rough.setText(str(self.model.Cmagnets.getSI(self.model.dipole)))

        try:
            if self.data.values['RFmode_rough'] == 'Gun':
                self.view.label_RF_rough.setText(str(self.model.gun.getAmpSP()))
            elif self.data.values['RFmode_rough'] == 'Linac':
                self.view.label_RF_rough.setText(str(self.model.linac1.getAmpSP()))
        except:
            self.view.label_RF_rough.setText('Mode not set')

        # align
        self.view.label_H_1.setText(str(self.model.Cbpms.getXFromPV(self.S02bpm)- self.data.values['target1'])+' mm')
        self.view.label_H_2.setText(str(self.model.cam.getX(self.S02cam)- self.data.values['target2'])+' mm')

        # fine measure
        self.view.label_H_3.setText(str(self.model.Cbpms.getXFromPV(self.C2Vbpm)- self.data.values['target3'])+' mm')

        # fine set
        self.view.label_I_fine.setText(str(self.model.Cmagnets.getSI(self.model.dipole)))

        try:
            if self.data.values['RFmode_fine'] == 'Gun':
                self.view.label_RF_fine.setText(str(self.model.gun.getAmpSP()))
            elif self.data.values['RFmode_fine'] == 'Linac':
                self.view.label_RF_fine.setText(str(self.model.linac1.getAmpSP()))
        except:
            self.view.label_RF_fine.setText('Mode not set')


        # check boxes
        if abs(self.model.Cbpms.getXFromPV(self.S02bpm) - self.data.values['target1']) < self.data.values['tol1']:
            self.view.checkBox.setCheckState(True)
            #print self.model.Cbpms.getXFromPV(self.S02bpm), self.data.values['target1'], abs(self.model.Cbpms.getXFromPV(self.S02bpm) - self.data.values['target1']), self.data.values['tol1']
            #print 'true'
            #time.sleep(0.5)
        else:
            self.view.checkBox.setCheckState(False)
            #print self.model.Cbpms.getXFromPV(self.S02bpm), self.data.values['target1'], abs(self.model.Cbpms.getXFromPV(self.S02bpm) - self.data.values['target1']), self.data.values['tol1']
            #print 'false'
            #time.sleep(0.5)

        if abs(self.model.cam.getX(self.S02cam) - self.data.values['target2']) < self.data.values['tol2']:
            self.view.checkBox_2.setCheckState(True)
        else:
            self.view.checkBox_2.setCheckState(False)

        # if (abs(self.model.Cbpms.getXFromPV(self.S02bpm) - self.data.values['target1']) < self.data.values['tol1']) and (abs(self.model.cam.getX(self.S02cam) - self.data.values['target2']) < self.data.values['tol2']):
        #     self.view.checkBox_3.setCheckState(True)
        # else:
        #     self.view.checkBox_3.setCheckState(False)
        if abs(self.model.Cbpms.getXFromPV(self.S02bpm) - self.data.values['target1']) < self.data.values['tol1']:
            self.view.checkBox_3.setCheckState(True)
        else:
            self.view.checkBox_3.setCheckState(False)


        # plots
        # rough measure - C2V BPM plot
        self.bg1.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV(self.C2Vbpm),0])
        self.bg1_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.Cbpms.getYFromPV(self.C2Vbpm)])
        # rough set - C2V BPM plot
        self.bg2.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV(self.C2Vbpm),0])
        self.bg2_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.Cbpms.getYFromPV(self.C2Vbpm)])
        # S02 BPM plot
        self.bg3.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV(self.S02bpm) - self.data.values['target1'],0])
        self.bg3_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.Cbpms.getYFromPV(self.S02bpm)- self.data.values['target1_y']])
        #self.bg3.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV(self.S02bpm)- self.data.values['target1'],0])
        #self.bg3_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.Cbpms.getYFromPV(self.S02bpm)- self.data.values['target1_y']])
        # S02 YAG plot
        self.bg4.setOpts(x=self.xdict.keys(), height=[1*self.model.cam.getX(self.S02cam) - self.data.values['target2'],0])
        self.bg4_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.cam.getY(self.S02cam) - self.data.values['target2_y']])
        # fine measure - C2V BPM plot
        self.bg5.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV(self.C2Vbpm),0])
        self.bg5_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.Cbpms.getYFromPV(self.C2Vbpm)])
        # fine set - C2V BPM plot
        self.bg6.setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV(self.C2Vbpm),0])
        self.bg6_y.setOpts(x=self.xdict.keys(), height=[0,1*self.model.Cbpms.getYFromPV(self.C2Vbpm)])

        self.sp.setData(self.model.dipCurrent, self.model.BPMPosition)
        self.dCurve.setData(x=self.model.dCurrents,y=self.model.dPositions)
        self.fCurve.setData(x=self.model.fCurrents,y=self.model.fPositions)
        self.displayDisp.setText('DISPERSION:<br>'+str(self.model.Dispersion)+' m/A')
        self.displayMom_S.setText('MOMENTUM SPREAD:<br>'+str(self.model.pSpread)+' MeV/c')
