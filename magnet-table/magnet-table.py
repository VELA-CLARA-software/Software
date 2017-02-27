#!python2
# -*- coding: utf-8 -*-
# encoding=utf8
"""
VELA/CLARA magnet table
v1.0, January 2017
Ben Shepherd
"""
from PyQt4 import QtCore, QtGui #for GUI building
import sys
from collections import namedtuple # for easy description of strength and units
import math # conversion between radians/degrees
import os # clicking URLs on labels, setting env variables
import numpy as np # handling polynomials
import re # parsing lattice files
import scipy.constants # speed of light
import webbrowser #to get help
import VELA_CLARA_MagnetControl as MagCtrl
from pkg_resources import resource_filename
#Note: to be able to import the magnet controller, I used
#pip install -e "\\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Software\VELA_CLARA_PYDs\bin\stage"

#TODO: do these need to be reset for the physical machine?
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"

class Element:
    "Used for parsing lattice files."
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
    'help.png': 'https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-help-circled-128.png'}
    
# Define the speed of light. We need this to convert field integral to angle or K.
# e.g. theta = field_int * c / p[eV/c]
# (derive using mv²/rho=BeV, field_int=B.s, theta=s/rho, p[kg.m/s]=p[eV/c].e.(1V)/c)
SPEED_OF_LIGHT = scipy.constants.c / 10**6 # in megametres/second, use with p in MeV/c

label_size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

#FIXME: should be {int_strength:.3f}
online_text_format = u'''<b>Read current</b>: {magnet.ref.riWithPol:.3f} A
                         <br><b>Integrated {attributes.strength_name}</b>: {int_strength:.3f} {attributes.int_strength_units}
                         <br><b>Central {attributes.strength_name}</b>: {strength:.3f} {attributes.strength_units}'''

# Each type of magnet has some common attributes - here's how we access them
mag_attr = namedtuple('mag_attr', 'friendly_name effect_name effect_units strength_name strength_units int_strength_units')
mag_attributes = {
    'BSOL': mag_attr('Bucking solenoid', 'Integrated field', 'T.mm', 'field', 'T', 'T.mm'),
    'SOL':  mag_attr('Solenoid', 'Integrated field', 'T.mm', 'field', 'T', 'T.mm'),
    'DIP':  mag_attr('Dipole', 'Angle', u'°', 'field', 'T', 'T.mm'),
    'QUAD': mag_attr('Quadrupole', 'K', u'm⁻²', 'gradient', 'T/m', 'T'),
    'SEXT': mag_attr('Sextupole', 'K', u'm⁻³', 'gradient', u'T/m²', 'T/m'),
    'HCOR': mag_attr('H Corrector', 'Angle', 'mrad', 'field', 'mT', 'T.mm'),
    'VCOR': mag_attr('V Corrector', 'Angle', 'mrad', 'field', 'mT', 'T.mm'),
    'UNKNOWN_MAGNET_TYPE': mag_attr('Unknown', 'Strength', 'AU', 'strength', 'AU', 'AU')}

def format_when_present(format_string, obj, attr):
    """"Returns a formatted string with the object's given attribute,
    or a blank string when the attribute is not present or begins UNKNOWN."""
    try:
        value = getattr(obj, attr)
        if type(value) is str and value[:7] == 'UNKNOWN':
            return ''
        else:
            return format_string.format(value)
    except AttributeError:
        return ''

def pixmap(icon_name):
    return QtGui.QPixmap(resource_filename('magnet-table', 'Icons/' + icon_name + '.png'))

class Magnet(object):
    "Currently doesn't do anything in particular - just a container for magnet properties."
    def __init__(self, name):
        self.name = name
        self.is_junction = False
        self.divert = False

