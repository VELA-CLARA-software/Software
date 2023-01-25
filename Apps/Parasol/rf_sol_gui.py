#!python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rf_sol_gui.ui'
# Created by: PyQt4 UI code generator 4.11.4
# Modified by Ben

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget

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
    'Gun-400.png': 'https://www.flaticon.com/free-icon/submachine-gun_1233',
    'Gun-10.png': 'https://www.flaticon.com/free-icon/pistol_116553',
    'Linac1.png': 'https://www.flaticon.com/free-icon/man-cycling_60693',
    'car.png': 'https://www.flaticon.com/free-icon/volkswagen-car-side-view_66906',
    'jet.png': 'https://www.flaticon.com/free-icon/fighter-jet-silhouette_25431',
    'rocket.png': 'https://www.flaticon.com/free-icon/small-rocket-ship-silhouette_25452',
}


def get_icon(name, on_name=None):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(f"resources/parasol/Icons/{name}.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    if on_name:
        icon.addPixmap(QtGui.QPixmap(f"resources/parasol/Icons/{on_name}.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
    return icon


def add_dropdown_items(dropdown, items):
    for name in items:
        if f'{name}.png' in image_credits:
            dropdown.addItem(get_icon(name), name)
        else:
            dropdown.addItem(name)


def combo_box(container, parent, items, tooltip):
    combo = QtWidgets.QComboBox(parent)
    max_fixed = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
    combo.setSizePolicy(max_fixed)
    combo.setMinimumSize(QtCore.QSize(0, 22))
    combo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
    add_dropdown_items(combo, items)
    combo.setToolTip(tooltip)
    container.addWidget(combo)
    return combo


def make_label(container, parent, text, bold=False):
    label = QtWidgets.QLabel(parent)
    label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred))
    label.setText(text)
    if bold:
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        label.setFont(font)
    container.addWidget(label)
    return label


def labelled_spinner(container, parent, text, suffix, tooltip, value, maximum, minimum=0, single_step=0.1):
    label = make_label(container, parent, text)
    spinbox = QtWidgets.QDoubleSpinBox(parent)
    spinbox.setKeyboardTracking(False)
    spinbox.setDecimals(3)
    spinbox.setSingleStep(single_step)
    spinbox.setMaximum(maximum)
    spinbox.setMinimum(minimum)
    spinbox.setValue(value)
    spinbox.setToolTip(tooltip)
    spinbox.setSuffix(f' {suffix}')
    container.addWidget(spinbox)
    label.setBuddy(spinbox)
    return label, spinbox


def plot(container, parent):
    widget = PlotWidget(parent)
    container.addWidget(widget)
    return widget


class ParasolUI(object):
    def __init__(self, rf_solenoid_tracker):
        fixed = QtWidgets.QSizePolicy.Fixed
        rf_solenoid_tracker.resize(781, 699)
        rf_solenoid_tracker.setWindowIcon(get_icon('parasol'))
        parent = QtWidgets.QWidget(rf_solenoid_tracker)
        main_vbox = QtWidgets.QVBoxLayout(parent)
        gun_hbox = QtWidgets.QHBoxLayout()
        self.gun_dropdown = combo_box(gun_hbox, parent,
                                      ['Gun-10', 'Gun-400', 'Linac1', 'gb-rf-gun', 'gb-dc-gun'],
                                      '<p>Select the RF/solenoid model to use.</p><p>'
                                      '<b>Gun-10</b>: VELA/CLARA 10 Hz gun<br>'
                                      '<b>Gun-400</b>: VELA/CLARA 400 Hz gun<br><b>Linac1</b>: CLARA Linac 1<br>'
                                      '<b>gb-rf-gun</b>: Gulliford-Bazarov RF gun example<br>'
                                      '<b>gb-dc-gun</b>: Gulliford-Bazarov DC gun example</p>')
        self.machine_mode_dropdown = combo_box(gun_hbox, parent, ['Offline', 'Virtual', 'Physical'],
                                               '<p>Switch between machine modes:</p><p>'
                                               '<b>Offline</b>: no interaction with machine<br>'
                                               '<b>Virtual</b>: connect to local virtual machine<br>'
                                               '<b>Physical</b>: connect to real machine via EPICS</p>')
        self.gun_label = make_label(gun_hbox, parent, 'Gun', True)
        _, self.peak_field_spin = labelled_spinner(gun_hbox, parent, "Pea&k field", "MV/m",
                                                   "Peak accelerating field produced inside the RF cavity", 96.5, 200)
        _, self.momentum_spin = labelled_spinner(gun_hbox, parent, "Fi&nal momentum", "MeV/c",
                                                 "Final momentum of a particle after traversing the RF cavity",
                                                 6.888, 1000)
        main_vbox.addLayout(gun_hbox)
        phase_hbox = QtWidgets.QHBoxLayout()
        _, self.phase_spin = labelled_spinner(phase_hbox, parent, "&Phase", "°",
                                              "Phase between injected electron and the RF cavity", 330, 720, -720)
        _, self.off_crest_spin = labelled_spinner(phase_hbox, parent, "&Off-crest", "°",
                                                  "Phase relative to off-crest value, or (unknown) when the crest "
                                                  "phase is unknown",
                                                  -360, 360, -360)
        self.off_crest_spin.setSpecialValueText("(unknown)")
        self.off_crest_spin.setPrefix("+")

        fixed_fixed = QtWidgets.QSizePolicy(fixed, fixed)
        self.crest_button = QtWidgets.QPushButton(parent)
        self.crest_button.setSizePolicy(fixed_fixed)
        self.crest_button.setIcon(get_icon('mountain-summit'))
        self.crest_button.setToolTip("Adjust the phase to produce the maximum momentum")
        self.crest_button.setText("&Crest")
        phase_hbox.addWidget(self.crest_button)

        self.lock_button = QtWidgets.QPushButton(parent)
        self.lock_button.setSizePolicy(fixed_fixed)
        self.lock_button.setIcon(get_icon('padlock-open', 'padlock-closed'))
        self.lock_button.setToolTip("Re-crest and keep the off-crest value when the RF peak field changes")
        self.lock_button.setText("Lo&ck")
        self.lock_button.setCheckable(True)
        phase_hbox.addWidget(self.lock_button)
        main_vbox.addLayout(phase_hbox)

        solenoids_hbox = QtWidgets.QHBoxLayout()
        self.bc_label, self.bc_spin = labelled_spinner(solenoids_hbox, parent, "&Bucking coil current", "A", "", 5, 8)
        self.sol_label, self.sol_spin = labelled_spinner(solenoids_hbox, parent, "&Solenoid current", "A", "", 300, 500)
        main_vbox.addLayout(solenoids_hbox)

        fields_hbox = QtWidgets.QHBoxLayout()
        tooltip = "Use the combined BC and solenoid field map to calculate the field at the cathode"
        _, self.cathode_field_spin = labelled_spinner(fields_hbox, parent, "&Field at cathode", "T", tooltip,
                                                      0, 10, -10, 0.01)
        _, self.sol_field_spin = labelled_spinner(fields_hbox, parent, "Solenoid &maximum field", "T",
                                                  "Peak field in the solenoid", 0.432, 1, single_step=0.01)
        tooltip = "Final Larmor angle of the particle after traversing the RF cavity and solenoid"
        _, self.larmor_angle_spin = labelled_spinner(fields_hbox, parent, "Final &Larmor angle", "°", tooltip,
                                                     100, 1000, -1000)
        main_vbox.addLayout(fields_hbox)

        field_graph_hbox = QtWidgets.QHBoxLayout()
        phase_vbox = QtWidgets.QVBoxLayout()
        self.phase_play_button = QtWidgets.QToolButton(parent)
        self.phase_play_button.setIcon(get_icon('play-button', 'pause-symbol'))
        self.phase_play_button.setCheckable(True)
        self.phase_play_button.setToolTip("Play an animation of the linac phase")
        phase_vbox.addWidget(self.phase_play_button)
        self.phase_slider = QtWidgets.QSlider(parent)
        self.phase_slider.setMaximum(360)
        self.phase_slider.setOrientation(QtCore.Qt.Vertical)
        self.phase_slider.setToolTip("<b>Linac phase</b> - use this to cycle through the displayed RF phase. "
                                     "This has no effect on the calculation.")
        phase_vbox.addWidget(self.phase_slider)
        field_graph_hbox.addLayout(phase_vbox)

        self.E_field_plot = plot(field_graph_hbox, parent)
        self.B_field_plot = plot(field_graph_hbox, parent)
        main_vbox.addLayout(field_graph_hbox)

        mom_la_hbox = QtWidgets.QHBoxLayout()
        self.momentum_plot = plot(mom_la_hbox, parent)
        self.larmor_angle_plot = plot(mom_la_hbox, parent)
        main_vbox.addLayout(mom_la_hbox)

        ustart_hbox = QtWidgets.QHBoxLayout()
        self.tracking_dropdown = QtWidgets.QComboBox(parent)
        self.tracking_dropdown.addItems(["Single particle", "Beam", "Ring"])
        ustart_hbox.addWidget(self.tracking_dropdown)
        self.ustart_label = make_label(ustart_hbox, parent, "Initial particle position", True)
        self.x_label, self.x_spin = labelled_spinner(ustart_hbox, parent, "&x", "mm",
                                                     "Initial horizontal position of the particle", 1, 200, -200)
        _, self.xdash_spin = labelled_spinner(ustart_hbox, parent, "x'", "mrad",
                                              "Initial horizontal angle of the particle", 0, 200, -200)
        self.y_label, self.y_spin = labelled_spinner(ustart_hbox, parent, "&y", "mm",
                                                     "Initial vertical position of the particle", 1, 200, -200)
        _, self.ydash_spin = labelled_spinner(ustart_hbox, parent, "y'", "mrad",
                                              "Initial vertical angle of the particle", 0, 200, -200)
        self.thickness_label, self.thickness_spin = labelled_spinner(ustart_hbox, parent, "thickness", "mm",
                                                                     "Thickness of a ring-shaped beam", 0.1, 10)
        self.thickness_label.setVisible(False)
        self.thickness_spin.setVisible(False)
        main_vbox.addLayout(ustart_hbox)

        self.xy_plot_hbox = QtWidgets.QHBoxLayout()
        self.xy_plot = plot(self.xy_plot_hbox, parent)
        self.xdash_ydash_plot = plot(self.xy_plot_hbox, parent)
        self.initial_beam_plot = self.final_beam_plot = None  # define these later in parasol.py
        main_vbox.addLayout(self.xy_plot_hbox)
        self.uend_label = QtWidgets.QLabel(parent)
        main_vbox.addWidget(self.uend_label)
        rf_solenoid_tracker.setCentralWidget(parent)
        rf_solenoid_tracker.setWindowTitle("Parasol - Combined RF & Solenoid Tracking")
        QtCore.QMetaObject.connectSlotsByName(rf_solenoid_tracker)
