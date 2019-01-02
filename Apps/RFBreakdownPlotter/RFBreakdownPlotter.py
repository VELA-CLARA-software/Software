import pickle
import sys, os, time, math, datetime
from PyQt4.QtCore import QObject, pyqtSignal, QThread, QTimer
from PyQt4.QtGui import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QTabWidget, QLineEdit, QFileDialog, QLabel, QAction
from pyqtgraph import LegendItem, mkPen, mkBrush, LabelItem, TableWidget, GraphicsLayoutWidget, setConfigOption, setConfigOptions, InfiniteLine
from pyqtgraph.graphicsItems.LegendItem import ItemSample
import glob
from itertools import groupby
import argparse
import json

parser = argparse.ArgumentParser(description='Monitor a directory for RF breakdown traces')
parser.add_argument('-d', '--directory', default='.')
parser.add_argument('-s', '--settings', default='October2018.json')

class myLegend(LegendItem):
    def __init__(self, size=None, offset=None, background=(255,255,255,255)):
        super(myLegend, self).__init__(size, offset)
        self.background = background

    def paint(self, p, *args):
        p.setPen(mkPen(0,0,0)) # outline
        p.setBrush(mkBrush(self.background))   # background
        p.drawRect(self.boundingRect())

    def addItem(self, item, name):
        """
        Add a new entry to the legend.

        ==============  ========================================================
        **Arguments:**
        item            A PlotDataItem from which the line and point style
                        of the item will be determined or an instance of
                        ItemSample (or a subclass), allowing the item display
                        to be customized.
        title           The title to display for this item. Simple HTML allowed.
        ==============  ========================================================
        """
        label = LabelItem(name, color=(0,0,0))
        if isinstance(item, ItemSample):
            sample = item
        else:
            sample = ItemSample(item)
        row = self.layout.rowCount()
        self.items.append((sample, label))
        self.layout.addItem(sample, row, 0)
        self.layout.addItem(label, row, 1)
        self.updateSize()

class watchWorker(QObject):

    fileadded = pyqtSignal(str)
    fileremoved = pyqtSignal()

    def __init__(self):
        super(watchWorker, self).__init__()
        self.path_to_watch = "."
        self.before = dict ([(f, None) for f in os.listdir (self.path_to_watch)])
        self.timer = QTimer()
        self.timer.timeout.connect(self.checkDirectory)
        self.timer.start(100)

    def checkDirectory(self):
        after = dict ([(f, None) for f in os.listdir (self.path_to_watch)])
        added = [f for f in after if not f in self.before]
        removed = [f for f in self.before if not f in after]
        if added:
            [self.fileadded.emit(f) for f in added]
        if removed: self.fileremoved.emit()
        self.before = after

from PyQt4.QtGui import QColor

tableau20 = [(255,0,0), (0,153,255), (0,172,0), (237,69, 201), (247,173,25)]

Qtableau20 = [QColor(i,j,k) for (i,j,k) in tableau20]

class pickleGUI(QMainWindow):
    def __init__(self, parent = None, args={}):
        super(pickleGUI, self).__init__(parent)
        global app
        self.resize(1800,900)
        self.centralWidget = QWidget()
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.thread = QThread()
        self.worker = watchWorker()
        self.worker.moveToThread(self.thread)

        self.tab = QTabWidget()
        self.picklePlot = picklePlotWidget(args)

        self.picklePlot.updateFileSelectionBox()
        self.worker.fileadded.connect(self.picklePlot.updateFileSelectionBox)
        self.worker.fileremoved.connect(self.picklePlot.updateFileSelectionBox)
        self.picklePlot.loadPickle()

        self.layout.addWidget(self.picklePlot)

        self.setCentralWidget(self.centralWidget)

        self.setWindowTitle("RF Breakdown Plotter")
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        reloadSettingsAction = QAction('Reload Settings', self)
        reloadSettingsAction.setStatusTip('Reload Settings YAML File')
        reloadSettingsAction.triggered.connect(self.picklePlot.reloadSettings)
        fileMenu.addAction(reloadSettingsAction)

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(app.quit)
        fileMenu.addAction(exitAction)

