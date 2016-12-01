# -*- coding: utf-8 -*-
# encoding=utf8
"""
VELA/CLARA magnet table
"""
from PyQt4 import QtCore, QtGui #for GUI building
import sys
from collections import namedtuple # for easy description of strength and units
import math # conversion between radians/degrees
from os import system # clicking URLs on labels

# Image credits
# Offline.png: http://www.iconarchive.com/show/windows-8-icons-by-icons8/Network-Disconnected-icon.html
# Virtual.png: https://thenounproject.com/search/?q=simulator&i=237636
# Physical.png: http://www.flaticon.com/free-icon/car-compact_31126#term=car&page=1&position=19
# undo.png: https://www.iconfinder.com/icons/49866/undo_icon
# warning.png: http://www.iconsdb.com/orange-icons/warning-3-icon.html
# error.png: http://www.iconsdb.com/soylent-red-icons/warning-3-icon.html
# magnet.png: https://www.iconfinder.com/icons/15217/magnet_icon

branch = 'Release'
branch = 'stage'
pyds_path = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\' + branch + '\\'
sys.path.append(pyds_path)
import VELA_CLARA_MagnetControl as MagCtrl

# Define the speed of light. We need this to convert field integral to angle or K.
# e.g. theta = field_int * c / p[eV/c]
# (derive using mv²/rho=BeV, field_int=B.s, theta=s/rho, p[kg.m/s]=p[eV/c].e.(1V)/c)
SPEED_OF_LIGHT = 299.792458 # in megametres/second, use with p in MeV/c

label_size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

online_text_format = u'''<b>Read current</b>: {magnet.riWithPol:.3f} A
                         <br><b>Integrated {attributes.strength_name}</b>: {int_strength:.3f} {attributes.int_strength_units}
                         <br><b>Central {attributes.strength_name}</b>: {strength:.3f} {attributes.strength_units}'''

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
    return QtGui.QPixmap('Icons\\' + icon_name + '.png')

class Window(QtGui.QMainWindow):
    magnet_current_changed = QtCore.pyqtSignal(str, float)
    
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.magInit = MagCtrl.init()

        self.settings = QtCore.QSettings('magnet-table.ini', QtCore.QSettings.IniFormat)
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
        sep = QtGui.QFrame()
        sep.setFrameShape(QtGui.QFrame.VLine)
        sep.setFrameShadow(QtGui.QFrame.Sunken)
        checkbox_grid.addWidget(sep)
        set_mode = self.settings.value('machine_mode', 'offline')
        for mode in machine_modes:
            radio = QtGui.QRadioButton(mode)
            radio.setIcon(QtGui.QIcon(pixmap(mode)))
            radio.setChecked(mode.lower() == set_mode)
            radio.clicked.connect(self.setMachineMode)
            self.setMachineMode(mode='offline')
            checkbox_grid.addWidget(radio)
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
            title = self.collapsing_header(header_hbox, magnet_list_frame, section)
            title.setFont(section_font)
            #TODO: set some sensible value
            momentum = self.spinbox(header_hbox, 'MeV', step=0.5, value=6.5)
            momentum
            #TODO: set event - what should happen if the momentum is changed?
            section_vbox.addLayout(header_hbox)
            magnet_list_vbox = QtGui.QVBoxLayout()
            magnet_list_frame.setLayout(magnet_list_vbox)
            magnet_list_vbox.momentum_spin = momentum # so we can reference it from a magnet
            magnet_list[section] = magnet_list_vbox
            section_vbox.addWidget(magnet_list_frame)
            section_list.addLayout(section_vbox)
            
        mag_names = self.controller.getMagnetNames() # but these don't come in the right order so...
