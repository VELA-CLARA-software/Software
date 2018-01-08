#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS 2017
# part of MagtnetApp
from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QApplication
from conditioning_gui import Ui_MainWindow
import datetime
from state import state
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from VELA_CLARA_RF_Protection_Control import RF_GUN_PROT_STATUS



class gui_conditioning(QMainWindow, Ui_MainWindow):
    # gui value dict
    vacuum_level = 'vacuum_level'
    vac_spike_status = 'vac_spike_status'
    DC_spike_status = 'DC_spike_status'
    rev_power_spike_status = 'rev_power_spike_status'
    #RF_lost_status = 'RF_lost_status'
    cav_temp = 'cav_temp'
    water_temp = 'water_temp'
    pulse_length = 'pulse_length'
    fwd_cav_power = 'fwd_cav_power'
    fwd_kly_power = 'fwd_kly_power'
    rev_kly_power = 'rev_kly_power'
    rev_cav_power = 'rev_cav_power'
    probe_power  = 'probe_power'
    vac_level = 'vac_level'
    vac_valve_status = 'vac_valve_status'
    breakdown_rate_limit = 'breakdown_rate_limit'
    measured_breakdown_rate = 'measured_breakdown_rate'
    breakdown_rate_statistics = 'breakdown_rate_statistics'
    modulator_state  = 'modulator_state'
    rfprot_state  = 'rfprot_state'
    llrf_enabled  = 'llrf_enabled'
    llrf_locked  = 'llrf_locked'
    pulse_count  = 'pulse_count'

    all_gui_values = [vac_spike_status,DC_spike_status,
                      rev_power_spike_status,modulator_state,
                      cav_temp,water_temp,pulse_length,
                      fwd_cav_power,fwd_kly_power,rev_kly_power,
                      rev_cav_power,probe_power,vac_level,
                      vac_valve_status,breakdown_rate_limit,
                      rfprot_state,llrf_locked,llrf_enabled,
                      measured_breakdown_rate,breakdown_rate_statistics]


    gui_values = {}
    [gui_values.update({x: -999}) for x in all_gui_values]

    def __init__(self, window_name = "", root = "/",update_time = 2000 ):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.update_time = update_time


        self.start_button.clicked.connect(self.handle_start_button)
        self.pause_ramp_button.clicked.connect(self.handle_pause_ramp_button)
        self.shutdown_rf_button.clicked.connect(self.handle_shutdown_rf_button)
        self.copy_to_clipboard_button.clicked.connect(self.handle_copy_to_clipboard_button)

        #self.outputWidget_15.setText(_translat
        #self.outputWidget_16.setText(_translat
        self.gui_values[self.vac_valve_status]= 'UNKNOWN'
        self.vac_valve_status_old = None

        self.gui_values[self.vac_spike_status] = state.UNKNOWN
        self.vac_spike_status_old = None
        self.gui_values[self.DC_spike_status] = state.UNKNOWN
        self.DC_spike_status_old = None
        self.gui_values[self.rev_power_spike_status] = state.UNKNOWN
        self.rev_power_spike_status_old = None
        #self.gui_values[self.RF_lost_status] = state.UNKNOWN

        self.gui_values[self.modulator_state] = RF_GUN_PROT_STATUS.UNKNOWN
        self.modulator_state_old = None
        self.gui_values[self.rfprot_state] = RF_GUN_PROT_STATUS.UNKNOWN
        self.rfprot_state_old = None
        self.gui_values[self.llrf_enabled] = 'UNKNOWN'
        self.llrf_enabled_old = None
        self.gui_values[self.llrf_locked] = 'UNKNOWN'
        self.llrf_locked_old = None

        dummy = -999
        self.gui_values[self.cav_temp] = dummy
        self.gui_values[self.water_temp] = dummy + 1
        self.gui_values[self.pulse_length]= dummy + 2
        self.gui_values[self.fwd_cav_power]= dummy + 3
        self.gui_values[self.fwd_kly_power]= dummy + 4
        self.gui_values[self.rev_kly_power]= dummy + 5
        self.gui_values[self.rev_cav_power]= dummy + 6
        self.gui_values[self.probe_power]= dummy + 7
        self.gui_values[self.vac_level]= dummy + 8
        self.gui_values[self.breakdown_rate_limit]= dummy + 10
        self.gui_values[self.measured_breakdown_rate]= dummy + 11
        self.gui_values[self.breakdown_rate_statistics]= dummy + 12

        # for timed_cooldown we have a timer
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update)
        self.timer.start(self.update_time)

    def handle_start_button(self):
        print 'handle_start_button'
    def handle_pause_ramp_button(self):
        print 'handle_pause_ramp_button'
    def handle_shutdown_rf_button(self):
        print 'handle_shutdown_rf_button'
    def handle_copy_to_clipboard_button(self):
        print 'handle_copy_to_clipboard_button'

    def set_status(self,widget,status):
        if self.gui_values[status] == state.UNKNOWN:
            widget.setStyleSheet("QLabel { background-color : magenta; color : black; }")
            widget.setText('UNKNOWN')#MAGIC_STRING
        elif self.gui_values[status] == state.GOOD:
            widget.setStyleSheet("QLabel { background-color : green; color : black; }")
            widget.setText('GOOD')#MAGIC_STRING
        elif self.gui_values[status] == state.BAD:
            widget.setStyleSheet("QLabel { background-color : red; color : black; }")
            widget.setText('BAD')#MAGIC_STRING
        else:
            widget.setStyleSheet("QLabel { background-color : yellow; color : black; }")
            widget.setText('ERR')#MAGIC_STRING

    def set_locked_enabled(self,widget,status):
        if self.gui_values[status] == True:
            widget.setStyleSheet("QLabel { background-color : green; color : black; }")
            widget.setText('OK')#MAGIC_STRING
        elif self.gui_values[status] == False:
            widget.setStyleSheet("QLabel { background-color : red; color : black; }")
            widget.setText('NOT OK')#MAGIC_STRING
        else:
            widget.setStyleSheet("QLabel { background-color : cyan; color : black; }")
            widget.setText('ERROR')#MAGIC_STRING

    def set_valve(self,widget,status):
        if self.gui_values[status] == VALVE_STATE.VALVE_OPEN:
            widget.setStyleSheet("QLabel { background-color : green; color : black; }")
            widget.setText('OPEN')#MAGIC_STRING
        elif self.gui_values[status] == VALVE_STATE.VALVE_CLOSED:
            widget.setStyleSheet("QLabel { background-color : red; color : black; }")
            widget.setText('CLOSED')#MAGIC_STRING
        elif self.gui_values[status] == VALVE_STATE.VALVE_TIMING:
            widget.setStyleSheet("QLabel { background-color : yellow; color : black; }")
            widget.setText('TIMING')#MAGIC_STRING
        elif self.gui_values[status] == VALVE_STATE.VALVE_ERROR:
            widget.setStyleSheet("QLabel { background-color : magenta; color : black; }")
            widget.setText('ERROR')  # MAGIC_STRING
        else:
            widget.setStyleSheet("QLabel { background-color : cyan; color : black; }")
            widget.setText('UNKNOWN')#MAGIC_STRING

    def set_RF_prot(self,widget,status):
        if self.gui_values[status] == RF_GUN_PROT_STATUS.GOOD:
            widget.setStyleSheet("QLabel { background-color : green; color : black; }")
            widget.setText('GOOD')#MAGIC_STRING
        elif self.gui_values[status] == RF_GUN_PROT_STATUS.BAD:
            widget.setStyleSheet("QLabel { background-color : red; color : black; }")
            widget.setText('BAD')#MAGIC_STRING
        elif self.gui_values[status] == RF_GUN_PROT_STATUS.ERROR:
            widget.setStyleSheet("QLabel { background-color : yellow; color : black; }")
            widget.setText('ERROR')#MAGIC_STRING
        elif self.gui_values[status] == RF_GUN_PROT_STATUS.UNKNOWN:
            widget.setStyleSheet("QLabel { background-color : magenta; color : black; }")
            widget.setText('UNKNOWN')  # MAGIC_STRING
        else:
            widget.setStyleSheet("QLabel { background-color : cyan; color : black; }")
            widget.setText('MAJOR_ERROR')#MAGIC_STRING

    def set_mod_state(self,widget,status):
        if self.gui_values[status] == GUN_MOD_STATE.Trig:
            widget.setStyleSheet("QLabel { background-color : green; color : black; }")
            widget.setText('Trig')  # MAGIC_STRING
        elif self.gui_values[status] == GUN_MOD_STATE.ERROR1:
            widget.setStyleSheet("QLabel { background-color : red; color : black; }")
            widget.setText('ERROR1')#MAGIC_STRING
        elif self.gui_values[status] == GUN_MOD_STATE.UNKNOWN1:
            widget.setStyleSheet("QLabel { background-color : magenta; color : black; }")
            widget.setText('UNKNOWN1')  # MAGIC_STRING
        elif self.gui_values[status] == GUN_MOD_STATE.OFF:
            widget.setStyleSheet("QLabel { background-color : red; color : black; }")
            widget.setText('OFF')  # MAGIC_STRING
        elif self.gui_values[status] == GUN_MOD_STATE.HV_Intrlock:
            widget.setStyleSheet("QLabel { background-color : red; color : black; }")
            widget.setText('HV_Intrlock')  # MAGIC_STRING
        elif self.gui_values[status] == GUN_MOD_STATE.Standby_Request:
            widget.setStyleSheet("QLabel { background-color : orange; color : black; }")
            widget.setText('Standby_Request')  # MAGIC_STRING
        elif self.gui_values[status] == GUN_MOD_STATE.Standby:
            widget.setStyleSheet("QLabel { background-color : orange; color : black; }")
            widget.setText('Standby')  # MAGIC_STRING
        elif self.gui_values[status] == GUN_MOD_STATE.HV_Off_Requ:
            widget.setStyleSheet("QLabel { background-color : magenta; color : black; }")
            widget.setText('HV_Off_Requ')  # MAGIC_STRING
        elif self.gui_values[status] == GUN_MOD_STATE.Trigger_Interl:
            widget.setStyleSheet("QLabel { background-color : red; color : black; }")
            widget.setText('Trigger_Interl')  # MAGIC_STRING
        elif self.gui_values[status] == GUN_MOD_STATE.HV_Request:
            widget.setStyleSheet("QLabel { background-color : orange; color : black; }")
            widget.setText('HV_Request')  # MAGIC_STRING
        elif self.gui_values[status] == GUN_MOD_STATE.HV_On:
            widget.setStyleSheet("QLabel { background-color : orange; color : black; }")
            widget.setText('HV_On')  # MAGIC_STRING
        elif self.gui_values[status] == GUN_MOD_STATE.Trig_Off_Req:
            widget.setStyleSheet("QLabel { background-color : magenta; color : black; }")
            widget.setText('Trig_Off_Req')  # MAGIC_STRING
        elif self.gui_values[status] == GUN_MOD_STATE.Trig_Request:
            widget.setStyleSheet("QLabel { background-color : magenta; color : black; }")
            widget.setText('Trig_Request')  # MAGIC_STRING


    def update(self):
        print('GUI UPDATE')
        if self.vac_spike_status_old != self.gui_values[self.vac_spike_status]:
            self.set_status(self.vac_spike_status_outputwidget,self.vac_spike_status)
            self.vac_spike_status_old = self.gui_values[self.vac_spike_status]

        if self.DC_spike_status_old != self.gui_values[self.DC_spike_status]:
            self.set_status(self.DC_spike_status_outputwidget,self.DC_spike_status)
            self.DC_spike_status_old = self.gui_values[self.DC_spike_status]

        if self.rev_power_spike_status_old != self.gui_values[self.rev_power_spike_status]:
            self.set_status(self.rev_power_spike_status_outputwidget,self.rev_power_spike_status)
            self.rev_power_spike_status_old = self.gui_values[self.rev_power_spike_status]

        if self.vac_valve_status_old != self.gui_values[self.vac_valve_status]:
            self.set_valve(self.vac_valve_status_outputwidget,self.vac_valve_status)
            self.vac_valve_status_old = self.gui_values[self.vac_valve_status]

        if self.modulator_state_old != self.gui_values[self.modulator_state]:
            self.set_mod_state(self.mod_state_outputwidget,self.modulator_state)
            self.modulator_state_old = self.gui_values[self.modulator_state]

        if self.rfprot_state_old != self.gui_values[self.rfprot_state]:
            self.set_RF_prot(self.RF_protection_outputwidget,self.rfprot_state)
            self.rfprot_state_old = self.gui_values[self.rfprot_state]

        if self.llrf_enabled_old != self.gui_values[self.llrf_enabled]:
            self.set_locked_enabled(self.llrf_enable_outputwidget,self.llrf_enabled)
            self.llrf_enabled_old = self.gui_values[self.llrf_enabled]

        if self.llrf_locked_old != self.gui_values[self.llrf_locked]:
            self.set_locked_enabled(self.llrf_locked_outputwidget,self.llrf_locked)
            self.llrf_locked_old = self.gui_values[self.llrf_locked]

        self.vac_level_outputwidget.setText('%.3f' % self.gui_values[self.vac_level])

        self.cav_temp_outputwidget.setText('%.3f' % self.gui_values[self.cav_temp])


        self.water_temp_outputwidget.setText('%.3f' % self.gui_values[self.water_temp])

        self.pulse_length_outputwidget.setText('%.3f' % self.gui_values[self.pulse_length])

        self.fwd_cav_power_outputwidget.setText('%.6f' % self.gui_values[self.fwd_cav_power])
        self.rev_cav_power_outputwidget.setText('%.6f' % self.gui_values[self.rev_cav_power])
        self.fwd_kly_power_outputwidget.setText('%.6f' % self.gui_values[self.fwd_kly_power])
        self.rev_kly_power_outputwidget.setText('%.6f' % self.gui_values[self.rev_kly_power])

        #self.vac_spike_status_outputwidget.setText(str(self.gui_values[self.vac_spike_status]))
        #self.vac_spike_status_outputwidget.setText('ERRRRR')
        self.DC_spike_status_outputwidget
        self.rev_power_spike_status_outputwidget
        #self.RF_lost_status_outputwidget
        self.cav_temp_outputwidget
        self.water_temp_outputwidget
        self.pulse_length_outputwidget
        self.fwd_cav_power_outputwidget
        self.fwd_kly_power_outputwidget
        self.rev_kly_power_outputwidget
        self.rev_cav_power_outputwidget
        self.probe_power_outputwidget
        self.vac_level_outputwidget
        self.vac_valve_status_outputwidget
        self.breakdown_rate_limit_outputwidget
        self.measured_breakdown_rate_outputwidget
        self.breakdown_rate_statistics_outputwidget
        QApplication.processEvents()