class picklePlotWidget(QWidget):

    def __init__(self, args={}, **kwargs):
        super(picklePlotWidget, self).__init__(**kwargs)
        self.directory = args.directory
        self.plotWidget = QTabWidget()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.plotWidget)
        self.folderButton = QPushButton('Select Directory')
        self.folderLineEdit = QLineEdit()
        self.folderLineEdit.setReadOnly(True)
        self.folderLineEdit.setText(self.directory)
        self.folderWidget = QWidget()
        self.folderLayout = QHBoxLayout()
        self.folderLayout.addWidget(self.folderButton)
        self.folderLayout.addWidget(self.folderLineEdit)
        self.folderWidget.setLayout(self.folderLayout)
        self.folderWidget.setMaximumWidth(800)
        self.fileCombo = QComboBox()
        self.fileCombo.setMaximumWidth(800)
        self.sortByLabel = QLabel('\tSort data by:')
        self.sortByLabel.setMaximumWidth(120)
        self.sortByCombo = QComboBox()
        self.sortByCombo.addItems(['time', 'eventID', 'pos'])
        self.sortBy = 'time'
        self.fileSortWidget = QWidget()
        self.fileSortWidgetLayout = QHBoxLayout()
        self.fileSortWidgetLayout.addWidget(self.fileCombo)
        self.fileSortWidgetLayout.addWidget(self.sortByLabel)
        self.fileSortWidgetLayout.addWidget(self.sortByCombo)
        self.fileSortWidget.setLayout(self.fileSortWidgetLayout)

        self.comboWidget = QWidget()
        self.comboLayout = QVBoxLayout()
        self.comboWidget.setLayout(self.comboLayout)
        self.comboLayout.addWidget(self.folderWidget)
        self.comboLayout.addWidget(self.fileSortWidget)
        self.layout.addWidget(self.comboWidget)
        self.layout.addWidget(self.plotWidget)

        self.folderButton.clicked.connect(self.changeDirectory)
        self.fileCombo.currentIndexChanged.connect(self.loadPickle)
        self.sortByCombo.currentIndexChanged.connect(self.setSortBy)

        self.floorLine = InfiniteLine(angle=0, pen='k')
        self.outsideMaskLine = InfiniteLine(angle=90, pen='k')
        #
        # self.plotorder = [ ['new_tab', 'Power'],
        #                     'KLYSTRON_FORWARD_POWER', 'KLYSTRON_REVERSE_POWER',
        #                     'next_row',
        #                     'HRRG_CAVITY_FORWARD_POWER', 'HRRG_CAVITY_REVERSE_POWER', 'HRRG_CAVITY_PROBE_POWER',
        #                     ['new_tab', 'Phase'],
        #                     'KLYSTRON_FORWARD_PHASE', 'KLYSTRON_REVERSE_PHASE',
        #                     'next_row',
        #                     'HRRG_CAVITY_FORWARD_PHASE', 'HRRG_CAVITY_REVERSE_PHASE', 'HRRG_CAVITY_PROBE_PHASE',
        #                     ['new_tab', 'Parameters'],
        #                     'trace_name',
        #                     ]
        try:
            with open(args.settings, "r") as infile:
                self.plotorder = json.load(infile)
        except IOError:
            self.reloadSettings()
        # exit()

    def reloadSettings(self):
        self.settingsFile = str(QFileDialog.getOpenFileName(self, 'Select Settings JSON', filter="JSON files (*.json);;", selectedFilter="JSON files (*.json)"))
        with open(self.settingsFile, "r") as infile:
            self.plotorder = json.load(infile)
        # print self.plotorder
        self.loadPickle()

    def setSortBy(self, index):
        self.sortBy = str(self.sortByCombo.currentText())
        self.updatePlot()

    def mkPen(self, colorindex, index):
        color = Qtableau20[index % len(Qtableau20)]
        if index == 0:
            pen = mkPen(color=color, width=3)
        else:
            pen = mkPen(color=color, width=2, dash=[1,1])
        return pen

    def loadPickle(self):
        self.data = []
        self.tracename = ''
        filename = str(self.fileCombo.currentText())
        if filename is not '':
            # print 'filename = ', filename
            pkl_file = open(filename, 'rb')
            data1 = pickle.load(pkl_file)
            pkl_file.close()
            event = {}
            reject_strings = ['time', 'EVID', 'value']
            for k, v in data1.iteritems():
                if 'name_' in k:
                    name = v
                    if not name in event:
                        # print name
                        event[name] = {'name': name, 'type': 'data'}
                    pos = k[[i for i, j in enumerate(k) if j == '_'][-1]+1:]
                    if isinstance(data1[k.replace('name', 'EVID')], str) and 'NOT_SET' in data1[k.replace('name', 'EVID')]:
                        data1[k.replace('name', 'EVID')] = -1
                    event[name][str(pos)] = {
                                        'data': data1[k.replace('name', 'value')][:600],
                                        'eventID': data1[k.replace('name', 'EVID')],
                                        'time': data1[k.replace('name', 'time')],
                                        'pos': pos
                                        }
                elif 'lo_mask_' in k or 'hi_mask_' in k:
                    try:
                        trydict = {'name': k, 'type': 'mask', 'data': v[:600]}
                        event[k] = trydict
                        # print 'mask = ', k
                    except:
                        print 'Error reading mask: ', k
                        event[k] = {'name': k, 'type': 'parameter', 'data': v}
                elif not any([x in k for x in reject_strings]) :
                    event[k] = {'name': k, 'type': 'parameter', 'data': v}
                    if 'trace_name' in k:
                        self.tracename = v
                    if k not in self.plotorder:
                        self.plotorder.append(k)
            self.data = event
            self.updatePlot()

    def changeDirectory(self):
        self.directory = str(QFileDialog.getExistingDirectory(self, "Select Directory", self.directory, QFileDialog.ShowDirsOnly))
        self.folderLineEdit.setText(self.directory)
        self.updateFileSelectionBox()

    def updateFileSelectionBox(self, modifiedFile=None):
        fileComboIndex = self.fileCombo.currentIndex()
        self.fileCombo.clear()
        self.fileCombo.currentIndexChanged.disconnect(self.loadPickle)
        i = -1
        for file in glob.glob(self.directory+"/*.pkl"):
            i += 1
            self.fileCombo.addItem(str(file))
            if str(file) == str(modifiedFile):
                self.fileCombo.setCurrentIndex(i)
        if modifiedFile == None:
            self.fileCombo.setCurrentIndex(0)
        self.fileCombo.currentIndexChanged.connect(self.loadPickle)
        self.loadPickle()

    def updatePlot(self):
        starttime =  time.time()
        self.setUpdatesEnabled(False)
        self.plotWidget.clear()
        self.tableData = []
        alldata = self.data
        j = -1
        # for datalabel, datadict in alldata.iteritems():
        for datalabel in self.plotorder:
            if (isinstance(datalabel, list) and datalabel[0] == 'new_tab') or datalabel in alldata or datalabel == 'next_row':
                if datalabel == 'next_row':
                    graphicslayoutwidget.nextRow()
                elif datalabel[0] == 'new_tab':
                    if datalabel[1] == 'Parameters':
                        w = TableWidget()
                        self.plotWidget.addTab(w, datalabel[1])
                    else:
                        graphicslayoutwidget = GraphicsLayoutWidget()
                        self.plotWidget.addTab(graphicslayoutwidget, datalabel[1])
                else:
                    datadict = alldata[datalabel]
                    if datadict['type'] == 'data':
                        j += 1
                        p = graphicslayoutwidget.addPlot(title=datalabel)
                        legendoffset = (-10,50)
                        legend = myLegend(offset=legendoffset)
                        legend.setParentItem(p)
                        evids = [[int(i), datadict[i][self.sortBy]] for i in datadict.keys() if 'eventID' in datadict[i]]
                        evidorder =  zip(*sorted(evids, key=lambda x: x[1]))[0]
                        colorindex = -1
                        for i in evidorder:
                            colorindex += 1
                            y = datadict[str(i)]['data']
                            x = range(len(y))
                            plot = p.plot(x=x, y=y, pen=self.mkPen(0, colorindex))
                            if i < 6:
                                if self.sortBy == 'time':
                                    # signaltime = datetime.datetime.fromtimestamp(datadict[str(i)]['time']).strftime('%H:%M:%S.%f')
                                    signaltime = datadict[str(i)]['time']
                                    legend.addItem(plot, signaltime)
                                else:
                                    legend.addItem(plot, str(datadict[str(i)][self.sortBy]))
                        newRange = p.vb.state['viewRange'][0]
                        newRange[1] += 0
                        p.vb.setXRange(*newRange, padding=0)
                        # p.autoRange(padding=0.3)
                        # if self.tracename == datalabel:
                        p.setTitle('<b>'+datalabel+'</b>', color='r')
                        yLO = alldata['lo_mask_'+datalabel]['data']
                        yHI = alldata['hi_mask_'+datalabel]['data']
                        maxpoint = max(max([x for x in yLO if not math.isinf(x)]), max([x for x in yHI if not math.isinf(x)]))
                        self.plotMask(yLO, p, maxpoint, 'min')
                        self.plotMask(yHI, p, maxpoint, 'max')
                        # if 'mask_floor' in alldata:
                        #     self.floorLine.setValue(alldata['mask_floor']['data'])
                        #     p.addItem(self.floorLine)
                        # if 'outside_mask_index' in alldata:
                        #     self.outsideMaskLine.setValue(alldata['outside_mask_index']['data'])
                        #     p.addItem(self.outsideMaskLine)
                    elif datadict['type'] == 'parameter':
                        self.tableData.append([datalabel, alldata[datalabel]['data']])
        # print self.tableData
        w.setData(self.tableData)
        self.setUpdatesEnabled(True)


    def plotMask(self, y, p, filllevel, minmax):
        x = range(len(y))
        xy = zip(x, y)
        xy = [list(grp) for k, grp in groupby(xy, lambda x: math.isinf(x[1]))]
        maskno = -1
        for mask in xy:
            maskno += 1
            x, y = zip(*mask)
            # self.data['mask_'+minmax+'_'+str(maskno)+'_start'] = {'name': 'mask_'+minmax+'_'+str(maskno)+'_start', 'type': 'parameter', 'data': x[0]}
            # self.data['mask_'+minmax+'_'+str(maskno)+'_end'] = {'name': 'mask_'+minmax+'_'+str(maskno)+'_end', 'type': 'parameter', 'data': x[-1]}
            # self.plotorder.append('mask_'+minmax+'_'+str(maskno)+'_start')
            # self.plotorder.append('mask_'+minmax+'_'+str(maskno)+'_end')
            if math.isinf(y[0]):
                y = [0 for i in x]
                p.plot(x=list(x), y=y, pen=None, fillLevel=1.5*filllevel, brush=mkBrush((211,211,211,75)))
            else:
                if minmax == 'min':
                    p.plot(x=list(x), y=list(y), pen=None, fillLevel=0, brush=mkBrush((211,211,211,128)))
                else:
                    p.plot(x=list(x), y=list(y), pen=None, fillLevel=1.5*filllevel, brush=mkBrush((211,211,211,128)))

def main():
    global app
    args = parser.parse_args()
    app = QApplication(sys.argv)
    setConfigOptions(antialias=True)
    setConfigOption('background', 'w')
    setConfigOption('foreground', 'k')
    # app.setStyle(QStyleFactory.create("plastique"))
    ex = pickleGUI(args=args)
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
