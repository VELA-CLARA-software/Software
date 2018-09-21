import sys, time, os
from datetime import datetime
sys.path.append(os.path.dirname( os.path.abspath(__file__)) + "/../")
import signalRecord as striptoolRecord
import tables as tables
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
import signal
import yaml
from epics import caget, caput, cainfo, PV
import numpy as np
sys.path.append(os.path.dirname( os.path.abspath(__file__)) + "/../")
from generic.pv import *

pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

def signal_term_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_term_handler)

def currentWorkFolder(today=None,createdirectory=False):
    if today is None:
        today = datetime.today()
    datetuple = today.timetuple()
    year, month, day, hour, minute = datetuple[0:5]
    month = str(month) if month >= 10 else '0' + str(month)
    day = str(day) if day >= 10 else '0' + str(day)
    hour = str(hour) if hour >= 10 else '0' + str(hour)
    minute = str(minute) if minute >= 10 else '0' + str(minute)
    folder = os.path.dirname( os.path.abspath(__file__))+'/'+str(year)+'/'+str(month)+'/'+str(day)+'/'#+str(hour)+str(minute)
    if not os.path.exists(folder) and createdirectory:
        os.makedirs(folder)
    return folder, datetuple[2]

class signalPV(QObject):
    def __init__(self, parent, pv, name, group, color=0, timer=1.0):
        super(signalPV, self).__init__(parent = parent)
        self.parent = parent
        self.pv = pv
        self.name = name
        try:
            self.pvlink = PVObject(self.pv)
            self.parent.sp.addSignal(name=name, pen=pg.mkColor(color), timer=timer, function=self.pvlink.getValue)
        except:
            print('Could not add signal: ', pv)

class signalRecorder(QObject):

    def __init__(self, settings=''):
        super(signalRecorder, self).__init__()
        ''' Create Parameter Tree'''
        self.settings = settings
        self.parameters = {}
        self.nPVs = 0
        self.initialiseRecorder(self.settings)
        self.start()

    def initialiseRecorder(self, settings):
        self.folder, self.day = currentWorkFolder(createdirectory=True)
        self.sp = striptoolRecord.signalRecorderH5(filename=self.folder+"/"+settings, flushtime=30)
        with open(settings, 'r') as stream:
            settings = yaml.load(stream)
        for types in settings:
            for name, pvs in settings[types].items():
                print('pvs = ', pvs)
                if 'timer' in pvs:
                    timer = pvs['timer']
                else:
                    timer = 1
                if 'suffix' in pvs:
                    for pv in pvs['suffix']:
                        self.nPVs += 1
                        signalPV(self, name+':'+pv, name.replace('-','_')+'_'+pv, types, color=self.nPVs, timer=1.0/timer)
                else:
                    self.nPVs += 1
                    signalPV(self, name, name.replace('-','_'), types, color=self.nPVs, timer=1.0/timer)

    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.checkFileName)
        self.timer.start(1000)

    def checkFileName(self):
        if datetime.today().timetuple()[2] is not self.day:
            self.sp.close()
            self.sp.deleteLater()
            self.initialiseRecorder(self.settings)

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    if len(sys.argv) > 1:
        sr = signalRecorder(settings=sys.argv[1])
    else:
        settings = str(QFileDialog.getOpenFileName()[0])
        sr = signalRecorder(settings=settings)
    sys.exit(app.exec_())
