#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS automtic gun conditioning PROTOTYPING SCRIPT, march 2017
import epics, time, math, numpy, sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
sys.path.append(os.path.abspath('.'))
# import striptool as stripTool
import pyqtgraph as pg
import linac_conditioner as lc
# import VELA_CLARA_MagnetControl as vmag
# import    VELA_CLARA_General_Monitor as vgen
# sys.path.append('C:\\Put a directory on PYTHONPATH here\\Software\\loggerwidget')
# import logging
# import loggerWidget as lw
# logger = logging.getLogger(__name__)

class linac_condition_edit_widget(QWidget):

    def __init__(self, param, label, gc, parent=None):
        super(linac_condition_edit_widget, self).__init__(parent)
        self.param = param
        self.label = label
        self.gc = gc
        self.labelWidget = QLabel(label[0])
        self.labelWidget.setMinimumWidth(130)
        self.editWidget = QLineEdit(str(getattr(self.gc,param)))
        self.editWidget.setToolTip(label[1])
        self.editWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.labelWidget,0)
        self.layout.addWidget(self.editWidget,1)
        self.setLayout(self.layout)

    def widgets(self):
        return self.layout

    def applySetting(self):
        val = self.editWidget.text()
        # print 'before = ', getattr(self.gc, self.param)
        setattr(self.gc, self.param, float(val))
        # print 'after = ', getattr(self.gc, self.param)

class linac_condition_view_widget(QWidget):

    def __init__(self, param, label, gc, parent=None):
        super(linac_condition_view_widget, self).__init__(parent)
        self.param = param
        self.label = label
        self.limit = label[2]
        self.gc = gc
        self.labelWidget = QLabel(label[0])
        self.labelWidget.setMinimumWidth(130)
        self.editWidget = QLineEdit(str(getattr(self.gc, self.param)))
        self.editWidget.setReadOnly(True)
        self.editWidget.setToolTip(label[1])
        self.editWidget.setStyleSheet(QString("background-color: #f2f2f2;"))
        self.editWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.gc.monitor_Signal.connect(self.update)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.labelWidget,0)
        self.layout.addWidget(self.editWidget,1)
        self.setLayout(self.layout)

    def widgets(self):
        return self.layout

    def update(self, signal):
        # print 'Signal Received! ', signal
        label, val = signal
        if label == self.param:
            self.editWidget.setText(str(val))
            if self.limit > 0:
                if val > self.limit:
                    self.editWidget.setStyleSheet(QString("background-color: #ffb3b3;"))
                else:
                    self.editWidget.setStyleSheet(QString("background-color: #d6f5d6;"))

class horizontallineWidget(QWidget):

    def __init__(self, parent = None):
        super(horizontallineWidget, self).__init__(parent)
        self.setFixedHeight(2)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet(QString("background-color: #ffffff;"))