#        mag_names = 'BSOL SOL HCOR01 VCOR01 HCOR02 VCOR02 QUAD01 QUAD02 QUAD03 QUAD04 HCOR03 VCOR03 HCOR04 VCOR04 DIP01 HCOR05 VCOR05 QUAD05 QUAD06 HCOR06 VCOR06 QUAD07 QUAD08 HCOR07 VCOR07 QUAD09 HCOR08 VCOR08 QUAD10 QUAD11 HCOR09 VCOR09 DIP02 HCOR10 VCOR10 QUAD12 DIP03 HCOR11 VCOR11 QUAD13 QUAD14 QUAD15'.split(' ')
        self.mag_refs = [self.controller.getMagObjConstRef(name) for name in mag_names]
        
        self.mag_refs.sort(key=lambda mag: mag.position)
        section = 'VELA Injector' #TODO: get this for each magnet
        # Each type of magnet has some common attributes - here's how we access them
        mag_attr = namedtuple('mag_attr', 'friendly_name effect_name effect_units strength_name strength_units int_strength_units')
        self.mag_attributes = {
            'BSOL': mag_attr('Bucking solenoid', 'Integrated field', 'T.mm', 'field', 'T', 'T.mm'),
            'SOL':  mag_attr('Solenoid', 'Integrated field', 'T.mm', 'field', 'T', 'T.mm'),
            'DIP':  mag_attr('Dipole', 'Angle', u'°', 'field', 'T', 'T.mm'),
            'QUAD': mag_attr('Quadrupole', 'K', u'm⁻²', 'gradient', 'T/m', 'T'),
            'SEXT': mag_attr('Sextupole', 'K', u'm⁻³', 'gradient', u'T/m²', 'T/m'),
            'HCOR': mag_attr('H Corrector', 'Angle', 'mrad', 'field', 'mT', 'T.mm'),
            'VCOR': mag_attr('V Corrector', 'Angle', 'mrad', 'field', 'mT', 'T.mm'),
            'UNKNOWN_MAGNET_TYPE': mag_attr('Unknown', 'Strength', 'AU', 'strength', 'AU', 'AU')}
        for magnet in self.mag_refs:
            magnet.prev_values = []
            magnet.active = False # whether magnet is being changed
            magnet_list_vbox = magnet_list[section]
            magnet.section = magnet_list_vbox
            magnet_frame = QtGui.QFrame()
            magnet_frame.setFrameShape(QtGui.QFrame.Box | QtGui.QFrame.Plain)
            #thicker border for magnets at the end of branches
            #TODO: this is a bit of a hack
            #TODO: show/hide branches (maybe automatically)
            end_of_branch = magnet.name in ('QUAD06', 'QUAD14')
            magnet_frame.setLineWidth(3 if end_of_branch else 1)
            magnet_frame.setContentsMargins(0, 0, 0, 3 if end_of_branch else 1)
            magnet_vbox = QtGui.QVBoxLayout()
            magnet_frame.setLayout(magnet_vbox)
            magnet_frame.mag_ref = magnet
            main_hbox = QtGui.QHBoxLayout()
            main_hbox.setAlignment(QtCore.Qt.AlignTop)
            magnet_vbox.addLayout(main_hbox)
            more_info = QtGui.QFrame()
            mag_type = str(magnet.magType)
            attributes = self.mag_attributes[mag_type]
            # 'H Corrector' -> 'Correctors'; 'Quadrupole' -> 'Quadrupoles'
            generic_name = attributes.friendly_name.split(' ')[-1].capitalize() + 's'

            icon = self.collapsing_header(main_hbox, more_info)
            icon.setPixmap(pixmap(generic_name).scaled(32, 32))
            # The tab here aligns all the current spinboxes nicely
            title_text = magnet.name.replace(mag_type, attributes.friendly_name + ' ') + '\t'
            title = self.collapsing_header(main_hbox, more_info, title_text)
            title.setFont(magnet_font)
            self.collapsing_header(main_hbox, more_info, attributes.effect_name)
            bipolar = not magnet.magRevType == MagCtrl.MAG_REV_TYPE.POS
            k_spin = self.spinbox(main_hbox, attributes.effect_units, step=0.1, decimals=3, bipolar=bipolar)
            magnet.k_spin = k_spin
            self.collapsing_header(main_hbox, more_info, 'Current')
            current_spin = self.spinbox(main_hbox, 'A', step=0.1, decimals=3, bipolar=bipolar)
            magnet.current_spin = current_spin
            current_spin.valueChanged.connect(self.currentValueChanged)
            current_spin.setValue(magnet.siWithPol)
            restore_button = QtGui.QToolButton()
            restore_button.setIcon(QtGui.QIcon(pixmap('undo')))
            restore_button.clicked.connect(self.restoreMagnet)
            main_hbox.addWidget(restore_button)
            magnet.restore_button = restore_button
            restore_button.hide()
            warning_icon = self.collapsing_header(main_hbox, more_info)
            warning_icon.hide()
            magnet.warning_icon = warning_icon
            #TODO: warn when magnet is switched off
            #TODO: warn when magnet needs degaussing
            # connect this event after setting the current so we don't trigger it unnecessarily
            k_spin.valueChanged.connect(self.kValueChanged)
            
            static_info = ('<b>', magnet.name, '</b> ', attributes.friendly_name,
                           format_when_present('<br><b>Manufactured by</b> {}', magnet, 'manufacturer'),
                           format_when_present('<br><b>Serial number</b> {}', magnet, 'serialNumber'),
                           format_when_present('<br><b>Magnetic length</b>: {:.1f} mm', magnet, 'magneticLength'),
                           format_when_present('<br><a href="{}">Measurement data</a>', magnet, 'measurementDataLocation'))
            
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
        
        self.magnet_current_changed.connect(self.setMagnetCurrent) #TODO: this might not be necessary after all
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
        if step:
            spinbox.setSingleStep(step)
        parent.addWidget(spinbox)
        spinbox.installEventFilter(self)
        return spinbox
    
    # these functions update the GUI and (re)start the timer
    def startMainViewUpdateTimer(self):
        self.widgetUpdateTimer = QtCore.QTimer()
        QtCore.QTimer.connect(self.widgetUpdateTimer, QtCore.SIGNAL("timeout()"), self.mainViewUpdate )
        self.widgetUpdateTimer.start(self.update_period)
    def mainViewUpdate(self):
        # conceivably the timer could restart this function before it complete - so guard against that
        try:
            self.updateMagnetWidgets()
        finally:
            self.widgetUpdateTimer.start(self.update_period)
            
    def updateMagnetWidgets(self):
        for magnet in self.mag_refs:
            if not magnet.psuState == MagCtrl.MAG_PSU_STATE.MAG_PSU_ON:
                magnet.warning_icon.setPixmap(pixmap('error'))
                magnet.warning_icon.setToolTip('Magnet PSU: ' + str(magnet.psuState)[8:])
                magnet.warning_icon.show()
            elif abs(magnet.siWithPol - magnet.riWithPol) > 0.01:
                magnet.warning_icon.setPixmap(pixmap('warning'))
                magnet.warning_icon.setToolTip('Read current and set current do not match')
                magnet.warning_icon.show()
            magnet.current_spin.setValue(magnet.siWithPol)
            mag_type = str(magnet.magType)
            attributes = self.mag_attributes[mag_type]
            int_strength = magnet.siWithPol * magnet.slope + magnet.intercept
            strength = int_strength / magnet.magneticLength if magnet.magneticLength else 0
            if mag_type[1:] == 'COR':
                strength *= 1000 # convert to mT for correctors
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
                    magnet = source.parent().mag_ref
                    magnet.active = False
                except AttributeError: # won't work for momentum spin boxes
                    pass
        return False#QtGui.QMainWindow.eventFilter(self, source, event)
    
    def labelLinkClicked(self, url):
        system('start "" "' + str(url) + '"')

    def toggleMagType(self, toggled):
        "Called when a magnet type checkbox is clicked. Hide or show all the magnets of that type."
        #which checkbox was clicked? remove 's' from end, last 6 letters, lower case
        mag_type = str(self.sender().text())
        mag_type = mag_type[-7:-1].lower() 
