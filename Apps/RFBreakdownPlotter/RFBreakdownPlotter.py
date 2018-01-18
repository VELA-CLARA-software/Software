import pickle
import sys, os, time, math, datetime
from PyQt4.QtCore import QObject, pyqtSignal, QThread, QTimer
from PyQt4.QtGui import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QTabWidget, QLineEdit, QFileDialog
import pyqtgraph as pg
import glob
from itertools import groupby
import argparse

parser = argparse.ArgumentParser(description='Monitor a directory for RF breakdown traces')
parser.add_argument('-d', '--directory', default='.')

class myLegend(pg.LegendItem):
    def __init__(self, size=None, offset=None, background=(255,255,255,255)):
        super(myLegend, self).__init__(size, offset)
        self.background = background

    def paint(self, p, *args):
        p.setPen(pg.mkPen(0,0,0)) # outline
        p.setBrush(pg.mkBrush(self.background))   # background
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
        label = pg.LabelItem(name, color=(0,0,0))
        if isinstance(item, pg.graphicsItems.LegendItem.ItemSample):
            sample = item
        else:
            sample = pg.graphicsItems.LegendItem.ItemSample(item)
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

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

Qtableau20 = [QColor(i,j,k) for (i,j,k) in tableau20]

class pickleGUI(QMainWindow):
    def __init__(self, parent = None, directory='.'):
        super(pickleGUI, self).__init__(parent)
        self.resize(1800,900)
        self.centralWidget = QWidget()
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.thread = QThread()
        self.worker = watchWorker()
        self.worker.moveToThread(self.thread)

        self.tab = QTabWidget()
        self.picklePlot = picklePlotWidget(directory)

        self.picklePlot.updateFileSelectionBox()
        self.worker.fileadded.connect(self.picklePlot.updateFileSelectionBox)
        self.worker.fileremoved.connect(self.picklePlot.updateFileSelectionBox)
        self.picklePlot.loadPickle()

        self.layout.addWidget(self.picklePlot)

        self.setCentralWidget(self.centralWidget)

