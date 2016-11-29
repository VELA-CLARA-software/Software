# -*- coding: utf-8 -*-
# encoding=utf8  
"""
VELA/CLARA magnet table
"""
try:
    from PyQt5 import QtCore, QtGui #for GUI building
except ImportError:
    from PyQt4 import QtCore, QtGui #for GUI building
import sys
from collections import namedtuple # for easy description of strength and units
import re # for reading in lines from config file
import math # conversion between radians/degrees
from epics import PV # for dealing directly with EPICS

branch = 'Release'
branch = 'stage'
pyds_path = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\' + branch + '\\'
sys.path.append(pyds_path)
import VELA_CLARA_MagnetControl

USING_CONTROLLERS = True # use magnet controllers, or go through EPICS directly?
# Define the speed of light. We need this to convert field integral to angle or K.
# e.g. theta = field_int * c / p[eV/c]
# (derive using mv²/rho=BeV, field_int=B.s, theta=s/rho, p[kg.m/s]=p[eV/c].e.(1V)/c)
SPEED_OF_LIGHT = 299.792458 # in megametres/second, use with p in MeV/c

def format_when_present(format_string, obj, attr):
    """"Returns a formatted string with the object's given attribute, 
    or a blank string when the attribute is not present."""
    try:
        return format_string.format(getattr(obj, attr))
    except AttributeError:
        return ''

line_regexp = re.compile('^(?P<parameter>.*) = (?P<value>.*);')

class Magnet:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
        
    def attachPVs(self):
        self.pvSI = PV(self.pv_root + ":SI")
        self.pvRI = PV(self.pv_root + ":RI")
        #TODO: add callbacks
        
class Window(QtGui.QMainWindow):
    magnet_current_changed = QtCore.pyqtSignal(str, float)
    
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.magInit = VELA_CLARA_MagnetControl.init()

        self.settings = QtCore.QSettings('magnet-table.ini', QtCore.QSettings.IniFormat)
        main_frame = QtGui.QFrame()
        layout = QtGui.QVBoxLayout(self)
        main_frame.setLayout(layout)
        self.setCentralWidget(main_frame)
        checkbox_grid = QtGui.QHBoxLayout()
        magnet_types = ('Dipoles', 'Quadrupoles', 'Correctors', 'Solenoids')
        for mag in magnet_types:
            checkbox = QtGui.QCheckBox(mag)
            #TODO: icons for checkboxes
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
        section_font = QtGui.QFont()
        section_font.setPointSize(16)
        section_font.setBold(True)
        magnet_font = QtGui.QFont()
        magnet_font.setPointSize(14)
        magnet_font.setBold(True)
        for section in section_names:
            section_vbox = QtGui.QVBoxLayout()
            header_hbox = QtGui.QHBoxLayout()
            #FIXME: this doesn't work - it should fold up to the top not the middle
            header_hbox.setSizeConstraint(QtGui.QLayout.SetFixedSize)
            title = QtGui.QLabel(section)
            title.setFont(section_font)
            header_hbox.addWidget(title)
            #TODO: set font size
            momentum = QtGui.QDoubleSpinBox()
            momentum.setSuffix(' MeV')
            momentum.setValue(6.5) #TODO: set some sensible value
            #TODO: set event - changed
            header_hbox.addWidget(momentum)
            section_vbox.addLayout(header_hbox)
            magnet_list_frame = QtGui.QFrame()
            magnet_list_vbox = QtGui.QVBoxLayout()
            magnet_list_frame.setLayout(magnet_list_vbox)
            magnet_list_vbox.momentum_spin = momentum # so we can reference it from a magnet
            magnet_list[section] = magnet_list_vbox
            section_vbox.addWidget(magnet_list_frame)
            section_list.addLayout(section_vbox)
            title.toggle_frame = magnet_list_frame
            
