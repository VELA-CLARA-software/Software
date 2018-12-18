from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys,os
import time
import numpy as np
import csv
from  functools import partial
sys.path.append("../../../")
import Software.Procedures.qt as qt
import Software.Widgets.loggerWidget.loggerWidget as lw
from Software.Procedures.Machine.signaller import machineReciever, machineSignaller
import logging
logger = logging.getLogger(__name__)

class GenericThread(QThread):
    def __init__(self, function, *args, **kwargs):
        QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.object = self.function(*self.args,**self.kwargs)
        print 'finished!'

class updatingTimer(qt.QThread):
    def __init__(self, name, type, delay, function, *args, **kwargs):
        super(updatingTimer, self).__init__()
        self.name = name
        self.type = type
        self.delay = delay
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.timer = qt.QTimer()
        self.timer.moveToThread(self)
        if self.type == 'widget':
            self.timer.timeout.connect(self.update_monitor_widget)
        elif self.type == 'function':
            self.timer.timeout.connect(self.update_monitor_function)
        self.timer.start(self.delay)
        self.exec_()

    def update_monitor_widget(self):
        val = self.function(*self.args, **self.kwargs)
        self.name.setValue(val)

    def update_monitor_function(self):
        val = self.function(*self.args, **self.kwargs)
        self.name(val)

class Controller(QObject):

    newDataSignal = pyqtSignal()
    loggerSignal = pyqtSignal(object)

    def __init__(self, app, view, model):
        super(Controller, self).__init__()
        '''define model and view'''
        self.view = view
        self.model = model
        self.app = app
        self.model.laser.app = self.app
        self.model.logger = self.loggerSignal
        # self.model.laser.logger = self.loggerSignal
        self.model.newData = self.newDataSignal
        # self.machineSignaller = machineSignaller(self.model.baseMachine)
        # self.machineReciever = machineReciever(self.model.baseMachine)
        # self.model.machine = self.machineSignaller
        # self.machineSignaller.toMachine.connect(self.machineReciever.toMachine)
        # self.machineReciever.fromMachine.connect(self.machineSignaller.fromMachine)
        self.loggerSignal.connect(self.setLabel)

        self.buttons = [
        self.view.laserNormalButton, self.view.laserBurstButton, self.view.qFireButton,
        self.view.nFireButton
        ]

        self.log = lw.loggerWidget()
        self.view.logTabLayout.addWidget(self.log)
        self.log.addLogger(logger)

        self.view.laserNormalButton.clicked.connect(self.setLaserNormal)
        self.view.laserBurstButton.clicked.connect(self.setLaserBurst)

        self.view.abortButton.clicked.connect(self.abortLaser)
        self.view.abortButton.setVisible(False)

        self.view.nFireButton.clicked.connect(self.fireNShots)
        self.view.qFireButton.clicked.connect(self.fireIntegratedCharge)

        self.setLabel('MODE: '+self.model.machineType+' '+self.model.lineType+' with '+self.model.gunType+' gun')

        self.monitors = {}
        self.monitors['laserMode'] = updatingTimer(self.laser_Mode_Monitor, 'function', 250, self.model.laser.isLaserOn)
        self.monitors['laserMode'].start()

    def laser_Mode_Monitor(self, state):
        if state == 0:
            self.view.laserNormalStatus.setStyleSheet("background-color: red")
            self.view.laserBurstStatus.setStyleSheet("background-color: green")
        else:
            self.view.laserNormalStatus.setStyleSheet("background-color: green")
            self.view.laserBurstStatus.setStyleSheet("background-color: red")

    def abortLaser(self):
        self.model.laser.abort = True

    def toggleVerbose(self, state):
        print 'state = ', state
        self.model.verbose = state

    def setButtonState(self, state=True):
        for b in self.buttons:
            b.setEnabled(state)

    def enableButtons(self):
        self.view.abortButton.setVisible(False)
        self.setButtonState(True)

    def disableButtons(self):
        self.view.abortButton.setVisible(True)
        self.setButtonState(False)

    def setLaserNormal(self):
        val = self.model.laser.turnOnLaserGating()
        self.setLabel('Set Laser Burst = '+ str(val))

    def setLaserBurst(self):
        val = self.model.laser.turnOffLaserGating()
        self.setLabel('Set Laser Burst = '+ str(val))

    def fireNShots(self):
        self.disableButtons()
        self.model.laser.turnOnForNPulse(n=self.view.nShotsSpinBox.value(), \
                        energy=self.view.nEnergySpinbox.value(), pos=self.view.nMotorPositionSpinBox.value(), \
                        comment=self.view.nCommentTextBox.text())
        self.enableButtons()

    def fireIntegratedCharge(self):
        self.disableButtons()
        self.model.laser.turnOnForIntegratedCharge(q=self.view.qIntegratedChargeSpinBox.value(), \
                        energy=self.view.qEnergySpinbox.value(), pos=self.view.qMotorPositionSpinBox.value(), \
                        comment=self.view.qCommentTextBox.text())
        self.enableButtons()

    def setLabel(self, string, severity='info'):
        getattr(logger,severity)(string)
        self.view.label_MODE.setText('Status: <font color="red">' + string + '</font>')
