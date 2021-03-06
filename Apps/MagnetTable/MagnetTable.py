#!python2
# -*- coding: utf-8 -*-
# encoding=utf8
"""
VELA/CLARA magnet table
v1.0, January 2017
Ben Shepherd
"""

from __future__ import print_function
from PyQt4 import QtCore, QtGui  # for GUI building
import sys
import time
from collections import namedtuple, OrderedDict
import math  # conversion between radians/degrees
import os  # clicking URLs on labels, setting env variables
import numpy as np  # handling polynomials
import re  # parsing lattice files
import scipy.constants  # speed of light
import webbrowser  # to get help
import functools  # for magnet on/off menu actions
sys.path.insert(0, r'\\apclara1\ControlRoomApps\Controllers\bin\Release')
import Magnet_Control_Physics_Units as VC_MagCtrl
import VELA_CLARA_BPM_Control
# import VELA_CLARA_enums
# sys.path[0] = r'\\apclara1\ControlRoomApps\Controllers\bin\Release'
import epics  # for setting momentum
sys.path.append('../../Widgets/loggerWidget')
try:
    import loggerWidget as lw
except ImportError:
    lw = None
import logging

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
    'BPM.png': 'https://www.flaticon.com/free-icon/target_118753#term=target&page=1&position=31',
    'cycle.png': 'https://thenounproject.com/term/cycle/4195/',
    'on.png': 'https://www.flaticon.com/free-icon/power-on-semicircle_17131',
    'off.png': 'https://www.flaticon.com/free-icon/power-on-semicircle_17131',
    'yes.png': 'https://www.flaticon.com/free-icon/check-symbol_60731',
    'no.png': 'https://www.flaticon.com/free-icon/clear-button_60994',
    'yes-all.png': 'https://www.flaticon.com/free-icon/double-tick-indicator_60727',
    'degauss.gif': 'http://icon-park.com/icon/loadingpreloading-image-spin-4-blue/',
}
    
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


class ExtendedDialog(QtGui.QMessageBox):
    """Extension of QMessageBox with checkboxes and a comment input."""

    def __init__(self, parent=None, checkboxes=[]):
        super(ExtendedDialog, self).__init__()

        # Access the Layout of the MessageBox to add the Checkboxes
        layout = self.layout()
        vbox = QtGui.QVBoxLayout()
        layout.addLayout(vbox, 1, 1)
        self.checkboxes = []
        for i, (name, checked) in enumerate(checkboxes):
            checkbox = QtGui.QCheckBox(name)
            checkbox.setChecked(checked)
            vbox.addWidget(checkbox)
            self.checkboxes.append(checkbox)
        hbox = QtGui.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addWidget(QtGui.QLabel('Comment:'))
        self.textbox = QtGui.QLineEdit()
        self.textbox.setMinimumWidth(200)
        hbox.addWidget(self.textbox)

    def exec_(self, *args, **kwargs):
        """Override the exec_ method so you can return the value of the checkboxes and the input box."""
        return QtGui.QMessageBox.exec_(self, *args, **kwargs), [box.isChecked() for box in self.checkboxes], str(self.textbox.text())


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
frame_style_sheet = '#branch {background-color: #ffffee;} #junction {background-color: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #f0f0f0, stop:1 #ffffee);}'

# Are we bundled as an EXE, or running as a script?
is_bundled = getattr(sys, 'frozen', False)
file_name = sys.executable if is_bundled else __file__
build_date = os.path.getmtime(file_name)
bundle_dir = os.path.dirname(file_name)
dburt_folder = r'\\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Snapshots\DBURT'