class Window(QtGui.QMainWindow):
    
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.magInit = MagCtrl.init()

        ini_filename = resource_filename('magnet-table', 'magnet-table.ini')
        self.settings = QtCore.QSettings(ini_filename, QtCore.QSettings.IniFormat)
        main_frame = QtGui.QFrame()
        layout = QtGui.QVBoxLayout(self)
        main_frame.setLayout(layout)
        self.setCentralWidget(main_frame)
        checkbox_grid = QtGui.QHBoxLayout()
        magnet_types = ('Dipoles', 'Quadrupoles', 'Correctors', 'Solenoids')
        for mag in magnet_types:
            checkbox = QtGui.QCheckBox(mag)
            checkbox.setIcon(QtGui.QIcon(pixmap(mag)))
            checkbox.setChecked(True)
            checkbox.clicked.connect(self.toggleMagType)
            checkbox_grid.addWidget(checkbox)

        machine_modes = ('Offline', 'Virtual', 'Physical')
        mode_combo = QtGui.QComboBox()
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
        
        checkbox_grid.addWidget(QtGui.QLabel('Momentum change mode'))
        mom_modes = ('Change K/angle', 'Change current')
        mode_combo = QtGui.QComboBox()
        checkbox_grid.addWidget(mode_combo)
        mode_combo.activated.connect(self.momentumModeRadioClicked)
        [mode_combo.addItem(mode) for mode in mom_modes]
        set_mode = self.settings.value('momentum_mode', 'Change K/angle').toString()
        try:
            i = mom_modes.index(set_mode)
        except ValueError:
            i = 0
        mode_combo.setCurrentIndex(i)
        self.mom_mode_combo = mode_combo

        load_button = QtGui.QPushButton(QtGui.QIcon(pixmap('Open')), 'Load...')
        checkbox_grid.addWidget(load_button)
        load_button.clicked.connect(self.loadButtonClicked)

        help_button = QtGui.QPushButton(QtGui.QIcon(pixmap('help')), '')
        checkbox_grid.addWidget(help_button)
        help_button.clicked.connect(self.helpButtonClicked)

        layout.addLayout(checkbox_grid)
            
        scroll_area = QtGui.QScrollArea(self)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        layout.addWidget(scroll_area)
        
        section_container = QtGui.QWidget()
        section_list = QtGui.QVBoxLayout(section_container)
        scroll_area.setWidgetResizable(True)

        scroll_area.setWidget(section_container)

        magnet_list = {}
        section_names = ('VELA Injector',)
        section_font = QtGui.QFont('', 16, QtGui.QFont.Bold)
        magnet_font = QtGui.QFont('', 14, QtGui.QFont.Bold)
        for section in section_names:
            section_vbox = QtGui.QVBoxLayout()
            header_hbox = QtGui.QHBoxLayout()
            header_hbox.setAlignment(QtCore.Qt.AlignTop)
            magnet_list_frame = QtGui.QFrame()
            title = self.collapsing_header(header_hbox, magnet_list_frame, section + '\t')
            title.setFont(section_font)
            #TODO: set some sensible value
            momentum = self.spinbox(header_hbox, 'MeV', step=0.5, value=6.5)
            momentum.valueChanged.connect(self.momentumChanged)
            section_vbox.addLayout(header_hbox)
            magnet_list_vbox = QtGui.QVBoxLayout()
            magnet_list_frame.setLayout(magnet_list_vbox)
            magnet_list_vbox.momentum_spin = momentum # so we can reference it from a magnet
            momentum.magnet_list_vbox = magnet_list_vbox
            magnet_list[section] = magnet_list_vbox
            section_vbox.addWidget(magnet_list_frame)
            section_list.addLayout(section_vbox)
            
        mag_names = list(self.controller.getMagnetNames()) # but these don't come in the right order so...
        mag_names.sort(key=lambda name: self.controller.getPosition(name))
