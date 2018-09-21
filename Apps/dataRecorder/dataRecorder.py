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
            self.parent.addParameterSignal(name, group)
        except:
            print('Could not add signal: ', pv)

class signalRecorder(QMainWindow):

    def __init__(self, settings=''):
        super(signalRecorder, self).__init__()
        ''' Create Parameter Tree'''
        self.settings = settings
        self.parameterTree = ParameterTree()
        self.parameters = {}
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.parameterTree)
        self.exitButton = QPushButton('Exit')
        self.exitButton.clicked.connect(sys.exit)
        self.layout.addWidget(self.exitButton)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.nPVs = 0
        self.show()
        self.initialiseRecorder(self.settings)
        self.start()
        self.windows = {}

    def initialiseRecorder(self, settings):
        self.folder, self.day = currentWorkFolder(createdirectory=True)
        self.sp = striptoolRecord.signalRecorderH5(self.folder+"/"+os.path.basename(settings))
        with open(settings, 'r') as stream:
            settings = yaml.load(stream)
        for types in settings:
            for name, pvs in settings[types].items():
                print('Adding PV ', name)
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

    def contrasting_text_color(self, color):
        r, g, b, a = pg.colorTuple(pg.mkColor(color))
        return pg.mkBrush('000' if 1 - (r * 0.299 + g * 0.587 + b * 0.114) / 255 < 0.5 else 'fff')

    def valueFormatter(self, value):
        return "{:.4}".format(value)

    def addParameterSignal(self, name, group):
        gparams = [
            {'name': group, 'type': 'group'}
            ]
        params = [
            {'name': name, 'type': 'group', 'children': [
                    {'name': 'Samples', 'type': 'int', 'readonly': True},
                    {'name': 'Mean', 'type': 'float', 'readonly': True},
                    {'name': 'Standard Deviation', 'type': 'float', 'readonly': True},
                    {'name': 'Max', 'type': 'float', 'readonly': True},
                    {'name': 'Min', 'type': 'float', 'readonly': True},
                    {'name': 'Plot', 'type': 'action'},
                ]}
            ]
        if not group in self.parameters:
            parameter = Parameter.create(name='params', type='group', children=gparams)
            self.parameters[group] = parameter
            self.parameterTree.addParameters(parameter, showTop=False)
            header = self.parameterTree.findItems(group,Qt.MatchContains | Qt.MatchRecursive)[0]
            header.setExpanded(False)
        else:
            parameter = self.parameters[group]
        param = parameter.child(group)
        if name not in param.names:
            p = param.addChildren(params)
        pChild = param.child(name)
        self.sp.records[name]['worker'].nsamplesSignal.connect(lambda x : pChild.child('Samples').setValue(x))
        self.sp.records[name]['worker'].recordMeanSignal.connect(lambda x : pChild.child('Mean').setValue(x))
        self.sp.records[name]['worker'].recordStandardDeviationSignal.connect(lambda x : pChild.child('Standard Deviation').setValue(x))
        self.sp.records[name]['worker'].recordMinSignal.connect(lambda x : pChild.child('Min').setValue(x))
        self.sp.records[name]['worker'].recordMaxSignal.connect(lambda x : pChild.child('Max').setValue(x))
        pChild.child('Plot').sigActivated.connect(lambda x: self.showPlot(name=str(name)))
        header = self.parameterTree.findItems(name,Qt.MatchContains | Qt.MatchRecursive)[0]
        header.setExpanded(False)
        header.setForeground(0,self.contrasting_text_color(self.sp.records[name]['pen']))
        header.setBackground(0,pg.mkBrush(self.sp.records[name]['pen']))

    def showPlot(self, name):
        if not name in self.windows:
            self.windows[name] = plotWindow(sp=self.sp, name=name)
        else:
            self.windows[name].show()

