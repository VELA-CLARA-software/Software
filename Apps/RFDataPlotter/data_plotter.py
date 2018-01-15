import pprint, pickle

import sys, os, time, math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import subprocess
import glob

class pickleGUI(QMainWindow):
    def __init__(self, parent = None):
        super(pickleGUI, self).__init__(parent)

        self.centralWidget = QWidget()
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.tab = QTabWidget()
        self.sddsPlot = picklePlotWidget()

        self.sddsPlot.loadPickle()

        self.layout.addWidget(self.sddsPlot)

        self.setCentralWidget(self.centralWidget)
        # self.runAndUpdate()

class picklePlotWidget(QWidget):

    def __init__(self, **kwargs):
        super(picklePlotWidget, self).__init__(**kwargs)
        self.plotWidget = pg.PlotWidget()
        self.plot1 = self.plotWidget.plot()
        self.plot2 = self.plotWidget.plot()
        self.plot3 = self.plotWidget.plot()
        self.plotLO = self.plotWidget.plot()
        self.plotHI = self.plotWidget.plot()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.plotWidget)
        self.indexCombo = QComboBox()
        self.parameterCombo = QComboBox()
        self.indexCombo.currentIndexChanged.connect(self.updatePlot)
        self.parameterCombo.currentIndexChanged.connect(self.updatePlot)
        self.comboWidget = QWidget()
        self.comboLayout = QHBoxLayout()
        self.comboWidget.setLayout(self.comboLayout)
        self.comboLayout.addWidget(self.indexCombo)
        self.comboLayout.addWidget(self.parameterCombo)
        self.layout.addWidget(self.comboWidget)
        self.layout.addWidget(self.plotWidget)

    def loadPickle(self):
        self.data = []
        pkl_file = open('test.pkl', 'rb')
        data1 = pickle.load(pkl_file)
        pkl_file.close()
        i = -1
        for key, value in data1.iteritems():
            i += 1
            event = {}
            for k, v in value.iteritems():
                # print 'key = ', k
                if 'trace_nam' in k:
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
        print len(self.data)
        # print self.data[0]['LRRG_CAVITY_REVERSE_POWER']['-1']['time']
        self.updateIndexSelectionBox()
        self.updateParameterSelectionBox()
        self.updatePlot()

    def updateIndexSelectionBox(self):
        indexCombotext = self.indexCombo.currentText()
        self.indexCombo.currentIndexChanged.disconnect(self.updatePlot)
        for index in range(len(self.data)):
            self.indexCombo.addItem(str(index))
            if str(index) == str(indexCombotext):
                self.parameterCombo.setCurrentIndex(index)
        if indexCombotext == '':
            self.indexCombo.setCurrentIndex(0)
        self.indexCombo.currentIndexChanged.connect(self.updatePlot)

    def updateParameterSelectionBox(self):
        parameterComboText = self.parameterCombo.currentText()
        self.parameterCombo.currentIndexChanged.disconnect(self.updatePlot)
        allnames = []
        for name in self.data[self.indexCombo.currentIndex()]:
            allnames.append(name)
            if self.parameterCombo.findText(name) == -1 and '_mask' not in name:
                self.parameterCombo.addItem(name)
        for index in range(self.parameterCombo.count()):
            if not self.parameterCombo.itemText(index) in allnames:
                self.parameterCombo.removeItem(index)
            else:
                if self.parameterCombo.itemText(index) == parameterComboText:
                    self.parameterCombo.setCurrentIndex(index)
        if parameterComboText == '':
            self.parameterCombo.setCurrentIndex(0)
        self.parameterCombo.currentIndexChanged.connect(self.updatePlot)

    def updatePlot(self):
        alldata = self.data[int(self.indexCombo.currentText())]
        data = alldata[str(self.parameterCombo.currentText())]
        y1 = data['1']['data']
        x1 = range(len(y1))
        self.plot1.clear()
        self.plot1.setData(x1, y1, pen=pg.mkPen(color='r', width=2))
        y2 = data['-1']['data']
        x2 = range(len(y2))
        self.plot2.clear()
        self.plot2.setData(x2, y2, pen=pg.mkPen(color='r', dash=[2,2]))
        y3 = data['-2']['data']
        x3 = range(len(y3))
        self.plot3.clear()
        self.plot3.setData(x3, y3, pen=pg.mkPen(color='r', dash=[4,4]))
        # print 'plot key = ', data.key()
        self.plotLO.clear()
        self.plotHI.clear()
        if self.tracename == str(self.parameterCombo.currentText()):
            print str(self.parameterCombo.currentText())
            yLO = alldata['lo_mask']['data']
            xLO = range(len(yLO))
            self.plotLO.setData(xLO, yLO, pen=pg.mkPen(color='b'))
            yHI = alldata['hi_mask']['data']
            xHI = range(len(yHI))
            self.plotHI.clear()
            self.plotHI.setData(xHI, yHI, pen=pg.mkPen(color='b'))

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