class linac_condition_window(QMainWindow):

    applySettingsSignal = pyqtSignal()

    def __init__(self, parent = None):
        super(linac_condition_window, self).__init__()
        self.gc = lc.linac_condition()
        self.timer = QTimer()
        self.timer.timeout.connect(self.gc.main_loop)
        self.timer.start(10)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralLayout = QHBoxLayout()
        self.centralWidget.setLayout(self.centralLayout)

        self.centralSplitter = QSplitter()
        self.centralLayout.addWidget(self.centralSplitter)

        self.gunlogTab = QTabWidget()
        self.centralSplitter.addWidget(self.gunlogTab)

        self.gunParametersWidget = QWidget()
        self.gunlogTab.addTab(self.gunParametersWidget,'RF Params')

        self.gunParametersWidgetLayout = QGridLayout()
        self.gunParametersWidget.setLayout(self.gunParametersWidgetLayout)

        self.gunParameters = {
        'normal_RF_increase': ['Power Step','Step increase in RF power'],
        }

        self.gunParametersReadbacks = {
                'rep_rate': ['Machine Rep Rate','Rep Rate in Hz', 0],
                'wait_time': ['Script Wait Time','Wait time at current Rep Rate', 0],
                'breakdown_count': ['BreakDown Count','Total Number of Breakdowns', 0],
                'breakdown_per_minute': ['BreakDowns per minute','Breakdown rate per minute', 0],
                'breakdown_rate': ['BreakDown Rate','Breakdown rate per 30 minutes', 1],
                'rev_pwr_mean': ['Average CAV REV PWR','Average REV PWR int he cavity over the last 10 shots', 0],
                'dont_panic_text': ['Information','They don\'t like it up \'em!', 0],
        }

        self.plotParameters = {
        }

        row = 0
        for param, label in self.gunParameters.iteritems():
            gunwidget = linac_condition_edit_widget(param, label, self.gc, self)
            self.applySettingsSignal.connect(gunwidget.applySetting)
            self.gunParametersWidgetLayout.addWidget(gunwidget,row,0,1,2)
            row += 1
        self.applyButton = QPushButton('Apply')
        self.applyButton.setMaximumWidth(200)
        self.applyButton.clicked.connect(self.applySettings)
        self.gunParametersWidgetLayout.addWidget(self.applyButton,row,1,1,1)
        row += 1

        self.lineWidget1 = QWidget()
        self.lineWidget1.setFixedHeight(2)
        self.lineWidget1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.lineWidget1.setStyleSheet(QString("background-color: #c0c0c0;"))
        self.gunParametersWidgetLayout.addWidget(self.lineWidget1,row,0,1,2)
        row += 1

        for param, label in self.gunParametersReadbacks.iteritems():
            gunwidget = linac_condition_view_widget(param, label, self.gc, self)
            self.gunParametersWidgetLayout.addWidget(gunwidget,row,0,1,2)
            row += 1

        self.lineWidget2 = QWidget()
        self.lineWidget2.setFixedHeight(2)
        self.lineWidget2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.lineWidget2.setStyleSheet(QString("background-color: #c0c0c0;"))
        self.gunParametersWidgetLayout.addWidget(self.lineWidget2,row,0,1,2)
        row += 1

        self.startStopWidget = QWidget()
        self.startStopWidgetLayout = QHBoxLayout()
        self.startButton = QPushButton('Start')
        self.startButton.setCheckable(False)
        self.startButton.clicked.connect(self.startScript)
        self.gunParametersWidgetLayout.addWidget(self.startButton)
        self.stopButton = QPushButton('Stop')
        self.stopButton.clicked.connect(self.stopScript)
        self.startStopWidgetLayout.addWidget(self.startButton)
        self.startStopWidgetLayout.addWidget(self.stopButton)
        self.startStopWidget.setLayout(self.startStopWidgetLayout)
        self.gunParametersWidgetLayout.addWidget(self.startStopWidget,row,0,1,2)
        row += 1

        # self.general = vgen.init()
        # self.pvids = []

        # self.sp = stripTool.stripPlot(plotRateBar=False,crosshairs=True)
        # self.sp.start()
        # self.sp.pausePlotting(False)
        # self.sp.setPlotScale(60)
        # self.centralSplitter.addWidget(self.sp)
        for pv, pvparams in self.plotParameters.iteritems():
            self.generalPVFunction(pv,pvparams)

    def generalPVFunction(self, pvname, pvproperties):
        # global general
        pv = epics.PV(pvname)
        # logger.debug('pv = '+str(pv))
        self.pvids.append(pv)
        testFunction = lambda: pv.get()
        # logger.debug('pv value = '+str(testFunction()))
        # self.sp.addSignal(name=pvproperties['name'],pen=pvproperties['pen'], function=testFunction, timer=1.0/pvproperties['freq'], logscale=pvproperties['logscale'],
        # VerticalOffset=pvproperties['VerticalOffset'], VerticalScale=pvproperties['verticalScale'])

    def applySettings(self):
        self.applySettingsSignal.emit()

    def startScript(self, paused):
        self.startButton.setCheckable(True)
        self.startButton.clicked.disconnect(self.startScript)
        self.startButton.toggled.connect(self.pauseScript)
        # self.gc.getInitialValues() # Re-initialize the img and REV PWR histories
        self.gc.doConditioning = True
        self.startButton.setText('Running...')

    def pauseScript(self, paused):
        if paused:
            self.gc.doConditioning = False
            self.startButton.setText('Paused')
        else:
            self.gc.doConditioning = True
            self.startButton.setText('Running...')

    def stopScript(self):
        self.gc.doConditioning = False
        self.startButton.toggled.disconnect(self.pauseScript)
        self.startButton.clicked.connect(self.startScript)
        self.startButton.setCheckable(False)
        self.startButton.setText('Start')

def main():
    app = QApplication(sys.argv)
    pg.setConfigOptions(antialias=True)
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    app.setStyle(QStyleFactory.create("plastique"))
    gc = linac_condition_window()
    gc.gc.updateLatestValues()
    gc.gc.getRepRate()
    gc.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
