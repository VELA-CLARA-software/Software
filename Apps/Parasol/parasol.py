#!python2
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from rf_sol_tracking import RFSolTracker
import rf_sol_gui
import pyqtgraph as pg
import numpy as np
import os
sys.path.insert(0, r'\\apclara1\ControlRoomApps\Controllers\bin\Release')
try:
    import VELA_CLARA_Magnet_Control as MagCtrl
except ImportError:
    MagCtrl = None

os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"

## Switch to using dark grey background and white foreground
# pg.setConfigOption('background', 0.2)
pg.setConfigOption('foreground', 'w')

image_credits = {
    'parasol.png': 'https://www.shareicon.net/parasol-sun-umbrella-travel-tools-and-utensils-summer-sunshade-summertime-794079',
    'Offline.png': 'http://www.iconarchive.com/show/windows-8-icons-by-icons8/Network-Disconnected-icon.html',
    'Virtual.png': 'https://thenounproject.com/search/?q=simulator&i=237636',
    'Physical.png': 'http://www.flaticon.com/free-icon/car-compact_31126#term=car&page=1&position=19',
    'mountain-summit.png': 'http://www.flaticon.com/free-icon/mountain-summit_27798#term=peak&page=1&position=6',
    'padlock-closed.png': 'https://www.iconfinder.com/icons/49855/closed_padlock_icon#size=32',
    'padlock-open.png': 'https://www.iconfinder.com/icons/49856/open_padlock_unlocked_unsecure_icon#size=32',
    'play-button.png': 'http://www.flaticon.com/free-icon/play-button_149657#term=play&page=1&position=11',
    'pause-symbol.png': 'http://www.flaticon.com/free-icon/pause-symbol_25696#term=pause&page=1&position=7',
    'submachine-gun.png': 'https://www.flaticon.com/free-icon/submachine-gun_1233',
    'pistol.png': 'https://www.flaticon.com/free-icon/pistol_116553',
    'bike.png': 'https://www.flaticon.com/free-icon/man-cycling_60693',
    'car.png': 'https://www.flaticon.com/free-icon/volkswagen-car-side-view_66906',
    'jet.png': 'https://www.flaticon.com/free-icon/fighter-jet-silhouette_25431',
    'rocket.png': 'https://www.flaticon.com/free-icon/small-rocket-ship-silhouette_25452',
}

# figure out where the script is (or EXE file if we've been bundled)
bundle_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
# Ui_MainWindow, QtBaseClass = uic.loadUiType(bundle_dir + "/resources/parasol/rf_sol_gui.ui")

def noFeedback(method):
    """Wrapper to prevent feedback loops - don't keep cycling through (e.g.) current <-> field calculations."""
    def feedbackless(*args, **kw):
        if sys._getframe(1).f_code.co_name == '<module>':
            return method(*args, **kw)
    return feedbackless


