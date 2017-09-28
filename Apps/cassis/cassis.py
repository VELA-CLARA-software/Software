#!python2
# -*- coding: utf-8 -*-

"""Cassis: Dark Current Observations
This app scans the gun gradient and solenoid and bucking coil currents, at each point taking an image of the screen
and grabbing traces from the wall current monitor and beam loss monitors via the Q-scope."""

import sys
from PyQt4 import QtCore, QtGui, uic
import os
sys.path.insert(0, r'\\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Software\VELA_CLARA_PYDs\bin\Release')
import VELA_CLARA_Magnet_Control as MagCtrl
import VELA_CLARA_Scope_Control as Scope_Control
import pyqtgraph as pg
from cassis_model import DarkCurrentScan
from time import gmtime, strftime
import numpy as np
from libtiff import TIFF

os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"

## Switch to using dark grey background and white foreground
pg.setConfigOption('background', 0.2)
pg.setConfigOption('foreground', 'w')

image_credits = {
    'blackcurrant.png': 'https://github.com/aisamanra/fruit-icons/blob/master/images/blackcurrant.svg',
    'Offline.png': 'http://www.iconarchive.com/show/windows-8-icons-by-icons8/Network-Disconnected-icon.html',
    'Virtual.png': 'https://thenounproject.com/search/?q=simulator&i=237636',
    'Physical.png': 'http://www.flaticon.com/free-icon/car-compact_31126#term=car&page=1&position=19',
    'submachine-gun.png': 'https://www.flaticon.com/free-icon/submachine-gun_1233',
    'pistol.png': 'https://www.flaticon.com/free-icon/pistol_116553',
}

Ui_MainWindow, QtBaseClass = uic.loadUiType("cassis.ui")


class CassisApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        #TODO: get initial parameters from INI file, and save them as we go
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        [label.setText('') for label in (self.mom_now_label, self.sol_now_label, self.bc_now_label)]
        self.progressBar.setValue(0)

        self.wcm_plot.setLabels(title='Wall current monitor', left='voltage [V]', bottom='time [µs]')
        self.wcm_plot.showGrid(True, True)
        self.blm_plot.setLabels(title='Beam loss monitor', left='voltage [V]', bottom='time [µs]')
        self.blm_plot.showGrid(True, True)

        self.go_button.clicked.connect(self.goButtonClicked)
        self.cancel_button.clicked.connect(self.cancelButtonClicked)

        self.magInit = MagCtrl.init()
        self.scopeInit = Scope_Control.init()
        self.machine_mode_dropdown.activated.connect(self.machineModeChanged)
        self.machineModeChanged()
        self.update_period = 100  # milliseconds
        self.startMainViewUpdateTimer()

        # for testing
        # filename = r'\\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Work\2017\09\27\0911-dark-current\sol-100-new.tif'
        # self.screen_image.setImage(TIFF.open(filename).read_image())

    # these functions update the GUI and (re)start the timer
    def startMainViewUpdateTimer(self):
        self.widgetUpdateTimer = QtCore.QTimer()
        self.widgetUpdateTimer.timeout.connect(self.mainViewUpdate)
        self.widgetUpdateTimer.start(self.update_period)
    def mainViewUpdate(self):
        # conceivably the timer could restart this function before it complete - so guard against that
        try:
            if not self.machine_mode == 'Offline':
                pass #TODO: update gun vacuum value
        finally:
            self.widgetUpdateTimer.start(self.update_period)

    def goButtonClicked(self):
        """Start recording dark current data."""
        self.work_folder = r'\\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Work' + \
                      strftime("\\%Y\\%m\\%d\\%H%M-dark-current", gmtime())
        os.makedirs(self.work_folder)
        self.work_folder_label.setText('Data saved to <a href="{}">work folder</a>'.format(self.work_folder))
        with open(self.work_folder + '\\metadata.txt', 'w') as f:
            f.write('Machine: ' + self.machine_dropdown.currentText())
            f.write('Gun: ' + self.gun_dropdown.currentText())
            f.write('Cathode: ' + self.cathode_dropdown.currentText())
            f.write('RF pulse width [µs]: ' + self.pulse_width_spinbox.value())
            f.write(self.vacuum_label.text())
        self.scan = DarkCurrentScan(self.magnet_controller, self.scope_controller, self.work_folder)
        mom_range = np.arange(self.mom_from_spinbox.value(), self.mom_to_spinbox.value() + 1e-3, self.mom_step_spinbox.value())
        sol_range = np.arange(self.sol_from_spinbox.value(), self.sol_to_spinbox.value() + 1e-3, self.sol_step_spinbox.value())
        bc_range = np.arange(self.bc_from_spinbox.value(), self.bc_to_spinbox.value() + 1e-3, self.bc_step_spinbox.value())
        self.scan.startLoop(mom_range, sol_range, bc_range, self.updateProgress)

    def cancelButtonClicked(self):
        """Cancel the dark current recording process."""
        self.scan.stopLoop()

    def updateProgress(self, scan_params, traces, sc1_img, progress):
        """Callback function from the DC recording thread. Update the parameters, progress and plots."""
        mom, sol_current, bc_current = scan_params
        wcm1, wcm2, blm1, blm2 = traces
        # update momentum, sol and BC current displayed
        self.mom_now_label.setText('now: {:.1f} MeV'.format(mom))
        self.sol_now_label.setText('now: {:.1f} A'.format(sol_current))
        self.bc_now_label.setText('now: {:.1f} A'.format(bc_current))
        self.progress_bar.setValue(progress)
        # update plots and screen image on window
        self.wcm_plot.plot(wcm1, clear=True)
        self.wcm_plot.plot(wcm2)
        self.blm_plot.plot(blm1, clear=True)
        self.blm_plot.plot(blm2)
        self.screen_image.setImage(sc1_img)
        # save all data to work folder (image is already saved)
        file_prefix = '\\mom={:.1f}_sol={:.1f}_bc={.1f}'.format(mom, sol_current, bc_current)
        np.savetxt(self.work_folder + file_prefix + '_wcm1.csv', wcm1, delimiter=',')
        np.savetxt(self.work_folder + file_prefix + '_wcm2.csv', wcm2, delimiter=',')
        np.savetxt(self.work_folder + file_prefix + '_blm1.csv', blm1, delimiter=',')
        np.savetxt(self.work_folder + file_prefix + '_blm2.csv', blm2, delimiter=',')

    def machineModeChanged(self, index=None):
        mode = str(self.machine_mode_dropdown.currentText())
        self.setMachineMode(mode)

    def setMachineMode(self, mode=None):
        self.machine_mode = mode
        print('Setting machine mode:', mode)
        os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255" if mode == 'Physical' else "10.10.0.12"
        # Need to use MagCtrl's MACHINE_MODE enums as Scope_Control's ones won't work
        # https://astec-team.slack.com/archives/C2Z5G1X97/p1506330922000140
        self.magnet_controller = self.magInit.getMagnetController(MagCtrl.MACHINE_MODE.names[mode.upper()], MagCtrl.MACHINE_AREA.VELA_INJ)
        self.scope_controller = self.scopeInit.getScopeController(MagCtrl.MACHINE_MODE.names[mode.upper()], MagCtrl.MACHINE_AREA.VELA_INJ)
        scopeController.setBufferSize(1)
        # self.settings.setValue('machine_mode', mode)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = CassisApp()
    window.show()
    sys.exit(app.exec_())
