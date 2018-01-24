#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS 2017
from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtCore import QString
from conditioning_gui import Ui_MainWindow
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from VELA_CLARA_RF_Protection_Control import RF_GUN_PROT_STATUS
from VELA_CLARA_enums import STATE
from VELA_CLARA_LLRF_Control import LLRF_TYPE
import data.rf_condition_data_base as dat
# ok - so gui should get a object ref
# and then update as appropriate!
# every time
# other data  should be monitored in the dat aclass?


class gui_conditioning(QMainWindow, Ui_MainWindow):
    my_name = 'gui_conditioning'
    # clipboard
    clip_app = QApplication([])
    clip = clip_app.clipboard()
    # global state
    can_run = False
    #constant colors
    good = open  = trig = 'green'
    bad  = error = closed = 'red'
    err = 'orange'
    unknown = 'magenta'
    major_error = 'cyan'
    timing = 'yellow'

    # custom close signal to send to controller
    closing = pyqtSignal()
    # 
    update_via_controller = {}
    [update_via_controller.update({x: False}) for x in dat.all_value_keys]
    widget = {}
    previous_values = {}
    [previous_values.update({x: None}) for x in dat.all_value_keys]
    
        
    def __init__(self,
                 window_name = "",
                 root = "/",
                 update_time = 2000,
                 data = None,
                 ):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.values  = data.values
        self.data = data
        # CONNECT BUTTONS TO FUNCTIONS
        self.start_button.clicked.connect(self.handle_start_button)
        self.pause_ramp_button.clicked.connect(self.handle_pause_ramp_button)
        self.shutdown_rf_button.clicked.connect(self.handle_shutdown_rf_button)
        self.copy_to_clipboard_button.clicked.connect(self.handle_copy_to_clipboard_button)

        # widgets are held in dict, with same keys as data
        self.init_widget_dict(data)
        # the clipboard has a string version of data
        self.clip_vals = self.values.copy()
        # init to paused
        #self.handle_pause_ramp_button()
        self.handle_start_button()
        # update timer
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(update_time)
    # customclose function
    def closeEvent(self,event):
        self.closing.emit()
    # button functions
    def handle_start_button(self):
        print self.my_name +' is statrting RF conditioning'
        self.label.setStyleSheet('Qlabel { background-color : '+ self.good +'; color : black; }')
        self.can_run = True

    def handle_pause_ramp_button(self):
        print self.my_name +' is pausing RF conditioning'
        self.label.setStyleSheet('Qlabel { background-color : '+ self.bad +'; color : black; }')
        self.can_run = False

    def handle_shutdown_rf_button(self):
        print 'handle_shutdown_rf_button'

    def handle_copy_to_clipboard_button(self):
        string = ''
        for key,value in self.clip_vals.iteritems():
            string += key + ' : ' + str(value) + '\n'
        self.clip.setText(QString(string))

    # main update gui function, loop over all data and update gui with new values
    def update_gui(self):
        for key,val in self.widget.iteritems():
            if self.value_is_new(key, self.values[key]):
                self.update_widget(key, self.values[key], val)

        # #print 'update_gui'
        # for key,val in self.values.iteritems():
        #         if self.value_is_new(key,val):
        #             try:
        #                 widget = self.widget[key]
        #             except (KeyError):
        #                 pass
                    #print 'MAJOR ERROR MISSING WIDGET ' + key
    # the outputwidget is update based on data type
    def update_widget(self, key, val, widget):
        #print(type(val),key,widget.objectName())
        if type(val) is long:
            widget.setText('%i' % val)
            self.clip_vals[key] = widget.text()
        elif type(val) is int:
            widget.setText('%i' % val)
            self.clip_vals[key] = widget.text()
        elif type(val) is float:
            widget.setText('%.3E' % val)
            self.clip_vals[key] = widget.text()
        elif type(val) is RF_GUN_PROT_STATUS:
            self.set_RF_prot(widget, val, key)
        elif type(val) is STATE:
            self.set_status(widget, val, key)
        elif type(val) is GUN_MOD_STATE:
            self.set_mod_state(widget, val, key)
        elif type(val) is VALVE_STATE:
            self.set_valve(widget, val, key)
        elif type(val) is bool:
            self.set_locked_enabled(widget, val, key)
        else:
            print 'update_widget error ' + str(val) + ' ' + str(type(val))
    # if a value is new we update the widget
    def value_is_new(self,key,val):
        try:
            if self.previous_values[key] != val:
                self.previous_values[key] = val
                return True
            else:
                return False
        except:
            return True
    # functions to update colors in widgets
    def set_status(self, widget, val, status):
        if val == STATE.UNKNOWN:
            self.set_widget_color_text(widget, 'UNKNOWN', self.unknown, status)
        elif val == STATE.GOOD:
            self.set_widget_color_text(widget, 'GOOD', self.good, status)
        elif val == STATE.BAD:
            self.set_widget_color_text(widget, 'BAD', self.bad, status)
        elif val == STATE.ERR:
            self.set_widget_color_text(widget, 'ERR', self.err, status)
        else:
            self.set_widget_color_text(widget, 'MAJOR_ERROR', self.major_error, status)

    def set_locked_enabled(self, widget, val, status):
        if val == True:
            self.set_widget_color_text(widget, 'GOOD', self.good, status)
        elif val == False:
            self.set_widget_color_text(widget, 'BAD', self.bad, status)
        else:
            self.set_widget_color_text(widget, 'MAJOR_ERROR', self.major_error, status)

    def set_valve(self,widget, val, status):
        if val == VALVE_STATE.VALVE_OPEN:
            self.set_widget_color_text(widget, 'OPEN', self.open, status)
        elif val == VALVE_STATE.VALVE_CLOSED:
            self.set_widget_color_text(widget, 'CLOSED', self.closed, status)
        elif val == VALVE_STATE.VALVE_TIMING:
            self.set_widget_color_text(widget, 'TIMING', self.timing, status)
        elif val == VALVE_STATE.VALVE_ERROR:
            self.set_widget_color_text(widget, 'ERROR', self.error, status)
        else:
            self.set_widget_color_text(widget, 'MAJOR_ERROR', self.major_error, status)

    def set_RF_prot(self,widget, val, status):
        if val == RF_GUN_PROT_STATUS.GOOD:
            self.set_widget_color_text(widget, 'GOOD', self.good, status)
        elif val == RF_GUN_PROT_STATUS.BAD:
            self.set_widget_color_text(widget, 'BAD', self.bad,status)
        elif val == RF_GUN_PROT_STATUS.ERROR:
            self.set_widget_color_text( widget, 'ERROR', self.error,status)
        elif val == RF_GUN_PROT_STATUS.UNKNOWN:
            self.set_widget_color_text(widget, 'UNKNOWN', self.unknown,status)
        else:
            self.set_widget_color_text(widget, 'MAJOR_ERROR', self.major_error, status)

    def set_mod_state(self,widget, val, status):
        if val == GUN_MOD_STATE.Trig:
            self.set_widget_color_text(widget, 'Trig', self.trig, status)
        elif val == GUN_MOD_STATE.ERROR1:
            self.set_widget_color_text(widget, 'ERROR1', self.error, status)
        elif val == GUN_MOD_STATE.UNKNOWN1:
            widget.setStyleSheet("QLabel { background-color : magenta; color : black; }")
            widget.setText('UNKNOWN1')  # MAGIC_STRING
        elif val == GUN_MOD_STATE.OFF:
            widget.setStyleSheet("QLabel { background-color : red; color : black; }")
            widget.setText('OFF')  # MAGIC_STRING
        elif val == GUN_MOD_STATE.HV_Intrlock:
            widget.setStyleSheet("QLabel { background-color : red; color : black; }")
            widget.setText('HV_Intrlock')  # MAGIC_STRING
        elif val == GUN_MOD_STATE.Standby_Request:
            widget.setStyleSheet("QLabel { background-color : orange; color : black; }")
            widget.setText('Standby_Request')  # MAGIC_STRING
        elif val == GUN_MOD_STATE.Standby:
            widget.setStyleSheet("QLabel { background-color : orange; color : black; }")
            widget.setText('Standby')  # MAGIC_STRING
        elif val == GUN_MOD_STATE.HV_Off_Requ:
            widget.setStyleSheet("QLabel { background-color : magenta; color : black; }")
            widget.setText('HV_Off_Requ')  # MAGIC_STRING
        elif val == GUN_MOD_STATE.Trigger_Interl:
            widget.setStyleSheet("QLabel { background-color : red; color : black; }")
            widget.setText('Trigger_Interl')  # MAGIC_STRING
        elif val == GUN_MOD_STATE.HV_Request:
            widget.setStyleSheet("QLabel { background-color : orange; color : black; }")
            widget.setText('HV_Request')  # MAGIC_STRING
        elif val == GUN_MOD_STATE.HV_On:
            widget.setStyleSheet("QLabel { background-color : orange; color : black; }")
            widget.setText('HV_On')  # MAGIC_STRING
        elif val == GUN_MOD_STATE.Trig_Off_Req:
            widget.setStyleSheet("QLabel { background-color : magenta; color : black; }")
            widget.setText('Trig_Off_Req')  # MAGIC_STRING
        elif val == GUN_MOD_STATE.Trig_Request:
            widget.setStyleSheet("QLabel { background-color : magenta; color : black; }")
            widget.setText('Trig_Request')  # MAGIC_STRING
        self.clip_vals[status] = str(widget.text())

    def set_widget_color_text(self, widget, text, color, status):
        widget.setStyleSheet('QLabel { background-color : '+color+'; color : black; }')
        widget.setText(text)  # MAGIC_STRING
        self.clip_vals[status] = str(widget.text())

    def init_widget_dict(self, data):
        #MANUALLY CONNECT THESE UP :/
        self.widget[dat.probe_pwr] =self.probe_power_outputwidget
        self.widget[dat.vac_spike_status] =self.vac_spike_status_outputwidget
        self.widget[dat.DC_spike_status] =self.DC_spike_status_outputwidget
        self.widget[dat.modulator_state] =self.mod_state_outputwidget
        self.widget[dat.rfprot_state] =self.RF_protection_outputwidget
        self.widget[dat.llrf_output] =self.llrf_output_outputwidget
        self.widget[dat.llrf_ff_amp_locked] =self.llrf_ff_amp_locked_outputwidget
        self.widget[dat.llrf_ff_ph_locked] =self.llrf_ff_ph_locked_outputwidget
        self.widget[dat.vac_level] =self.vac_level_outputwidget
        self.widget[dat.cav_temp] =self.cav_temp_outputwidget
        self.widget[dat.water_temp] =self.water_temp_outputwidget
        self.widget[dat.pulse_length] =self.pulse_length_outputwidget
        self.widget[dat.fwd_cav_pwr] =self.fwd_cav_power_outputwidget
        self.widget[dat.rev_cav_pwr] =self.rev_cav_power_outputwidget
        self.widget[dat.fwd_kly_pwr] =self.fwd_kly_power_outputwidget
        self.widget[dat.rev_kly_pwr] =self.rev_kly_power_outputwidget
        self.widget[dat.elapsed_time] =self.elapsed_time_outputwidget
        self.widget[dat.breakdown_rate] =self.measured_breakdown_rate_outputwidget
        self.widget[dat.breakdown_count] =self.breakdown_count_outputwidget
        self.widget[dat.pulse_count] =self.pulse_count_outputwidget
        self.widget[dat.rev_power_spike_status] =self.rev_power_spike_status_outputwidget
        self.widget[dat.breakdown_rate_limit] =self.breakdown_rate_limit_outputwidget
        self.widget[dat.vac_valve_status] =self.vac_valve_status_outputwidget
        self.widget[dat.amp_ff] =self.amp_set_outputwidget
        self.widget[dat.DC_level] =self.dc_level_outputwidget