#        mag_names = self.controller.getMagnetNames() # but these don't come in the right order so...
        if USING_CONTROLLERS:
            mag_names = 'BSOL SOL HCOR01 VCOR01 HCOR02 VCOR02 QUAD01 QUAD02 QUAD03 QUAD04 HCOR03 VCOR03 HCOR04 VCOR04 DIP01 HCOR05 VCOR05 QUAD05 QUAD06 HCOR06 VCOR06 QUAD07 QUAD08 HCOR07 VCOR07 QUAD09 HCOR08 VCOR08 QUAD10 QUAD11 HCOR09 VCOR09 DIP02 HCOR10 VCOR10 QUAD12 DIP03 HCOR11 VCOR11 QUAD13 QUAD14 QUAD15'.split(' ')
            self.mag_refs = [self.controller.getMagObjConstRef(name) for name in mag_names]
        else:
            # Another way to get the magnet references - go through EPICS
            # That way we can get callbacks every time a PV is updated elsewhere
            # First read in the magnet data from the config file
            self.mag_refs = []
            magnet = None
    #        with open(pyds_path + '..\\..\\Config\\velaINJMagnets.config') as config_file:
            with open('C:\\Documents\\CLARA\\VELA-CLARA-Controllers\\VELA-CLARA-Controllers\\Config\\velaINJMagnets.config') as config_file:
                for line in config_file:
                    matches = line_regexp.match(line)
                    if matches:
                        parameter, value = matches.groups()
                        if parameter == 'NAME':
                            magnet = Magnet(name=value)
                            self.mag_refs.append(magnet)
                        elif magnet:
                            try:
                                value_float = float(value)
                                value = value_float
                            except ValueError:
                                pass
                            setattr(magnet, parameter.lower(), value)
                            
            [mag.attachPVs() for mag in self.mag_refs]
        
