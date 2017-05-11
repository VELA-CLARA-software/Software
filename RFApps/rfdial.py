import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import epics

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.phasePV = epics.PV('CLA-GUNS-LRF-CTRL-01:vm:dsp:sp_ph:phase')
        self.phasedial = QDial()
        self.phasedial.setNotchesVisible(False)
        self.phasedial.setRange(-180,180)
        self.phasespinbox = QSpinBox()
        self.phasespinbox.setRange(-180,180)
        self.phasedial.setValue(self.phasePV.get())
        self.phasespinbox.setValue(self.phasePV.get())
        phaselayout = QHBoxLayout()
        phaselayout.addWidget(self.phasedial)
        phaselayout.addWidget(self.phasespinbox)
        phasewidget = QWidget()
        phasewidget.setLayout(phaselayout)

        self.ampPV = epics.PV('CLA-GUNS-LRF-CTRL-01:vm:dsp:sp_amp:amplitude')
        self.ampdial = QDial()
        self.ampdial.setNotchesVisible(False)
        self.ampdial.setRange(0,14500)
        self.ampspinbox = QSpinBox()
        self.ampspinbox.setRange(0,14500)
        self.ampdial.setValue(self.ampPV.get())
        self.ampspinbox.setValue(self.ampPV.get())
        amplayout = QHBoxLayout()
        amplayout.addWidget(self.ampdial)
        amplayout.addWidget(self.ampspinbox)
        ampwidget = QWidget()
        ampwidget.setLayout(amplayout)

        layout = QVBoxLayout()
        layout.addWidget(ampwidget)
        layout.addWidget(phasewidget)

        self.setLayout(layout)

        self.phasedial.valueChanged.connect(self.phasespinbox.setValue)
        self.phasespinbox.valueChanged.connect(self.phasedial.setValue)
        self.phasespinbox.valueChanged.connect(self.setRFPhase)

        self.ampdial.valueChanged.connect(self.ampspinbox.setValue)
        self.ampspinbox.valueChanged.connect(self.ampdial.setValue)
        self.ampspinbox.valueChanged.connect(self.setRFAmplitude)

        self.setWindowTitle("RF Dials")

    def setRFAmplitude(self):
        self.ampPV.put(self.ampspinbox.value())

    def setRFPhase(self):
        self.phasePV.put(self.phasespinbox.value())

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
