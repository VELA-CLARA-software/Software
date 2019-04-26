import sys, time, os
from datetime import datetime
sys.path.append("../../Widgets/Striptool2")
import signalRecord as striptoolRecord
import yaml
sys.path.append("../../Widgets/")
sys.path.append("../../../")
import Software.Procedures.qt as qt
from generic.pv import *
import argparse
import signal

parser = argparse.ArgumentParser(description='Record EPICS data to HDF5 file')
parser.add_argument('-f', '--filename', default=None, help='Set output filename', type=str)
parser.add_argument('-d', '--directory', default=None, help='Set output directory', type=str)
parser.add_argument('-c', '--comment', default=None, help='Set filename comment', type=str)
parser.add_argument('-t', '--timeout', default=None, help='Set time to run', type=int)
parser.add_argument('-g', '--gui', default=0, help='Show GUI', type=int)
parser.add_argument('settings', metavar='settings file',
                   help='File containing the input settings')
args = parser.parse_args()

def currentWorkFolder(basedir=None,today=None,createdirectory=False):
    if basedir is None:
        basedir = os.path.dirname( os.path.abspath(__file__))
    if today is None:
        today = datetime.today()
    datetuple = today.timetuple()
    year, month, day, hour, minute = datetuple[0:5]
    month = str(month) if month >= 10 else '0' + str(month)
    day = str(day) if day >= 10 else '0' + str(day)
    hour = str(hour) if hour >= 10 else '0' + str(hour)
    minute = str(minute) if minute >= 10 else '0' + str(minute)
    folder = basedir +'/'+str(year)+'/'+str(month)+'/'+str(day)+'/'#+str(hour)+str(minute)
    if not os.path.exists(folder) and createdirectory:
        combinedf = basedir
        for f in [str(year), str(month), str(day)]:
            combinedf = combinedf + '/' + f
            try:
                os.makedirs(combinedf)
            except:
                pass
    return folder, datetuple[3]

class signalPV(qt.QObject):
    def __init__(self, parent):
        super(signalPV, self).__init__(parent = parent)
        self.parent = parent

    def addSignal(self, pv, name, group, color=0, timer=1.0, arrayData=False):
        self.pv = pv
        self.name = name
        # try:
        self.pvlink = PVObject(self.pv)
        if args.gui is not 0:
            self.parent.sp.addSignal(name=name, pen=pg.mkColor(color), timer=timer, function=self.pvlink.getValue)
        else:
            self.parent.sp.addSignal(name=name, pen='', timer=timer, function=self.pvlink.getValue)
        return name, group
        # except:
        #     print('Could not add signal: ', pv)

class recorderInstance(qt.QObject):

    def __init__(self):
        super(recorderInstance, self).__init__()
        self.nPVs = 0

    def initialiseRecorder(self):
        self.open_file()
        with open(args.settings, 'r') as stream:
            settings = yaml.load(stream)
        namesgroups = []
        for types in settings:
            for name, pvs in settings[types].items():
                # name = name.replace(' ','_').replace(':','$')
                if 'timer' in pvs:
                    timer = pvs['timer']
                else:
                    timer = 1
                if 'name' in pvs:
                    display_name = pvs['name'].replace(' ','_').replace(':','_')
                else:
                    display_name = name.replace(' ','_').replace(':','_')
                if 'arrayData' in pvs:
                    arrayData = pvs['arrayData']
                else:
                    arrayData = False
                if 'suffix' in pvs:
                    for pv in pvs['suffix']:
                        self.nPVs += 1
                        signal = signalPV(self)
                        name, group = signal.addSignal(name+':'+pv, display_name+'_'+pv, types, color=self.nPVs, timer=1.0/timer, arrayData=arrayData)
                else:
                    self.nPVs += 1
                    signal = signalPV(self)
                    name, group = signal.addSignal(name, display_name, types, color=self.nPVs, timer=1.0/timer, arrayData=arrayData)
                namesgroups.append([name, group])
        return namesgroups

    def open_file(self, reopen=False):
        self.folder, self.hour = currentWorkFolder(basedir=args.directory, createdirectory=True)
        if args.filename == None:
            self.filename = os.path.basename(args.settings)
        else:
            self.filename = os.path.splitext(args.filename)[0]
        self.filename = os.path.splitext(self.filename)[0]
        print self.filename
        print args.comment
        if args.comment is not None:
            self.filename = self.filename + '_' + str(args.comment)
        self.filename = self.filename + '.csv'
        print self.filename
        timestr = time.strftime("%H%M%S")
        self.filename = timestr + '_' + self.filename
        if reopen:
            self.sp.open_file(self.folder+"/"+self.filename)
        else:
            self.sp = striptoolRecord.signalRecorderCSV(self.folder+"/"+self.filename)

    def start(self):
        self.timer = qt.QTimer()
        self.timer.timeout.connect(self.checkFileName)
        self.timer.start(1000)
        self.starttime = time.time()

    def checkFileName(self):
        datetuple = datetime.today().timetuple()
        year, month, day, hour, minute = datetuple[0:5]
        if hour is not self.hour:
            print 'hour change: ', hour, ' =!= ', self.hour
            self.sp.close()
            self.open_file(reopen=True)
        # elif hasattr(self, 'filename') and os.path.getsize(self.folder+'/'+self.filename)/(1024*1024.0) > 1024:
        #     self.sp.close()
        #     self.sp.deleteLater()
        #     self.initialiseRecorder()
        elif args.timeout is not None:
            if (time.time() - self.starttime) > args.timeout:
                self.close()

    # def close(self):
    #     print 'Closing dataRecorder!'
    #     self.timer.stop()
    #     self.sp.close()
    #     print 'Finished Closing!'
    #     exit()
    #
    # def closeEvent(self, *args, **kwargs):
    #     self.close()