#        print(mag_type, toggled)
        for mag_list in self.magnet_controls.values():
            for i in range(mag_list.count()):
                magnet_vbox = mag_list.itemAt(i).widget()
                attributes = self.mag_attributes[str(magnet_vbox.mag_ref.magType)]
                if attributes.friendly_name[-6:].lower() == mag_type:
                    magnet_vbox.setVisible(toggled)

    def currentValueChanged(self, value):
        "Called when a current spin box is changed by the user."
        magnet = self.sender().parent().mag_ref
        self.magnet_current_changed.emit(magnet.name, value)
        self.calcKFromCurrent(magnet, value)
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
        
    def calcKFromCurrent(self, magnet, current):
        "Calculate the K value (or bend angle) of a magnet based on its current."
        # What is the momentum in this section?
        momentum = magnet.section.momentum_spin.value()
        # Get the integrated strength, based on an excitation curve
        # This is in T.mm for dipoles, T for quads, T/m for sextupoles
        int_strength = magnet.slope * current + magnet.intercept
        # Calculate the normalised effect on the beam
        # This is in radians for dipoles, m⁻¹ for quads, m⁻² for sextupoles
        effect = SPEED_OF_LIGHT * int_strength / momentum
        # Depending on the magnet type, convert to meaningful units
        mag_type = str(magnet.magType)
        if mag_type == 'DIP':
            # Get deflection in degrees
            # int_strength was in T.mm so we divide by 1000
            k = math.degrees(effect / 1000)
        elif mag_type in ('QUAD', 'SEXT'):
            k = 1000 * effect / magnet.magneticLength # focusing term K
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
        magnet = spinbox.parent().mag_ref
        self.calcCurrentFromK(magnet, value)
        
    def calcCurrentFromK(self, magnet, k):
        "Calculate the current to set in a magnet based on its K value (or bend angle)."
        # What is the momentum in this section?
        momentum = magnet.section.momentum_spin.value()
        mag_type = str(magnet.magType)
        int_strength = None
        if mag_type == 'DIP': # k represents deflection in degrees
            effect = math.radians(k) * 1000
        elif mag_type in ('QUAD', 'SEXT'):
            #TODO: check correct for sextupoles
            effect = k * magnet.magneticLength / 1000
        elif mag_type in ('HCOR', 'VCOR'): # k represents deflection in mrad
            effect = k
        else: # solenoids
            int_strength = k
        if int_strength is None:
            int_strength = effect * momentum / SPEED_OF_LIGHT
        current = (int_strength - magnet.intercept) / magnet.slope
        magnet.current_spin.setValue(current)