class picklePlotWidget(QWidget):

    def __init__(self, directory='.', **kwargs):
        super(picklePlotWidget, self).__init__(**kwargs)
        self.directory = directory
        self.plotWidget = QTabWidget()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.plotWidget)
        self.folderButton = QPushButton('Select Directory')
        self.folderButton.clicked.connect(self.changeDirectory)
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
        self.fileCombo.currentIndexChanged.connect(self.loadPickle)
        self.fileCombo.setMaximumWidth(800)
        self.comboWidget = QWidget()
        self.comboLayout = QVBoxLayout()
        self.comboWidget.setLayout(self.comboLayout)
        self.comboLayout.addWidget(self.folderWidget)
        self.comboLayout.addWidget(self.fileCombo)
        self.layout.addWidget(self.comboWidget)
        self.layout.addWidget(self.plotWidget)
        self.pens = pg.mkPen(color='r', dash=[4,4])
        self.plotorder = [ ['new_tab', 'Power'],
                            'KLYSTRON_FORWARD_POWER', 'KLYSTRON_REVERSE_POWER',
                            'next_row',
                            'LRRG_CAVITY_FORWARD_POWER', 'LRRG_CAVITY_REVERSE_POWER',
                            ['new_tab', 'Phase'],
                            'KLYSTRON_FORWARD_PHASE', 'KLYSTRON_REVERSE_PHASE',
                            'next_row',
                            'LRRG_CAVITY_FORWARD_PHASE', 'LRRG_CAVITY_REVERSE_PHASE',
                            ['new_tab', 'Parameters'],
                            'trace_name',
                            ]

    def mkPen(self, colorindex, index):
        color = Qtableau20[index]
        if index == -2:
            pen = pg.mkPen(color='g', dash=[6,6])
        elif index == -1:
            pen = pg.mkPen(color='b', dash=[4,4])
        elif index == 0:
            pen = pg.mkPen(color='r', width=2)
        elif index == 1:
            pen = pg.mkPen(color='k', dash=[2,2])
        return pen

    def loadPickle(self):
        self.data = []
        filename = str(self.fileCombo.currentText())
        if filename is not '':
            # print 'filename = ', filename
            pkl_file = open(filename, 'rb')
            data1 = pickle.load(pkl_file)
            pkl_file.close()
            event = {}
            for k, v in data1.iteritems():

                if 'trace_name' in k:
                    self.tracename = v
                    event[k] = {'data': v}
                if 'name_' in k:
                    name = v
                    if not name in event:
                        # print name
                        event[name] = dict()
                    pos = k[[i for i, j in enumerate(k) if j == '_'][-1]+1:]
                    # print name, '  ', pos
                    event[name][str(pos)] = {'data': data1[k.replace('name', 'value')][:600],
                                        'eventID': data1[k.replace('name', 'EVID')],
                                        'time': data1[k.replace('name', 'time')],
                                        'pos': pos
                                        }
                elif '_mask' in k:
                    event[k] = {'data': v[:600]}
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
        self.plotWidget.clear()
        self.tableData = {}
        alldata = self.data
        j = -1
        # for datalabel, datadict in alldata.iteritems():
        for datalabel in self.plotorder:
            if (isinstance(datalabel, list) and datalabel[0] == 'new_tab') or datalabel in alldata or datalabel == 'next_row':
                if datalabel == 'next_row':
                    graphicslayoutwidget.nextRow()
                elif datalabel[0] == 'new_tab':
                    if datalabel[1] == 'Parameters':
                        w = pg.TableWidget()
                        self.plotWidget.addTab(w, datalabel[1])
                    else:
                        graphicslayoutwidget = pg.GraphicsLayoutWidget()
                        self.plotWidget.addTab(graphicslayoutwidget, datalabel[1])
                else:
                    datadict = alldata[datalabel]
                    # print 'keys = ', datadict.keys()
                    if len(datadict.keys()) > 1:
                        j += 1
                        p = graphicslayoutwidget.addPlot(title=datalabel)
                        legendoffset = (-10,50)
                        legend = myLegend(offset=legendoffset)
                        legend.setParentItem(p)
                        legendoffsett = list(legendoffset)
                        legendoffsett[1] += 150
                        legendt = myLegend(offset=legendoffsett)
                        legendt.setParentItem(p)
                        evids = [[int(i), datadict[str(i)]['time']] for i in datadict.keys() if 'eventID' in datadict[str(i)]]
                        # print datalabel
                        # print 'evids = ', evids
                        # print 'sorted evids = ', sorted(evids, key=lambda x: x[1])
                        evidorder =  zip(*sorted(evids, key=lambda x: x[1]))[0]
                        for i in evidorder:
                            y = datadict[str(i)]['data']
                            x = range(len(y))
                            plot = p.plot(x=x, y=y, pen=self.mkPen(0, i))
                            legend.addItem(plot, str(datadict[str(i)]['eventID']))
                            time = datetime.datetime.fromtimestamp(datadict[str(i)]['time']).strftime('%H:%M:%S.%f')
                            legendt.addItem(plot, time)
                        newRange = p.vb.state['viewRange'][0]
                        newRange[1] += 0
                        p.vb.setXRange(*newRange, padding=0)
                        # p.autoRange(padding=0.3)
                        if self.tracename == datalabel:
                            p.setTitle('<b>'+datalabel+'</b>', color='r')
                            yLO = alldata['lo_mask']['data']
                            yHI = alldata['hi_mask']['data']
                            maxpoint = max(max([x for x in yLO if not math.isinf(x)]), max([x for x in yHI if not math.isinf(x)]))
                            self.plotMask(yLO, p, maxpoint, 'min')
                            self.plotMask(yHI, p, maxpoint, 'max')
                    else:
                        self.tableData[datalabel] = datadict
        w.setData(self.tableData)

    def plotMask(self, y, p, filllevel, minmax):
        x = range(len(y))
        xy = zip(x, y)
        xy = [list(grp) for k, grp in groupby(xy, lambda x: math.isinf(x[1]))]
        for mask in xy:
            x, y = zip(*mask)
            if math.isinf(y[0]):
                y = [0 for i in x]
                p.plot(x=list(x), y=y, pen=None, fillLevel=1.5*filllevel, brush=pg.mkBrush((211,211,211,75)))
            else:
                if minmax == 'min':
                    p.plot(x=list(x), y=list(y), pen=None, fillLevel=0, brush=pg.mkBrush((211,211,211,128)))
                else:
                    p.plot(x=list(x), y=list(y), pen=None, fillLevel=1.5*filllevel, brush=pg.mkBrush((211,211,211,128)))

def main():
    args = parser.parse_args()
    app = QApplication(sys.argv)
    pg.setConfigOptions(antialias=True)
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    # app.setStyle(QStyleFactory.create("plastique"))
    ex = pickleGUI(directory=args.directory)
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
