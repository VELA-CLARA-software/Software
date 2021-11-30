import sys, os
sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\packages\\CATAP\\bin')
sys.path.append('..\\..\\Utils\\MachineState\\Version 2')
from CATAP.HardwareFactory import *
import src.machine_state as machine_state
import time
from datetime import datetime

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QDoubleSpinBox, QLabel
from PyQt5 import QtCore
from PyQt5 import QtGui

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.gun_calibration_data = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\2021\\07\\27\\Gun_power_momentum_scan_cathode22.xlsx'
        self.l01_calibration_data = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\2021\\07\\28\\Linac_power_momentum_scan_cathode22.xlsx'


    def initUI(self):

        self.mainVBox = QVBoxLayout()

        self.gunCrestHBox = QHBoxLayout()
        self.gunCrestLabel = QLabel("Gun Crest (deg)", self)
        self.gunCrest = QDoubleSpinBox()
        self.gunCrest.setDecimals(1)
        self.gunCrest.setMinimum(-180)
        self.gunCrest.setMaximum(180)
        self.gunCrest.setSingleStep(1)
        self.gunCrest.setProperty("value", 0)
        self.gunCrestLabel.setFont(QtGui.QFont('Times', 10))
        self.gunCrest.setFont(QtGui.QFont('Times', 10))
        self.gunCrestHBox.addWidget(self.gunCrestLabel)
        self.gunCrestHBox.addWidget(self.gunCrest)
        self.l01CrestHBox = QHBoxLayout()
        self.l01CrestLabel = QLabel("Linac 1 Crest (deg)", self)
        self.l01Crest = QDoubleSpinBox()
        self.l01Crest.setDecimals(1)
        self.l01Crest.setMinimum(-180)
        self.l01Crest.setMaximum(180)
        self.l01Crest.setSingleStep(1)
        self.l01Crest.setProperty("value", 0)
        self.l01CrestLabel.setFont(QtGui.QFont('Times', 10))
        self.l01Crest.setFont(QtGui.QFont('Times', 10))
        self.l01CrestHBox.addWidget(self.l01CrestLabel)
        self.l01CrestHBox.addWidget(self.l01Crest)

        self.qbtn = QPushButton()
        self.qbtn.setMinimumSize(QtCore.QSize(300, 300))
        self.qbtn.setFont(QtGui.QFont('Times', 15))
        self.qbtn.setText('Save snapshot')
        self.qbtn.clicked.connect(self.saveSnapshot)

        self.fileLocationLabel = QLabel("", self)
        self.fileLocationLabel.setFont(QtGui.QFont('Times', 10))

        self.mainVBox.addLayout(self.gunCrestHBox)
        self.mainVBox.addLayout(self.l01CrestHBox)
        self.mainVBox.addWidget(self.qbtn)
        self.mainVBox.addWidget(self.fileLocationLabel)
        self.mainVBox.addStretch(1)

        self.setLayout(self.mainVBox)

        self.setWindowTitle('Save Machine Snapshot')
        self.resize(850, 400)
        self.show()

    def saveSnapshot(self):#
        self.filename = self.getSnapshotDirectory()
        self.qbtn.setText("Saving....")
        QApplication.processEvents()
        self.gun_name = 'CLA-LRG1-GUN-CAV'
        self.l01_name = 'CLA-L01-CAV'

        self.crest_phases = {}
        self.crest_phases.update({self.gun_name: self.gunCrest.value()})
        self.crest_phases.update({self.l01_name: self.l01Crest.value()})

        # Set up CATAP
        self.mode = STATE.PHYSICAL
        if not hasattr(self, 'machinestate'):
            self.machinestate = machine_state.MachineState()
            self.mode = STATE.PHYSICAL
            self.machinestate.useOnlineModelLattice(om=True)
        self.machinestate.initialiseCATAP(self.mode, crest_phases=self.crest_phases,
                                          gun_calibration_data=self.gun_calibration_data,
                                          l01_calibration_data=self.l01_calibration_data)
        time.sleep(1)

        # Get the dictionary containing all CATAP hardware objects (used for controlling and monitoring the machine)
        self.catapdict = self.machinestate.getCATAPDict(self.mode)

        # Returns the machine state dictionary from CATAP
        self.catapdata = self.machinestate.getMachineStateFromCATAP(self.mode, crest_phases=self.crest_phases)
        time.sleep(1)
        self.machinestate.exportParameterValuesToYAMLFile(self.filename+".yaml", self.catapdata)
        self.qbtn.setText("Save snapshot")
        QApplication.processEvents()

        self.fileLocationLabel.setText('File saved to ' + self.filename+".yaml")

    def getSnapshotDirectory(self):
        self.possibleDirectories = ['legacy', 'dev', 'stage', 'release']
        self.scandir = "\\\\claraserv3\\claranet\\apps\\dev\\logs\\machineSnapshot\\"
        for i in self.possibleDirectories:
            if i in os.getcwd():
                self.scandir = "\\\\claraserv3\\claranet\\apps\\"+i+"\\logs\\machineSnapshot\\"
        if not os.path.isdir(self.scandir):
            os.makedirs(self.scandir)
        self.filename = self.scandir+datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        return self.filename


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()