import sys, math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import epics

class eSlider(QSlider):
    def __init__(self, parent=None, min=-10, max=10, orientation=Qt.Horizontal, factor=1):
        QSlider.__init__(self, parent)
        self.factor = factor
        self.min = min*self.factor
        self.max = max*self.factor
        self.range = self.max - self.min
        self.setOrientation(orientation)
        self.setValue(0)

    def wheelEvent(self, evt):
        modifiers = QApplication.keyboardModifiers()
        val = self.value()
        if modifiers == Qt.ControlModifier:
            step = self.singleStep()/10
        elif modifiers == Qt.ShiftModifier:
            step = self.singleStep()*10
        else:
            step = self.singleStep()
        step = math.copysign(step,evt.delta())
        self.setValue(step+val)

class eDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None, min=-10, max=10, factor=1):
        QDoubleSpinBox.__init__(self, parent)
        self.factor = factor
        self.min = min*self.factor
        self.max = max*self.factor
        self.range = self.max - self.min
        self.setValue(0)

    def wheelEvent(self, evt):
        modifiers = QApplication.keyboardModifiers()
        val = self.value()
        if modifiers == Qt.ControlModifier:
            step = self.singleStep()/10
        elif modifiers == Qt.ShiftModifier:
            step = self.singleStep()*10
        else:
            step = self.singleStep()
        step = math.copysign(step,evt.delta())
        self.setValue(step+val)

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # self.phasePV = epics.PV('CLA-GUNS-LRF-CTRL-01:vm:dsp:sp_ph:phase')
        # self.ampPV = epics.PV('CLA-GUNS-LRF-CTRL-01:vm:dsp:sp_amp:amplitude')

        self.ampgroupbox = self.sliderAndSpinBox("RF Amplitude", 'CLA-GUNS-LRF-CTRL-01:vm:dsp:sp_amp:amplitude', 0, 14500, step=100)
        self.phasegroupbox = self.sliderAndSpinBox("RF Phase", 'CLA-GUNS-LRF-CTRL-01:vm:dsp:sp_ph:phase' , -180, 180, step=1)

        layout = QHBoxLayout()
        layout.addWidget(self.ampgroupbox)
        layout.addWidget(self.phasegroupbox)

        self.setLayout(layout)

        self.setWindowTitle("RF Controls")

    def magnetController(self, name):
        pass

    def sliderAndSpinBox(self, name, pvname, min, max, step=1, sliderfactor=10):
        pv = epics.PV(pvname)
        slider = eSlider(min=min, max=max, factor=sliderfactor, orientation=Qt.Horizontal)
        slider.setRange(min*sliderfactor, max*sliderfactor)
        slider.setValue(pv.get()*sliderfactor)
        slider.setSingleStep(sliderfactor*step)
        slider.setPageStep(sliderfactor*step*10)

        spinbox = eDoubleSpinBox()
        spinbox.setRange(min,max)
        spinbox.setValue(pv.get())
        spinbox.setSingleStep(step)
        # spinbox.setPageStep(step*10)

        layout = QHBoxLayout()
        layout.addWidget(slider)
        layout.addWidget(spinbox)
        widget = QWidget()
        widget.setLayout(layout)
        groupbox = QGroupBox(self)
        groupbox.setTitle(name)
        groupbox.setLayout(layout)
        slider.valueChanged.connect(lambda x: spinbox.setValue(float(x)/float(sliderfactor)))
        spinbox.valueChanged.connect(lambda x: slider.setValue(float(x)*float(sliderfactor)))
        spinbox.valueChanged.connect(lambda x: self.setPV(pv, x))
        epics.camonitor(pvname, callback=lambda **x: self.updateControls(slider,spinbox,**x))
        return groupbox

    def updateControls(self, slider, spinbox, **kwargs):
        spinbox.setValue(kwargs['value'])

    def setPV(self, pv, val):
        # pass
        pv.put(val)

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
