from pv import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
import numpy as np
from full_gauge import *
from bpmWidget import *

class testPV(QMainWindow):
    def __init__(self, parent = None):
        super(testPV, self).__init__(parent)
        PVs = ['MS1QUA03_cmd', 'MS1QUA04_cmd']

        stdicon = self.style().standardIcon
        style = QStyle
        self.setWindowTitle("Testing PVs Application")

        self.stylesheet = "stylesheet.qss"
        with open(self.stylesheet,"r") as fh:
            self.setStyleSheet(fh.read())

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.layout = QHBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.groupBox = groupBox()
        self.layout.addWidget(self.groupBox)

        for pv in PVs:
            self.groupBox.addWidget(epicsSliderWidget(PVBuffer(pv)))
        for f in ['IA1BPA01', 'IA1BPB01', 'IA3BPC01']:
            chart = epicsBPM2D(f)
            self.layout.addWidget(chart)

class epicsWidget(QWidget):
    def __init__(self, pv=None, parent = None):
        super(epicsWidget, self).__init__(parent=parent)
        self.setMaximumHeight(200)
        self.pv = pv

    def changeValue(self, value):
        print ('new value ', self.pv.name, ' = ', value)

    @property
    def lineEditChildren(self):
        return self.findChildren(epicsTextWidget)

    def pauseUpdating(self):
        for child in self.lineEditChildren:
            self.pv.newValue.disconnect(child.updateValue)

    def startUpdating(self):
        for child in self.lineEditChildren:
            self.pv.newValue.connect(child.updateValue)

    def updateValue(self, value):
        pass

class epicsBPM2D(QWidget):
    def __init__(self, pv, parent = None):
        super(epicsBPM2D, self).__init__(parent=parent)
        self.setMinimumWidth(250)
        self.setMinimumHeight(600)
        self.pvh = PVObject(pv+'_H')
        print (self.pvh.pv.upper_disp_limit)
        self.pvv = PVObject(pv+'_V')
        self.pvi = PVObject(pv+'_I')
        self.pvph = PVObject(pv+'_PH')
        self.pvh_ref = PVObject(pv+'_H_ref')
        self.pvv_ref = PVObject(pv+'_V_ref')
        self.pvi_ref = PVObject(pv+'_I_ref')
        self.pvph_ref = PVObject(pv+'_PH_ref')

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.bpmWidget = bpmWidget(pv)
        self.bpmWidget.positionWidget.setScaleX(self.pvh.pv.upper_disp_limit)
        self.bpmWidget.positionWidget.setScaleY(self.pvv.pv.upper_disp_limit)
        self.layout.addWidget(self.bpmWidget)
        self.updateValues()
        self.pvh.newValue.connect(self.bpmWidget.set_x)
        self.pvv.newValue.connect(self.bpmWidget.set_y)
        self.pvh_ref.newValue.connect(self.bpmWidget.set_x_ref)
        self.pvv_ref.newValue.connect(self.bpmWidget.set_y_ref)

        self.pvi.newValue.connect(self.bpmWidget.set_I)
        self.pvi_ref.newValue.connect(self.bpmWidget.set_I_ref)
        self.pvph.newValue.connect(self.bpmWidget.set_phase)
        self.pvph_ref.newValue.connect(self.bpmWidget.set_phase_ref)

    def updateValues(self):
        self.bpmWidget.set_x(*self.pvh.get())
        self.bpmWidget.set_x_ref(*self.pvh_ref.get())
        self.bpmWidget.set_y(*self.pvv.get())
        self.bpmWidget.set_y_ref(*self.pvv_ref.get())
        self.bpmWidget.set_phase(*self.pvph.get())
        self.bpmWidget.set_phase_ref(*self.pvph_ref.get())
        self.bpmWidget.set_I(*self.pvi.get())
        self.bpmWidget.set_I_ref(*self.pvi_ref.get())

class QCustomSlider(QWidget):
    def __init__(self, sliderOrientation=Qt.Vertical, parent = None):
        super(QCustomSlider, self).__init__(parent=parent)
        self.orientation = sliderOrientation
        self._size = 30
        self.setFixedSize(5*self._size, 5*self._size)
        self._slider = QDial()
        self._slider.setFixedSize(3*self._size,3*self._size)
        self.setRange(0, 360)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self._slider, 0, 0, 3, 3)
        listWithLabels = [[0,2,0, Qt.AlignRight], [360,2,2, Qt.AlignLeft], [180 ,0, 1, Qt.AlignCenter]]
        lengthOfList = len(listWithLabels)
        for index in listWithLabels:
            label = QLabel(str(index[0]))
            label.setAlignment(index[3])
            
            label.setFixedSize(1*self._size, 1*self._size)
            label.setContentsMargins(0, 0, 0, 0)
            self.layout.addWidget(label, index[1], index[2], 1,1)

    def setRange(self, mini, maxi):
        self._slider.setRange(mini, maxi)

    def setPageStep(self, value):
        self._slider.setPageStep(value)

    def setTickInterval(self, value):
        self._slider.setTickInterval(value)

    def setTickPosition(self, position):
        self._slider.setTickPosition(position)

    def setValue(self, value):
        self._slider.setValue(value)

    def onValueChangedCall(self, function):
        self._slider.valueChanged.connect(function)

