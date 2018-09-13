import sys, os, time
import VELA_CLARA_enums as vce
from PyQt4 import QtGui, QtCore
from snapshot_gui import snapshotGUI
from machine_snapshot import MachineSnapshot

# this class handles everything
class snapshotButton(QtGui.QApplication):
    def __init__(self,argv):
        QtGui.QWidget.__init__(self, argv)
        self.snapshotgui = snapshotGUI()
        self.snapshotgui.show()
        self.machinesnapshot = MachineSnapshot(MAG_Ctrl=None, BPM_Ctrl=None, CHG_Ctrl=None,
				 SCR_Ctrl=None, CAM_Ctrl=None, GUN_Ctrl=None,
				 GUN_Type=None, GUN_Crest=0.0, L01_Ctrl=None, L01_Crest=0.0,
				 PIL_Ctrl=None, MACHINE_MODE=vce.MACHINE_MODE.PHYSICAL, MACHINE_AREA=vce.MACHINE_AREA.CLARA_2_BA1_BA2, messages=False)
        self.directory = self.machinesnapshot.getdirectory()
        time.sleep(5)

        self.widgetUpdateTimer = QtCore.QTimer()
        self.widgetTimerUpdateTime_ms = 200  # MAGIC_NUMBER
        self.filename = self.machinesnapshot.setfilename()
        self.snapshotgui.getDirectoryLineEdit.setText(self.filename)

        self.snapshotgui.saveSnapshotButton.clicked.connect(self.handle_savefile)
        # self.snapshotgui.setJSON.clicked.connect(self.handle_filename)
        self.snapshotgui.setHDF5.clicked.connect(self.handle_filename)
        self.snapshotgui.setAll.clicked.connect(self.handle_filename)

    def handle_savefile(self,r):
        if self.snapshotgui.setHDF5.isChecked():
            self.machinesnapshot.writetohdf5()
        elif self.snapshotgui.setAll.isChecked():
            self.machinesnapshot.writetohdf5()

    def handle_filename(self,r):
        self.snapshotgui.getDirectoryLineEdit.setText("")
        if self.snapshotgui.setHDF5.isChecked():
            self.snapshotgui.getDirectoryLineEdit.setText(self.filename + ".hdf5")
        elif self.snapshotgui.setAll.isChecked():
            self.snapshotgui.getDirectoryLineEdit.setText(self.filename + ".hdf5")

if __name__ == '__main__':
    print "starting button"
    app = snapshotButton(sys.argv)
    sys.exit(app.exec_())
