#!python2
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, uic
from rf_sol_tracking import RFSolTracker
import pyqtgraph as pg
import numpy as np

## Switch to using grey background and black foreground
pg.setConfigOption('background', 0.9375)
pg.setConfigOption('foreground', 'k')

qtCreatorFile = "rf_sol_gui.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        #TODO: get initial parameters from INI file, and save them as we go
        self.gun = RFSolTracker('Gun-10')
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.E_field_plot.setLabels(title='Electric field', left='E [MV/m]', bottom='z [m]')
        self.B_field_plot.setLabels(title='Magnetic field', left='B [T]', bottom='z [m]')
        self.momentum_plot.setLabels(title='Momentum', left='p [MeV/c]', bottom='z [m]')
        self.larmor_angle_plot.setLabels(title='Larmor angle', left='&theta;<sub>L</sub> [&deg;]', bottom='z [m]')
        self.E_field_plot.setLabels(title='E field', left='E [MV/m]', bottom='z [m]')
        self.xy_plot.setLabels(title='Particle position', left='x, y [mm]', bottom='z [m]')
        # self.xy_plot.addLegend()
        self.xdash_ydash_plot.setLabels(title='Particle angle', left="x', y' [mrad]", bottom='z [m]')
        # self.xdash_ydash_plot.addLegend()
        for plot in (self.E_field_plot, self.B_field_plot, self.momentum_plot,
                     self.larmor_angle_plot, self.E_field_plot, self.xy_plot, self.xdash_ydash_plot):
            plot.showGrid(True, True)

        self.peak_field_spin.valueChanged.connect(self.gunParamsChanged)
        self.phase_spin.valueChanged.connect(self.gunParamsChanged)
        self.crest_button.clicked.connect(self.crestButtonClicked)
        self.bc_spin.valueChanged.connect(self.solCurrentsChanged)
        self.sol_spin.valueChanged.connect(self.solCurrentsChanged)
        self.cathode_field_spin.valueChanged.connect(self.cathodeFieldChanged)
        self.sol_field_spin.valueChanged.connect(self.solPeakFieldChanged)
        self.momentum_spin.valueChanged.connect(self.momentumChanged)
        self.larmor_angle_spin.valueChanged.connect(self.larmorAngleChanged)
        for spin in (self.x_spin, self.xdash_spin, self.y_spin, self.ydash_spin):
            spin.valueChanged.connect(self.ustartChanged)

        self.gunParamsChanged()

    def gunParamsChanged(self, value=None):
        """The gun parameters have been modified - rerun the simulation and update the GUI."""
        self.gun.setRFPeakField(self.peak_field_spin.value())
        self.gun.setRFPhase(self.phase_spin.value())
        self.E_field_plot.clear()
        self.E_field_plot.plot(self.gun.getZRange(), self.gun.getRFFieldMap() / 1e6, pen='r')
        self.momentum_plot.clear()
        self.momentum_plot.plot(self.gun.getZRange(), self.gun.getMomentumMap(), pen='r')
        self.momentum_spin.setValue(self.gun.getFinalMomentum())
        self.solCurrentsChanged()

    def crestButtonClicked(self):
        """Find the crest of the RF cavity."""
        self.phase_spin.setValue(self.gun.crestCavity())

    def solCurrentsChanged(self, value=None):
        """The bucking coil or solenoid parameters have been modified - rerun the simulation and update the GUI."""
        self.gun.setBuckingCoilCurrent(self.bc_spin.value())
        self.gun.setSolenoidCurrent(self.sol_spin.value())
        self.B_field_plot.clear()
        self.B_field_plot.plot(self.gun.getZRange(), self.gun.getMagneticFieldMap(), pen='r')
        self.larmor_angle_plot.clear()
        self.larmor_angle_plot.plot(self.gun.getZRange(), self.gun.getLarmorAngleMap(), pen='r')
        self.larmor_angle_spin.setValue(self.gun.getFinalLarmorAngle())
        self.ustartChanged()

    def cathodeFieldChanged(self, value=None):
        """The cathode field has been modified - find the bucking coil current that gives this field."""
        # Prevent feedback loops
        if sys._getframe(1).f_code.co_name == '<module>':
            self.bc_spin.setValue(self.gun.setCathodeField(value))

    def solPeakFieldChanged(self, value=None):
        """The solenoid peak field has been modified - find the solenoid current that gives this field."""
        # Prevent feedback loops
        if sys._getframe(1).f_code.co_name == '<module>':
            self.sol_spin.setValue(self.gun.setPeakMagneticField(value))

    def momentumChanged(self, value=None):
        """The momentum has been modified - find the gun peak field that gives this value."""
        # Prevent feedback loops
        if sys._getframe(1).f_code.co_name == '<module>':
            self.peak_field_spin.setValue(self.gun.setFinalMomentum(value))

    def larmorAngleChanged(self, value=None):
        """The Larmor angle has been modified - find the solenoid current that gives this value."""
        # Prevent feedback loops
        if sys._getframe(1).f_code.co_name == '<module>':
            self.sol_spin.setValue(self.gun.setLarmorAngle(value))

    def ustartChanged(self, value=None):
        """The particle start position has been modified - track the particle through the fields."""
        uend = self.gun.trackBeam(1e-3 * np.matrix([spin.value() for spin in (self.x_spin, self.xdash_spin, self.y_spin, self.ydash_spin)], dtype='float').T)
        self.xy_plot.clear()
        self.xy_plot.plot(self.gun.getZRange(), 1e3 * self.gun.u_array[:, 0], pen='r', name='x')
        self.xy_plot.plot(self.gun.getZRange(), 1e3 * self.gun.u_array[:, 2], pen='g', name='y')
        self.xdash_ydash_plot.clear()
        self.xdash_ydash_plot.plot(self.gun.getZRange(), 1e3 * self.gun.u_array[:, 1], pen='r', name="x'")
        self.xdash_ydash_plot.plot(self.gun.getZRange(), 1e3 * self.gun.u_array[:, 3], pen='g', name="y'")
        self.uend_label.setText("'<b>Final particle position</b> x {0:.3f} mm, x' {1:.3f} mrad; y {2:.3f} mm, y' {3:.3f} mrad".format(*uend.flat))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())