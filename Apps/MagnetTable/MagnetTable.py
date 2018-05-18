#!python2
# -*- coding: utf-8 -*-
# encoding=utf8
"""
VELA/CLARA magnet table
v1.0, January 2017
Ben Shepherd
"""

from PyQt4 import QtCore, QtGui  # for GUI building
import sys
from collections import namedtuple, OrderedDict
import math  # conversion between radians/degrees
import os  # clicking URLs on labels, setting env variables
import numpy as np  # handling polynomials
import re  # parsing lattice files
import scipy.constants  # speed of light
import webbrowser  # to get help
sys.path.insert(0, r'\\apclara1\ControlRoomApps\Controllers\bin\Release')
import VELA_CLARA_Magnet_Control as VC_MagCtrl
import VELA_CLARA_BPM_Control
import epics
# import CLARA_Magnet_Control as CLARA_MagCtrl
from pkg_resources import resource_filename
sys.path.append('../../Widgets/loggerWidget')
try:
    import loggerWidget as lw
except ImportError:
    lw = None
import logging
from time import sleep, time

os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"

class Element:
    """Used for parsing lattice files."""
    def __init__(self, el_type, **attribs):
        self.el_type = el_type
        self.attribs = attribs
        
    def __repr__(self):
        return self.el_type + ' ' + str(self.attribs)


image_credits = {
    'Offline.png': 'http://www.iconarchive.com/show/windows-8-icons-by-icons8/Network-Disconnected-icon.html',
    'Virtual.png': 'https://thenounproject.com/search/?q=simulator&i=237636',
    'Physical.png': 'http://www.flaticon.com/free-icon/car-compact_31126#term=car&page=1&position=19',
    'undo.png': 'https://www.iconfinder.com/icons/49866/undo_icon',
    'warning.png': 'http://www.iconsdb.com/orange-icons/warning-3-icon.html',
    'error.png': 'http://www.iconsdb.com/soylent-red-icons/warning-3-icon.html',
    'magnet.png': 'https://www.iconfinder.com/icons/15217/magnet_icon',
    'Open.png': 'https://www.iconfinder.com/icons/146495/data_document_documents_file_files_folder_open_open_file_open_folder_icon#size=24',
    'help.png': 'https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-help-circled-128.png',
    'log.png': 'http://www.charitysciencehealth.com/',
    'BPM.png': 'https://www.flaticon.com/free-icon/target_118753#term=target&page=1&position=31'}
    
# Define the speed of light. We need this to convert field integral to angle or K.
# e.g. theta = field_int * c / p[eV/c]
# (derive using mv²/rho=BeV, field_int=B.s, theta=s/rho, p[kg.m/s]=p[eV/c].e.(1V)/c)
SPEED_OF_LIGHT = scipy.constants.c / 1e6  # in megametres/second, use with p in MeV/c

label_size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

online_text_format = u'''<b>Read current</b>: {read_current:.3f} A
                         <br><b>Integrated {attributes.strength_name}</b>: {int_strength:.3f} {attributes.int_strength_units}
                         <br><b>Central {attributes.strength_name}</b>: {strength:.3f} {attributes.strength_units}'''

# Each type of magnet has some common attributes - here's how we access them
mag_attr = namedtuple('mag_attr', 'friendly_name effect_name effect_units strength_name strength_units int_strength_units')
mag_attributes = {
    'BSOL': mag_attr('Bucking solenoid', 'Field at cathode', 'T', 'field', 'T', 'T.mm'),
    'SOL':  mag_attr('Solenoid', 'Larmor angle', u'°', 'field', 'T', 'T.mm'),
    'DIP':  mag_attr('Dipole', 'Angle', u'°', 'field', 'T', 'T.mm'),
    'QUAD': mag_attr('Quadrupole', 'K', u'm⁻²', 'gradient', 'T/m', 'T'),
    'SEXT': mag_attr('Sextupole', 'K', u'm⁻³', 'gradient', u'T/m²', 'T/m'),
    'HCOR': mag_attr('H Corrector', 'Angle', 'mrad', 'field', 'mT', 'T.mm'),
    'VCOR': mag_attr('V Corrector', 'Angle', 'mrad', 'field', 'mT', 'T.mm'),
    'UNKNOWN_MAGNET_TYPE': mag_attr('Unknown', 'Strength', 'AU', 'strength', 'AU', 'AU'),
    'BPM': mag_attr('Beam position monitor', 'X position', '', 'Y position', '', '')}

def format_when_present(format_string, obj, attr):
    """"Returns a formatted string with the object's given attribute,
    or a blank string when the attribute is not present or begins UNKNOWN."""
    try:
        value = getattr(obj, attr)
        if (type(value) is str and value[:7] == 'UNKNOWN') or value is None:
            return ''
        else:
            return format_string.format(value)
    except AttributeError:
        return ''

def pixmap(icon_name):
    icon_filename = os.getcwd() + r'\resources\magnetTable\Icons\{}.png'.format(icon_name)
    return QtGui.QPixmap(icon_filename)

# for debugging
import functools
def echo(fn):
     from itertools import chain
     @functools.wraps(fn)
     def wrapped(*v, **k):
         name = fn.__name__
         print ("%s(%s)" % (name, ", ".join(map(repr, chain(v, k.values())))))
         return fn(*v, **k)
     return wrapped


class Magnet(object):
    """Currently doesn't do anything in particular - just a container for magnet properties."""

    def __init__(self, name):
        self.name = name
        self.is_junction = False
        self.divert = False

    def __repr__(self):
        return '<Magnet {}>'.format(self.name)


