import sys, time, os
from datetime import datetime
sys.path.append("..")
import striptoolRecord as striptoolRecord
import tables as tables
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

def currentWorkFolder(today=None,createdirectory=False):
    if today is None:
        today = datetime.today()
    datetuple = today.timetuple()
    year, month, day, hour, minute = datetuple[0:5]
    month = str(month) if month >= 10 else '0' + str(month)
    day = str(day) if day >= 10 else '0' + str(day)
    hour = str(hour) if hour >= 10 else '0' + str(hour)
    minute = str(minute) if minute >= 10 else '0' + str(minute)
    folder = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+str(year)+'\\'+str(month)+'\\'+str(day)+'\\'#+str(hour)+str(minute)
    if not os.path.exists(folder) and createdirectory:
        os.makedirs(folder)
    return folder, datetuple[2]

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
        self.show()
        self.general = vgen.init()
        self.pvids = []
        self.initialiseRecorder(self.settings)
        self.start()

    def initialiseRecorder(self, settings):
        self.folder, self.day = currentWorkFolder(createdirectory=True)
        self.sp = striptoolRecord.signalRecorderH5(self.folder+"Signal_Archive")
        stream = file(settings, 'r')
        settings = yaml.load(stream)
        stream.close()
        for types in settings:
            for name,pvs in settings[types].iteritems():
                for pv in pvs:
                    self.addGeneralPV(name+':'+pv,name.replace('-','_')+'_'+pv, types)

    def addGeneralPV(self, functionArgument, name, group):
        try:
            pvtype="DBR_DOUBLE"
            pvid = self.general.connectPV(str(functionArgument),pvtype)
            self.pvids.append(pvid)
            testFunction = lambda: self.general.getValue(pvid)
            self.sp.addSignal(name=name, pen=pg.mkColor(len(self.pvids)),timer=1.0, function=testFunction, arg=[])
            self.addParameterSignal(name, group)
        except:
            print 'Could not add signal: ', name

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
        header = self.parameterTree.findItems(name,Qt.MatchContains | Qt.MatchRecursive)[0]
        header.setExpanded(False)
        header.setForeground(0,self.contrasting_text_color(self.sp.records[name]['pen']))
        header.setBackground(0,pg.mkBrush(self.sp.records[name]['pen']))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if len(sys.argv) > 1:
        sr = signalRecorder(settings=sys.argv[1])
    else:
        settings = QFileDialog.getOpenFileName()
        sr = signalRecorder(settings=settings)
    sys.exit(app.exec_())