class Window(QtGui.QMainWindow):

    def createMenuItem(self, title, parent, event=None, help_text=None, checkable=False, icon_name=None, shortcut=None):
        action = QtGui.QAction(self)
        action.setText(title)
        parent.addAction(action)
        if event:
            action.triggered.connect(event)
        action.setCheckable(checkable)
        if icon_name:
            action.setIcon(QtGui.QIcon(pixmap(icon_name)))
        if shortcut:
            action.setShortcut(shortcut)
        if help_text:
            action.setStatusTip(help_text)
        return action

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.setStyleSheet('''QDoubleSpinBox[linked="true"]  {background-color: yellow;}
                              QDoubleSpinBox[waiting="true"] {color: gray;}
                              QFrame[branch="true"] {background-color: #ffffee;}
                              QFrame[junction="true"] {background-color: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #f0f0f0, stop:1 #ffffee);}''')

        ini_filename = os.getcwd() + r'\resources\magnetTable\MagnetTable.ini'
        self.settings = QtCore.QSettings(ini_filename, QtCore.QSettings.IniFormat)
        main_frame = QtGui.QFrame()
        layout = QtGui.QVBoxLayout(self)
        main_frame.setLayout(layout)
        self.setCentralWidget(main_frame)

        magnet_types = [('Dipoles', ('DIP',)), ('Quadrupoles', ('QUAD',)), ('Correctors', ('HCOR', 'VCOR')),
                        ('Solenoids', ('SOL', 'BSOL')), ('BPMs', ('BPM',))]

        main_menu = self.menuBar()
        self.setStatusBar(QtGui.QStatusBar(self))
        file_menu = main_menu.addMenu('&File')
        machine_menu = main_menu.addMenu('&Machine')
        view_menu = main_menu.addMenu('&View')
        help_menu = main_menu.addMenu('&Help')
        self.createMenuItem('&Load LTE...', file_menu, shortcut='Ctrl+L', event=self.loadButtonClicked,
                            help_text='Load magnet settings from an .lte (lattice) file.')
        self.createMenuItem('Load &DBURT...', file_menu, shortcut='Ctrl+O').setEnabled(False)
        self.createMenuItem('&Save DBURT...', file_menu, shortcut='Ctrl+S', event=self.saveDBURT).setEnabled(False)
        self.mru_menu = file_menu.addMenu('&Recent')
        self.updateMRUMenu()

        # TODO: add recent files
        self.createMenuItem('E&xit', file_menu, event=self.close, shortcut="Esc",
                            help_text='Close the program.')

        machine_menu.setSeparatorsCollapsible(False)  # so we can see top label
        machine_menu.addSeparator().setText('Mode')
        machine_mode_group = QtGui.QActionGroup(self, exclusive=True)
        machine_modes = (('Offline', 'Ctrl+0', "Don't connect to anything."),
                         ('Virtual', 'Ctrl+1', "Connect to a local virtual machine."),
                         ('Physical', 'Ctrl+2', "Connect to the real machine."))
        set_mode = str(self.settings.value('machine_mode', 'Offline').toString())
        for mode, shortcut, help_text in machine_modes:
            action = self.createMenuItem('&' + mode, machine_mode_group, icon_name=mode, shortcut=shortcut,
                                         event=self.machineModeChanged, checkable=True, help_text=help_text)
            action.setChecked(mode == set_mode)
            action.mode = mode  # so we know which one to set when this menu item is selected
            machine_menu.addAction(action)
        self.machine_mode_status = QtGui.QLabel('')
        self.statusBar().addPermanentWidget(self.machine_mode_status)
        self.status_bar_message = QtGui.QLabel('')
        self.statusBar().addWidget(self.status_bar_message)
        self.status_bar_message.linkActivated.connect(self.linkClicked)
        self.setMachineMode(set_mode)

        help_texts = ("Recalculate all the K values when the momentum is changed.",
                      "Rescale the magnet currents when the momentum is changed, and keep the K values the same.")
        shortcuts = ('Ctrl+K', 'Ctrl+I')
        machine_menu.addSeparator().setText('On momentum change')
        mom_mode_group = QtGui.QActionGroup(self, exclusive=True)
        mom_set_mode, ok = self.settings.value('momentum_mode', VC_MagCtrl.MomentumMode.RECALCULATE_K).toInt()
        self.mom_mode_action = {}
        for mode, help_text, shortcut in zip(VC_MagCtrl.MomentumMode, help_texts, shortcuts):
            name = mode.name.replace('_', ' ').title()
            action = self.createMenuItem('&' + name, mom_mode_group, icon_name=mode.name.lower(), shortcut=shortcut,
                                         checkable=True, event=self.momentumModeRadioClicked, help_text=help_text)
            machine_menu.addAction(action)
            action.mode = mode
            action.setChecked(mode == mom_set_mode)
            self.mom_mode_action[mode] = action  # so we can set it checked manually if necessary
        self.always_rescale = False

        machine_menu.addSeparator().setText('Visible magnets')
        for mag_menu_name, mods in (('visible', 'Ctrl+'), ('all', 'Ctrl+Shift+')):
            machine_menu.addSeparator().setText('{} magnets'.format(mag_menu_name.title()))
            self.createMenuItem('All o&n', machine_menu, shortcut=mods+'+', event=functools.partial(self.powerMagnets, 'on', mag_menu_name), icon_name='on')
            self.createMenuItem('All o&ff', machine_menu, shortcut=mods+'-', event=functools.partial(self.powerMagnets, 'off', mag_menu_name), icon_name='off')
            self.createMenuItem('&Degauss', machine_menu, shortcut=mods+'G', event=functools.partial(self.degaussMagnets, mag_menu_name), icon_name='cycle')

        for mag, types in magnet_types:
            action = self.createMenuItem('&' + mag, view_menu, self.toggleMagType,
                                         checkable=True, icon_name=mag, shortcut='Ctrl+' + mag[0],
                                         help_text='Toggle visibility of {}.'.format(mag.lower()))
            action.types_to_show = types
            action.help_text = 'Toggle visibility of <b>' + mag.lower() + '</b>.'
            action.setChecked(True)
        view_menu.addSeparator()
        log_action = self.createMenuItem('&Log', view_menu, checkable=True, icon_name='log', shortcut='Ctrl+L', event=self.logButtonClicked)
        log_action.setEnabled(lw is not None)

        self.createMenuItem('&Wiki help', help_menu, shortcut='F1', icon_name='help',
                            event=lambda: webbrowser.open('http://projects.astec.ac.uk/VELAManual2/index.php/Magnet_table'))
        self.createMenuItem('&About', help_menu, event=self.showAbout)

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
        self.wait_for = {}  # what magnet(s) and SI are we waiting for?
        pv_root_re = re.compile('^VM-(.*):$')
        for key, section in sections.items():
            section_name = section.title
            section_vbox = QtGui.QVBoxLayout()
            header_hbox = QtGui.QHBoxLayout()
            header_hbox.setAlignment(QtCore.Qt.AlignTop)
            magnet_list_frame = QtGui.QFrame()
            vis = self.settings.value(key + '/show', True).toBool()
            title = self.collapsing_header(header_hbox, magnet_list_frame, (u'▲ ' if vis else u'▼') + section_name + '\t',
                                           help_text="Click to collapse/expand the " + section_name + " section.")
            magnet_list_frame.setVisible(vis)
            title.setFont(section_font)
            title.section_key = key
            magnet_list_frame.title_label = title
            min_momentum = 1.0
            momentum_value, ok = self.settings.value(key + '/momentum', section.default_momentum).toFloat()
            step = float(self.settings.value(key + '/mom_step', 0.1).toString())
            momentum = self.spinbox(header_hbox, 'MeV/c', step=step, value=momentum_value, decimals=3,
                                    min_value=min_momentum, help_text="Set the momentum of the " + section_name + " section. ")
            momentum.setMaximumWidth(200)
            momentum.valueChanged.connect(self.momentumChanged)
            section_vbox.addLayout(header_hbox)
            magnet_list_vbox = QtGui.QVBoxLayout(magnet_list_frame)
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
                # magnet_frame.setStyleSheet(frame_style_sheet)
                magnet_vbox = QtGui.QVBoxLayout()
                magnet_frame.setLayout(magnet_vbox)
                main_hbox = QtGui.QHBoxLayout()
                main_hbox.setAlignment(QtCore.Qt.AlignTop)
                magnet_vbox.addLayout(main_hbox)
                more_info = QtGui.QFrame()
                attributes = mag_attributes[mag_type]
                # 'H Corrector' -> 'Correctors'; 'Quadrupole' -> 'Quadrupoles'
                generic_name = attributes.friendly_name + 's'

                show_hide_info = "Click to show/hide more information about {}.".format(name)
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
                offline_info.linkActivated.connect(self.linkClicked)
                offline_info.setAlignment(QtCore.Qt.AlignTop)
                offline_info.help_text = ''
                more_info_layout.addWidget(offline_info)
                online_info = QtGui.QLabel()
                online_info.linkActivated.connect(self.onlineInfoLinkClicked)
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
                    self.collapsing_header(main_hbox, more_info, 'Charge', help_text=show_hide_info)
                    bpm.q_label = self.collapsing_header(main_hbox, more_info, help_text=show_hide_info)
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

                    magnet.prev_values = [magnet.ref.siWithPol]
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
                    # The float(.toString()) here is necessary since Qt's string-to-float conversion doesn't match Python's
                    step = float(self.settings.value('{}/{}_k_step'.format(key, name), 0.01 if mag_type == 'BSOL' else 0.1).toString())
                    help_text = "Set the {} in the {} magnet. The magnet current will be set depending on the momentum in the {} section. ".format(
                        attributes.effect_name.lower(), magnet.name, section_name)
                    k_spin = self.spinbox(main_hbox, attributes.effect_units, step=step, decimals=3,
                                          help_text=help_text)  #, min_value=min_k, max_value=max_k)
                    magnet.k_spin = k_spin
                    branch_name = magnet.ref.magnetBranch
                    in_branch = branch_name != 'UNKNOWN_MAGNET_BRANCH'
                    if mag_type == 'DIP':
                        magnet.branch_button = QtGui.QToolButton()
                        magnet.branch_button.setCheckable(True)
                        magnet.branch_button.clicked.connect(self.branchButtonClicked)
                        magnet.branch_button.magnet = magnet  # link back to this magnet when clicked
                        magnet.branch_button.setToolTip('Toggle branch on/off')
                        magnet.branch_button.setStatusTip("Click to toggle this dipole, either sending the beam straight through, or onto a branch.")
                        branch_icon = QtGui.QIcon()
                        branch_icon.addPixmap(pixmap('branch-off'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        branch_icon.addPixmap(pixmap('branch-on'), QtGui.QIcon.Normal, QtGui.QIcon.On)
                        magnet.branch_button.setIcon(branch_icon)
                        main_hbox.addWidget(magnet.branch_button)
                        if name == 'DIP01':
                            # We can use this dipole to set the momentum - add a button to the section header
                            set_mom_button = QtGui.QPushButton('Set momentum from ' + name)
                            set_mom_button.setMaximumWidth(200)
                            set_mom_button.clicked.connect(functools.partial(self.setMomentum, magnet))
                            header_hbox.addWidget(set_mom_button)

                    self.collapsing_header(main_hbox, more_info, lbl, help_text=show_hide_info)
                    help_text = "Set the current in the {} magnet. The {} will be calculated, depending on the momentum in the {} section. ".format(
                        magnet.name, attributes.effect_name.lower(), section_name)
                    step = float(self.settings.value('{}/{}_i_step'.format(key, name), 0.1).toString())
                    current_spin = self.spinbox(main_hbox, units, step=step, decimals=3,
                                                min_value=min_current, max_value=max_current, help_text=help_text)
                    magnet.current_spin = current_spin

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
                    magnet_frame.setProperty('branch', True)
                    junc_magnet = self.magnets[key + "_" + branch_name]
                    junc_magnet.is_junction = True
                    junc_magnet.magnet_frame.setProperty('junction', True)
                end_of_branch = False  # magnet.name in ('QUAD06', 'QUAD14')
                magnet_frame.setLineWidth(3 if end_of_branch else 1)
                magnet_frame.setContentsMargins(0, 0, 0, 3 if end_of_branch else 1)

        if lw is not None:
            self.log_widget = lw.loggerWidget(logger)
            self.log_widget.hide()
            hbox.addWidget(self.log_widget, 2)

        # set up events (need to do setup first)
        for magnet in self.magnets.values():
            magnet.current_spin.setValue(magnet.ref.siWithPol)
            magnet.k_spin.setValue(magnet.ref.k)
            magnet.current_spin.valueChanged.connect(self.currentValueChanged)
            magnet.k_spin.valueChanged.connect(self.kValueChanged)
            magnet.restore_button.setEnabled(False)  # will be automatically shown when event triggered
            magnet.active = False

        self.degauss_animation = QtGui.QMovie(os.getcwd() + r'\resources\magnetTable\Icons\degauss.gif')
        self.degauss_animation.setScaledSize(QtCore.QSize(32, 32))

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
            label.setStatusTip(help_text)
        label.setSizePolicy(label_size_policy)
        label.setCursor(QtCore.Qt.PointingHandCursor)
        label.toggle_frame = more_info
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
        more_help_text = help_text + "SHIFT + wheel = small steps, CTRL + SHIFT + wheel = big steps."
        spinbox.setStatusTip(more_help_text)
        spinbox.lineEdit().setStatusTip(more_help_text)
        parent.addWidget(spinbox)
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
            magnet_on = magnet.ref.psuState == VC_MagCtrl.MAG_PSU_STATE.MAG_PSU_ON
            degaussing = magnet.ref.isDegaussing
            magnet.current_spin.setEnabled(not degaussing)
            magnet.k_spin.setEnabled(not degaussing)
            if degaussing:
                # light orange when magnets are being degaussed, and disable spin boxes
                magnet.magnet_frame.setStyleSheet('background-color: rgb(255, 178, 102);')
                magnet.warning_icon.setToolTip('Degaussing')
                if not magnet.warning_icon.movie():
                    magnet.warning_icon.setMovie(self.degauss_animation)
                    self.degauss_animation.start()
            elif not magnet_on and not offline:
                # red background to highlight magnets that are OFF
                magnet.magnet_frame.setStyleSheet('background-color: rgb(139, 0, 0);')
                magnet.warning_icon.setPixmap(pixmap('error'))
                magnet.warning_icon.setToolTip('Magnet PSU: ' + str(magnet.ref.psuState)[8:])
            elif abs(set_current - read_current) > magnet.ref.riTolerance:
                magnet.magnet_frame.setStyleSheet('')
                magnet.warning_icon.setPixmap(pixmap('warning'))
                magnet.warning_icon.setToolTip('Read current and set current do not match')
            else:
                magnet.magnet_frame.setStyleSheet('')
                magnet.warning_icon.setPixmap(self.empty_icon)
            mag_type = str(magnet.ref.magType)
            if mag_type == 'QUAD':
                magnet.icon.setPixmap(pixmap('Quadrupole_' + ('F' if magnet.k_spin.value() >= 0 else 'D')).scaled(32, 32))
            # are we waiting for the SI value or K value for this magnet to 'take'?
            try:
                attribute, wait_val = self.wait_for[magnet]
                if attribute == 'current':  # we're waiting for the SI value to take
                    now_val = set_current
                    update_spin = magnet.k_spin
                    update_val = magnet.ref.k
                else:  # we're waiting for the K value to take
                    now_val = magnet.ref.k
                    update_spin = magnet.current_spin
                    update_val = set_current
                if abs(now_val - wait_val) <= 0.001:  # it's taken now! # TODO: tolerance from somewhere?
                    self.wait_for.pop(magnet)  # remove it from 'waiting for' list
                    update_spin.setProperty('waiting', False)
                    update_spin.setValue(update_val)
            except KeyError:  # we're not waiting for this one
                if not magnet.current_spin.hasFocus():
                    magnet.current_spin.setValue(set_current)
                if not magnet.k_spin.hasFocus():
                    magnet.k_spin.setValue(magnet.ref.k)
            attributes = mag_attributes[mag_type]
            int_strength = np.copysign(np.polyval(magnet.fieldIntegralCoefficients, abs(set_current)), set_current)
            strength = int_strength / magnet.ref.magneticLength if magnet.ref.magneticLength else 0
            if mag_type == 'QUAD' or mag_type[1:] == 'COR':
                strength *= 1000  # convert to mT for correctors, T/m for quads
            online_text = online_text_format.format(**locals()) if (magnet_on or offline) else \
                '<a href="{}/{}/on">Switch magnet ON</a>'.format(magnet.section.id, magnet.ref.name)
            if mag_type == 'DIP':
                online_text += '<br><b>Section momentum</b>: {:.3f} MeV/c'.format(magnet.section.momentum_spin.value())
            online_text += '<p style="color:red"><b>Degaussing</b>: {} steps remaining</p>'.format(magnet.ref.remainingDegaussSteps) if degaussing else \
                '<br><a href="{}/{}/degauss">Degauss magnet</a>'.format(magnet.section.id, magnet.ref.name)

            magnet.online_info.setText(online_text)
        for bpm in self.bpms.values():
            bpm.x_label.setText('<b>{:.3f} mm</b>\t'.format(bpm.ref.xPV))
            bpm.y_label.setText('<b>{:.3f} mm</b>'.format(bpm.ref.yPV))
            bpm.q_label.setText('<b>{:.3f} pC</b>'.format(bpm.ref.q))

    def onlineInfoLinkClicked(self, url):
        """A link was clicked in the 'online info' box."""
        section, magnet, action = str(url).split('/')
        if action == 'on':
            magnet_controllers[section].switchONpsu(magnet)
        elif action == 'degauss':
            magnet_controllers[section].degauss(magnet)

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
                try:  # is this a section? if so, remember whether it was collapsed or not
                    self.settings.setValue(frame.title_label.section_key + '/show', not vis)
                except AttributeError:
                    pass
            except:
                pass  # no toggle_frame - never mind (or perhaps no title_label)
        elif type(source) in (QtGui.QLineEdit, QtGui.QDoubleSpinBox):
            # event was triggered in a magnet spin box (K or current)
            if evType == QtCore.QEvent.Wheel:
                # don't allow changes if Shift isn't pressed -
                # makes it easier to scroll the window up and down
                if not (modifiers & QtCore.Qt.ShiftModifier):
                    return True  # do nothing
            elif evType in (QtCore.QEvent.FocusOut, QtCore.QEvent.FocusIn):
                focused = evType == QtCore.QEvent.FocusIn
                # record the change to a magnet when defocused
                try:
                    magnet = source.parent().magnet
                    magnet.active = focused
                    magnet.k_spin.setProperty('linked', focused)
                    magnet.current_spin.setProperty('linked', focused)
                except AttributeError: # won't work for momentum spin boxes
                    print(type(source))
                    source.setProperty('linked', focused)
                    print(source.property('linked').toBool())
                    self.highlightMagControls(source.magnet_list_vbox, focused)
            elif evType == QtCore.QEvent.ContextMenu and isinstance(source, QtGui.QDoubleSpinBox):
                # Create a submenu item to adjust the step size, with a nice inline slider
                single_step = source.singleStep()
                menu = source.lineEdit().createStandardContextMenu()  #QtGui.QMenu(self) to create a blank menu
                menu.addSeparator().setText('Step size')
                step_sizes = [i * 10**j for j in range(-3, 2) for i in (1, 2, 5)]
                frame = QtGui.QFrame(menu)
                hbox = QtGui.QHBoxLayout(menu)
                frame.setLayout(hbox)
                slider = QtGui.QSlider(QtCore.Qt.Horizontal)
                slider.setRange(0, len(step_sizes) - 1)
                slider.setValue(step_sizes.index(single_step))
                hbox.addWidget(slider)
                # Show a label on the right displaying the actual value
                label = QtGui.QLabel('{:.3g}'.format(single_step))
                label.setMinimumWidth(30)  # about right for the widest value (0.005) - if we don't do this, the slider will change size as we slide

                def setStepSize(i):
                    step = step_sizes[i]
                    source.setSingleStep(step)
                    label.setText(str(step))
                    try:  # do we have a magnet spin box?
                        magnet = source.parent().magnet
                        spinbox_type = 'k' if source is magnet.k_spin else 'i'
                        settings_key = '{0.section.id}/{0.name}_{1}_step'.format(magnet, spinbox_type)
                    except AttributeError:  # no, a momentum one!
                        section = source.magnet_list_vbox
                        settings_key = section.id + '/mom_step'
                    self.settings.setValue(settings_key, step)
                slider.valueChanged.connect(setStepSize)
                hbox.addWidget(label)
                widget_action = QtGui.QWidgetAction(menu)
                widget_action.setDefaultWidget(frame)
                menu.addAction(widget_action)
                menu.exec_(event.globalPos())
                menu.deleteLater()
                return True

        elif evType == QtCore.QEvent.Wheel and (modifiers & QtCore.Qt.ShiftModifier):
            # don't allow scrolling if Shift _is_ held outwith a spin box -
            # otherwise we'll accidentally scroll the window while we're trying to
            # modify the spin box and the mouse slips a bit
            return True
        return QtGui.QMainWindow.eventFilter(self, source, event)

    def highlightMagControls(self, section, focused):
        """When a momentum spinbox has the focus, highlight all the magnet spinboxes (K or current)
        that will be affected by a change in momentum. This should make it clear what mode we are in."""
        mode, ok = self.settings.value('momentum_mode', VC_MagCtrl.MomentumMode.RECALCULATE_K).toInt()
        for magnet in self.magnets.values():
            if magnet.section == section:
                magnet.k_spin.setProperty('linked', focused and mode == VC_MagCtrl.MomentumMode.RECALCULATE_K)
                magnet.current_spin.setProperty('linked', focused and mode == VC_MagCtrl.MomentumMode.SCALE_CURRENTS)

    def toggleMagType(self, toggled):
        """Called when a magnet type checkbox is clicked. Hide or show all the magnets of that type."""
        # which checkbox was clicked? remove 's' from end, last 6 letters, lower case
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
        self.status_bar_message.setText('')  # get rid of any 'saved' message
        # Stop the GUI updating until the SI value 'takes' - otherwise it will update from an old value and be 'sticky'
        # Add it to a list of "waiting for" magnets. We might need more than one if we're changing the momentum in a section
        self.wait_for[magnet] = ('current', value)  # indicates we are waiting for a current value to take
        magnet.k_spin.setProperty('waiting', True)

        # To avoid a lot of iterating between K and current: check the calling function's name
        # if not sys._getframe(1).f_code.co_name == 'calcCurrentFromK':
        #     self.calcKFromCurrent(magnet)

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

    def setMomentum(self, magnet):
        """'Set momentum' button has been pressed - we are using this dipole to check the momentum.
        Calculate and set the momentum for this section."""
        current = magnet.current_spin.value()
        sign = np.copysign(1, current)
        coeffs = np.append(magnet.fieldIntegralCoefficients[:-1] * sign, magnet.fieldIntegralCoefficients[-1])
        int_strength = np.polyval(coeffs, abs(current))
        angle = 45  # reset to 45°
        momentum = 0.001 * SPEED_OF_LIGHT * int_strength / np.radians(angle)
        mode, ok = self.settings.value('momentum_mode', VC_MagCtrl.MomentumMode.RECALCULATE_K).toInt()

        if mode == VC_MagCtrl.MomentumMode.SCALE_CURRENTS and not self.always_rescale:
            # need to check this is really what we want!
            message_box = QtGui.QMessageBox(self)
            message_box.setWindowTitle('Magnet Table')
            message_box.setIcon(QtGui.QMessageBox.Warning)
            message_box.setText("Momentum change - ready to rescale currents")
            info_text = "Changing the momentum to {:.3f} MeV/c based on a current value of {:.3f} A in {}.\n\n" \
                        "This will scale all the magnet currents in {}. Is this what you want to do?"
            message_box.setInformativeText(info_text.format(momentum, current, magnet.name, magnet.section.id))
            message_box.addButton("Yes, once", QtGui.QMessageBox.YesRole).setIcon(QtGui.QIcon(pixmap('yes')))
            yes_always = message_box.addButton("Yes, always", QtGui.QMessageBox.YesRole)
            yes_always.setIcon(QtGui.QIcon(pixmap('yes-all')))
            no = message_box.addButton("No, cancel", QtGui.QMessageBox.NoRole)
            no.setIcon(QtGui.QIcon(pixmap('no')))
            switch_mode = message_box.addButton("No, switch mode", QtGui.QMessageBox.NoRole)
            switch_mode.setIcon(QtGui.QIcon(pixmap('recalculate_k')))
            message_box.exec_()
            button = message_box.clickedButton()
            if button == yes_always:
                self.always_rescale = True
            elif button == no:
                return  # don't do anything
            elif button == switch_mode:
                self.mom_mode_action['Recalculate K'].trigger()  # change mode before setting the momentum
        # Set the dipole angle without resetting the current
        magnet.k_spin.blockSignals(True)
        magnet.k_spin.setValue(angle)
        magnet.k_spin.blockSignals(False)
        magnet.section.momentum_spin.setValue(momentum)


    def momentumChanged(self, value):
        """Called when a momentum spin box is changed by the user."""
        section = self.sender().magnet_list_vbox
        momentum = self.sender().value()
        self.settings.setValue(section.id + '/momentum', momentum)
        # Put the momentum in the correct PV
        try:
            if self.settings.value('machine_mode') == 'Physical':
                if section.id == 'S01':
                    epics.caput('CLA-LRG1-DIA-MOM-01:RB', momentum)
                elif section.id == 'S02':
                    epics.caput('CLA-L01-DIA-MOM-01:RB', momentum)
        except:
            pass

        magnet_controllers[section.id].setMomentum(momentum)
        # mode = self.settings.value('momentum_mode', mom_modes[0])
        # changeFunc = self.calcKFromCurrent if mode == 'Recalculate K' else self.calcCurrentFromK
        # # are we adjusting the spinbox directly? or is it being changed by the "Set momentum" routine?
        # # direct = sys._getframe(1).f_code.co_name == '<module>'
        for magnet in self.magnets.values():
            if magnet.section == section:
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
        # so we invert the coefficients (except the offset) for negative current
        # This gives a smooth transition through zero
        sign = np.copysign(1, current)
        coeffs = np.append(magnet.fieldIntegralCoefficients[:-1] * sign, magnet.fieldIntegralCoefficients[-1])
        int_strength = np.polyval(coeffs, abs(current))
        # Calculate the normalised effect on the beam
        # This is in radians for dipoles, m⁻¹ for quads, m⁻² for sextupoles
        # effect = np.copysign(SPEED_OF_LIGHT * int_strength / momentum, current)
        effect = SPEED_OF_LIGHT * int_strength / momentum
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
        # if str(magnet.ref.magType) == 'DIP' and magnet.set_mom_checkbox.isChecked():
        #     self.setMomentum(magnet)
        # To avoid a lot of iterating between K and current: check the calling function's name
        if not sys._getframe(1).f_code.co_name == 'updateMagnetWidgets':
            magnet.ref.k = value
            self.wait_for[magnet] = ('k', value)
            magnet.current_spin.setProperty('waiting', True)
            # self.calcCurrentFromK(magnet)
        
    def calcCurrentFromK(self, magnet):
        """Calculate the current to set in a magnet based on its K value (or bend angle)."""
        k = magnet.k_spin.value()
        # What is the momentum in this section?
        momentum = magnet.section.momentum_spin.value()
        mag_type = str(magnet.ref.magType)
        int_strength = None
        if mag_type == 'DIP':  # k represents deflection in degrees
            effect = math.radians(k) * 1000
        elif mag_type in ('QUAD', 'SEXT'):
            effect = k * magnet.ref.magneticLength / 1000
        elif mag_type in ('HCOR', 'VCOR'):  # k represents deflection in mrad
            effect = k
        else: # solenoids
            int_strength = k
        if int_strength is None:
            int_strength = effect * momentum / SPEED_OF_LIGHT
        coeffs = np.copy(magnet.k_coeffs if mag_type in ('SOL', 'BSOL') else magnet.fieldIntegralCoefficients)
        # are we above or below residual field? Need to set coeffs accordingly to have a smooth transition through zero
        sign = np.copysign(1, int_strength - coeffs[-1])
        coeffs = np.append(coeffs[:-1] * sign, coeffs[-1])
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
        current = np.copysign(roots[-1].real, sign) # last root is always x value (#TODO: can prove this?)
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

    def powerMagnets(self, on_off, mag_group):
        """Switch magnets on or off, either visible or all."""
        self.statusBar().showMessage('Switching {} magnets {}.'.format(mag_group, on_off.upper()), msecs=10000)
        on_state = VC_MagCtrl.MAG_PSU_STATE.MAG_PSU_ON if on_off == 'on' else VC_MagCtrl.MAG_PSU_STATE.MAG_PSU_OFF
        for magnet in self.magnets.values():
            if mag_group == 'all' or magnet.magnet_frame.isVisible():
                magnet.ref.PSU = on_state

    def degaussMagnets(self, mag_group):
        """Degauss magnets, either visible or all."""
        self.statusBar().showMessage('Degaussing {} magnets...'.format(mag_group), msecs=30000)
        for magnet in self.magnets.values():
            if mag_group == 'all' or magnet.magnet_frame.isVisible():
                magnet_controllers[magnet.section.id].degauss(magnet.name)

    def machineModeChanged(self):
        mode = self.sender().mode  # Each "change mode" menu item has a 'mode' attribute
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

    def momentumModeRadioClicked(self):
        combo = self.sender()
        mode = combo.mode  # currentText()
        logger.info('Set momentum mode: ' + mode.name)
        self.settings.setValue('momentum_mode', mode.value)
        for controller in magnet_controllers.values():
            controller.momentum_mode = mode
        # check if we are focused on a momentum spinbox
        for magnet_list in self.magnet_controls.values():
            if magnet_list.momentum_spin.hasFocus():
                self.highlightMagControls(magnet_list, True)  # make sure correct boxes are highlighted

    def setMachineMode(self, mode=None):
        """Set the machine mode (offline/virtual/physical and redefine the controllers accordingly."""
        logger.info('Set machine mode: ' + mode)
        os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255" if mode == 'Physical' else "10.10.0.12"
        magnet_controllers.clear()
        bpm_controllers.clear()
        # mode_name = VELA_CLARA_enums.MACHINE_MODE.names[mode.upper()]
        for key, section in sections.items():
            # area = VELA_CLARA_enums.MACHINE_AREA.names[section.machine_area]
            # magnet_controller = mag_init_VC.getMagnetController(mode_name, area)
            get_controller = getattr(mag_init_VC, '{}_{}_Magnet_Controller'.format(mode.lower(), section.machine_area))
            magnet_controller = get_controller()
            try:
                magnet_controller.setMomentum(self.magnet_controls[key].momentum_spin.value())
            except AttributeError:  # won't work on startup - no spinbox yet
                pass
            magnet_controllers[key] = magnet_controller
            try:
                # bpm_controller = bpm_init.getBPMController(mode_name, area)
                get_controller = getattr(bpm_init, '{}_{}_BPM_Controller'.format(mode.lower(), section.machine_area))
                bpm_controller = get_controller()
                bpm_controllers[key] = bpm_controller
            except RuntimeError:
                print("Couldn't load {} BPM controller for area {}".format(mode, section.machine_area))
                bpm_controllers[key] = None
        self.settings.setValue('machine_mode', mode)
        self.machine_mode_status.setText(mode)
        #TODO: check that it actually worked

    def loadButtonClicked(self):
        """Choose an LTE file and apply it."""
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open lattice file', '', 'Lattice files (*.lte);;All files (*.*)')
        if filename != ''
            self.loadLTEFile(filename)

    def loadLTEFile(self, filename):
        """Load a lattice file and apply it to magnets."""
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

    def saveDBURT(self):
        """Save a DBURT file."""
        # how to decide which areas to save? ask the user, defaulting to the ones that are currently open
        checkboxes = [(section.title, self.magnet_controls[id].parent().isVisible()) for id, section in sections.items()]
        message_box = ExtendedDialog(self, checkboxes)
        message_box.setWindowTitle('Magnet Table')
        message_box.setIcon(QtGui.QMessageBox.Question)
        message_box.setText('Select areas to save. Individual DBURT files will be created in the <a href="{}">default folder</a>.'.format(dburt_folder))
        save = message_box.addButton("Save", QtGui.QMessageBox.YesRole)
        message_box.addButton("Cancel", QtGui.QMessageBox.NoRole)
        ret, boxes_ticked, comment = message_box.exec_()
        if message_box.clickedButton() == save:
            status_links = []
            timestamp = time.strftime(r'%Y-%m-%d-%H%M')
            for ticked, id in zip(boxes_ticked, sections.keys()):
                if ticked:
                    # Currently keywords doesn't do anything - but put one in anyway in case it gets implemented later
                    filename = dburt_folder + '\\' + id + '_' + timestamp + '.dburt'
                    magnet_controllers[id].writeDBURT(filename, comment, 'magnet-table')
                    status_links.append('<a href="{}">{}</a>'.format(filename, id))
            plural = 's' if len(status_links) > 1 else ''
            status_message = "Saved DBURT{}: {} with timestamp {}".format(plural, ', '.join(status_links), timestamp)
            self.status_bar_message.setText(status_message)

    def addToMRU(self, filename):
        """Add a filename to the most recently used list in the File menu."""
        self.settings.beginGroup('Recent')
        self.settings.setValue(time.strftime(r'%Y%m%d%H%M%S'), filename)
        # Remove the oldest item from the menu
        keys = self.settings.childKeys()
        if len(keys) > 9:
            oldest_key = min([str(k) for k in keys])
            self.settings.remove(oldest_key)
        self.settings.endGroup()
        self.updateMRUMenu()

    def updateMRUMenu(self):
        """Update the most recently used list in the File menu."""
        self.settings.beginGroup('Recent')
        self.mru_menu.clear()
        keys = sorted(self.settings.childKeys())
        for i, key in enumerate(keys):
            full_name = self.settings.value(key)
            path, filename = os.path.split(full_name)
            self.createMenuItem('&{}: {}'.format(i, filename), self.mru_menu, event=functools.partial(self.mruEntryClicked, full_name),
                                help_text=full_name)
        self.settings.endGroup()

    def mruEntryClicked(self, filename):
        """An entry in the most recently used list has been clicked."""
        if not os.path.isfile(filename):
            QtGui.QMessageBox.information(self, 'Magnet Table', 'File "{}" not found.'.format(filename), icon=QtGui.QMessageBox.Warning)
            return
        # What kind of file?
        main, ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext == '.dburt':
            self.applyDBURT(filename)
        elif ext == '.lte':
            self.loadLTEFile(filename)
        else:
            QtGui.QMessageBox.information(self, 'Magnet Table', 'File "{}" is not a DBURT or LTE file.'.format(filename), icon=QtGui.QMessageBox.Warning)

    def linkClicked(self, url):
        """A link was clicked in a label - maybe the status_bar_message or offline_info boxes.
        Open an Explorer window with that file highlighted."""
        os.system('explorer.exe /select,"{}"'.format(url))

    def logButtonClicked(self):
        """Show or hide the log."""
        self.log_widget.setVisible(not self.log_widget.isVisible())

    def showAbout(self):
        about_text = 'Magnet Table\nBen Shepherd\nBuilt on {}'.format(time.strftime('%Y/%m/%d %H:%M', time.localtime(build_date)))
        QtGui.QMessageBox.about(self, 'Magnet Table', about_text)

    def closeEvent(self, event):
        logger.info('Close app')
        self.widgetUpdateTimer.stop()
        self.settings.setValue('geometry', self.geometry())
        exit()
        
    def __repr__(self):
        return '<Magnet Table GUI>'

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyle(QtGui.QStyleFactory.create('Plastique'))
    # app.setStyleSheet('''*[linked="true"] {background-color: yellow;}
    #                      *[waiting="true"] {color: gray;}''')

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