#        self.mag_refs.sort(key=lambda mag: mag.position)
        section = 'VELA Injector' #TODO: get this for each magnet
        label_size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        # Each type of magnet has some common attributes - here's how we access them
        # The conv_func here converts normalised strength (ns) and length (l) into
        # meaningful units for this type of magnet. Normalised strength is equal to
        # 299.8 * integrated_strength / momentum [MeV]
        mag_attr = namedtuple('mag_attr', 'friendly_name int_strength_name int_strength_units strength_name strength_units')
        self.mag_attributes = {
            'BSOL': mag_attr('Bucking solenoid', 'Integrated field', 'T.mm', 'field', 'T'),
            'SOL': mag_attr('Solenoid', 'Integrated field', 'T.mm', 'field', 'T'),
            'DIP': mag_attr('Dipole', 'Angle', u'°', 'field', 'T'),
            'QUAD': mag_attr('Quadrupole', 'K', u'm⁻²', 'gradient', 'T/m'),
            'SEXT': mag_attr('Sextupole', 'K', u'm⁻³', 'gradient', u'T/m²'),
            'HCOR': mag_attr('H Corrector', 'Angle', 'mrad', 'field', 'T'),
            'VCOR': mag_attr('V Corrector', 'Angle', 'mrad', 'field', 'T'),
            'UNKNOWN_MAGNET_TYPE': mag_attr('Unknown', 'Strength', 'AU', 'strength', 'AU')}
        for magnet in self.mag_refs:
            magnet_list_vbox = magnet_list[section]
            magnet.section = magnet_list_vbox
            magnet_frame = QtGui.QFrame()
            magnet_vbox = QtGui.QVBoxLayout()
            magnet_frame.setLayout(magnet_vbox)
            magnet_frame.mag_ref = magnet
            main_hbox = QtGui.QHBoxLayout()
            magnet_vbox.addLayout(main_hbox)
            mag_type = str(magnet.magType) if USING_CONTROLLERS else magnet.mag_type
            attributes = self.mag_attributes[mag_type]
            title = QtGui.QLabel(magnet.name.replace(mag_type, attributes.friendly_name + ' '))
            title.setFont(magnet_font)
            main_hbox.addWidget(title)
            label = QtGui.QLabel(attributes.int_strength_name)
            label.setSizePolicy(label_size_policy)
            #TODO: hand cursor
            main_hbox.addWidget(label)
            if USING_CONTROLLERS:
                bipolar = not magnet.magRevType == VELA_CLARA_MagnetControl.MAG_REV_TYPE.POS
            else:
                bipolar = not magnet.mag_rev_type == 'POS'
            k_spin = QtGui.QDoubleSpinBox()
            k_spin.setSuffix(' ' + attributes.int_strength_units)
            k_spin.setValue(0) #TODO: get from somewhere
            k_spin.setMinimum(float('-inf') if bipolar else 0)
            k_spin.setMaximum(float('inf'))
            k_spin.setDecimals(3)
            magnet.k_spin = k_spin
            #TODO: only change if Control held down
            #TODO: set event - changed
            main_hbox.addWidget(k_spin)
            label = QtGui.QLabel('Current')
            label.setSizePolicy(label_size_policy)
            main_hbox.addWidget(label)
            current_spin = QtGui.QDoubleSpinBox()
            main_hbox.addWidget(current_spin)
            current_spin.setMinimum(-999.999 if bipolar else 0)
            current_spin.setMaximum(999.999)
            current_spin.setDecimals(3)
            current_spin.setSuffix(' A')
            magnet.current_spin = current_spin
            current_spin.valueChanged.connect(self.currentValueChanged)
            current_spin.setValue(magnet.siWithPol)
            # connect this event after setting the current so we don't trigger it unnecessarily
            k_spin.valueChanged.connect(self.kValueChanged)
            
            static_info = ''.join(('<b>', magnet.name, '</b> ', attributes.friendly_name,
                          format_when_present('<br><b>Manufactured by</b> {}', magnet, 'manufacturer'),
                          format_when_present('<br><b>Serial number</b> {}', magnet, 'serialNumber'),
                          format_when_present('<br><b>Measurement data location</b>: {}', magnet, 'measurentDataLocation'),
                          format_when_present('<br><b>Magnetic length</b>: {:.1f} mm', magnet, 'magneticLength')))
            
            #FIXME: this probably won't work when it gets tested...
            more_info = QtGui.QFrame()
            more_info_layout = QtGui.QHBoxLayout()
            more_info.setLayout(more_info_layout)
            
            offline_info = QtGui.QLabel(static_info)
            more_info_layout.addWidget(offline_info)
            online_info = QtGui.QLabel()
            more_info_layout.addWidget(online_info)
            magnet.online_info = online_info
            more_info.hide()
            magnet_vbox.addWidget(more_info)
            title.toggle_frame = more_info
            magnet_list_vbox.addWidget(magnet_frame)
        
        self.magnet_current_changed.connect(self.setMagnetCurrent) #TODO: this might not be necessary after all
        self.magnet_controls = magnet_list
        self.setWindowTitle('magnet table')
        self.setGeometry(300, 300, 300, 450)
        self.update_period = 100 # milliseconds
        self.startMainViewUpdateTimer()
        self.show()

    # these fucntions updatet the GUI and (re)start the timer
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
            #TODO: maybe this if block not necessary...
            if not round(magnet.siWithPol, 3) == round(magnet.current_spin.value(), 3):
                print(magnet.name)
                magnet.current_spin.setValue(magnet.siWithPol)
                #TODO: calc K from current (is it done automatically?)
            online_text_format = u'''<br><b>Read current</b>: {magnet.riWithPol:.3f} A
                                     <br><b>Integrated strength</b>: {int_strength:.3f} {attributes.int_strength_units}
                                     <br><b>Central {attributes.strength_name}</b>: {strength:.3f} {attributes.strength_units}'''
            mag_type = str(magnet.magType) if USING_CONTROLLERS else magnet.mag_type
            attributes = self.mag_attributes[mag_type]
            int_strength = magnet.siWithPol * magnet.slope + magnet.intercept
            strength = int_strength / magnet.magneticLength if magnet.magneticLength else 0
            magnet.online_info.setText(online_text_format.format(**locals()))

    def eventFilter(self, source, event):
        "Handle events - QLabel doesn't have click or wheel events."
        evType = event.type()
        if evType == QtCore.QEvent.MouseButtonRelease:
            try:
                vis = source.toggle_frame.isVisible()
                source.toggle_frame.setVisible(not vis)
            except:
                pass
        return QtGui.QMainWindow.eventFilter(self, source, event)
    
    def toggleMagType(self, toggled):
        "Called when a magnet type checkbox is clicked. Hide or show all the magnets of that type."
        #which checkbox was clicked? remove 's' from end, last 6 letters, lower case
        mag_type = str(self.sender().text())
        mag_type = mag_type[-7:-1].lower() 
        print(mag_type, toggled)
        for mag_list in self.magnet_controls.values():
            for i in range(mag_list.count()):
                magnet_vbox = mag_list.itemAt(i).widget()
                attributes = self.mag_attributes[str(magnet_vbox.mag_ref.magType)]
                if attributes.friendly_name[-6:].lower() == mag_type:
                    magnet_vbox.setVisible(toggled)
    
    def currentValueChanged(self, value):
        "Called when a current spin box is changed by the user."
        spinbox = self.sender()
        magnet = spinbox.parent().mag_ref
        self.magnet_current_changed.emit(magnet.name, value)
        self.calcKFromCurrent(magnet, value)
        
    def calcKFromCurrent(self, magnet, current):
        "Calculate the K value (or bend angle) of a magnet based on its current."
        # What is the momentum in this section?
        momentum = magnet.section.momentum_spin.value()
        # Get the integrated strength, based on an excitation curve
        int_strength = magnet.slope * current + magnet.intercept
        # Calculate the normalised strength
        norm_strength = SPEED_OF_LIGHT * int_strength / momentum
        # Depending on the magnet type, convert to meaningful units
        mag_type = str(magnet.magType)
        if mag_type == 'DIP':
            k = math.degrees(norm_strength / 1000) # deflection in degrees
        elif mag_type in ('QUAD', 'SEXT'):
            #TODO: check this is correct for sextupoles (although none for CLARA anyway!)
            k = 1000 * norm_strength / magnet.magneticLength # focusing term K
        elif mag_type in ('HCOR', 'VCOR'):
            k = norm_strength # deflection in mrad
        else: # solenoids
            #TODO: something more meaningful?
            k = int_strength # for now, just use field
        magnet.k_spin.setValue(k)
        print('{magnet.name}: current {current:.3f} -> k {k:.3f}'.format(**locals()))
        
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
            norm_strength = math.radians(k) * 1000
        elif mag_type in ('QUAD', 'SEXT'):
            #TODO: check correct for sextupoles
            norm_strength = k * magnet.magneticLength / 1000
        elif mag_type in ('HCOR', 'VCOR'): # k represents deflection in mrad
            norm_strength = k
        else: # solenoids
            int_strength = k
        if int_strength is None:
            int_strength = norm_strength * momentum / SPEED_OF_LIGHT
        
        current = (int_strength - magnet.intercept) / magnet.slope
        magnet.current_spin.setValue(current)
        print('{magnet.name}: k {k:.3f} -> current {current:.3f}'.format(**locals()))
        
    def setMagnetCurrent(self, mag_name, value):
        self.controller.setSI(str(mag_name), value)
        
    def setMachineMode(self, checked=False, mode=None):
        radio_button = self.sender()
        if not radio_button == None:
            mode = str(radio_button.text()).lower()
        controller_func = self.magInit.__getattribute__(mode + '_VELA_INJ_Magnet_Controller')
        self.controller = controller_func()
        self.settings.setValue('machine_mode', mode)
        #TODO: check that it actually worked
        #TODO: apply magnet settings to GUI

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    # Create and display the splash screen
#    splash_pix = QtGui.QPixmap('Icons\\hourglass_256.png')
#    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
#    splash.setMask(splash_pix.mask())
#    splash.show()
#    app.processEvents()

    window = Window()
    app.installEventFilter(window)
    app.aboutToQuit.connect(window.close)
    window.show()
#    splash.finish(window)
    sys.exit(app.exec_())