class ParasolApp(QtGui.QMainWindow): #, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.machine_mode = 'Offline'
        #TODO: get initial parameters from INI file, and save them as we go
        self.gun = RFSolTracker('Gun-10', quiet=True)
        self.ui = rf_sol_gui.Ui_RF_Solenoid_Tracker()
        self.MainWindow = QtGui.QMainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

        # QtGui.QMainWindow.__init__(self)
        # Ui_MainWindow.__init__(self)
        # self.setupUi(self)
        self.ui.peak_field_spin.setValue(self.gun.rf_peak_field)
        self.ui.phase_spin.setValue(self.gun.phase)
        self.ui.bc_spin.setValue(self.gun.solenoid.bc_current)
        self.ui.sol_spin.setValue(self.gun.solenoid.sol_current)
        self.crest_phase = float('nan')
        self.phase_lock = self.ui.lock_button.isChecked()
        self.ui.E_field_plot.setLabels(title='Electric field', left='E [MV/m]', bottom='z [m]')
        self.ui.B_field_plot.setLabels(title='Magnetic field', left='B [T]', bottom='z [m]')
        # self.proxy = pg.SignalProxy(self.B_field_plot.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        self.ui.momentum_plot.setLabels(title='Momentum', left='p [MeV/c]', bottom='z [m]')
        self.ui.larmor_angle_plot.setLabels(title='Larmor angle', left='&theta;<sub>L</sub> [&deg;]', bottom='z [m]')
        self.ui.E_field_plot.setLabels(title='E field', left='E [MV/m]', bottom='z [m]')
        self.ui.xy_plot.setLabels(title='Particle position', left='x, y [mm]', bottom='z [m]')
        self.ui.xy_plot.addLegend()
        self.ui.xdash_ydash_plot.setLabels(title='Particle angle', left="x', y' [mrad]", bottom='z [m]')
        self.ui.xdash_ydash_plot.addLegend()

        self.ui.peak_field_spin.valueChanged.connect(self.rfPeakFieldChanged)
        self.ui.phase_spin.valueChanged.connect(self.phaseChanged)
        self.ui.off_crest_spin.valueChanged.connect(self.offCrestSpinChanged)
        self.ui.crest_button.clicked.connect(self.crestButtonClicked)
        self.ui.lock_button.clicked.connect(self.lockButtonClicked)
        self.ui.lock_button.setEnabled(False)
        self.ui.bc_spin.valueChanged.connect(self.solCurrentsChanged)
        self.ui.sol_spin.valueChanged.connect(self.solCurrentsChanged)
        self.ui.cathode_field_spin.valueChanged.connect(self.cathodeFieldChanged)
        self.ui.sol_field_spin.valueChanged.connect(self.solPeakFieldChanged)
        self.ui.momentum_spin.valueChanged.connect(self.momentumChanged)
        self.ui.larmor_angle_spin.valueChanged.connect(self.larmorAngleChanged)
        self.ui.phase_slider.valueChanged.connect(self.phaseSliderChanged)
        for spin in (self.ui.x_spin, self.ui.xdash_spin, self.ui.y_spin, self.ui.ydash_spin):
            spin.valueChanged.connect(self.ustartChanged)
        self.ui.tracking_dropdown.activated.connect(self.trackingDropdownChanged)

        # Add these to the GUI with a custom ui parameter, so we can show axes on the plots
        for name in ('initial', 'final'):
            plot = pg.ImageView(view=pg.PlotItem())
            setattr(self.ui, name + '_beam_plot', plot)
            plot.setPredefinedGradient('thermal')
            view = plot.getView()
            view.invertY(False)  # otherwise positive Y is at the bottom
            view.setLabels(title=name.title() + ' beam', left='y [mm]', bottom='x [mm]')
            view.showGrid(True, True)
            # I want the grid to be shown on top, otherwise the black areas of the image obscure the grid
            # This works, but means that the image can only be panned horizontally
            # so I'll comment it out for now
            # https://stackoverflow.com/questions/46584438/show-grid-lines-over-image-in-pyqtgraph/46605797#46605797
            # https://github.com/pyqtgraph/pyqtgraph/pull/565
            # for axis_name in ui.axes:
            #     axis = ui.getAxis(axis_name)
            #     axis.setZValue(1)  # ensure grid is drawn on top of image
            self.ui.xy_plot_hbox.addWidget(plot)
            plot.setVisible(False)
        [link(self.ui.initial_beam_plot.getView()) for link in (view.setXLink, view.setYLink)]

        for plot in (self.ui.E_field_plot, self.ui.B_field_plot, self.ui.momentum_plot,
                     self.ui.larmor_angle_plot, self.ui.E_field_plot, self.ui.xy_plot, self.ui.xdash_ydash_plot):
            plot.showGrid(True, True)

        self.ui.gun_dropdown.activated.connect(self.gunChanged)
        if MagCtrl is None:
            self.magInit = None
            self.ui.machine_mode_dropdown.setEnabled(False)  # use "offline" mode only!
        else:
            self.magInit = MagCtrl.init()
            self.ui.machine_mode_dropdown.activated.connect(self.machineModeChanged)
            self.machineModeChanged()
        self.update_period = 100  # milliseconds
        self.startMainViewUpdateTimer()
        self.gunChanged() # initial update

        # self.label.setText(
        #     "<span style='font-size: 14pt; color: white'> x = %0.2f, <span style='color: white'> y = %0.2f</span>" % (
        #     mousePoint.x(), mousePoint.y()))

    def resizeEvent(self, resizeEvent):
        # Remove plots one row at a time as the window shrinks
        height = self.ui.geometry().height()
        show_beam = self.ui.tracking_dropdown.currentIndex() == 1
        self.ui.xy_plot.setVisible(height >= 512 and not show_beam)
        self.ui.xdash_ydash_plot.setVisible(height >= 512 and not show_beam)
        self.ui.initial_beam_plot.setVisible(height >= 512 and show_beam)
        self.ui.final_beam_plot.setVisible(height >= 512 and show_beam)
        field_plots = (self.ui.E_field_plot, self.ui.B_field_plot, self.ui.phase_play_button, self.ui.phase_slider)
        [control.setVisible(height >= 420) for control in field_plots]
        self.ui.B_field_plot.setVisible(height >= 420)
        self.ui.momentum_plot.setVisible(height >= 250)
        self.ui.larmor_angle_plot.setVisible(height >= 250)

    # these functions update the GUI and (re)start the timer
    def startMainViewUpdateTimer(self):
        self.widgetUpdateTimer = QtCore.QTimer()
        self.widgetUpdateTimer.timeout.connect(self.mainViewUpdate)
        self.widgetUpdateTimer.start(self.update_period)
    def mainViewUpdate(self):
        # Increment the phase slider if it's running
        if self.ui.phase_play_button.isChecked():
            self.ui.phase_slider.setValue((self.ui.phase_slider.value() + 5) % 360)
        # conceivably the timer could restart this function before it complete - so guard against that
        try:
            if not self.machine_mode == 'Offline':
                if not self.ui.bc_spin.hasFocus():
                    self.ui.bc_spin.setValue(self.bc_ref.siWithPol)
                if not self.ui.sol_spin.hasFocus():
                    self.ui.sol_spin.setValue(self.sol_ref.siWithPol)
        finally:
            self.widgetUpdateTimer.start(self.update_period)

    def gunChanged(self, index=None):
        """The model has been changed. Refresh the display."""
        self.gun = RFSolTracker(self.ui.gun_dropdown.currentText(), quiet=True)
        is_linac = 'Linac' in self.gun.name
        self.ui.gun_label.setText('Linac' if is_linac else 'Gun')
        self.ui.bc_label.setText('Solenoid 1 current' if is_linac else 'Bucking coil current')
        self.ui.sol_label.setText('Solenoid 2 current' if is_linac else 'Solenoid current')
        self.ui.cathode_field_spin.setEnabled(not is_linac)
        has_bc = self.gun.solenoid.bc_current is not None
        self.ui.bc_spin.setEnabled(has_bc)
        if has_bc:
            self.ui.bc_spin.setRange(*self.gun.solenoid.bc_range)
        self.ui.sol_spin.setRange(*self.gun.solenoid.sol_range)
        widgets = (self.ui.phase_spin, self.ui.off_crest_spin, self.ui.crest_button, self.ui.lock_button,
                   self.ui.phase_play_button, self.ui.phase_slider)
        [widget.setEnabled(self.gun.freq > 0) for widget in widgets]
        self.rfPeakFieldChanged(update=False)
        self.phaseChanged(self.gun.phase)

    def rfPeakFieldChanged(self, value=None, update=True):
        """The RF peak field has been changed."""
        self.gun.setRFPeakField(self.ui.peak_field_spin.value())
        if self.phase_lock:
            self.crest_phase = self.gun.crestCavity()
            self.ui.phase_spin.setValue(self.crest_phase + self.ui.off_crest_spin.value())
        else:
            self.crest_phase = float('nan')
            self.ui.off_crest_spin.setValue(self.ui.off_crest_spin.minimum())  # show special value (unknown)
            # self.ui.crest_button.show()
            self.ui.lock_button.setEnabled(False)
        if update:
            self.gunParamsChanged()

    def phaseChanged(self, value=None):
        """The RF phase has been changed."""
        if value <= -360:
            self.ui.phase_spin.setValue(value + 360)
            return
        elif value >= 360:
            self.ui.phase_spin.setValue(value - 360)
            return
        if not np.isnan(self.crest_phase):
            self.ui.off_crest_spin.setValue(value - self.crest_phase)
        self.gun.setRFPhase(self.ui.phase_spin.value())
        self.gunParamsChanged()

    def phaseSliderChanged(self):
        """The phase slider has been altered. Update the RF field plot. (No extra calculation needed.)"""
        self.ui.E_field_plot.plot(self.gun.getZRange(), self.gun.getRFFieldMap(phase=np.radians(self.ui.phase_slider.value())) / 1e6, pen='w', clear=True)
        title = 'Electric field' + (u', phase {:.0f}°'.format(self.ui.phase_slider.value()) if self.ui.phase_slider.isEnabled() else '')
        self.ui.E_field_plot.setTitle(title)
        # self.ui.phase_play_button.setChecked(False)

    def gunParamsChanged(self):
        """The gun parameters have been modified - rerun the simulation and update the GUI."""
        self.ui.E_field_plot.setYRange(-self.gun.rf_peak_field, self.gun.rf_peak_field)
        self.phaseSliderChanged()  # update the RF field plot
        self.ui.momentum_plot.plot(self.gun.getZRange(), self.gun.getMomentumMap(), pen='w', clear=True)
        self.ui.momentum_spin.setValue(self.gun.getFinalMomentum())
        self.solCurrentsChanged()

    def offCrestSpinChanged(self, value):
        """The off-crest value has been changed - change the phase accordingly."""
        if value == self.ui.off_crest_spin.minimum():
            # it's set to 'unknown' due to RF peak field being changed (and lock not set)
            return
        self.ui.off_crest_spin.setPrefix('+' if value > 0 else '')
        if np.isnan(self.crest_phase):
            # Just come off special value (unknown)
            self.ui.off_crest_spin.setValue(0)
            self.crestButtonClicked()
        else:
            self.ui.phase_spin.setValue(self.crest_phase + value)

    def crestButtonClicked(self):
        """Find the crest of the RF cavity."""
        self.crest_phase = self.gun.crestCavity()
        self.ui.phase_spin.setValue(self.crest_phase)
        self.ui.off_crest_spin.setValue(0)
        self.ui.lock_button.setEnabled(True)
        self.phase_lock = True
        self.ui.lock_button.setChecked(self.phase_lock)
        # self.ui.crest_button.hide()

    def lockButtonClicked(self):
        """Set the phase lock state - does the off-crest value persist even when the RF peak field is changed?"""
        self.phase_lock = self.ui.lock_button.isChecked()

    def solCurrentsChanged(self, value=None):
        """The bucking coil or solenoid parameters have been modified - rerun the simulation and update the GUI."""
        sol = self.gun.solenoid
        self.gun.setBuckingCoilCurrent(self.ui.bc_spin.value())
        self.gun.setSolenoidCurrent(self.ui.sol_spin.value())
        if self.machine_mode != 'Offline':
            self.controller.setSI('BSOL', self.ui.bc_spin.value())
            self.controller.setSI('SOL', self.ui.sol_spin.value())
        self.ui.cathode_field_spin.setValue(sol.getMagneticField(0))
        self.ui.sol_field_spin.setValue(sol.getPeakMagneticField())
        self.ui.B_field_plot.plot(sol.getZMap(), sol.getMagneticFieldMap(), pen='w', clear=True)
        self.ui.larmor_angle_plot.plot(self.gun.getZRange(), self.gun.getLarmorAngleMap(), pen='w', clear=True)
        self.ui.larmor_angle_spin.setValue(self.gun.getFinalLarmorAngle())
        self.ustartChanged()

    @noFeedback
    def cathodeFieldChanged(self, value=None):
        """The cathode field has been modified - find the bucking coil current that gives this field."""
        self.ui.bc_spin.setValue(self.gun.solenoid.setCathodeField(value))

    @noFeedback
    def solPeakFieldChanged(self, value=None):
        """The solenoid peak field has been modified - find the solenoid current that gives this field."""
        self.ui.sol_spin.setValue(self.gun.solenoid.setPeakMagneticField(value))

    @noFeedback
    def momentumChanged(self, value=None):
        """The momentum has been modified - find the gun peak field that gives this value."""
        self.ui.peak_field_spin.setValue(self.gun.setFinalMomentum(value))

    @noFeedback
    def larmorAngleChanged(self, value=None):
        """The Larmor angle has been modified - find the solenoid current that gives this value."""
        self.ui.sol_spin.setValue(self.gun.setLarmorAngle(value))

    def trackingDropdownChanged(self, index=None):
        """The tracking type dropdown has changed. Rerun the tracking."""
        show_beam = index == 1
        self.ui.xy_plot.setVisible(not show_beam)
        self.ui.xdash_ydash_plot.setVisible(not show_beam)
        self.ui.initial_beam_plot.setVisible(show_beam)
        self.ui.final_beam_plot.setVisible(show_beam)
        self.ui.ustart_label.setText('Beam size (sigma)' if show_beam else 'Initial particle position')
        self.ustartChanged()

    def ustartChanged(self, value=None):
        """The particle start position has been modified - track the particle/beam through the fields."""
        show_beam = self.ui.tracking_dropdown.currentIndex() == 1
        spin_values = [spin.value() for spin in (self.ui.x_spin, self.ui.xdash_spin, self.ui.y_spin, self.ui.ydash_spin)]
        if show_beam:
            matrix = self.gun.getOverallMatrix()
            n = 30000
            x0 = np.matrix([np.random.normal(0, sigma * 1e-3, n) for sigma in spin_values])
            x1 = np.array([matrix.dot(x.T) for x in x0.T])

            bins = 60
            for xy_data, plot in ((np.asarray(x0)[0::2], self.ui.initial_beam_plot),
                                  (np.squeeze(x1[:, 0::2].T), self.ui.final_beam_plot)):
                histogram, x_edges, y_edges = np.histogram2d(*xy_data, bins=bins)
                x_edges *= 1e3
                y_edges *= 1e3
                x_range = x_edges[-1] - x_edges[0]
                y_range = y_edges[-1] - y_edges[0]
                plot.setImage(histogram, pos=(x_edges[0], y_edges[0]), scale=(x_range / bins, y_range / bins))
            label_text = "<b>Final beam size</b> ({n:.3g} particles): x {0:.3g} mm, x' {1:.3g} mrad; y {2:.3g} mm, y' {3:.3g} mrad"
            self.ui.uend_label.setText(label_text.format(*np.std(x1[:, :, 0], 0) * 1e3, n=n))
        else:
            uend = self.gun.trackBeam(1e-3 * np.matrix(spin_values, dtype='float').T)
            self.ui.xy_plot.plotItem.legend.items = []
            self.ui.xy_plot.plot(self.gun.getZRange(), 1e3 * self.gun.u_array[:, 0], pen='w', name='x', clear=True)
            self.ui.xy_plot.plot(self.gun.getZRange(), 1e3 * self.gun.u_array[:, 2], pen='g', name='y')
            self.ui.xdash_ydash_plot.plotItem.legend.items = []
            self.ui.xdash_ydash_plot.plot(self.gun.getZRange(), 1e3 * self.gun.u_array[:, 1], pen='w', name="x'", clear=True)
            self.ui.xdash_ydash_plot.plot(self.gun.getZRange(), 1e3 * self.gun.u_array[:, 3], pen='g', name="y'")
            self.ui.uend_label.setText("<b>Final particle position</b> x {0:.3g} mm, x' {1:.3g} mrad; y {2:.3g} mm, y' {3:.3g} mrad".format(*uend.flat))

    def machineModeChanged(self, index=None):
        mode = str(self.ui.machine_mode_dropdown.currentText())
        self.setMachineMode(mode)
        self.bc_ref = self.controller.getMagObjConstRef('BSOL')
        self.sol_ref = self.controller.getMagObjConstRef('SOL')

    def setMachineMode(self, mode=None):
        self.machine_mode = mode
        # print('Setting machine mode:', mode)
        os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255" if mode == 'Physical' else "10.10.0.12"
        self.controller = self.magInit.getMagnetController(MagCtrl.MACHINE_MODE.names[mode.upper()], MagCtrl.MACHINE_AREA.VELA_INJ)
        # self.settings.setValue('machine_mode', mode)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = ParasolApp()
    # window.show()
    sys.exit(app.exec_())