#        print('{magnet.name}: k {k:.3f} -> current {current:.3f}'.format(**locals()))
        
    def setMagnetCurrent(self, mag_name, value):
        self.controller.setSI(str(mag_name), value)
        
    def restoreMagnet(self):
        "Implement an 'undo' button for each magnet."
        magnet = self.sender().parent().mag_ref
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
        
    def setMachineMode(self, checked=False, mode=None):
        radio_button = self.sender()
        # mode can be defined already, we call this function on initial setup
        if not mode:
            mode = str(radio_button.text())
        self.controller = self.magInit.getMagnetController(MagCtrl.MACHINE_MODE.names[mode.upper()], MagCtrl.MACHINE_AREA.VELA_INJ)
        self.settings.setValue('machine_mode', mode)
        #TODO: check that it actually worked
        #TODO: apply magnet settings to GUI

    def closeEvent(self, event):
        exit()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    # Create and display the splash screen
#    splash_pix = QtGui.QPixmap('Icons\\hourglass_256.png')
#    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
#    splash.setMask(splash_pix.mask())
#    splash.show()
#    app.processEvents()

    window = Window()
#    app.installEventFilter(window)
    app.aboutToQuit.connect(window.close)
    window.show()
#    splash.finish(window)
    sys.exit(app.exec_())