#        mag_names = 'BSOL SOL HCOR01 VCOR01 HCOR02 VCOR02 QUAD01 QUAD02 QUAD03 QUAD04 HCOR03 VCOR03 HCOR04 VCOR04 DIP01 HCOR05 VCOR05 QUAD05 QUAD06 HCOR06 VCOR06 QUAD07 QUAD08 HCOR07 VCOR07 QUAD09 HCOR08 VCOR08 QUAD10 QUAD11 HCOR09 VCOR09 DIP02 HCOR10 VCOR10 QUAD12 DIP03 HCOR11 VCOR11 QUAD13 QUAD14 QUAD15'.split(' ')
        self.mag_refs = [self.controller.getMagObjConstRef(name) for name in mag_names] #TODO: needed?
        self.magnets = [Magnet(name) for name in mag_names]
        mag_dict = {} # used to assign is_junction
        section = 'VELA Injector' #TODO: get this for each magnet
        pv_root_re = re.compile('^VM-(.*):$')
        for magnet in self.magnets:
            mag_dict[magnet.name] = magnet
            magnet.ref = self.controller.getMagObjConstRef(magnet.name)
            # Replace the PV root VM-XXX: --> XXX
            magnet.pv_base = re.sub(pv_root_re, r'\1', magnet.ref.pvRoot)
            magnet.prev_values = []
            magnet.active = False # whether magnet is being changed
            magnet_list_vbox = magnet_list[section]
            magnet.section = magnet_list_vbox
            magnet_frame = QtGui.QFrame()
            magnet_frame.setFrameShape(QtGui.QFrame.Box | QtGui.QFrame.Plain)
            magnet_frame.setStyleSheet('#branch {background-color: #ffffee;} #junction {background-color: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #f0f0f0, stop:1 #ffffee);}')
        
            #different shading for magnets in branches, and smooth transition at junctions
            in_branch = magnet.ref.magnetBranch != 'UNKNOWN_MAGNET_BRANCH'
            if in_branch:
                magnet_frame.setObjectName('branch')
                junc_magnet = mag_dict[magnet.ref.magnetBranch]
                junc_magnet.is_junction = True
                junc_magnet.magnet_frame.setObjectName('junction')
            end_of_branch = False#magnet.name in ('QUAD06', 'QUAD14')
            magnet_frame.setLineWidth(3 if end_of_branch else 1)
            magnet_frame.setContentsMargins(0, 0, 0, 3 if end_of_branch else 1)
            magnet_vbox = QtGui.QVBoxLayout()
            magnet_frame.setLayout(magnet_vbox)
            magnet_frame.magnet = magnet
            magnet.magnet_frame = magnet_frame
            main_hbox = QtGui.QHBoxLayout()
            main_hbox.setAlignment(QtCore.Qt.AlignTop)
            magnet_vbox.addLayout(main_hbox)
            more_info = QtGui.QFrame()
            mag_type = str(magnet.ref.magType)
            attributes = mag_attributes[mag_type]
            # 'H Corrector' -> 'Correctors'; 'Quadrupole' -> 'Quadrupoles'
            generic_name = attributes.friendly_name.split(' ')[-1].capitalize() + 's'

            icon = self.collapsing_header(main_hbox, more_info)
            icon.setPixmap(pixmap(generic_name).scaled(32, 32))
            # The tab here aligns all the current spinboxes nicely
            title_text = magnet.name.replace(mag_type, attributes.friendly_name + ' ') + '\t'
            title = self.collapsing_header(main_hbox, more_info, title_text)
            title.setFont(magnet_font)
            magnet.title = title
            self.collapsing_header(main_hbox, more_info, attributes.effect_name)
            bipolar = not magnet.ref.magRevType == MagCtrl.MAG_REV_TYPE.POS
            k_spin = self.spinbox(main_hbox, attributes.effect_units, step=0.1, decimals=3, bipolar=bipolar)
            magnet.k_spin = k_spin
            self.collapsing_header(main_hbox, more_info, 'Current')
            current_spin = self.spinbox(main_hbox, 'A', step=0.1, decimals=3, bipolar=bipolar)
            magnet.current_spin = current_spin
            restore_button = QtGui.QToolButton()
            restore_button.setIcon(QtGui.QIcon(pixmap('undo')))
            restore_button.clicked.connect(self.restoreMagnet)
            main_hbox.addWidget(restore_button)
            magnet.restore_button = restore_button
            restore_button.hide()
            warning_icon = self.collapsing_header(main_hbox, more_info)
            warning_icon.hide()
            magnet.warning_icon = warning_icon
            #TODO: warn when magnet needs degaussing
            
            static_info = ('<b>', magnet.name, '</b> ', attributes.friendly_name,
                           format_when_present('<br><b>Manufactured by</b> {}', magnet.ref, 'manufacturer'),
                           format_when_present('<br><b>Serial number</b> {}', magnet.ref, 'serialNumber'),
                           format_when_present('<br><b>Magnetic length</b>: {:.1f} mm', magnet.ref, 'magneticLength'),
                           format_when_present('<br><a href="{}">Measurement data</a>', magnet.ref, 'measurementDataLocation'))
            
            more_info_layout = QtGui.QHBoxLayout()
            more_info.setLayout(more_info_layout)
            
            offline_info = QtGui.QLabel(''.join(static_info))
            offline_info.linkActivated.connect(self.labelLinkClicked)
            offline_info.setAlignment(QtCore.Qt.AlignTop)
            more_info_layout.addWidget(offline_info)
            online_info = QtGui.QLabel()
            online_info.setAlignment(QtCore.Qt.AlignTop)
            more_info_layout.addWidget(online_info)
            magnet.online_info = online_info
            more_info.hide()
            magnet_vbox.addWidget(more_info)
            title.toggle_frame = more_info
            title.installEventFilter(self)
            magnet_list_vbox.addWidget(magnet_frame)

        # set up events (need to do setup first)        
        for magnet in self.magnets:
            magnet.current_spin.valueChanged.connect(self.currentValueChanged)
            magnet.current_spin.setValue(magnet.ref.siWithPol)
            magnet.k_spin.valueChanged.connect(self.kValueChanged)
            magnet.restore_button.hide() # will be automatically shown when event triggered
            magnet.active = False
        
        self.magnet_controls = magnet_list
        self.setWindowTitle('Magnet Table')
        self.setGeometry(300, 300, 300, 450)
        self.update_period = 100 # milliseconds
        self.startMainViewUpdateTimer()
        self.setWindowIcon(QtGui.QIcon(pixmap('magnet')))
        self.show()

    def collapsing_header(self, parent_widget, more_info, label_text=''):
        "Make a label that shows or hides the more_info widget when clicked."
        label = QtGui.QLabel(label_text)
        label.setSizePolicy(label_size_policy)
        label.setCursor(QtCore.Qt.PointingHandCursor)
        label.toggle_frame = more_info
        label.installEventFilter(self)
        parent_widget.addWidget(label)
        return label
        
    def spinbox(self, parent, units, step=None, value=0, decimals=2, bipolar=False):
        "Make a double-valued spinbox."
        spinbox = QtGui.QDoubleSpinBox()
        spinbox.setSuffix(' ' + units)
        spinbox.setValue(value)
        spinbox.setDecimals(decimals)
        spinbox.setRange(float('-inf') if bipolar else 0, float('inf'))
        spinbox.setKeyboardTracking(False)
        if step:
            spinbox.setSingleStep(step)
        parent.addWidget(spinbox)
        spinbox.installEventFilter(self)
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
        for magnet in self.magnets:
            if not magnet.ref.psuState == MagCtrl.MAG_PSU_STATE.MAG_PSU_ON:
                magnet.warning_icon.setPixmap(pixmap('error'))
                magnet.warning_icon.setToolTip('Magnet PSU: ' + str(magnet.ref.psuState)[8:])
                magnet.warning_icon.show()
            elif abs(magnet.ref.siWithPol - magnet.ref.riWithPol) > magnet.ref.riTolerance:
                magnet.warning_icon.setPixmap(pixmap('warning'))
                magnet.warning_icon.setToolTip('Read current and set current do not match')
                magnet.warning_icon.show()
            else:
                magnet.warning_icon.hide()
            if not magnet.current_spin.hasFocus():
                magnet.current_spin.setValue(magnet.ref.siWithPol)
            mag_type = str(magnet.ref.magType)
            attributes = mag_attributes[mag_type]
            int_strength = np.copysign(np.polyval(magnet.ref.fieldIntegralCoefficients, abs(magnet.ref.siWithPol)), magnet.ref.siWithPol)
            strength = int_strength / magnet.ref.magneticLength if magnet.ref.magneticLength else 0
            if mag_type == 'QUAD' or mag_type[1:] == 'COR':
                strength *= 1000 # convert to mT for correctors, T/m for quads
            magnet.online_info.setText(online_text_format.format(**locals()))

    def eventFilter(self, source, event):
        "Handle events - QLabel doesn't have click or wheel events."
        evType = event.type()
        if evType == QtCore.QEvent.MouseButtonRelease:
            try:
                vis = source.toggle_frame.isVisible()
                source.toggle_frame.setVisible(not vis)
            except:
                pass # no toggle_frame - never mind
        elif type(source) in (QtGui.QLineEdit, QtGui.QDoubleSpinBox):
            # event was triggered in a magnet spin box (K or current)
            if evType == QtCore.QEvent.Wheel:
                # don't allow changes if Shift isn't pressed -
                # makes it easier to scroll the window up and down
                modifiers = QtGui.QApplication.keyboardModifiers()
                if not (modifiers & QtCore.Qt.ShiftModifier):
                    return True # do nothing
            elif evType == QtCore.QEvent.FocusOut:
                # record the change to a magnet
                try:
                    magnet = source.parent().magnet
                    magnet.active = False
                except AttributeError: # won't work for momentum spin boxes
                    pass
        return QtGui.QMainWindow.eventFilter(self, source, event)
    
    def labelLinkClicked(self, url):
        os.system('start "" "' + str(url) + '"')

    def toggleMagType(self, toggled):
        "Called when a magnet type checkbox is clicked. Hide or show all the magnets of that type."
        #which checkbox was clicked? remove 's' from end, last 6 letters, lower case
        mag_type = str(self.sender().text())
        mag_type = mag_type[-7:-1].lower() 
