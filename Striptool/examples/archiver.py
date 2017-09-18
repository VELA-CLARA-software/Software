import sys, time, os
from datetime import date
sys.path.append("..")
import striptoolRecord as striptoolRecord
import tables as tables
import numpy as np
import progressbar
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
import signal
import yaml
import VELA_CLARA_General_Monitor as vgen

def signal_term_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_term_handler)

''' This is a signal generator. It could easily read a magnet current using the hardware controllers
'''
def createRandomSignal(offset=0):
    signalValue = np.sin(2*2*np.pi*time.time()+0.05)+np.sin(1.384*2*np.pi*time.time()-0.1)+5*np.random.normal()
    return signalValue+offset

def currentWorkFolder(today=None,createdirectory=False):
    if today is None:
        today = date.today()
    datetuple = today.timetuple()
    year, month, day = datetuple[0:3]
    month = str(month) if month > 10 else '0' + str(month)
    day = str(day) if day > 10 else '0' + str(day)
    folder = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+str(year)+'\\'+str(month)+'\\'+str(day)+'\\'
    if not os.path.exists(folder) and createdirectory:
        os.makedirs(folder)
    return folder

class signalRecorder(QMainWindow):

    def __init__(self, time):
        super(signalRecorder, self).__init__()
        self.time = int(time)
        # self.bar = progressbar.ProgressBar(max_value=100)
        self.barpos = 0
        ''' Create Parameter Tree'''
        self.parameterTree = ParameterTree()
        self.parameters = {}
        self.parameterGroups = []
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.parameterTree)
        self.exitButton = QPushButton('Exit')
        self.exitButton.clicked.connect(sys.exit)
        self.layout.addWidget(self.exitButton)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.show()
        self.general = vgen.init()
        self.pvids = []
        self.folder = currentWorkFolder(createdirectory=True)

        self.sp = striptoolRecord.signalRecorderH5(self.folder+"test")

        stream = file('archiver_pvs.yaml', 'r')
        settings = yaml.load(stream)
        stream.close()

        for types in settings:
            for name,pvs in settings[types].iteritems():
                for pv in pvs:
                    self.addGeneralPV(name+':'+pv,name.replace('-','_')+'_'+pv, types)

    def addGeneralPV(self, functionArgument, name, group):
        # try:
            pvtype="DBR_DOUBLE"
            pvid = self.general.connectPV(str(functionArgument),pvtype)
            self.pvids.append(pvid)
            #print 'pvid = ', pvid
            testFunction = lambda: self.general.getValue(pvid)
            self.sp.addSignal(name=name, pen=pg.mkColor(len(self.pvids)),timer=1.0, function=testFunction, arg=[])
            self.addParameterSignal(name, group)
        # except:
        #     print 'Could not add signal: ', name

    def start(self):
        # QTimer.singleShot(1000*self.time, self.finish)
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateBar)
        self.timer.start(1000*self.time/10)

    def updateBar(self):
        self.barpos += 10
        # self.bar.update(self.barpos)
        if self.barpos >= 100:
            sys.exit()

    def contrasting_text_color(self, color):
        # (r, g, b) = (hex_str[:2], hex_str[2:4], hex_str[4:])
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
                    {'name': 'Mean', 'type': 'float', 'readonly': True},
                    {'name': 'Standard Deviation', 'type': 'float', 'readonly': True},
                    {'name': 'Max', 'type': 'float', 'readonly': True},
                    {'name': 'Min', 'type': 'float', 'readonly': True},
                ]}
            ]
        if not group in self.parameterGroups:
            self.parameterGroups.append(group)
            parameter = Parameter.create(name='params', type='group', children=gparams)
            self.parameters[group] = parameter
            self.parameterTree.addParameters(parameter, showTop=False)
            header = self.parameterTree.findItems(group,Qt.MatchContains | Qt.MatchRecursive)[0]
            header.setExpanded(False)
        else:
            parameter = self.parameters[group]
        param = parameter.child(group)
        p = param.addChildren(params)
        pChild = param.child(name)
        self.sp.records[name]['worker'].recordMeanSignal.connect(lambda x : pChild.child('Mean').setValue(x))
        self.sp.records[name]['worker'].recordStandardDeviationSignal.connect(lambda x : pChild.child('Standard Deviation').setValue(x))
        self.sp.records[name]['worker'].recordMinSignal.connect(lambda x : pChild.child('Min').setValue(x))
        self.sp.records[name]['worker'].recordMaxSignal.connect(lambda x : pChild.child('Max').setValue(x))
        header = self.parameterTree.findItems(name,Qt.MatchContains | Qt.MatchRecursive)[0]
        header.setExpanded(False)
        header.setForeground(0,self.contrasting_text_color(self.sp.records[name]['pen']))
        header.setBackground(0,pg.mkBrush(self.sp.records[name]['pen']))
        self.sp.records[name]['worker'].nsamplesSignal.connect(lambda x :header.setText(0,name + ': ' + str(x)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if len(sys.argv) >= 2:
        sr = signalRecorder(sys.argv[1])
    else:
        sr = signalRecorder(10)
    # sr.start()
    sys.exit(app.exec_())