class plotWindow(QMainWindow):
    def __init__(self, parent=None, sp=None, name=''):
        super(plotWindow, self).__init__(parent)
        self.setWindowTitle(name)
        self.sp = sp
        self.name = name
        self.plot = dataPlot(sp=self.sp, name=name)
        #self.signalProxy = pg.SignalProxy(self.plot.sigXRangeChanged, rateLimit=1, slot=self.update)
        self.widget = QWidget()
        self.layout = QGridLayout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

        self.updateButton = QPushButton('Update')
        self.updateButton.clicked.connect(self.update)

        self.autoUpdateCheckBox = QCheckBox('Auto Update')
        self.autoUpdateCheckBox.stateChanged.connect(self.autoUpdate)

        self.layout.addWidget(self.plot,1,0,3,3)
        self.layout.addWidget(self.autoUpdateCheckBox,0,0,1,1)
        self.layout.addWidget(self.updateButton,0,1,1,1)
        self.show()

    def update(self):
        #self.signalProxy.disconnect()
        if self.isVisible():
            self.plot.update()
        #self.signalProxy = pg.SignalProxy(self.plot.sigXRangeChanged, rateLimit=1, slot=self.update)


    def autoUpdate(self):
        if self.autoUpdateCheckBox.isChecked() is True:
            self.timer.start(1000)
        else:
            self.timer.stop()

class HAxisTime(pg.AxisItem):
    def __init__(self, orientation=None, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        super(HAxisTime, self).__init__(parent=parent, orientation=orientation, linkView=linkView)
        self.dateTicksOn = True
        self.autoscroll = True

    def updateTimeOffset(self,time):
        self.timeOffset = time
        self.resizeEvent()
        self.update()

    def tickStrings(self, values, scale, spacing):
        if not hasattr(self, 'fixedtimepoint'):
            self.fixedtimepoint = round(time.time(),2)
        if self.dateTicksOn:
            if self.autoscroll:
                reftime = round(time.time(),2)
            else:
                reftime = self.fixedtimepoint
            try:
                ticks = [time.strftime("%H:%M:%S", time.localtime(x)) for x in values]
            except:
                ticks = []
            return ticks
        else:
            places = max(0, np.ceil(-np.log10(spacing*scale)))
            strings = []
            for v in values:
                vs = v * scale
                if abs(vs) < .001 or abs(vs) >= 10000:
                    vstr = "%g" % vs
                else:
                    vstr = ("%%0.%df" % places) % vs
                strings.append(vstr)
            return strings

class dataPlot(pg.PlotWidget):
    def __init__(self, parent=None, sp=None, name=''):
        super(dataPlot, self).__init__(parent, axisItems={'bottom': HAxisTime(orientation = 'bottom')})
        self.sp = sp
        self.name = name
        self.plotItem = self.getPlotItem()
        self.plotItem.setXRange(time.time()-100, time.time())
        self.bpmPlot = self.plotItem.plot(symbol='+', symbolPen='r')
        self.fittedPlot = self.plotItem.plot(pen='b')
        self.plotItem.showGrid(x=True, y=True)
        self.date_axis = self.getAxis('bottom')
        # self.plotItem.
        self.lastTime = time.time()
        self.update()

    def update(self):
        start = -100
        start = self.plotItem.viewRange()[0][0]
        stop = -1
        stop = self.plotItem.viewRange()[0][1]
        self.data = np.array(self.sp.getDataTime(name=self.name, start=start, stop=stop))
        if len(self.data) > 1:
            self.bpmPlot.setData(self.data)
            self.fittedPlot.setData(self.data)
        self.plotItem.vb.translateBy(x=time.time() - self.lastTime)
        #self.plotItem.setXRange(start+1, stop+1, padding=0)
        self.lastTime = time.time()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if len(sys.argv) > 1:
        sr = signalRecorder(settings=sys.argv[1])
    else:
        settings = str(QFileDialog.getOpenFileName()[0])
        print ('settings = ', settings)
        sr = signalRecorder(settings=settings)
    sys.exit(app.exec_())