#        print(mag_type, toggled)
        for mag_list in self.magnet_controls.values():
            for i in range(mag_list.count()):
                magnet_vbox = mag_list.itemAt(i).widget()
                attributes = mag_attributes[str(magnet_vbox.magnet.ref.magType)]
                if attributes.friendly_name[-6:].lower() == mag_type:
                    magnet_vbox.setVisible(toggled)

    def currentValueChanged(self, value):
        "Called when a current spin box is changed by the user."
        magnet = self.sender().parent().magnet
        self.controller.setSI(magnet.name, value)
        self.calcKFromCurrent(magnet)
        # If we're already changing this magnet, alter the last value
        # Otherwise add a value
        if magnet.active:
            magnet.prev_values[-1] = value
        else:
            magnet.prev_values.append(value)
        try:
            magnet.restore_button.show()
            magnet.restore_button.setToolTip('Restore previous value ({:.3f} A)'.format(magnet.prev_values[-2]))
            magnet.active = True
        except (AttributeError, IndexError):
            # fails on first time (no button yet)
            # and when first value is restored (no -2 index)
            pass
#        print('val changed', magnet.name, value, magnet.active, magnet.prev_values)
    
    def momentumChanged(self, value):
        "Called when a momentum spin box is changed by the user."
        section = self.sender().magnet_list_vbox
        mode = self.mom_mode_combo.currentText()
        changeFunc = self.calcKFromCurrent if mode == 'Change K/angle' else self.calcCurrentFromK
        [changeFunc(magnet) for magnet in self.magnets if magnet.section == section]

    def calcKFromCurrent(self, magnet):
        "Calculate the K value (or bend angle) of a magnet based on its current."
        current = magnet.current_spin.value()
        # What is the momentum in this section?
        momentum = magnet.section.momentum_spin.value()
        # Get the integrated strength, based on an excitation curve
        # This is in T.mm for dipoles, T for quads, T/m for sextupoles
        # Note that excitation curves are defined with positive current,
        # so we have to take the absolute value and then later reapply the sign
        int_strength = np.polyval(magnet.ref.fieldIntegralCoefficients, abs(current))
        # Calculate the normalised effect on the beam
        # This is in radians for dipoles, m⁻¹ for quads, m⁻² for sextupoles
        effect = np.copysign(SPEED_OF_LIGHT * int_strength / momentum, current)
        # Depending on the magnet type, convert to meaningful units
        mag_type = str(magnet.ref.magType)
        if mag_type == 'DIP':
            # Get deflection in degrees
            # int_strength was in T.mm so we divide by 1000
            k = math.degrees(effect / 1000)
            if magnet.is_junction:
                # hide/show magnets in branch
                magnet.divert = k > 22.5 # fairly arbitrary!
                beam_branch = 'UNKNOWN_MAGNET_BRANCH'
                for i, mag in enumerate(self.magnets):
                    highlight = mag.ref.magnetBranch == beam_branch
                    mag.title.setStyleSheet('color:#000000;' if highlight else 'color:#a0a0a0;')
                    if mag.is_junction and mag.divert and beam_branch == 'UNKNOWN_MAGNET_BRANCH':
                        beam_branch = mag.name
        elif mag_type in ('QUAD', 'SEXT'):
            k = 1000 * effect / magnet.ref.magneticLength # focusing term K
        elif mag_type in ('HCOR', 'VCOR'):
            k = effect # deflection in mrad
        else: # solenoids
            #TODO: something more meaningful?
            k = int_strength # for now, just use field
        magnet.k_spin.setValue(k)
