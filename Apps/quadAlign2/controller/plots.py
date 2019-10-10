import numpy as np
import pyqtgraph as pg

pg.setConfigOption('background', 'w')

class plotWidgets(pg.GraphicsView):

    def __init__(self, sensor):
        super(plotWidgets, self).__init__()
        self.sensor = sensor
        self.actuators = ['S01-HCOR2', 'S01-VCOR2']
        self.layout = pg.GraphicsLayout(border=(100,100,100))
        self.setCentralItem(self.layout)
        self.mainPlot = {}
        self.subPlots = {}
        self.mainPlot['BPM'] = self.layout.addPlot(title=self.sensor+" Callibration")
        self.mainPlot['BPM'].showGrid(x=True, y=True)
        self.mainPlot['BPM'].setLabel('left', 'BPM Reading', 'mm')
        self.mainPlot['BPM'].setLabel('bottom', text='Corrector', units='Amps')

        for a in ['BPM']:
            for b in self.actuators:
                self.subPlots[b] = {}
            self.subPlots['S01-HCOR2']['negative'] = self.mainPlot[a].plot(symbolPen = 'b', symbol='o', width=0, symbolSize=9, symbolBrush='w', pen=None)
            self.subPlots['S01-HCOR2']['positive'] = self.mainPlot[a].plot(symbolPen = 'r', symbol='o', width=0, symbolSize=9, symbolBrush='w', pen=None)
            self.subPlots['S01-VCOR2']['negative'] = self.mainPlot[a].plot(symbolPen = 'k', symbol='o', width=0, symbolSize=9, symbolBrush='w', pen=None)
            self.subPlots['S01-VCOR2']['positive'] = self.mainPlot[a].plot(symbolPen = 'm', symbol='o', width=0, symbolSize=9, symbolBrush='w', pen=None)

    def newData(self, actuator, polarity, data):
        actuator = str(actuator)
        polarity = str(polarity)
        # try:
        xdata, ydata = [np.array(a) for a in [data['xData'], data['yData']]]
        self.subPlots[actuator][polarity].setData(x=xdata, y=ydata)
        # except:
            # pass
