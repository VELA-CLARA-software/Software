from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os
import pyqtgraph as pg
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '\\..\\..\\..\\..')
import Software.Widgets.Striptool2.generalPlot as generalplot
pg.setConfigOptions(antialias=False)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super(TimeAxisItem,self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        # PySide's QTime() initialiser fails miserably and dismisses args/kwargs
        return [time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(value)) for value in values]


class Controller():
    def __init__(self, view, model):
        '''define model and view'''
        self.view = view
        self.model = model
        # Display for y profile
        monitorData = pg.GraphicsView()
        layoutData = pg.GraphicsLayout()
        monitorData.setCentralItem(layoutData)
        self.box = layoutData.addPlot(axisItems={'bottom': TimeAxisItem(orientation='bottom')})

        #print str(self.view.timeEdit.time().hour())
        self.view.pushButton.clicked.connect(self.plotData)

        self.view.gridLayout.addWidget(monitorData)


    def plotData(self):
        self.box.clear()
        self.model.getData(self.view.lineEdit.text(),
                           self.view.calendarWidget.selectedDate(),
                           self.view.timeEdit.time(),
                           self.view.calendarWidget_2.selectedDate(),
                           self.view.timeEdit_2.time())
        self.box.plot(x=self.model.secs, y=self.model.vals, pen='g')