class signalRecorder(qt.QMainWindow):

    def __init__(self, settings=''):
        super(signalRecorder, self).__init__()
        ''' Create Parameter Tree'''
        self.settings = settings
        self.parameterTree = ParameterTree()
        self.parameters = {}
        self.widget = qt.QWidget()
        self.layout = qt.QVBoxLayout()
        self.layout.addWidget(self.parameterTree)
        self.exitButton = qt.QPushButton('Exit')
        self.exitButton.clicked.connect(sys.exit)
        self.layout.addWidget(self.exitButton)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.show()
        self.recorder = recorderInstance()
        namesgroups = self.recorder.initialiseRecorder()
        for ng in namesgroups:
            self.addParameterSignal(*ng)
        self.recorder.start()
        self.windows = {}

    # def close(self):
    #     self.recorder.close()
    #     exit()
    #
    # def closeEvent(self, e):
    #     self.close()

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
            header = self.parameterTree.findItems(group,qt.Qt.MatchContains | qt.Qt.MatchRecursive)[0]
            header.setExpanded(False)
        else:
            parameter = self.parameters[group]
        param = parameter.child(group)
        if name not in param.names:
            p = param.addChildren(params)
        pChild = param.child(name)
        self.recorder.sp.records[name]['worker'].nsamplesSignal.connect(lambda x : pChild.child('Samples').setValue(x))
        self.recorder.sp.records[name]['worker'].recordMeanSignal.connect(lambda x : pChild.child('Mean').setValue(x))
        self.recorder.sp.records[name]['worker'].recordStandardDeviationSignal.connect(lambda x : pChild.child('Standard Deviation').setValue(x))
        self.recorder.sp.records[name]['worker'].recordMinSignal.connect(lambda x : pChild.child('Min').setValue(x))
        self.recorder.sp.records[name]['worker'].recordMaxSignal.connect(lambda x : pChild.child('Max').setValue(x))
        header = self.parameterTree.findItems(name,qt.Qt.MatchContains | qt.Qt.MatchRecursive)[0]
        header.setExpanded(False)
        header.setForeground(0,self.contrasting_text_color(self.recorder.sp.records[name]['pen']))
        header.setBackground(0,pg.mkBrush(self.recorder.sp.records[name]['pen']))

if args.gui is not 0:
    import pyqtgraph as pg
    from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
    pg.setConfigOptions(antialias=True)
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

class commandLineInterface(qt.QObject):

    def __init__(self):
        super(commandLineInterface, self).__init__()

    def updateOutput(self, output):
        sys.stdout.write(output + '\r')
        sys.stdout.flush()

    def startTimer(self):
        self.timer = qt.QTimer()
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)
        self.starttime = time.time()

    def updateTime(self):
        # print 'Running for '+str(self.starttime - time.time())+' secs'.ljust(80)
        self.updateOutput('Running for '+str(round(time.time() - self.starttime))+' secs'.ljust(80))

    # def close(self):
    #     self.timer.stop()
    #     exit()
    #
    # def closeEvent(self, e):
    #     self.close()

def signal_term_handler(signal, frame):
    app.exit()

signal.signal(signal.SIGINT, signal_term_handler)

if __name__ == '__main__':
    global app, sr, cli
    if args.gui is not 0:
        app = qt.QApplication(sys.argv)
        sr = signalRecorder(settings=args)
    else:
        app = qt.QCoreApplication(sys.argv)
        sr = recorderInstance()
        namesgroups = sr.initialiseRecorder()
        sr.start()
    cli = commandLineInterface()
    cli.startTimer()
    sys.exit(app.exec_())