#        print('{magnet.name}: current {current:.3f} -> k {k:.3f}'.format(**locals()))
        
    def kValueChanged(self, value):
        "Called when a K spin box is changed by the user."
        spinbox = self.sender()
        magnet = spinbox.parent().magnet
        self.calcCurrentFromK(magnet)
        
    def calcCurrentFromK(self, magnet):
        "Calculate the current to set in a magnet based on its K value (or bend angle)."
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
        coeffs = list(magnet.ref.fieldIntegralCoefficients)
        coeffs[-1] -= int_strength # Need to find roots of polynomial, i.e. a1*x + a0 - y = 0
        roots = np.roots(coeffs)
        current = np.copysign(roots[-1].real, k) # last root is always x value (#TODO: can prove this?)
        magnet.current_spin.setValue(current)
#        print('{magnet.name}: k {k:.3f} -> current {current:.3f}'.format(**locals()))
        
    def restoreMagnet(self):
        "Implement an 'undo' button for each magnet."
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
                magnet.restore_button.hide()
#            print('undo', magnet.name, undo_val, magnet.active, magnet.prev_values)
        except IndexError: # pop from empty list - shouldn't happen!
            magnet.restore_button.hide()
    
    def machineModeRadioClicked(self, index):
        combo = self.sender()
        mode = str(combo.currentText())
        self.setMachineMode(mode)
        # Change all the magnet references
        for magnet in self.magnets:
            magnet.ref = self.controller.getMagObjConstRef(magnet.name)
            # Set the current_spin value
            magnet.current_spin.setValue(magnet.ref.siWithPol)
            # Reset the undo state
            magnet.prev_values = [magnet.ref.siWithPol]
            magnet.active = False
            magnet.restore_button.hide()

    def momentumModeRadioClicked(self, index):
        combo = self.sender()
        mode = combo.currentText()
        self.settings.setValue('momentum_mode', mode)
        
    def setMachineMode(self, mode=None):
        print('Setting machine mode:', mode)
        self.controller = self.magInit.getMagnetController(MagCtrl.MACHINE_MODE.names[mode.upper()], MagCtrl.MACHINE_AREA.VELA_INJ)
        self.settings.setValue('machine_mode', mode)
        #TODO: check that it actually worked

    def loadButtonClicked(self):
        "Load a lattice file and apply it to magnets."
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open lattice file', '', 'Lattice files (*.lte);;All files (*.*)')
        if filename == '': # Cancel clicked
            return
        text = open(filename).read()
        # Handle continuation character & at end of lines
        text = text.replace('&\n', '')
        
        applied_list = ''
        for mag in self.magnets:
            mag_type = str(mag.ref.magType)
            # What parameter name are we looking for in the LTE file?
            if mag_type == 'QUAD':
                param = 'K1'
                conv_func = lambda k: k # use as-is
            elif mag_type == 'DIP':
                param = 'ANGLE'
                conv_func = math.degrees # .lte files have angles in radians
            else:
                continue # nothing to do for other types
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
        else:
            message = 'No applicable magnet settings found in {filename}'.format(**locals())
        QtGui.QMessageBox.about(self, 'Magnet table', message)
 
    def helpButtonClicked(self):
        webbrowser.open('http://projects.astec.ac.uk/VELAManual2/index.php/Magnet_table')
           

    def closeEvent(self, event):
        print('closing')
        self.widgetUpdateTimer.stop()
        exit()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    # Create and display the splash screen
    splash_pix = pixmap('splash-screen')
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    window = Window()
#    app.installEventFilter(window)
    app.aboutToQuit.connect(window.close)
    window.show()
    splash.finish(window)
    sys.exit(app.exec_())