class BPM(object):
    """Currently doesn't do anything in particular - just a container for BPM properties."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<BPM {}>'.format(self.name)


logger = logging.getLogger('Magnet Table')
mag_init_VC = VC_MagCtrl.init()
bpm_init = VELA_CLARA_BPM_Control.init()
magnet_controllers = {}
bpm_controllers = {}
section_attr = namedtuple('section_attr', 'title machine_area default_momentum min_pos max_pos')
section_attr.__new__.__defaults__ = (float('-inf'), float('inf'))
sections = OrderedDict([
                        ('VELA_INJ', section_attr('VELA Injector', 'VELA_INJ',  4.0)),
                        ('S01', section_attr('CLARA Straight 1',   'CLARA_PH1', 4.0, -1, 1)),
                        ('S02', section_attr('CLARA Straight 2',   'CLARA_PH1', 50.0, 1)),
                        ])

class Window(QtGui.QMainWindow):
    
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        ini_filename = os.getcwd() + r'\resources\magnetTable\MagnetTable.ini'
        self.settings = QtCore.QSettings(ini_filename, QtCore.QSettings.IniFormat)
        main_frame = QtGui.QFrame()
        layout = QtGui.QVBoxLayout(self)
        main_frame.setLayout(layout)
        self.setCentralWidget(main_frame)

        checkbox_grid = QtGui.QHBoxLayout()
        magnet_types = [('Dipoles', ('DIP',)), ('Quadrupoles', ('QUAD',)), ('Correctors', ('HCOR', 'VCOR')),
                        ('Solenoids', ('SOL', 'BSOL')), ('BPMs', ('BPM',))]
        for mag, types in magnet_types:
            checkbox = QtGui.QCheckBox(mag)
            checkbox.help_text = 'Toggle visibility of <b>' + mag.lower() + '</b>.'
            checkbox.setIcon(QtGui.QIcon(pixmap(mag)))
            checkbox.setChecked(True)
            checkbox.types_to_show = types
            checkbox.clicked.connect(self.toggleMagType)
            checkbox_grid.addWidget(checkbox)

        layout.addLayout(checkbox_grid)
        checkbox_grid = QtGui.QHBoxLayout()

        machine_modes = ('Offline', 'Virtual', 'Physical')
        mode_combo = QtGui.QComboBox()
        mode_combo.help_text = "Switch between the <b>virtual</b> and <b>physical</b> machines. There is also an " \
            "<b>offline</b> mode that doesn't connect to anything."
        checkbox_grid.addWidget(mode_combo)
        mode_combo.activated.connect(self.machineModeRadioClicked)
        [mode_combo.addItem(QtGui.QIcon(pixmap(mode)), mode) for mode in machine_modes]
        set_mode = str(self.settings.value('machine_mode', 'Offline').toString())
        try:
            i = machine_modes.index(set_mode)
        except ValueError:
            i = 0
        mode_combo.setCurrentIndex(i)
        self.setMachineMode(set_mode)

        label = QtGui.QLabel('On momentum change:')
        checkbox_grid.addWidget(label)
        mom_modes = ('Recalculate K', 'Scale currents')
        mode_combo = QtGui.QComboBox()
        help_text = "When the momentum value is altered for a section, either <b>recalculate</b> all the " \
            "K values for that section, or <b>scale</b> the magnet currents to keep the K values the same."
        label.help_text = help_text
        mode_combo.help_text = help_text
        checkbox_grid.addWidget(mode_combo)
        mode_combo.activated.connect(self.momentumModeRadioClicked)
        [mode_combo.addItem(QtGui.QIcon(pixmap(mode.lower().replace(' ', '_'))), mode) for mode in mom_modes]
        set_mode = self.settings.value('momentum_mode', mom_modes[0]).toString()
        try:
            i = mom_modes.index(set_mode)
        except ValueError:
            i = 0
        mode_combo.setCurrentIndex(i)
        self.mom_mode_combo = mode_combo

        load_button = QtGui.QPushButton(QtGui.QIcon(pixmap('Open')), 'Load...')
        load_button.help_text = "<b>Load</b> magnet settings from an .lte (lattice) file."
        load_button.setToolTip('Read in a lattice file')
        checkbox_grid.addWidget(load_button)
        load_button.clicked.connect(self.loadButtonClicked)

        help_button = QtGui.QPushButton(QtGui.QIcon(pixmap('help')), '')

        help_button.setToolTip('Get help on this program')
        help_button.setMaximumWidth(32)
        checkbox_grid.addWidget(help_button, 0)
        help_button.clicked.connect(lambda: webbrowser.open('http://projects.astec.ac.uk/VELAManual2/index.php/Magnet_table'))

        log_button = QtGui.QPushButton(QtGui.QIcon(pixmap('log')), '')
        log_button.setCheckable(True)
        log_button.setToolTip('Show the log')
        log_button.setMaximumWidth(32)
        checkbox_grid.addWidget(log_button, 0)
        log_button.clicked.connect(self.logButtonClicked)
        log_button.setEnabled(lw is not None)

        layout.addLayout(checkbox_grid)

        hbox = QtGui.QHBoxLayout()
        layout.addLayout(hbox)

        scroll_area = QtGui.QScrollArea(self)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        hbox.addWidget(scroll_area, 3)
        
        section_container = QtGui.QWidget()
        section_list = QtGui.QVBoxLayout(section_container)
        scroll_area.setWidgetResizable(True)

        scroll_area.setWidget(section_container)

        magnet_list = {}
        section_font = QtGui.QFont('', 16, QtGui.QFont.Bold)
        magnet_font = QtGui.QFont('', 14, QtGui.QFont.Bold)
        self.magnets = OrderedDict()
        self.bpms = OrderedDict()
        self.wait_for = {} # what magnet(s) and SI are we waiting for?
        pv_root_re = re.compile('^VM-(.*):$')
        for key, section in sections.items():
            section_name = section.title
            section_vbox = QtGui.QVBoxLayout()
            header_hbox = QtGui.QHBoxLayout()
            header_hbox.setAlignment(QtCore.Qt.AlignTop)
            magnet_list_frame = QtGui.QFrame()
            title = self.collapsing_header(header_hbox, magnet_list_frame, u'▲ ' + section_name + '\t',
                                           help_text="Click to collapse/expand the " + section_name + " section.")
            title.setFont(section_font)
            magnet_list_frame.title_label = title
            min_momentum = 1.0
            momentum_value, ok = self.settings.value(section.title + '/momentum', section.default_momentum).toFloat()
            momentum = self.spinbox(header_hbox, 'MeV/c', step=0.1, value=momentum_value, decimals=3,
                                    min_value=min_momentum, help_text="Set the momentum of the " + section_name + " section. ")
            momentum.valueChanged.connect(self.momentumChanged)
            section_vbox.addLayout(header_hbox)
            magnet_list_vbox = QtGui.QVBoxLayout()
            magnet_list_frame.setLayout(magnet_list_vbox)
            magnet_list_vbox.momentum_spin = momentum  # so we can reference it from a magnet
            magnet_list_vbox.id = key
            momentum.magnet_list_vbox = magnet_list_vbox
            magnet_list[key] = magnet_list_vbox
            section_vbox.addWidget(magnet_list_frame)
            section_list.addLayout(section_vbox)

            magnet_controller = magnet_controllers[key]
            bpm_controller = bpm_controllers[key]
            mag_names = list(magnet_controller.getMagnetNames())
            bpm_names = list(bpm_controller.getBPMNames()) if bpm_controller is not None else []
            # Filter to make sure we only get the ones for this section
            mag_names = [(magnet_controller.getPosition(name), name) for name in mag_names
                         if section.min_pos <= magnet_controller.getPosition(name) <= section.max_pos]
            mag_names.extend([(bpm_controller.getPosition(name), name) for name in bpm_names
                         if section.min_pos <= bpm_controller.getPosition(name) <= section.max_pos])
            # These don't come in the right order so need to sort them too
            mag_names.sort()
            for pos, name in mag_names:
                # Extract type without querying the object directly, e.g. L01-SOL -> SOL, C2V-BPM01 -> BPM
                mag_type = ''.join([c for c in name.split('-')[-1] if not c.isdigit()])
                magnet_frame = QtGui.QFrame()
                magnet_frame.setFrameShape(QtGui.QFrame.Box | QtGui.QFrame.Plain)
                magnet_frame.setStyleSheet(
                    '#branch {background-color: #ffffee;} #junction {background-color: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #f0f0f0, stop:1 #ffffee);}')
                magnet_vbox = QtGui.QVBoxLayout()
                magnet_frame.setLayout(magnet_vbox)
                main_hbox = QtGui.QHBoxLayout()
                main_hbox.setAlignment(QtCore.Qt.AlignTop)
                magnet_vbox.addLayout(main_hbox)
                more_info = QtGui.QFrame()
                attributes = mag_attributes[mag_type]
                # 'H Corrector' -> 'Correctors'; 'Quadrupole' -> 'Quadrupoles'
                generic_name = attributes.friendly_name + 's'

                show_hide_info = "Click to show/hide more information about <b>{}</b>.".format(name)
                icon = self.collapsing_header(main_hbox, more_info, help_text=show_hide_info)
                icon.setPixmap(pixmap(generic_name).scaled(32, 32))
                # The tab here aligns all the current spinboxes nicely
                # Remove the S01- or S02- prefix at the start for a cleaner look
                title_text = name.split('-')[-1] + '\t'
                title = self.collapsing_header(main_hbox, more_info, title_text, help_text=show_hide_info)
                title.setFont(magnet_font)
                self.collapsing_header(main_hbox, more_info, attributes.effect_name, help_text=show_hide_info)
                static_info = ['<b>', name, '</b> ', attributes.friendly_name]

                more_info_layout = QtGui.QHBoxLayout()
                more_info.setLayout(more_info_layout)

                offline_info = QtGui.QLabel()
                offline_info.linkActivated.connect(lambda url: os.system('start "" "' + str(url) + '"'))
                offline_info.setAlignment(QtCore.Qt.AlignTop)
                offline_info.help_text = ''
                more_info_layout.addWidget(offline_info)
                online_info = QtGui.QLabel()
                online_info.setAlignment(QtCore.Qt.AlignTop)
                online_info.help_text = ''
                more_info_layout.addWidget(online_info)

                if 'BPM' in name:
                    bpm = BPM(name)
                    self.bpms[key + '_' + name] = bpm
                    bpm.ref = bpm_controller.getBPMDataObject(name)
                    bpm.x_label = self.collapsing_header(main_hbox, more_info, help_text=show_hide_info)
                    # show "Y position" label
                    self.collapsing_header(main_hbox, more_info, attributes.strength_name, help_text=show_hide_info)
                    bpm.y_label = self.collapsing_header(main_hbox, more_info, help_text=show_hide_info)
                    static_info.append(format_when_present('<br><b>Position</b>: {:.3f} m', bpm.ref, 'position'))
                    # No branch info for BPMs (yet), we have to add it ourselves
                    if 'C2V' in name:
                        in_branch = True
                        branch_name = 'DIP01'
                    elif key == 'VELA_INJ' and name == 'BPM03':
                        in_branch = True
                        branch_name = 'DIP01'
                    else:
                        in_branch = False
                        branch_name = 'UNKNOWN_MAGNET_BRANCH'
                    magnet_frame.magnet = bpm
                else:
                    # need a more specific dict key, since self.magnets contains magnets from several sections
                    magnet = Magnet(name)
                    self.magnets[key + '_' + name] = magnet
                    magnet.section = magnet_list_vbox
                    magnet.ref = magnet_controller.getMagObjConstRef(magnet.name)
                    lbl, units = 'Current', 'A'

                    # Replace the PV root VM-XXX: --> XXX
                    magnet.pv_base = re.sub(pv_root_re, r'\1', magnet.ref.pvRoot)

                    if mag_type in ('SOL', 'BSOL'):
                        # The coefficients work a little differently - use a different attribute to calculate the
                        # K value (Larmor angle or field at cathode)
                        # and replace the original so that it really represents the coeffs for integrated strength
                        magnet.k_coeffs = np.array(magnet.ref.fieldIntegralCoefficients[:-4])
                        magnet.fieldIntegralCoefficients = np.array(magnet.ref.fieldIntegralCoefficients[-4:])
                    else:
                        # In any case, make the FICs an attribute of the magnet object rather than the ref
                        # so that it persists even when we switch between machine modes
                        magnet.fieldIntegralCoefficients = np.array(magnet.ref.fieldIntegralCoefficients)
                    # rev_type = magnet.ref.magRevType  #  23/6 magRevType not implemented

                    magnet.prev_values = []
                    magnet.active = False  # whether magnet is being changed

                    magnet_frame.magnet = magnet
                    magnet.magnet_frame = magnet_frame
                    magnet.icon = icon
                    magnet.title = title
                    # bipolar = mag_type in ('BSOL', 'SOL', 'DIP')  # not rev_type == VC_MagCtrl.MAG_REV_TYPE.POS
                    max_current = magnet.ref.maxI
                    min_current = magnet.ref.minI
                    if min_current == -999.999:  # default value, means no min has been set
                        min_current = float('-inf')
                        # min_k = min_current
                    # else:
                    #     min_k = self.getK(magnet, min_current, min_momentum)
                    if max_current == -999.999:  # default value, means no max has been set
                        max_current = float('inf')
                        # max_k = max_current
                    # else:
                    #     max_k = self.getK(magnet, max_current, min_momentum)
                    step = 0.01 if mag_type == 'BSOL' else 0.1
                    help_text = "Set the {} in the <b>{}</b> magnet. The magnet current will be automatically adjusted, depending on the momentum in the {} section. ".format(
                        attributes.effect_name.lower(), magnet.name, section_name)
                    k_spin = self.spinbox(main_hbox, attributes.effect_units, step=step, decimals=3,
                                          help_text=help_text) #, min_value=min_k, max_value=max_k)
                    magnet.k_spin = k_spin
                    branch_name = magnet.ref.magnetBranch
                    in_branch = branch_name != 'UNKNOWN_MAGNET_BRANCH'
                    if mag_type == 'DIP':
                        magnet.branch_button = QtGui.QToolButton()
                        magnet.branch_button.setCheckable(True)
                        magnet.branch_button.clicked.connect(self.branchButtonClicked)
                        magnet.branch_button.magnet = magnet  # link back to this magnet when clicked
                        magnet.branch_button.setToolTip('Toggle branch on/off')
                        magnet.branch_button.help_text = "Click to toggle this dipole, either sending the beam straight through, or onto a branch."
                        branch_icon = QtGui.QIcon()
                        branch_icon.addPixmap(pixmap('branch-off'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        branch_icon.addPixmap(pixmap('branch-on'), QtGui.QIcon.Normal, QtGui.QIcon.On)
                        magnet.branch_button.setIcon(branch_icon)
                        main_hbox.addWidget(magnet.branch_button)

                    self.collapsing_header(main_hbox, more_info, lbl, help_text=show_hide_info)
                    help_text = "Set the current in the <b>{}</b> magnet. The {} will be calculated, depending on the momentum in the {} section. ".format(
                        magnet.name, attributes.effect_name.lower(), section_name)
                    current_spin = self.spinbox(main_hbox, units, step=0.1, decimals=3,
                                                min_value=min_current, max_value=max_current, help_text=help_text)
                    magnet.current_spin = current_spin
                    if mag_type == 'DIP':
                        magnet.set_mom_checkbox = QtGui.QCheckBox('Set momentum')
                        magnet.set_mom_checkbox.setSizePolicy(label_size_policy)
                        magnet.set_mom_checkbox.setToolTip("Calculate the beam's momentum by adjusting this magnet's current")
                        magnet.set_mom_checkbox.help_text = u"Measure the momentum using this dipole. First, set the dipole angle to 45°. " \
                            "Then check this box and adjust the current until the beam is centred on the screen. The momentum in the {} section " \
                            "will be automatically set. Finally, clear the checkbox."
                        main_hbox.addWidget(magnet.set_mom_checkbox)

                    restore_button = QtGui.QToolButton()
                    restore_button.setIcon(QtGui.QIcon(pixmap('undo')))
                    restore_button.clicked.connect(self.restoreMagnet)
                    restore_button.setToolTip('Undo')
                    restore_button.help_text = "Undo the previous change to the <b>{}</b> magnet. Multiple changes while the control has the focus are counted as one.".format(magnet.name)
                    main_hbox.addWidget(restore_button)
                    magnet.restore_button = restore_button
                    restore_button.setEnabled(False)
                    self.empty_icon = QtGui.QPixmap(24, 24)
                    self.empty_icon.fill(QtCore.Qt.transparent)
                    warning_icon = self.collapsing_header(main_hbox, more_info)
                    warning_icon.setPixmap(self.empty_icon)
                    warning_icon.help_text = "An orange warning icon indicates that the magnet's read value and set value are different. Red indicates that the magnet is not powered on. " + show_hide_info
                    magnet.warning_icon = warning_icon
                    #TODO: warn when magnet needs degaussing
                    static_info.extend(
                        [format_when_present('<br><b>Manufactured by</b> {}', magnet.ref, 'manufacturer'),
                         format_when_present('<br><b>Serial number</b> {}', magnet.ref, 'serialNumber'),
                         format_when_present('<br><b>Magnetic length</b>: {:.1f} mm', magnet.ref,
                                             'magneticLength'),
                         format_when_present('<br><a href="{}">Measurement data</a>', magnet.ref,
                                             'measurementDataLocation'),
                         format_when_present('<br><b>Position</b>: {:.3f} m', magnet.ref, 'position')])
                    magnet.online_info = online_info
                offline_info.setText(''.join(static_info))
                more_info.hide()
                magnet_vbox.addWidget(more_info)
                title.toggle_frame = more_info
                    # title.installEventFilter(self)
                magnet_list_vbox.addWidget(magnet_frame)

                # different shading for magnets in branches, and smooth transition at junctions
                if in_branch:
                    magnet_frame.setObjectName('branch')
                    junc_magnet = self.magnets[key + "_" + branch_name]
                    junc_magnet.is_junction = True
                    junc_magnet.magnet_frame.setObjectName('junction')
                end_of_branch = False  # magnet.name in ('QUAD06', 'QUAD14')
                magnet_frame.setLineWidth(3 if end_of_branch else 1)
                magnet_frame.setContentsMargins(0, 0, 0, 3 if end_of_branch else 1)

        self.helpLabel = QtGui.QLabel()
        self.helpLabel.setWordWrap(True)
        self.helpLabel.setStyleSheet("QLabel { background-color : rgb(255, 248, 220); }")
        self.helpLabel.setText('Welcome to the <b>Magnet Table</b>. Hover over any control for detailed help.')
        self.helpLabel.help_text = ''
        layout.addWidget(self.helpLabel)

        if lw is not None:
            self.log_widget = lw.loggerWidget(logger)
            self.log_widget.hide()
            hbox.addWidget(self.log_widget, 2)

        # set up events (need to do setup first)
        for magnet in self.magnets.values():
            magnet.current_spin.valueChanged.connect(self.currentValueChanged)
            magnet.current_spin.setValue(magnet.ref.siWithPol)
            magnet.k_spin.valueChanged.connect(self.kValueChanged)
            magnet.restore_button.setEnabled(False) # will be automatically shown when event triggered
            magnet.active = False

        self.magnet_controls = magnet_list
        self.setWindowTitle('Magnet Table')
        rect = self.settings.value('geometry', QtCore.QRect(300, 300, 400, 600)).toRect()
        self.setGeometry(rect)
        self.update_period = 100  # milliseconds
        self.startMainViewUpdateTimer()
        self.setWindowIcon(QtGui.QIcon(pixmap('magnet')))
        self.show()

    def collapsing_header(self, parent_widget, more_info, label_text='', help_text=''):
        """Make a label that shows or hides the more_info widget when clicked."""
        label = QtGui.QLabel(label_text)
        if help_text:
            label.help_text = help_text
        label.setSizePolicy(label_size_policy)
        label.setCursor(QtCore.Qt.PointingHandCursor)
        label.toggle_frame = more_info
        # label.installEventFilter(self)
        parent_widget.addWidget(label)
        return label
        
    def spinbox(self, parent, units, step=None, value=float('nan'), decimals=2,
                min_value=float('-inf'), max_value=float('inf'), help_text = ''):
        """Make a double-valued spinbox."""
        spinbox = QtGui.QDoubleSpinBox()
        spinbox.setSuffix(' ' + units)
        spinbox.setValue(value)
        spinbox.setDecimals(decimals)
        spinbox.setRange(min_value, max_value)
        spinbox.setKeyboardTracking(False)
        if step:
            spinbox.setSingleStep(step)
        more_help_text = help_text + "Hold SHIFT + mouse wheel to adjust by small steps, and CTRL + SHIFT + mouse wheel to adjust by large steps."
        spinbox.help_text = more_help_text
        spinbox.lineEdit().help_text = more_help_text
        parent.addWidget(spinbox)
        # spinbox.installEventFilter(self)
        return spinbox
    
    # these functions update the GUI and (re)start the timer
    def startMainViewUpdateTimer(self):
        self.widgetUpdateTimer = QtCore.QTimer()
        self.widgetUpdateTimer.timeout.connect(self.mainViewUpdate)
        self.widgetUpdateTimer.start(self.update_period)
    def mainViewUpdate(self):
        # conceivably the timer could restart this function before it complete - so guard against that
        try:
            self.updateMagnetWidgets()
        finally:
            self.widgetUpdateTimer.start(self.update_period)
            
    def updateMagnetWidgets(self):
        """Update the GUI with values from the control system."""
        # For 'offline', the readbacks are useless, so just don't bother
        offline = self.settings.value('machine_mode') == 'Offline'
        for magnet in self.magnets.values():
            set_current = magnet.current_spin.value() if offline else magnet.ref.siWithPol
            read_current = magnet.current_spin.value() if offline else magnet.ref.riWithPol
            if not magnet.ref.psuState == VC_MagCtrl.MAG_PSU_STATE.MAG_PSU_ON:
                magnet.warning_icon.setPixmap(pixmap('error'))
                magnet.warning_icon.setToolTip('Magnet PSU: ' + str(magnet.ref.psuState)[8:])
            elif abs(set_current - read_current) > magnet.ref.riTolerance:
                magnet.warning_icon.setPixmap(pixmap('warning'))
                magnet.warning_icon.setToolTip('Read current and set current do not match')
            else:
                magnet.warning_icon.setPixmap(self.empty_icon)
            mag_type = str(magnet.ref.magType)
            if mag_type == 'QUAD':
                magnet.icon.setPixmap(pixmap('Quadrupole_' + ('F' if set_current >= 0 else 'D')).scaled(32, 32))
            # are we waiting for the SI value for this magnet to 'take'?
            try:
                if abs(set_current - self.wait_for[magnet]) <= 0.001:  # it's taken now! # TODO: tolerance from somewhere?
                    self.wait_for.pop(magnet)  # remove it from 'waiting for' list
            except KeyError:  # we're not waiting for this one
                if not magnet.current_spin.hasFocus():
                    magnet.current_spin.setValue(set_current)
            # if magnet is self.wait_for_magnet and abs(set_current - self.wait_for_value) <= 0.001:  # it's taken now! # TODO: tolerance from somewhere?
            #     self.wait_for_magnet = None
            # if not magnet.current_spin.hasFocus() and magnet is not self.wait_for_magnet:
            #     magnet.current_spin.setValue(set_current)
            attributes = mag_attributes[mag_type]
            int_strength = np.copysign(np.polyval(magnet.fieldIntegralCoefficients, abs(set_current)), set_current)
            strength = int_strength / magnet.ref.magneticLength if magnet.ref.magneticLength else 0
            if mag_type == 'QUAD' or mag_type[1:] == 'COR':
                strength *= 1000  # convert to mT for correctors, T/m for quads
            magnet.online_info.setText(online_text_format.format(**locals()))
        for bpm in self.bpms.values():
            bpm.x_label.setText('<b>{:.3f} mm</b>\t'.format(bpm.ref.xPV))
            bpm.y_label.setText('<b>{:.3f} mm</b>'.format(bpm.ref.yPV))

    def eventFilter(self, source, event):
        """Enable scroll wheel functionality for the spin boxes, and also make clickable labels that
        make extra information appear and disappear (collapsing_headers)."""
        evType = event.type()
        modifiers = QtGui.QApplication.keyboardModifiers()
        if evType == QtCore.QEvent.MouseButtonRelease:
            try:
                frame = source.toggle_frame
                vis = frame.isVisible()
                frame.setVisible(not vis)
                frame.title_label.setText((u'▼' if vis else u'▲') + frame.title_label.text()[1:])
            except:
                pass  # no toggle_frame - never mind (or perhaps no title_label)
        elif evType == QtCore.QEvent.MouseMove:
            # show help text when mouse hovers over a control
            try:
                text = source.parent().help_text if type(source) is QtGui.QLineEdit else source.help_text
                self.helpLabel.setText(text)
            except AttributeError:  # no help text for this control
                pass
        elif type(source) in (QtGui.QLineEdit, QtGui.QDoubleSpinBox):
            # event was triggered in a magnet spin box (K or current)
            if evType == QtCore.QEvent.Wheel:
                # don't allow changes if Shift isn't pressed -
                # makes it easier to scroll the window up and down
                if not (modifiers & QtCore.Qt.ShiftModifier):
                    return True  # do nothing
            elif evType == QtCore.QEvent.FocusOut:
                # record the change to a magnet
                try:
                    magnet = source.parent().magnet
                    magnet.active = False
                except AttributeError: # won't work for momentum spin boxes
                    pass
        elif evType == QtCore.QEvent.Wheel and (modifiers & QtCore.Qt.ShiftModifier):
            # don't allow scrolling if Shift _is_ held outwith a spin box -
            # otherwise we'll accidentally scroll the window while we're trying to
            # modify the spin box and the mouse slips a bit_length
            return True
        return QtGui.QMainWindow.eventFilter(self, source, event)
    
    def toggleMagType(self, toggled):
        """Called when a magnet type checkbox is clicked. Hide or show all the magnets of that type."""
        #which checkbox was clicked? remove 's' from end, last 6 letters, lower case
        types_to_show = self.sender().types_to_show
        logger.info(('Show ' if toggled else 'Hide ') + ','.join(types_to_show))
        for mag_list in self.magnet_controls.values():
            for i in range(mag_list.count()):
                magnet_vbox = mag_list.itemAt(i).widget()
                mag_type = ''.join([c for c in magnet_vbox.magnet.name.split('-')[-1] if not c.isdigit()])
                if mag_type in types_to_show:
                    magnet_vbox.setVisible(toggled)

    def currentValueChanged(self, value):
        """Called when a current spin box is changed by the user."""
        magnet = self.sender().parent().magnet
        magnet_controllers[magnet.section.id].setSI(magnet.name, value)
        # Stop the GUI updating until the SI value 'takes' - otherwise it will update from an old value and be 'sticky'
        # Add it to a list of "waiting for" magnets. We might need more than one if we're changing the momentum in a section
        self.wait_for[magnet] = value
        # self.wait_for_magnet, self.wait_for_value = magnet, value
        
        if str(magnet.ref.magType) == 'DIP' and magnet.set_mom_checkbox.isChecked():
            # 'Set momentum' checkbox is ticked - we are using this dipole to check the momentum
            # Calculate and set the momentum for this section
            int_strength = np.polyval(magnet.fieldIntegralCoefficients, abs(value))
            angle = magnet.k_spin.value()
            momentum = 0.001 * SPEED_OF_LIGHT * int_strength / np.radians(angle)
            magnet.section.momentum_spin.setValue(momentum)
            # To avoid a lot of iterating between K and current: check the calling function's name
        elif not sys._getframe(1).f_code.co_name == 'calcCurrentFromK':
            self.calcKFromCurrent(magnet)

        # If we're already changing this magnet, alter the last value
        # Otherwise add a value
        if magnet.active:
            magnet.prev_values[-1] = value
        else:
            magnet.prev_values.append(value)
        try:
            magnet.restore_button.setEnabled(True)
            magnet.restore_button.setToolTip('Restore previous value ({:.3f} A)'.format(magnet.prev_values[-2]))
            magnet.active = True
        except (AttributeError, IndexError):
            # fails on first time (no button yet)
            # and when first value is restored (no -2 index)
            pass

    def momentumChanged(self, value):
        """Called when a momentum spin box is changed by the user."""
        section = self.sender().magnet_list_vbox
        momentum = self.sender().value()
        self.settings.setValue(section.id + '/momentum', momentum)
        # Put the momentum in the correct PV
        try:
            if section.id == 'S01':
                epics.caput('CLA-LRG1-DIA-MOM-01:RB', momentum)
            elif section.id == 'S02':
                epics.caput('CLA-L01-DIA-MOM-01:RB', momentum)
        except:
            pass

        mode = self.mom_mode_combo.currentText()
        changeFunc = self.calcKFromCurrent if mode == 'Recalculate K' else self.calcCurrentFromK
        for magnet in self.magnets.values():
            if magnet.section == section:
                # Ensure dipoles with the "Set momentum" checkbox ticked are not modified
                if not (str(magnet.ref.magType) == 'DIP' and magnet.set_mom_checkbox.isChecked()):
                    changeFunc(magnet)

    def magnetsOfType(self, section, type_str):
        """Return all magnets of a given type within the given section."""
        for magnet in self.magnets.values():
            if magnet.section == section and str(magnet.ref.magType) == type_str:
                yield magnet

    def calcKFromCurrent(self, magnet):
        """Calculate the K value (or bend angle) of a magnet based on its current, and update the GUI."""
        current = magnet.current_spin.value()
        # What is the momentum in this section?
        momentum = magnet.section.momentum_spin.value()
        # Call procedure to actually do the calculation
        k = self.getK(magnet, current, momentum)
        mag_type = str(magnet.ref.magType)
        if mag_type == 'SOL' and magnet.ref.magnetBranch != 'UNKNOWN_MAGNET_BRANCH':
            # A solenoid with a defined branch signifies that it has an attached bucking solenoid
            # We should also recalculate the field at the cathode
            self.calcKFromCurrent(next(self.magnetsOfType(magnet.section, 'BSOL')))
        magnet.k_spin.setValue(k)

    def branchButtonClicked(self, checked):
        """The 'branch' tool button on a dipole has been clicked. Toggle 0 or 45° for the angle.from scipy import constants"""
        magnet = self.sender().magnet
        # Currently only have 45° dipoles, need to update this for spectrometer line dipoles which are 30°
        magnet.k_spin.setValue(45 if checked else 0)

    def getK(self, magnet, current, momentum):
        """Perform the calculation of K value (or bend angle)."""

        # Get the integrated strength, based on an excitation curve
        # This is in T.mm for dipoles, T for quads, T/m for sextupoles
        # Note that excitation curves are defined with positive current,
        # so we have to take the absolute value and then later reapply the sign
        int_strength = np.polyval(magnet.fieldIntegralCoefficients, abs(current))
        # Calculate the normalised effect on the beam
        # This is in radians for dipoles, m⁻¹ for quads, m⁻² for sextupoles
        effect = np.copysign(SPEED_OF_LIGHT * int_strength / momentum, current)
        # Depending on the magnet type, convert to meaningful units
        mag_type = str(magnet.ref.magType)
        if mag_type == 'DIP':
            # Get deflection in degrees
            # int_strength was in T.mm so we divide by 1000
            k = math.degrees(effect / 1000)
        elif mag_type in ('QUAD', 'SEXT'):
            k = 1000 * effect / magnet.ref.magneticLength  # focusing term K
        elif mag_type in ('HCOR', 'VCOR'):
            k = effect  # deflection in mrad
        elif mag_type == 'BSOL':  # bucking coil
            # For the BSOL, coefficients refer to the solenoid current as well as the BSOL current
            # The 'K' value is the field at the cathode
            # x is BC current, y is solenoid current
            x = current
            y = next(self.magnetsOfType(magnet.section, 'SOL')).current_spin.value() #ref.siWithPol
            k = np.dot(magnet.k_coeffs,
                       [y, y**2, y**3, x, x*y, x*y**2, x**2, x**2*y, x**2*y**2, x**2*y**3, x**3, x**3*y])
        elif mag_type == 'SOL': # solenoids
            # For the solenoid, coefficients also refer to the momentum
            # The 'K' value is the Larmor angle
            I = current
            p = momentum
            k = np.dot(magnet.k_coeffs, [I, p*I, p**2*I, p**3*I, p**4*I])
        return k

    def kValueChanged(self, value):
        """Called when a K spin box is changed by the user."""
        spinbox = self.sender()
        magnet = spinbox.parent().magnet
        if str(magnet.ref.magType) == 'DIP' and magnet.is_junction:
            # hide/show magnets in branch
            magnet.divert = value > 22.5  # fairly arbitrary!
            magnet.branch_button.setChecked(magnet.divert)
            beam_branch = magnet.name
            mag_list = self.magnets.values()
            # Go through the list starting at the magnet following the junction
            for mag in mag_list[(mag_list.index(magnet) + 1):]:
                # Highlight the branch when divert is in place, and everything else when not
                highlight = (mag.ref.magnetBranch == beam_branch) == magnet.divert
                mag.title.setStyleSheet('color:#000000;' if highlight else 'color:#a0a0a0;')
        # To avoid a lot of iterating between K and current: check the calling function's name
        if not sys._getframe(1).f_code.co_name == 'calcKFromCurrent':
            self.calcCurrentFromK(magnet)
        
    def calcCurrentFromK(self, magnet):
        """Calculate the current to set in a magnet based on its K value (or bend angle)."""
        k = magnet.k_spin.value()
        # We need the absolute value, since excitation curves are only defined with positive current
        abs_k = abs(k)
        # What is the momentum in this section?
        momentum = magnet.section.momentum_spin.value()
        mag_type = str(magnet.ref.magType)
        int_strength = None
        if mag_type == 'DIP': # k represents deflection in degrees
            effect = math.radians(abs_k) * 1000
        elif mag_type in ('QUAD', 'SEXT'):
            effect = abs_k * magnet.ref.magneticLength / 1000
        elif mag_type in ('HCOR', 'VCOR'): # k represents deflection in mrad
            effect = abs_k
        else: # solenoids
            int_strength = abs_k
        if int_strength is None:
            int_strength = effect * momentum / SPEED_OF_LIGHT
        coeffs = np.copy(magnet.k_coeffs if mag_type in ('SOL', 'BSOL') else magnet.fieldIntegralCoefficients)
        if mag_type == 'BSOL':
            # These coefficients depend on solenoid current too - need to group together like terms
            y = next(self.magnetsOfType(magnet.section, 'SOL')).current_spin.value() #ref.siWithPol
            ypows = y ** np.arange(4)
            coeffs = [np.dot(coeffs[10:], ypows[:2]),  # (c10 + c11*y) * x**3
                      np.dot(coeffs[6:10], ypows),     # (c6 + c7*y + c8*y**2 + c9*y**3) * x**2
                      np.dot(coeffs[3:6], ypows[:-1]), # (c3 + c4*y + c5*y**2) * x
                      np.dot(coeffs[:3], ypows[1:])]   # (c0*y + c1*y**2 + c2*y**3)
        elif mag_type == 'SOL' and len(coeffs) > 2:
            # These coefficients depend on momentum too - need to group together like terms
            ppows = momentum ** np.arange(5)
            coeffs = [np.dot(coeffs[:5], ppows), 0]  # (c1 + c2*p + c3*p**2 + c4*p**3 + c5*p**4) * Isol

        coeffs[-1] -= int_strength  # Need to find roots of polynomial, i.e. a1*x + a0 - y = 0
        roots = np.roots(coeffs)
        current = np.copysign(roots[-1].real, k) # last root is always x value (#TODO: can prove this?)
        magnet.current_spin.setValue(current)
        if mag_type == 'SOL' and magnet.ref.magnetBranch != 'UNKNOWN_MAGNET_BRANCH':
            # We should also recalculate the field at the cathode
            self.calcKFromCurrent(next(self.magnetsOfType(magnet.section, 'BSOL')))

    def restoreMagnet(self):
        """Implement an 'undo' button for each magnet."""
        magnet = self.sender().parent().magnet
        magnet.active = False
        try:
            magnet.prev_values.pop() # first get rid of the last changed value
            undo_val = magnet.prev_values.pop() # now set the value we want to restore
            # This will fire the change event, which will append the last value (which we want)
            # and make the magnet active (which we don't)
            magnet.current_spin.setValue(undo_val)
            magnet.active = False
            if len(magnet.prev_values) == 1: # we're at the initial state
                magnet.restore_button.setEnabled(False)
                magnet.restore_button.setToolTip('')
            logger.info('Undo {magnet.name} to {undo_val:.3f} A'.format(**locals()))
        except IndexError: # pop from empty list - shouldn't happen!
            magnet.restore_button.setEnabled(False)
            magnet.restore_button.setToolTip('')
    
    def machineModeRadioClicked(self, index):
        combo = self.sender()
        mode = str(combo.currentText())
        self.setMachineMode(mode)
        # Change all the magnet references
        for magnet in self.magnets.values():
            magnet.ref = magnet_controllers[magnet.section.id].getMagObjConstRef(magnet.name)
            # Set the current_spin value
            magnet.current_spin.setValue(magnet.ref.siWithPol)
            # Reset the undo state
            magnet.prev_values = [magnet.ref.siWithPol]
            magnet.active = False
            magnet.restore_button.setEnabled(False)
            magnet.restore_button.setToolTip('')

    def momentumModeRadioClicked(self, index):
        combo = self.sender()
        mode = combo.currentText()
        logger.info('Set momentum mode: ' + mode)
        self.settings.setValue('momentum_mode', mode)
        
    def setMachineMode(self, mode=None):
        """Set the machine mode (offline/virtual/physical and redefine the controllers accordingly."""
        logger.info('Set machine mode: ' + mode)
        os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255" if mode == 'Physical' else "10.10.0.12"
        magnet_controllers.clear()
        bpm_controllers.clear()
        mode_name = VC_MagCtrl.MACHINE_MODE.names[mode.upper()]
        for key, section in sections.items():
            area = VC_MagCtrl.MACHINE_AREA.names[section.machine_area]
            magnet_controller = mag_init_VC.getMagnetController(mode_name, area)
            magnet_controllers[key] = magnet_controller
            try:
                bpm_controller = bpm_init.getBPMController(mode_name, area)
                bpm_controllers[key] = bpm_controller
            except RuntimeError:
                print("Couldn't load {} BPM controller for area {}".format(mode_name, area))
                bpm_controllers[key] = None
        self.settings.setValue('machine_mode', mode)
        #TODO: check that it actually worked

    def loadButtonClicked(self):
        """Load a lattice file and apply it to magnets."""
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open lattice file', '', 'Lattice files (*.lte);;All files (*.*)')
        if filename == '': # Cancel clicked
            return
        text = open(filename).read()
        # Handle continuation character & at end of lines
        text = text.replace('&\n', '')
        
        applied_list = ''
        for mag in self.magnets.values():
            mag_type = str(mag.ref.magType)
            # What parameter name are we looking for in the LTE file?
            if mag_type == 'QUAD':
                param = 'K1'
                conv_func = lambda k: k  # use as-is
            elif mag_type == 'DIP':
                param = 'ANGLE'
                conv_func = math.degrees  # .lte files have angles in radians
            else:
                continue  # nothing to do for other types
            regexp = '"{mag.pv_base}.*?{param}=([^,]+)'.format(**locals())
            l = re.findall(regexp, text)
            if l:
                val = conv_func(float(l[0]))
                effect = mag_attributes[mag_type].effect_name
                units = mag_attributes[mag_type].effect_units
                applied_list += u'{mag.name}: {effect} = {val:.3f} {units}\n'.format(**locals())
                mag.k_spin.setValue(val)
            
        if applied_list:
            message = u'Applied the following settings from {filename}:\n\n{applied_list}'.format(**locals())
            for line in message.split('\n'):
                logger.info(message)
        else:
            message = 'No applicable magnet settings found in {filename}'.format(**locals())
            logger.warning(message)
        QtGui.QMessageBox.about(self, 'Magnet table', message)

    def logButtonClicked(self):
        """Show or hide the log."""
        self.log_widget.setVisible(not self.log_widget.isVisible())

    def closeEvent(self, event):
        logger.info('Close app')
        self.widgetUpdateTimer.stop()
        self.settings.setValue('geometry', self.geometry())
        exit()
        
    def __repr__(self):
        return '<Magnet Table GUI>'

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    # Create and display the splash screen
    splash_pix = pixmap('splash-screen')
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    window = Window()
    app.installEventFilter(window)
    app.aboutToQuit.connect(window.close)
    window.show()
    splash.finish(window)
    sys.exit(app.exec_())
