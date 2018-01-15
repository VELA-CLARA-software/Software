import pickle
import sys, os, time, math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import glob

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
    def __init__(self, parent = None):
        super(pickleGUI, self).__init__(parent)
        self.resize(1000,900)
        self.centralWidget = QWidget()
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.thread = QThread()
        self.worker = watchWorker()
        self.worker.moveToThread(self.thread)

        self.tab = QTabWidget()
        self.picklePlot = picklePlotWidget()

        self.picklePlot.updateFileSelectionBox()
        self.worker.fileadded.connect(self.picklePlot.updateFileSelectionBox)
        self.worker.fileremoved.connect(self.picklePlot.updateFileSelectionBox)
        self.picklePlot.loadPickle()

        self.layout.addWidget(self.picklePlot)

        self.setCentralWidget(self.centralWidget)

class picklePlotWidget(QWidget):

    def __init__(self, **kwargs):
        super(picklePlotWidget, self).__init__(**kwargs)
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.plotWidget)
        self.indexCombo = QComboBox()
        self.indexCombo.currentIndexChanged.connect(self.updatePlot)
        self.fileCombo = QComboBox()
        self.fileCombo.currentIndexChanged.connect(self.loadPickle)
        self.comboWidget = QWidget()
        self.comboLayout = QHBoxLayout()
        self.comboWidget.setLayout(self.comboLayout)
        self.comboLayout.addWidget(self.fileCombo)
        self.comboLayout.addWidget(self.indexCombo)
        self.layout.addWidget(self.comboWidget)
        self.layout.addWidget(self.plotWidget)
        self.pens = pg.mkPen(color='r', dash=[4,4])
        self.plotorder = [  'KLYSTRON_FORWARD_POWER', 'LRRG_CAVITY_FORWARD_POWER', 'next_row',
                            'KLYSTRON_REVERSE_POWER', 'LRRG_CAVITY_REVERSE_POWER', 'next_row',
                            'KLYSTRON_FORWARD_PHASE', 'LRRG_CAVITY_FORWARD_PHASE', 'next_row',
                            'KLYSTRON_REVERSE_PHASE',  'LRRG_CAVITY_REVERSE_PHASE', 'next_row',
                            'hi_mask', 'lo_mask']

    def mkPen(self, colorindex, index):
        color = Qtableau20[index]
        if index == -2:
            pen = pg.mkPen(color=color, dash=[6,6])
        elif index == -1:
            pen = pg.mkPen(color=color, dash=[4,4])
        elif index == 0:
            pen = pg.mkPen(color=color, width=2)
        elif index == 1:
            pen = pg.mkPen(color=color, dash=[2,2])
        return pen

    def loadPickle(self):
        self.data = []
        filename = str(self.fileCombo.currentText())
        if filename is not '':
            pkl_file = open(filename, 'rb')
            data1 = pickle.load(pkl_file)
            pkl_file.close()
            i = -1
            for key, value in data1.iteritems():
                i += 1
                event = {}
                for k, v in value.iteritems():
                    # print 'key = ', k
                    if 'trace_name' in k:
                        self.tracename = v
                    if 'name_' in k:
                        name = v
                        if not name in event:
                            event[name] = {'-1': dict(), '-2': dict(), '0': dict(), '1': dict}
                        pos = k[[i for i, j in enumerate(k) if j == '_'][-1]+1:]
                        # print 'pos = ', pos, '  name = ', name
                        event[name][pos] = { 'data': value[k.replace('name', 'value')],
                                            'eventID': value[k.replace('name', 'EVID')],
                                            'time': value[k.replace('name', 'time')]
                                            }
                    elif '_mask' in k:
                        # print 'k = ', k
                        event[k] = {'data': v}
                        # print event.keys()
                self.data.append(event)
            # print len(self.data)
            # print self.data[0]['LRRG_CAVITY_REVERSE_POWER']['-1']['time']
            self.updateIndexSelectionBox()
            self.updatePlot()

    def updateIndexSelectionBox(self):
        indexCombotext = self.indexCombo.currentText()
        self.indexCombo.clear()
        self.indexCombo.currentIndexChanged.disconnect(self.updatePlot)
        for index in range(len(self.data)):
            self.indexCombo.addItem(str(index))
            if str(index) == str(indexCombotext):
                self.indexCombo.setCurrentIndex(index)
        if indexCombotext == '':
            self.indexCombo.setCurrentIndex(0)
        self.indexCombo.currentIndexChanged.connect(self.updatePlot)

    def updateFileSelectionBox(self, modifiedFile=None):
        fileComboIndex = self.fileCombo.currentIndex()
        self.fileCombo.clear()
        self.fileCombo.currentIndexChanged.disconnect(self.loadPickle)
        i = -1
        for file in glob.glob("*.pkl"):
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
        if not self.indexCombo.currentText() == '':
            alldata = self.data[int(self.indexCombo.currentText())]
            j = -1
            # for datalabel, datadict in alldata.iteritems():
            for datalabel in self.plotorder:
                if datalabel in alldata or datalabel == 'next_row':
                    if datalabel == 'next_row':
                        self.plotWidget.nextRow()
                    else:
                        datadict = alldata[datalabel]
                        if len(datadict) > 1:
                            j += 1
                            p = self.plotWidget.addPlot(title=datalabel)
                            for i in range(-2,1):
                                y = datadict[str(i)]['data']
                                x = range(len(y))
                                p.plot(x=x, y=y, pen=self.mkPen(0, i))
                            if self.tracename == datalabel:
                                p.setTitle('<b>'+datalabel+'</b>', color='r')
                                yLO = alldata['lo_mask']['data']
                                xLO = range(len(yLO))
                                yHI = alldata['hi_mask']['data']
                                xHI = range(len(yHI))
                                p.plot(x=xLO, y=yLO, pen=pg.mkPen(color='b', width=0.25))
                                p.plot(x=xHI, y=yHI, pen=pg.mkPen(color='b', width=0.25))

def main():
   app = QApplication(sys.argv)
   pg.setConfigOptions(antialias=True)
   pg.setConfigOption('background', 'w')
   pg.setConfigOption('foreground', 'k')
   # app.setStyle(QStyleFactory.create("plastique"))
   ex = pickleGUI()
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