class BPMChart(QChartView):
    def __init__(self, color=None, parent = None):
        super(BPMChart, self).__init__(parent=parent)
        self.chart = QChart()        
        self.chart.legend().hide()
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)

        self.series = BPMSeries(Qt.red)
        self.chart.addSeries(self.series)

        self.series_ref = BPMSeries(Qt.blue)
        self.chart.addSeries(self.series_ref)

        self.chart.createDefaultAxes()
        self.chart.axisX().setRange(-20,20)
        self.chart.axisY().setRange(-20,20)


class BPMSeries(QScatterSeries):
    def __init__(self, color=None, parent = None):
        super(BPMSeries, self).__init__(parent=parent)
        self.x = 0
        self.y = 0
        self.setMarkerShape(QScatterSeries.MarkerShapeCircle)
        self.append(self.x, self.y)
        self.setColor(color)

    def setColor(self, color):
        self.color = color
        pen = self.pen()
        if color is not None:
            pen.setColor(color)
        pen.setWidthF(.1)
        self.setPen(pen)

    def updateValueX(self, time, value):
        self.x = value
        self.update()

    def updateValueY(self, time, value):
        self.y = value
        self.update()
    
    def update(self):
        self.replace(0, self.x, self.y)

class epicsTextWidget(epicsWidget):
    def __init__(self, pv=None, parent = None):
        super(epicsTextWidget, self).__init__(pv=pv, parent=parent)
        self.pv.newValue.connect(self.updateValue)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel(self.pv.name)
        self.textBox = QLineEdit()
        self.textBox.setText("{0:.3f}".format(self.pv.lastValue()))
        self.textBox.setReadOnly(True)
        self.textBox.setMinimumWidth(40)
        self.textBox.setMaximumWidth(60)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.textBox)

    def updateValue(self, time, value):
        self.textBox.setText("{0:.3f}".format(value))

class epicsSliderWidget(epicsWidget):
    def __init__(self, pv=None, multiplier=100, parent = None):
        super(epicsSliderWidget, self).__init__(pv=pv, parent=parent)
        self.multiplier = multiplier
        self.setMouseTracking(True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.textWidget = epicsTextWidget(pv)

        self.slider = QDoubleSlider(self.multiplier, Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus);

        self.slider.setTickPosition(QSlider.TicksBothSides);
        self.slider.setTickInterval(1);
        self.slider.setSingleStep(0.01);
        self.slider.setPageStep(0.1)
        self.slider.setRange(-10,10)
        self.slider.setTracking(False)
        self.slider.valueChanged.connect(self.changeValue)
        self.slider.sliderPressed.connect(self.pauseUpdating)
        self.slider.sliderReleased.connect(self.startUpdating)

        self.groupBox = highlightingGroupBox(pv.name, self.slider)
        self.groupBoxLayout = QVBoxLayout()
        self.groupBox.setLayout(self.groupBoxLayout)

        self.groupBoxLayout.addWidget(self.textWidget)
        self.groupBoxLayout.addWidget(self.slider)

        self.layout.addWidget(self.groupBox)


    def changeValue(self, value):
        value = float(self.slider.value()) / self.multiplier
        print ('new value ', self.pv.name, ' = ', value)

    def updateValue(self, time, value):
        self.slider.setValue(value*multiplier)

class highlightingGroupBox(QGroupBox):
    """group box with highlighting"""
    def __init__(self, label = None, focus = None, parent = None):
        super(highlightingGroupBox, self).__init__(parent)
        self.focusWidget = focus
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        self.focusWidget.setFocus()
        self.setStyleSheet("""
               QGroupBox 
               { 
                   background-color: rgb(255, 255,255); 
                   border:1px solid rgb(50, 50, 50);
                   border-radius: 9px;
                   margin-top: 0.5em;
               }
               """
        )

    def leaveEvent(self, event):
        self.setStyleSheet("")

class groupBox(QGroupBox):
    """group box."""
    def __init__(self, parent = None):
        super(groupBox, self).__init__(parent)
        self.table = QGridLayout()
        self.table.setRowStretch(0,0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True) # CRITICAL
        inner = QFrame(scroll)
        inner.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        inner.setLayout(self.table)
        scroll.setWidget(inner) # CRITICAL
        gLayout = QVBoxLayout()
        gLayout.addWidget(scroll)
        self.setLayout(gLayout)
        self.row = 0
        self.knobs = {}

    def addWidget(self, widget):
        self.knobs[self.row] = widget
        self.table.addWidget(widget, self.row, 0)
        self.row += 1

class QDoubleSlider(QSlider):

    def __init__(self, multiplier=100, *args, **kwargs):
        super(QSlider, self).__init__(*args, **kwargs)
        self.multiplier = multiplier
      
    def setRange(self, min, max):
        super(QDoubleSlider, self).setRange(self.multiplier*min, self.multiplier*max)

    def setPageStep(self, step):
        super(QDoubleSlider, self).setPageStep(self.multiplier*step)

    def setSingleStep(self, step):
        super(QDoubleSlider, self).setSingleStep(self.multiplier*step)

    def setTickInterval(self, interval):
        super(QDoubleSlider, self).setTickInterval(self.multiplier*interval)

def main():
   app = QApplication(sys.argv)
   ex = testPV()
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
