import numpy as np
import pyqtgraph as pg

class HAxisRF(pg.AxisItem):
    def __init__(self, orientation=None, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        super(HAxisRF, self).__init__(parent=parent, orientation=orientation, linkView=linkView)
        self.setTickSpacing(major=20, minor=5)

    def tickStrings(self, values, scale, spacing):
        """Return the strings that should be placed next to ticks. This method is called
        when redrawing the axis and is a good method to override in subclasses.
        The method is called with a list of tick values, a scaling factor (see below), and the
        spacing between ticks (this is required since, in some instances, there may be only
        one tick and thus no other way to determine the tick spacing)

        The scale argument is used when the axis label is displaying units which may have an SI scaling prefix.
        When determining the text to display, use value*scale to correctly account for this prefix.
        For example, if the axis label's units are set to 'V', then a tick value of 0.001 might
        be accompanied by a scale value of 1000. This indicates that the label is displaying 'mV', and
        thus the tick should display 0.001 * 1000 = 1.
        """
        if self.logMode:
            return self.logTickStrings(values, scale, spacing)

        places = max(0, np.ceil(-np.log10(spacing*scale)))
        strings = []
        for v in values:
            vs = np.mod(v * scale + 180, 360) - 180
            if abs(vs) < .001 or abs(vs) >= 10000:
                vstr = "%g" % vs
            else:
                vstr = ("%%0.%df" % places) % vs
            strings.append(vstr)
        return strings

class plotWidgets(pg.GraphicsView):

    def __init__(self, cavity, approximateText='Charge', approximateUnits='pC'):
        super(plotWidgets, self).__init__()
        self.actuators = ['approx', 'dipole', 'fine', 'screen']
        self.cavity = cavity
        self.layout = pg.GraphicsLayout(border=(100,100,100))
        self.setCentralItem(self.layout)
        self.mainPlot = {}
        self.subPlots = {}
        haxisrfapprox = HAxisRF(orientation='bottom')
        self.mainPlot['approx'] = self.layout.addPlot(title="Approximate Callibration", axisItems={'bottom': haxisrfapprox})
        self.mainPlot['approx'].showGrid(x=True, y=True)
        self.mainPlot['approx'].setLabel('left', approximateText, approximateUnits)
        self.mainPlot['approx'].setLabel('bottom', text='Phase', units='Degrees')
        self.subPlots['approx'] = {}
        self.layout.nextRow()
        self.mainPlot['dipole'] = self.layout.addPlot(title="Dipole Current Set")
        self.mainPlot['dipole'].showGrid(x=True, y=True)
        self.mainPlot['dipole'].setLabel('left', text='X BPM Position', units='mm')
        self.mainPlot['dipole'].setLabel('bottom', text='Dipole Current', units='Amps')
        self.subPlots['dipole'] = {}
        self.layout.nextRow()
        haxisrffine = HAxisRF(orientation='bottom')
        self.mainPlot['fine'] = self.layout.addPlot(title="Fine BPM Callibration", axisItems={'bottom': haxisrffine})
        self.mainPlot['fine'].showGrid(x=True, y=True)
        self.mainPlot['fine'].setLabel('left', text='X BPM Position', units='mm')
        self.mainPlot['fine'].setLabel('bottom', text='Phase', units='Degrees')
        self.subPlots['fine'] = {}
        if self.cavity is not 'Gsun':
            self.layout.nextRow()
            haxisrfscreen = HAxisRF(orientation='bottom')
            self.mainPlot['screen'] = self.layout.addPlot(title="Fine Screen Callibration", axisItems={'bottom': haxisrfscreen})
            self.mainPlot['screen'].showGrid(x=True, y=True)
            self.mainPlot['screen'].setLabel('left', text='X Screen Position', units='mm')
            self.mainPlot['screen'].setLabel('bottom', text='Phase', units='Degrees')
            self.subPlots['screen'] = {}
        else:
            self.actuators = ['approx', 'dipole', 'fine']

        for a in self.actuators:
            self.subPlots[a]['data'] = self.mainPlot[a].plot(symbolPen = 'b', symbol='o', width=0, symbolSize=1, pen=None)
            self.subPlots[a]['fit'] = self.mainPlot[a].plot(pen = 'r', width=50)
            self.subPlots[a]['std'] = pg.ErrorBarItem(x=np.array([]), y=np.array([]), height=np.array([]), beam=None, pen={'color':'b', 'width':2})
            self.mainPlot[a].addItem(self.subPlots[a]['std'])

    def newData(self, cavity, actuator, data):
        actuator = str(actuator)
        try:
            if str(cavity) == self.cavity:
                # print(self.cavity, ' - Received data = ', data)
                if 'xData' in data and 'yData' in data and 'yStd' in data:
                    if actuator == 'approx' and self.cavity == 'Gun':
                        xdata, ydata, stddata = [np.array(a) for a in [data['xData'], data['yData'], data['yStd']]]
                    else:
                        newdata = zip(data['xData'], data['yData'], data['yStd'])
                        xdata, ydata, stddata = [np.array(a) for a in zip(*[a for a in newdata if a[1] is not float('nan')])]
                    self.subPlots[actuator]['data'].setData(x=xdata, y=ydata)
                    self.subPlots[actuator]['std'].setData(x=xdata, y=ydata, height=stddata)
                if 'xFit' in data and 'yFit' in data:
                    self.subPlots[actuator]['fit'].setData(x=data['xFit'], y=data['yFit'])
        except:
            pass
