#!python3
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import pyqtgraph
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from rf_sol_gui import ParasolUI
from rf_sol_tracking import RFSolTracker

sys.path.insert(0, r'\\apclara1\ControlRoomApps\Controllers\bin\Release')
try:
    import VELA_CLARA_Magnet_Control as MagCtrl
except ImportError:
    MagCtrl = None

os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"

# Switch to using dark grey background and white foreground
# pg.setConfigOption('background', 0.2)
pg.setConfigOption('foreground', 'w')


# figure out where the script is (or EXE file if we've been bundled)
bundle_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))


# Ui_MainWindow, QtBaseClass = uic.loadUiType(bundle_dir + "/resources/parasol/rf_sol_gui.ui")


def no_feedback(method):
    """Wrapper to prevent feedback loops - don't keep cycling through (e.g.) current <-> field calculations."""

    def feedbackless(*args, **kw):
        if sys._getframe(1).f_code.co_name == '<module>':
            return method(*args, **kw)

    return feedbackless


class ParasolApp(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(ParasolApp, self).__init__(parent=parent)
        self.controller = None
        self.sol_ref = None
        self.bc_ref = None
        self.widget_update_timer = None
        self.machine_mode = 'Offline'
        # TODO: get initial parameters from INI file, and save them as we go
        self.gun = RFSolTracker('Gun-10', quiet=True)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = ParasolUI(self.MainWindow)
        self.resized.connect(self.resize_window)
        self.MainWindow.show()

        self.ui.peak_field_spin.setValue(self.gun.rf_peak_field)
        self.ui.phase_spin.setValue(self.gun.phase)
        self.ui.bc_spin.setValue(self.gun.solenoid.bc_current)
        self.ui.sol_spin.setValue(self.gun.solenoid.sol_current)
        self.crest_phase = float('nan')
        self.phase_lock = self.ui.lock_button.isChecked()
        z_label = 'z [m]'
        self.ui.E_field_plot.setLabels(title='Electric field', left='E [MV/m]', bottom=z_label)
        self.ui.B_field_plot.setLabels(title='Magnetic field', left='B [T]', bottom=z_label)
        # self.proxy = pg.SignalProxy(self.B_field_plot.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        self.ui.momentum_plot.setLabels(title='Momentum', left='p [MeV/c]', bottom=z_label)
        self.ui.larmor_angle_plot.setLabels(title='Larmor angle', left='&theta;<sub>L</sub> [&deg;]', bottom=z_label)
        self.ui.E_field_plot.setLabels(title='E field', left='E [MV/m]', bottom=z_label)
        self.ui.xy_plot.setLabels(title='Particle position', left='x, y [mm]', bottom=z_label)
        self.ui.xy_plot.addLegend()
        self.ui.xdash_ydash_plot.setLabels(title='Particle angle', left="x', y' [mrad]", bottom=z_label)
        self.ui.xdash_ydash_plot.addLegend()

        self.ui.peak_field_spin.valueChanged.connect(self.rf_peak_field_changed)
        self.ui.phase_spin.valueChanged.connect(self.phase_changed)
        self.ui.off_crest_spin.valueChanged.connect(self.off_crest_spin_changed)
        self.ui.crest_button.clicked.connect(self.crest_button_clicked)
        self.ui.lock_button.clicked.connect(self.lock_button_clicked)
        self.ui.lock_button.setEnabled(False)
        self.ui.bc_spin.valueChanged.connect(self.sol_currents_changed)
        self.ui.sol_spin.valueChanged.connect(self.sol_currents_changed)
        self.ui.cathode_field_spin.valueChanged.connect(self.cathode_field_changed)
        self.ui.sol_field_spin.valueChanged.connect(self.sol_peak_field_changed)
        self.ui.momentum_spin.valueChanged.connect(self.momentum_changed)
        self.ui.larmor_angle_spin.valueChanged.connect(self.larmor_angle_changed)
        self.ui.phase_slider.valueChanged.connect(self.phase_slider_changed)
        for spin in (self.ui.x_spin, self.ui.xdash_spin, self.ui.y_spin, self.ui.ydash_spin, self.ui.thickness_spin):
            spin.valueChanged.connect(self.ustart_changed)
        self.ui.tracking_dropdown.activated.connect(self.tracking_dropdown_changed)

        # Add these to the GUI with a custom ui parameter, so we can show axes on the plots
        for name in ('initial', 'final'):
            plot = pg.ImageView(view=pg.PlotItem())
            setattr(self.ui, f'{name}_beam_plot', plot)
            plot.setPredefinedGradient('thermal')
            view = plot.getView()
            view.invertY(False)  # otherwise positive Y is at the bottom
            view.setLabels(title=f'{name.title()} beam', left='y [mm]', bottom='x [mm]')
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
        self.xy_plots = [pyqtgraph.PlotCurveItem(clear=True, pen=pen, name=name)
                         for name, pen in [('x', 'w'), ('y', 'g'), ("x'", 'w'), ("y'", 'g')]]
        self.ui.xy_plot.addItem(self.xy_plots[0])
        self.ui.xy_plot.addItem(self.xy_plots[1])
        self.ui.xdash_ydash_plot.addItem(self.xy_plots[2])
        self.ui.xdash_ydash_plot.addItem(self.xy_plots[3])

        self.ui.gun_dropdown.activated.connect(self.gun_changed)
        if MagCtrl is None:
            self.magInit = None
            self.ui.machine_mode_dropdown.setEnabled(False)  # use "offline" mode only!
        else:
            self.magInit = MagCtrl.init()
            self.ui.machine_mode_dropdown.activated.connect(self.machine_mode_changed)
            self.machine_mode_changed()
        self.update_period = 100  # milliseconds
        self.start_main_view_update_timer()
        self.gun_changed()  # initial update

        # self.label.setText(
        #     "<span style='font-size: 14pt; color: white'> x = %0.2f, <span style='color: white'> y = %0.2f</span>" % (
        #     mousePoint.x(), mousePoint.y()))

    def resizeEvent(self, event):
        self.resized.emit()
        return super(ParasolApp, self).resizeEvent(event)

    def resize_window(self):
        # Remove plots one row at a time as the window shrinks
        # TODO: this doesn't currently work
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
    def start_main_view_update_timer(self):
        self.widget_update_timer = QtCore.QTimer()
        self.widget_update_timer.timeout.connect(self.main_view_update)
        self.widget_update_timer.start(self.update_period)

    def main_view_update(self):
        # Increment the phase slider if it's running
        if self.ui.phase_play_button.isChecked():
            self.ui.phase_slider.setValue((self.ui.phase_slider.value() + 5) % 360)
        # conceivably the timer could restart this function before it complete - so guard against that
        try:
            if self.machine_mode != 'Offline':
                if not self.ui.bc_spin.hasFocus():
                    self.ui.bc_spin.setValue(self.bc_ref.siWithPol)
                if not self.ui.sol_spin.hasFocus():
                    self.ui.sol_spin.setValue(self.sol_ref.siWithPol)
        finally:
            self.widget_update_timer.start(self.update_period)

    def gun_changed(self, index=None):
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
        self.rf_peak_field_changed(update=False)
        self.phase_changed(self.gun.phase)

    def rf_peak_field_changed(self, value=None, update=True):
        """The RF peak field has been changed."""
        self.gun.set_rf_peak_field(self.ui.peak_field_spin.value())
        if self.phase_lock:
            self.crest_phase = self.gun.crest_cavity()
            self.ui.phase_spin.setValue(self.crest_phase + self.ui.off_crest_spin.value())
        else:
            self.crest_phase = float('nan')
            self.ui.off_crest_spin.setValue(self.ui.off_crest_spin.minimum())  # show special value (unknown)
            # self.ui.crest_button.show()
            self.ui.lock_button.setEnabled(False)
        if update:
            self.gun_params_changed()

    def phase_changed(self, value=None):
        """The RF phase has been changed."""
        if value <= -360:
            self.ui.phase_spin.setValue(value + 360)
            return
        elif value >= 360:
            self.ui.phase_spin.setValue(value - 360)
            return
        if not np.isnan(self.crest_phase):
            self.ui.off_crest_spin.setValue(value - self.crest_phase)
        self.gun.set_rf_phase(self.ui.phase_spin.value())
        self.gun_params_changed()

    def phase_slider_changed(self):
        """The phase slider has been altered. Update the RF field plot. (No extra calculation needed.)"""
        self.ui.E_field_plot.plot(self.gun.get_z_range(),
                                  self.gun.get_rf_field_map(phase=np.radians(self.ui.phase_slider.value())) / 1e6,
                                  pen='w', clear=True)
        slider_enabled = self.ui.phase_slider.isEnabled()
        title = 'Electric field' + (f', phase {self.ui.phase_slider.value():.0f}°' if slider_enabled else '')
        self.ui.E_field_plot.setTitle(title)
        # self.ui.phase_play_button.setChecked(False)

    def gun_params_changed(self):
        """The gun parameters have been modified - rerun the simulation and update the GUI."""
        self.ui.E_field_plot.setYRange(-self.gun.rf_peak_field, self.gun.rf_peak_field)
        self.phase_slider_changed()  # update the RF field plot
        self.ui.momentum_plot.plot(self.gun.get_z_range(), self.gun.get_momentum_map(), pen='w', clear=True)
        self.ui.momentum_spin.setValue(self.gun.get_final_momentum())
        self.sol_currents_changed()

    def off_crest_spin_changed(self, value):
        """The off-crest value has been changed - change the phase accordingly."""
        if value == self.ui.off_crest_spin.minimum():
            # it's set to 'unknown' due to RF peak field being changed (and lock not set)
            return
        self.ui.off_crest_spin.setPrefix('+' if value > 0 else '')
        if np.isnan(self.crest_phase):
            # Just come off special value (unknown)
            self.ui.off_crest_spin.setValue(0)
            self.crest_button_clicked()
        else:
            self.ui.phase_spin.setValue(self.crest_phase + value)

    def crest_button_clicked(self):
        """Find the crest of the RF cavity."""
        self.crest_phase = self.gun.crest_cavity()
        self.ui.phase_spin.setValue(self.crest_phase)
        self.ui.off_crest_spin.setValue(0)
        self.ui.lock_button.setEnabled(True)
        self.phase_lock = True
        self.ui.lock_button.setChecked(self.phase_lock)
        # self.ui.crest_button.hide()

    def lock_button_clicked(self):
        """Set the phase lock state - does the off-crest value persist even when the RF peak field is changed?"""
        self.phase_lock = self.ui.lock_button.isChecked()

    def sol_currents_changed(self, value=None):
        """The bucking coil or solenoid parameters have been modified - rerun the simulation and update the GUI."""
        sol = self.gun.solenoid
        self.gun.set_bucking_coil_current(self.ui.bc_spin.value())
        self.gun.set_solenoid_current(self.ui.sol_spin.value())
        if self.machine_mode != 'Offline':
            self.controller.setSI('BSOL', self.ui.bc_spin.value())
            self.controller.setSI('SOL', self.ui.sol_spin.value())
        self.ui.cathode_field_spin.setValue(sol.get_magnetic_field(0))
        self.ui.sol_field_spin.setValue(sol.get_peak_magnetic_field())
        self.ui.B_field_plot.plot(sol.get_z_map(), sol.get_magnetic_field_map(), pen='w', clear=True)
        self.ui.larmor_angle_plot.plot(self.gun.get_z_range(), self.gun.get_larmor_angle_map(), pen='w', clear=True)
        self.ui.larmor_angle_spin.setValue(self.gun.get_final_larmor_angle())
        self.ustart_changed()

    @no_feedback
    def cathode_field_changed(self, value=None):
        """The cathode field has been modified - find the bucking coil current that gives this field."""
        self.ui.bc_spin.setValue(self.gun.solenoid.set_cathode_field(value))

    @no_feedback
    def sol_peak_field_changed(self, value=None):
        """The solenoid peak field has been modified - find the solenoid current that gives this field."""
        self.ui.sol_spin.setValue(self.gun.solenoid.set_peak_magnetic_field(value))

    @no_feedback
    def momentum_changed(self, value=None):
        """The momentum has been modified - find the gun peak field that gives this value."""
        self.ui.peak_field_spin.setValue(self.gun.set_final_momentum(value))

    @no_feedback
    def larmor_angle_changed(self, value=None):
        """The Larmor angle has been modified - find the solenoid current that gives this value."""
        self.ui.sol_spin.setValue(self.gun.set_larmor_angle(value))

    def tracking_dropdown_changed(self, index=None):
        """The tracking type dropdown has changed. Rerun the tracking."""
        show_beam = index > 0
        self.ui.xy_plot.setVisible(not show_beam)
        self.ui.xdash_ydash_plot.setVisible(not show_beam)
        self.ui.initial_beam_plot.setVisible(show_beam)
        self.ui.final_beam_plot.setVisible(show_beam)
        self.ui.ustart_label.setText(['Initial particle position', 'Beam size (sigma)', 'Ellipse parameters'][index])
        pos_description = ["position of the particle", 'beam size', 'radius of a ring-shaped beam distribution'][index]
        self.ui.x_spin.setToolTip(f"Initial horizontal {pos_description}")
        self.ui.y_spin.setToolTip(f"Initial vertical {pos_description}")
        angle_description = ('angular beam size' if show_beam else 'angle of the particle')
        self.ui.xdash_spin.setToolTip(f"Initial horizontal {angle_description}")
        self.ui.ydash_spin.setToolTip(f"Initial vertical {angle_description}")
        ring = index == 2
        self.ui.x_label.setText('r&x' if ring else '&x')
        self.ui.y_label.setText('r&y' if ring else '&y')
        self.ui.thickness_label.setVisible(ring)
        self.ui.thickness_spin.setVisible(ring)
        self.ustart_changed()

    def ustart_changed(self, value=None):
        """The particle start position has been modified - track the particle/beam through the fields."""
        spin_values = [spin.value() for spin in
                       (self.ui.x_spin, self.ui.xdash_spin, self.ui.y_spin, self.ui.ydash_spin)]
        tracking_type = self.ui.tracking_dropdown.currentIndex()
        if tracking_type == 0:
            self.plot_particle(spin_values)
        else:
            self.plot_beam(spin_values, tracking_type)

    def plot_particle(self, spin_values):
        uend = self.gun.track_beam(1e-3 * np.matrix(spin_values, dtype='float').T)
        self.xy_plots[0].setData(self.gun.get_z_range(), 1e3 * self.gun.u_array[:, 0])
        self.xy_plots[1].setData(self.gun.get_z_range(), 1e3 * self.gun.u_array[:, 2])
        self.xy_plots[2].setData(self.gun.get_z_range(), 1e3 * self.gun.u_array[:, 1])
        self.xy_plots[3].setData(self.gun.get_z_range(), 1e3 * self.gun.u_array[:, 3])
        label_template = "<b>Final particle position</b> x {0:.3g} mm, x' {1:.3g} mrad; y {2:.3g} mm, y' {3:.3g} mrad"
        self.ui.uend_label.setText(label_template.format(*uend.flat))

    def plot_beam(self, spin_values, tracking_type):
        matrix = self.gun.get_overall_matrix()
        n = 30000
        if tracking_type == 1:  # beam
            x0 = np.matrix([np.random.normal(0, sigma * 1e-3, n) for sigma in spin_values])
        else:  # ring
            alpha = np.linspace(0, 2 * np.pi, n)
            thickness = self.ui.thickness_spin.value()
            delta_r = np.random.normal(0, thickness, n)
            x = (spin_values[0] + delta_r) * 1e-3 * np.cos(alpha)
            x_dash = np.random.normal(0, spin_values[1] * 1e-3, n)
            y = (spin_values[2] + delta_r) * 1e-3 * np.sin(alpha)
            y_dash = np.random.normal(0, spin_values[3] * 1e-3, n)
            x0 = np.matrix([x, x_dash, y, y_dash])

        x1 = np.array([matrix.dot(x.T) for x in x0.T])

        bins = 60
        for xy_data, plot in ((np.asarray(x0)[::2], self.ui.initial_beam_plot),
                              (np.squeeze(x1[:, 0::2].T), self.ui.final_beam_plot)):
            histogram, x_edges, y_edges = np.histogram2d(*xy_data, bins=bins)
            x_edges *= 1e3
            y_edges *= 1e3
            x_range = x_edges[-1] - x_edges[0]
            y_range = y_edges[-1] - y_edges[0]
            plot.setImage(histogram, pos=(x_edges[0], y_edges[0]), scale=(x_range / bins, y_range / bins))
        cov = np.cov(x1[:, 0, 0].flatten(), x1[:, 2, 0].flatten())
        label_text = u"<b>Final beam size</b> ({n:.3g} particles): x {0:.3g} mm, x' {1:.3g} mrad; " \
                     u"y {2:.3g} mm, y' {3:.3g} mrad, covariance {cov:.3g} mm²"
        self.ui.uend_label.setText(label_text.format(*np.std(x1[:, :, 0], 0) * 1e3, n=n, cov=cov[0, 1]))

    def machine_mode_changed(self, index=None):
        mode = str(self.ui.machine_mode_dropdown.currentText())
        self.set_machine_mode(mode)
        self.bc_ref = self.controller.getMagObjConstRef('BSOL')
        self.sol_ref = self.controller.getMagObjConstRef('SOL')

    def set_machine_mode(self, mode=None):
        self.machine_mode = mode
        # print('Setting machine mode:', mode)
        os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255" if mode == 'Physical' else "10.10.0.12"
        self.controller = self.magInit.getMagnetController(MagCtrl.MACHINE_MODE.names[mode.upper()],
                                                           MagCtrl.MACHINE_AREA.VELA_INJ)
        # self.settings.setValue('machine_mode', mode)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ParasolApp()
    # window.show()
    sys.exit(app.exec_())
