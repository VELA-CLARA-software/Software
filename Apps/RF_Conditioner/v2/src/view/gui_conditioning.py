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
from VELA_CLARA_RF_Modulator_Control import L01_MOD_STATE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from VELA_CLARA_RF_Protection_Control import RF_GUN_PROT_STATUS
#from VELA_CLARA_enums import STATE
from VELA_CLARA_LLRF_Control import LLRF_TYPE
import src.data.rf_condition_data_base as dat
import src.data.rf_conditioning_data as rf_conditioning_data
from src.data.state import state
# ok - so gui should get a object ref
# and then update as appropriate!
# every time
# other data  should be monitored in the dat aclass?write_binary()
from src.base.base import base
import numpy as np
import pyqtgraph as pg

from PyQt4.QtGui import QPixmap
from PyQt4.QtCore import QObject
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QIcon
import sys


# redirecting std.out, works but slows the gui responsiveness, so needs more investigating
class EmittingStream(QObject):
    textWritten = pyqtSignal(str)
    def write(self, text):
        self.textWritten.emit(str(text))

class gui_conditioning(QMainWindow, Ui_MainWindow, base):
	my_name = 'gui_conditioning'
	# clipboard
	clip_app = QApplication([])
	clip = clip_app.clipboard()
	# global state
	can_ramp = True
	can_rf_output = False
	# constant colors for GUI update
	good = open = rf_on = 'green'
	bad = error = closed = off = rf_off = interlock = 'red'
	unknown = 'magenta'
	major_error = 'cyan'
	timing = 'yellow'
	init = 'orange'
	standby = 'purple'

	# custom close signal to send to controller
	closing = pyqtSignal()


	#

	def __init__(self,
				 window_name="",
				 root="/"
				 ):
		QMainWindow.__init__(self)
		super(base, self).__init__()
		self.setupUi(self)

		self.setWindowIcon(QIcon('resources\\rf_conditioning\\rficon_2NK_3.ico'))

		self.pixmap = QPixmap('resources\\rf_conditioning\\fine.png')
		self.label.setScaledContents(True)
		#self.label.setPixmap(self.pixmap.scaled(self.label.size()))
		self.label.setPixmap(self.pixmap)
		#sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
		self.data = base.data
		# CONNECT BUTTONS TO FUNCTIONS
		self.start_pause_ramp_button.clicked.connect(self.handle_start_pause_ramp_button)
		self.llrf_enable_button.clicked.connect(self.handle_llrf_enable_button)
		self.copy_to_clipboard_button.clicked.connect(self.handle_copy_to_clipboard_button)
		self.llrf_enable_button.clicked.connect(self.handle_can_rf_output)
		# error bars when plotting
		self.err = None
		self.handle_can_rf_output()

		# reference to the values dictionary
		self.data = rf_conditioning_data.rf_conditioning_data()
		self.values = self.data.values
		self.expert_values = self.data.expert_values

		#

		#
		self.update_via_controller = {}
		self.widget = {}
		self.previous_values = {}
		[self.previous_values.update({x: None}) for x in self.data.all_value_keys]
		[self.update_via_controller.update({x: False}) for x in self.data.all_value_keys]



	def gui_start_up(self):
		self.set_plot_error_bars()

		# base.data.values  = base.data.values
		# widgets are held in dict, with same keys as data
		self.init_widget_dict()
		# experts widgets are held in a similar, but different dictionary
		self.set_up_expert_widgets()

		# the clipboard has a string version of data
		self.clip_vals = base.data.values.copy()
		# init to paused
		# self.handle_pause_ramp_button()
		self.handle_start_pause_ramp_button()
		# update timer
		self.timer = QTimer()
		self.timer.setSingleShot(False)
		self.timer.timeout.connect(self.update_gui)
		self.timer.start(base.config.gui_config['GUI_UPDATE_TIME'])

	def __del__(self):
		pass
		# Restore sys.stdout
		#sys.stdout = sys.__stdout__

	def normalOutputWritten(self, text):
		"""Append text to the QTextEdit."""
		# Maybe QTextEdit.append() works as well, but this is how I do it:
		cursor = self.textEdit.textCursor()
		cursor.movePosition(QTextCursor.End)
		cursor.insertText(text)
		self.textEdit.setTextCursor(cursor)
		self.textEdit.ensureCursorVisible()

	def set_plot_error_bars(self):
		self.plot_item = self.graphicsView.getPlotItem()
		x = np.arange(10)
		y = np.arange(10) % 3
		top = np.linspace(1.0, 3.0, 10)
		bottom = np.linspace(2, 0.5, 10)
		self.plot_item.setWindowTitle('Amp SP vs KFPow')
		#self.err = pg.ErrorBarItem()
		self.err = pg.ErrorBarItem(x=x, y=y, top=top, bottom=bottom, beam=0.5)
		self.plot_item.addItem(self.err)
		#self.plot_item.plot(x, y, symbol='o', pen={'color': 0.8, 'width': 2})

	def update_plot(self):
		data = base.data.amp_vs_kfpow_running_stat
		x =  data.keys()
		x.sort()
		y = []
		# this SHOULD be err = np.sqrt([data[i][2] / (data[i][0] -1 ) for i in x])
		# but we ignore the minus 1 incase we get a div by zero
		ans = []
		for i in x:
			if data[i][0] == 0:
				ans.append( data[i][2] )
			else:
				ans.append(data[i][2] / (data[i][0]))
		err = np.sqrt( ans )
		#data =
		for item in x:
			y.append( data[item][1] )

		self.err.setData(x = np.array(x),
						 y = np.array(y),
						 top= err,
						 bottom=err,
						 beam=0.5)
		# do we need to clear ???
		self.plot_item.clear()
		self.plot_item.addItem(self.err)
		self.plot_item.plot(x, y, symbol='+', pen={'color': 0.8, 'width': 1})
		# add in straight line fits ...
		self.plot_item.plot( [base.data.values[dat.x_min], base.data.values[dat.x_max] ],
		                     [base.data.values[dat.y_min], base.data.values[dat.y_max]],
		                     pen={'color': 'r', 'width': 2})

		self.plot_item.plot( [base.data.values[dat.old_x_min], base.data.values[dat.old_x_max] ],
		                     [base.data.values[dat.old_y_min], base.data.values[dat.old_y_max]],
		                     pen={'color': 'y', 'width': 2})

	# custom close function
	def closeEvent(self, event):
		self.closing.emit()

	# button functions
	def handle_start_pause_ramp_button(self):
		print("handle_start_pause_ramp_button")
		if self.can_ramp:
			self.can_ramp = False
			# print self.my_name + ' is pausing RF conditioning'
			self.start_pause_ramp_button.setText("ENABLE RAMPING")
			self.start_pause_ramp_button.setStyleSheet(
				'QPushButton { background-color : ' + self.bad + '; color : black; }')
			base.logger.message(self.my_name + ' has disabled ramping RF', True)
		else:
			self.can_ramp = True
			self.start_pause_ramp_button.setText("DISABLE RAMPING")
			self.start_pause_ramp_button.setStyleSheet(
				'QPushButton { background-color : ' + self.good + '; color : black; }')
			base.logger.message(self.my_name + ' has enabled ramping RF', True)

	def handle_can_rf_output(self):
		if self.can_rf_output:
			self.can_rf_output = False
			print("can_rf_output = false")
			self.llrf_enable_button.setText("ENABLE RF OUTPUT")
			self.llrf_enable_button.setStyleSheet('QPushButton { background-color : ' + self.bad + '; color : black; }')
		else:
			self.can_rf_output = True
			print("can_rf_output = True")
			self.llrf_enable_button.setText("DISABLE RF OUTPUT")
			self.llrf_enable_button.setStyleSheet('QPushButton { background-color : ' + self.good + '; color : black; }')


	def handle_llrf_enable_button(self):
		print 'handle_llrf_enable_button'

	def handle_copy_to_clipboard_button(self):
		string = ''
		for key, value in self.clip_vals.iteritems():
			string += key + ' : ' + str(value) + '\n'  # shit python
		self.clip.setText(QString(string))

	# main update gui function, loop over all widgets, and if values is new update gui with new value
	def update_gui(self):
		for key, val in self.widget.iteritems():
			if self.value_is_new(key, self.values[key]):
				self.update_widget(key, self.values[key], val)

	# the outputwidget is update based on data type
	def update_widget(self, key, val, widget):
		# print(type(val),key,widget.objectName())
		# meh
		if key == self.data.breakdown_rate_hi:
			self.set_widget_color(widget, not val)

		elif key == self.data.vac_decay_level:
			self.set_widget_color(widget, val)


		elif key == self.data.pulse_length_status:
			self.set_widget_color(widget, val)
		elif key == self.data.llrf_interlock_status:
			self.set_widget_color_text( widget, val)
		elif key == self.data.llrf_trigger_status:
			self.set_widget_color_text( widget, val)

		elif key == self.data.vac_spike_status:
			self.set_widget_color_text( widget, val)
		elif key == self.data.DC_spike_status:
			self.set_widget_color_text( widget, val)

		elif key == self.data.llrf_DAQ_rep_rate_status:
			self.set_widget_color(widget, val)


		elif key == self.data.llrf_output_status:
			self.set_widget_color_text(widget, val)
		elif widget == self.event_pulse_count_outputwidget:
			widget.setText(('%i' % val) + ('/%i' % base.data.values[self.data.required_pulses]))
			self.clip_vals[key] = widget.text()
		elif type(val) is long:
			widget.setText('%i' % val)
			self.clip_vals[key] = widget.text()
		elif type(val) is int:
			#print(key,' is a int')
			widget.setText('%i' % val)
			self.clip_vals[key] = widget.text()
		elif type(val) is float:
			widget.setText('%.3E' % val)
			self.clip_vals[key] = widget.text()
		elif type(val) is RF_GUN_PROT_STATUS:
			self.set_RF_prot(widget, val)
		elif type(val) is GUN_MOD_STATE:
			self.set_gun_mod_state(widget, val, key)
		elif type(val) is L01_MOD_STATE:
			self.set_L01_mod_state(widget, val, key)
		elif type(val) is VALVE_STATE:
			self.set_valve(widget, val)
		elif type(val) is bool:
			self.set_widget_color_text(widget, val)
		elif type(val) is np.float64:
			widget.setText('%.3E' % val)
			self.clip_vals[key] = widget.text()
		elif type(val) is str:
			widget.setText('%i' % -1)
		else:
			print 'update_widget error ' + str(val) + ' ' + str(type(val))




	def update_rf_output_button(self,widget, val):
		self.set_widget_color_text(widget,val)
		if val:
			self.llrf_enable_button.setText("DISABLE RF OUTPUT")
			self.llrf_enable_button.setStyleSheet(
			'QPushButton { background-color : ' + self.good + '; color : black; }')
		else:
			self.llrf_enable_button.setText("ENABLE RF OUTPUT")
			self.llrf_enable_button.setStyleSheet(
				'QPushButton { background-color : ' + self.bad + '; color : black; }')



	# if a value is new we update the widget
	def value_is_new(self, key, val):
		if self.previous_values[key] != val:
			self.previous_values[key] = val
			return True
		else:
			return False

	def set_break_down_color(self, widget, val):
		if val:
			widget.setStyleSheet('QLabel { background-color : ' + self.bad + '; color : black; }')
		else:
			widget.setStyleSheet('QLabel { background-color : ' + self.good + '; color : black; }')

	# functions to update colors in widgets
	# def set_status(self, widget, val, status):
	# 	if val == state.UNKNOWN:
	# 		self.set_widget_color_text(widget, 'UNKNOWN', self.unknown, status)
	# 	elif val == state.GOOD:
	# 		self.set_widget_color_text(widget, 'GOOD', self.good, status)
	# 	elif val == state.BAD:
	# 		self.set_widget_color_text(widget, 'BAD', self.bad, status)
	# 	elif val == state.INIT:
	# 		self.set_widget_color_text(widget, 'INIT', self.init, status)
	# 	else:
	# 		self.set_widget_color_text(widget, 'MAJOR_ERROR', self.major_error, status)

	def set_widget_color_text(self, widget, val):
		self.set_widget_color(widget, val)
		self.set_widget_text(widget, val)  # MAGIC_STRING
		#self.clip_vals[status] = str(widget.text())


	def set_widget_text(self, widget, val):
		if val == state.GOOD:
			widget.setText('GOOD')
		elif val == state.BAD:
			widget.setText('BAD')
		elif val == state.INIT:
			widget.setText('INIT')
		elif val == state.UNKNOWN:
			widget.setText('UNKNOWN')
		elif val == True:
			widget.setText('GOOD')
		elif val == False:
			widget.setText('BAD')
		elif val == state.TIMING:
			widget.setText('TIMING')
		elif val == state.STANDBY:
			widget.setText('STANDBY')
		else:
			widget.setText('UNKNOWN')


	def set_widget_color(self, widget, val):
		if val == state.GOOD:
			widget.setStyleSheet('QLabel { background-color : ' + self.good + '; color : black; }')
		elif val == state.BAD:
			widget.setStyleSheet('QLabel { background-color : ' + self.bad + '; color : black; }')
		elif val == state.INIT:
			widget.setStyleSheet('QLabel { background-color : ' + self.init + '; color : black; }')
		elif val == state.UNKNOWN:
			widget.setStyleSheet('QLabel { background-color : ' + self.unknown + '; color : black; }')
		elif val == state.INTERLOCK:
			widget.setStyleSheet('QLabel { background-color : ' + self.interlock + '; color : black; }')
		elif val == True:
			widget.setStyleSheet('QLabel { background-color : ' + self.good + '; color : black; }')
		elif val == False:
			widget.setStyleSheet('QLabel { background-color : ' + self.bad + '; color : black; }')
		elif val == state.TIMING:
			widget.setStyleSheet('QLabel { background-color : ' + self.timing + '; color : black; }')
		elif val == state.STANDBY:
			widget.setStyleSheet('QLabel { background-color : ' + self.standby + '; color : black; }')
		else:
			widget.setStyleSheet('QLabel { background-color : ' + self.unknown + '; color : black; }')


	def set_locked_enabled(self, widget, val):
		self.set_widget_color_text(widget, val)


	def set_valve(self, widget, val):
		if val == VALVE_STATE.VALVE_OPEN:
			self.set_widget_color(widget, state.GOOD)
			widget.setText('OPEN')
		elif val == VALVE_STATE.VALVE_CLOSED:
			self.set_widget_color(widget, state.BAD)
			widget.setText('CLOSED')
		elif val == VALVE_STATE.VALVE_TIMING:
			self.set_widget_color_text(widget, state.TIMING)
			widget.setText('TIMING')
		elif val == VALVE_STATE.VALVE_ERROR:
			self.set_widget_color_text(widget, state.ERROR)
		else:
			self.set_widget_color_text(widget, state.ERROR)

	def set_RF_prot(self, widget, val):
		if val == RF_GUN_PROT_STATUS.GOOD:
			self.set_widget_color_text(widget, state.GOOD)
		elif val == RF_GUN_PROT_STATUS.BAD:
			self.set_widget_color_text(widget, state.BAD)
		elif val == RF_GUN_PROT_STATUS.ERROR:
			self.set_widget_color_text(widget, state.ERROR)
		elif val == RF_GUN_PROT_STATUS.UNKNOWN:
			self.set_widget_color_text(widget, state.UNKNOWN)
		else:
			self.set_widget_color_text(widget, state.ERROR)

	# these enums will need updating, especially as we introduce more RF structures ...
	def set_gun_mod_state(self, widget, val, status):
		'''Replace all this cancer with a dictionary '''
		if val == GUN_MOD_STATE.RF_ON:
			self.set_widget_color(widget, state.GOOD )
			widget.setText('RF_ON')
		elif val == GUN_MOD_STATE.UNKNOWN_STATE:
			self.set_widget_color(widget,state.UNKNOWN)
			widget.setText('RF_ON')
		elif val == GUN_MOD_STATE.OFF:
			self.set_widget_color(widget, state.BAD)
			widget.setText('OFF')
		elif val == GUN_MOD_STATE.OFF_REQUEST:
			self.set_widget_color(widget, state.TIMING)
			widget.setText('OFF_REQUEST')
		elif val == GUN_MOD_STATE.HV_INTERLOCK:
			self.set_widget_color(widget, state.INTERLOCK)
			widget.setText('HV_INTERLOCK')
		elif val == GUN_MOD_STATE.HV_OFF_REQUEST:
			self.set_widget_color(widget, state.TIMING)
			widget.setText('HV_OFF_REQUEST')
		elif val == GUN_MOD_STATE.HV_REQUEST:
			self.set_widget_color(widget, state.TIMING)
			widget.setText('HV_REQUEST')
		elif val == GUN_MOD_STATE.HV_ON:
			self.set_widget_color(widget, state.INIT)
			widget.setText('HV_ON')
		elif val == GUN_MOD_STATE.STANDBY_REQUEST:
			self.set_widget_color(widget, state.TIMING)
			widget.setText('STANDBY_REQUEST')
		elif val == GUN_MOD_STATE.STANDBY:
			self.set_widget_color(widget, state.STANDBY)
			widget.setText('STANDBY')
		elif val == GUN_MOD_STATE.STANDYBY_INTERLOCK:
			self.set_widget_color(widget, state.INTERLOCK)
			widget.setText('STANDYBY_INTERLOCK')
		elif val == GUN_MOD_STATE.RF_ON_REQUEST:
			self.set_widget_color(widget, state.TIMING)
			widget.setText('RF_ON_REQUEST')
		elif val == GUN_MOD_STATE.RF_OFF_REQUEST:
			self.set_widget_color(widget, state.TIMING)
			widget.setText('RF_OFF_REQUEST')
		elif val == GUN_MOD_STATE.RF_ON_INTERLOCK:
			self.set_widget_color(widget, state.INTERLOCK)
			widget.setText('RF_ON_INTERLOCK')
		else:
			self.set_widget_color_text(widget, state.ERROR)
			widget.setText('ERROR')
		self.clip_vals[status] = str(widget.text())


	def set_L01_mod_state(self, widget, val, status):
		if val == L01_MOD_STATE.STATE_UNKNOWN:
			self.set_widget_color_text(widget, 'STATE_UNKNOWN', gui_conditioning.error, status)
		elif val == L01_MOD_STATE.L01_OFF:
			self.set_widget_color_text(widget, 'L01_OFF', gui_conditioning.rf_off, status)
		elif val == L01_MOD_STATE.L01_STANDBY:
			self.set_widget_color_text(widget, 'L01_STANDBY', gui_conditioning.rf_off, status)
		elif val == L01_MOD_STATE.STATE_UNKNOWN:
			self.set_widget_color_text(widget, 'STATE_UNKNOWN', gui_conditioning.error, status)
		elif val == L01_MOD_STATE.L01_HV_ON:
			self.set_widget_color_text(widget, 'L01_HV_ON', gui_conditioning.rf_off, status)
		elif val == L01_MOD_STATE.L01_RF_ON:
			self.set_widget_color_text(widget, 'L01_RF_ON', gui_conditioning.rf_on, status)
		self.clip_vals[status] = str(widget.text())





	def init_widget_dict(self):
		# MANUALLY CONNECT THESE UP :/
		self.widget[self.data.probe_pwr] = self.probe_power_outputwidget
		self.widget[self.data.vac_level] = self.vac_level_outputwidget
		self.widget[self.data.cav_temp] = self.cav_temp_outputwidget
		self.widget[self.data.water_temp] = self.water_temp_outputwidget
		self.widget[self.data.pulse_length] = self.pulse_length_outputwidget
		self.widget[self.data.fwd_cav_pwr] = self.fwd_cav_power_outputwidget
		self.widget[self.data.rev_cav_pwr] = self.rev_cav_power_outputwidget
		self.widget[self.data.fwd_kly_pwr] = self.fwd_kly_power_outputwidget
		self.widget[self.data.rev_kly_pwr] = self.rev_kly_power_outputwidget
		self.widget[self.data.elapsed_time] = self.elapsed_time_outputwidget
		self.widget[self.data.breakdown_rate] = self.measured_breakdown_rate_outputwidget
		self.widget[self.data.breakdown_count] = self.breakdown_count_outputwidget
		self.widget[self.data.pulse_count] = self.pulse_count_outputwidget
		#self.widget[self.data.rev_power_spike_count] = self.rev_power_spike_status_outputwidget
		self.widget[self.data.amp_sp] = self.amp_set_outputwidget
		self.widget[self.data.DC_level] = self.dc_level_outputwidget
		self.widget[self.data.event_pulse_count] = self.event_pulse_count_outputwidget
		#self.widget[self.data.pulse_length_aim] = self.pulse_length_aim_outputwidget
		#self.widget[self.data.power_aim] = self.power_aim_outputwidget
		self.widget[self.data.breakdown_rate_aim] = self.breakdown_rate_limit_outputwidget
		self.widget[self.data.breakdown_rate_hi] = self.measured_breakdown_rate_outputwidget
		self.widget[self.data.last_106_bd_count] = self.last_106_count_outputwidget
		self.widget[self.data.last_mean_power] = self.last_setpoint_power_outputwidget
		self.widget[self.data.next_power_increase] = self.next_power_increase_outputwidget
		self.widget[self.data.next_sp_decrease] = self.next_sp_decrease_outputwidget
		self.widget[self.data.current_ramp_index] = self.current_index_outputwidget
		self.widget[self.data.sol_value] = self.sol_outputwidget
		self.widget[self.data.duplicate_pulse_count] = self.duplicate_count_outputwidget
		# states
		self.widget[self.data.modulator_state] = self.mod_state_outputwidget
		self.widget[self.data.rfprot_state] = self.RF_protection_outputwidget
		# states
		self.widget[self.data.llrf_interlock_status] = self.llrf_interlock_outputwidget
		self.widget[self.data.llrf_trigger_status] = self.llrf_trigger_outputwidget
		# pulse length is a state AND a number

		self.widget[self.data.pulse_length] = self.pulse_length_outputwidget
		self.widget[self.data.pulse_length_status] = self.pulse_length_outputwidget

		self.widget[self.data.llrf_interlock_status] = self.llrf_interlock_outputwidget


		self.widget[self.data.llrf_output_status] = self.llrf_output_outputwidget

		self.widget[self.data.llrf_ff_amp_locked] = self.llrf_ff_amp_locked_outputwidget
		self.widget[self.data.llrf_ff_ph_locked] = self.llrf_ff_ph_locked_outputwidget
		self.widget[self.data.DC_spike_status] = self.DC_spike_status_outputwidget
		self.widget[self.data.vac_spike_status] = self.vac_spike_status_outputwidget
		self.widget[self.data.vac_valve_status] = self.vac_valve_status_outputwidget
		self.widget[self.data.llrf_DAQ_rep_rate] = self.trace_rep_rate_outpuwidget
		self.widget[self.data.llrf_DAQ_rep_rate_status] = self.trace_rep_rate_outpuwidget

		self.widget[self.data.vac_val_limit_status] = self.vac_level_outputwidget


	def plot_amp_sp_pwr(self):
		#base.data.x_plot, base.data.y_plot, base.data.m, base.data.c, base.data.x_min, base.data.x_max,
		#		  [base.data.predicted_sp, base.data.requested_power]
		self.power_vs_pulses_plotwidget.cleasr()
		self.power_vs_pulses_plotwidget.plot( np.array(base.data.old_x_min, base.data.old_x_max),
						base.data.old_m *np.array([base.data.old_x_min,base.data.old_xmax]) + base.data.old_c,'-')

		self.power_vs_pulses_plotwidget.plot(base.data.x_plot, base.data.y_plot, '.')
		self.power_vs_pulses_plotwidget.plot(base.data.x_plot, (base.data.m * base.data.y_plot) + base.data.c, '-')

		self.power_vs_pulses_plotwidget.plot(base.data.predicted_sp, base.data.requested_power, '*')

		self.power_vs_pulses_plotwidget.show()
		base.data.old_xmin = base.data.x_min
		base.data.old_xmax = base.data.x_max
		base.data.old_m = base.data.m
		base.data.old_c = base.data.c


	def update_expert_widget(self, key, val, widget):

		if key is self.data.is_breakdown_monitor_kf_pow:
			self.set_widget_color_text( widget, val)
		elif key is self.data.is_breakdown_monitor_kr_pow:
			self.set_widget_color_text( widget, val)
		elif key is self.data.is_breakdown_monitor_cf_pow:
			self.set_widget_color_text( widget, val)
		elif key is self.data.is_breakdown_monitor_cr_pow:
			self.set_widget_color_text( widget, val)
		elif key is self.data.is_breakdown_monitor_cp_pow:
			self.set_widget_color_text( widget, val)
		elif key is self.data.is_breakdown_monitor_kf_pha:
			self.set_widget_color_text( widget, val)
		elif key is self.data.is_breakdown_monitor_cf_pha:
			self.set_widget_color_text( widget, val)
		elif key is self.data.is_breakdown_monitor_cr_pha:
			self.set_widget_color_text( widget, val)
		elif key is self.data.is_breakdown_monitor_cp_pha:
			self.set_widget_color_text( widget, val)
		else:
			pass



	def update_expert_values(self):
		"""
		update the exper_values panels
		:return: none
		"""
		# loop over each widghet in
		for key, value in self.expert_widget.iteritems():
			self.update_expert_widget(key, self.expert_values[key], value )


	def set_up_expert_widgets(self):
		# The value IS THE SAME as the key for the expert_values data dictionary, by doing this
		# we can link the two together
		self.expert_widget[self.data.vac_pv_val] = self.vac_pv_val
		self.expert_widget[self.data.vac_decay_mode_val] = self.vac_decay_mode_val
		self.expert_widget[self.data.vac_decay_level] = self.vac_decay_level
		self.expert_widget[self.data.vac_decay_time_val] = self.vac_decay_time_val
		self.expert_widget[self.data.vac_drop_amp] = self.vac_drop_amp
		self.expert_widget[self.data.vac_hi_pressure] = self.vac_hi_pressure
		self.expert_widget[self.data.vac_spike_delta_val] = self.vac_spike_delta_val
		self.expert_widget[self.data.vac_num_samples_to_average_val] = \
			self.vac_num_samples_to_average_val
		self.expert_widget[self.data.vac_drop_amp_val] = self.vac_drop_amp_val
		self.expert_widget[self.data.ramp_when_hi] = self.ramp_when_hi
		self.expert_widget[self.data.vac_decay_mode] = self.vac_decay_mode
		self.expert_widget[self.data.vac_decay_level_val] = self.vac_decay_level_val
		self.expert_widget[self.data.vac_hi_pressure_val] = self.vac_hi_pressure_val
		self.expert_widget[self.data.ramp_when_hi_val] = self.ramp_when_hi_val
		self.expert_widget[self.data.vac_spike_check_time_val] = self.vac_spike_check_time_val
		self.expert_widget[self.data.vac_spike_check_time] = self.vac_spike_check_time
		self.expert_widget[self.data.is_breakdown_monitor_kf_pow] = self.is_breakdown_monitor_kf_pow
		self.expert_widget[self.data.is_breakdown_monitor_kr_pow] = self.is_breakdown_monitor_kr_pow
		self.expert_widget[self.data.is_breakdown_monitor_cf_pow] = self.is_breakdown_monitor_cf_pow
		self.expert_widget[self.data.is_breakdown_monitor_cf_pow] = self.is_breakdown_monitor_cf_pow
		self.expert_widget[self.data.is_breakdown_monitor_cp_pow] = self.is_breakdown_monitor_cp_pow
		self.expert_widget[self.data.is_breakdown_monitor_kf_pha] = self.is_breakdown_monitor_kf_pha
		self.expert_widget[self.data.is_breakdown_monitor_kr_pha] = self.is_breakdown_monitor_kr_pha
		self.expert_widget[self.data.is_breakdown_monitor_cf_pha] = self.is_breakdown_monitor_cf_pha
		self.expert_widget[self.data.is_breakdown_monitor_cr_pha] = self.is_breakdown_monitor_cr_pha
		self.expert_widget[self.data.is_breakdown_monitor_cp_pha] = self.is_breakdown_monitor_cp_pha
		self.expert_widget[self.data.mean_start_kf_pow] = self.mean_start_kf_pow
		self.expert_widget[self.data.mean_start_kr_pow] = self.mean_start_kr_pow
		self.expert_widget[self.data.mean_start_cf_pow] = self.mean_start_cf_pow
		self.expert_widget[self.data.mean_start_cf_pow] = self.mean_start_cf_pow
		self.expert_widget[self.data.mean_start_cp_pow] = self.mean_start_cp_pow
		self.expert_widget[self.data.mean_start_kf_pha] = self.mean_start_kf_pha
		self.expert_widget[self.data.mean_start_kr_pha] = self.mean_start_kr_pha
		self.expert_widget[self.data.mean_start_cf_pha] = self.mean_start_cf_pha
		self.expert_widget[self.data.mean_start_cr_pha] = self.mean_start_cr_pha
		self.expert_widget[self.data.mean_start_cp_pha] = self.mean_start_cp_pha
		self.expert_widget[self.data.mean_end_kf_pow] = self.mean_end_kf_pow
		self.expert_widget[self.data.mean_end_kr_pow] = self.mean_end_kr_pow
		self.expert_widget[self.data.mean_end_cf_pow] = self.mean_end_cf_pow
		self.expert_widget[self.data.mean_end_cf_pow] = self.mean_end_cf_pow
		self.expert_widget[self.data.mean_end_cp_pow] = self.mean_end_cp_pow
		self.expert_widget[self.data.mean_end_kf_pha] = self.mean_end_kf_pha
		self.expert_widget[self.data.mean_end_kr_pha] = self.mean_end_kr_pha
		self.expert_widget[self.data.mean_end_cf_pha] = self.mean_end_cf_pha
		self.expert_widget[self.data.mean_end_cr_pha] = self.mean_end_cr_pha
		self.expert_widget[self.data.mean_end_cp_pha] = self.mean_end_cp_pha
		self.expert_widget[self.data.mask_unit_kf_pow] = self.mask_unit_kf_pow
		self.expert_widget[self.data.mask_unit_kr_pow] = self.mask_unit_kr_pow
		self.expert_widget[self.data.mask_unit_cf_pow] = self.mask_unit_cf_pow
		self.expert_widget[self.data.mask_unit_cf_pow] = self.mask_unit_cf_pow
		self.expert_widget[self.data.mask_unit_cp_pow] = self.mask_unit_cp_pow
		self.expert_widget[self.data.mask_unit_kf_pha] = self.mask_unit_kf_pha
		self.expert_widget[self.data.mask_unit_kr_pha] = self.mask_unit_kr_pha
		self.expert_widget[self.data.mask_unit_cf_pha] = self.mask_unit_cf_pha
		self.expert_widget[self.data.mask_unit_cr_pha] = self.mask_unit_cr_pha
		self.expert_widget[self.data.mask_unit_cp_pha] = self.mask_unit_cp_pha
		self.expert_widget[self.data.mask_start_kf_pow] = self.mask_start_kf_pow
		self.expert_widget[self.data.mask_start_kr_pow] = self.mask_start_kr_pow
		self.expert_widget[self.data.mask_start_cf_pow] = self.mask_start_cf_pow
		self.expert_widget[self.data.mask_start_cf_pow] = self.mask_start_cf_pow
		self.expert_widget[self.data.mask_start_cp_pow] = self.mask_start_cp_pow
		self.expert_widget[self.data.mask_start_kf_pha] = self.mask_start_kf_pha
		self.expert_widget[self.data.mask_start_kr_pha] = self.mask_start_kr_pha
		self.expert_widget[self.data.mask_start_cf_pha] = self.mask_start_cf_pha
		self.expert_widget[self.data.mask_start_cr_pha] = self.mask_start_cr_pha
		self.expert_widget[self.data.mask_start_cp_pha] = self.mask_start_cp_pha
		self.expert_widget[self.data.mask_end_kf_pow] = self.mask_end_kf_pow
		self.expert_widget[self.data.mask_end_kr_pow] = self.mask_end_kr_pow
		self.expert_widget[self.data.mask_end_cf_pow] = self.mask_end_cf_pow
		self.expert_widget[self.data.mask_end_cf_pow] = self.mask_end_cf_pow
		self.expert_widget[self.data.mask_end_cp_pow] = self.mask_end_cp_pow
		self.expert_widget[self.data.mask_end_kr_pha] = self.mask_end_kr_pha
		self.expert_widget[self.data.mask_end_kf_pha] = self.mask_end_kf_pha
		self.expert_widget[self.data.mask_end_cf_pha] = self.mask_end_cf_pha
		self.expert_widget[self.data.mask_end_cr_pha] = self.mask_end_cr_pha
		self.expert_widget[self.data.mask_end_cp_pha] = self.mask_end_cp_pha
		self.expert_widget[self.data.mask_window_start_kf_pow] = self.mask_window_start_kf_pow
		self.expert_widget[self.data.mask_window_start_kr_pow] = self.mask_window_start_kr_pow
		self.expert_widget[self.data.mask_window_start_cf_pow] = self.mask_window_start_cf_pow
		self.expert_widget[self.data.mask_window_start_cf_pow] = self.mask_window_start_cf_pow
		self.expert_widget[self.data.mask_window_start_cp_pow] = self.mask_window_start_cp_pow
		self.expert_widget[self.data.mask_window_start_kf_pha] = self.mask_window_start_kf_pha
		self.expert_widget[self.data.mask_window_start_kr_pha] = self.mask_window_start_kr_pha
		self.expert_widget[self.data.mask_window_start_cf_pha] = self.mask_window_start_cf_pha
		self.expert_widget[self.data.mask_window_start_cr_pha] = self.mask_window_start_cr_pha
		self.expert_widget[self.data.mask_window_start_cp_pha] = self.mask_window_start_cp_pha
		self.expert_widget[self.data.mask_window_end_kf_pow] = self.mask_window_end_kf_pow
		self.expert_widget[self.data.mask_window_end_kr_pow] = self.mask_window_end_kr_pow
		self.expert_widget[self.data.mask_window_end_cf_pow] = self.mask_window_end_cf_pow
		self.expert_widget[self.data.mask_window_end_cf_pow] = self.mask_window_end_cf_pow
		self.expert_widget[self.data.mask_window_end_cp_pow] = self.mask_window_end_cp_pow
		self.expert_widget[self.data.mask_window_end_kf_pha] = self.mask_window_end_kf_pha
		self.expert_widget[self.data.mask_window_end_kr_pha] = self.mask_window_end_kr_pha
		self.expert_widget[self.data.mask_window_end_cf_pha] = self.mask_window_end_cf_pha
		self.expert_widget[self.data.mask_window_end_cr_pha] = self.mask_window_end_cr_pha
		self.expert_widget[self.data.mask_window_end_cp_pha] = self.mask_window_end_cp_pha
		self.expert_widget[self.data.mask_min_kf_pow] = self.mask_min_kf_pow
		self.expert_widget[self.data.mask_min_kr_pow] = self.mask_min_kr_pow
		self.expert_widget[self.data.mask_min_cf_pow] = self.mask_min_cf_pow
		self.expert_widget[self.data.mask_min_cf_pow] = self.mask_min_cf_pow
		self.expert_widget[self.data.mask_min_cp_pow] = self.mask_min_cp_pow
		self.expert_widget[self.data.mask_min_kf_pha] = self.mask_min_kf_pha
		self.expert_widget[self.data.mask_min_kr_pha] = self.mask_min_kr_pha
		self.expert_widget[self.data.mask_min_cf_pha] = self.mask_min_cf_pha
		self.expert_widget[self.data.mask_min_cr_pha] = self.mask_min_cr_pha
		self.expert_widget[self.data.mask_min_cp_pha] = self.mask_min_cp_pha
		self.expert_widget[self.data.num_averages_kf_pow] = self.num_averages_kf_pow
		self.expert_widget[self.data.num_averages_kr_pow] = self.num_averages_kr_pow
		self.expert_widget[self.data.num_averages_cf_pow] = self.num_averages_cf_pow
		self.expert_widget[self.data.num_averages_cf_pow] = self.num_averages_cf_pow
		self.expert_widget[self.data.num_averages_cp_pow] = self.num_averages_cp_pow
		self.expert_widget[self.data.num_averages_kf_pha] = self.num_averages_kf_pha
		self.expert_widget[self.data.num_averages_kr_pha] = self.num_averages_kr_pha
		self.expert_widget[self.data.num_averages_cf_pha] = self.num_averages_cf_pha
		self.expert_widget[self.data.num_averages_cr_pha] = self.num_averages_cr_pha
		self.expert_widget[self.data.num_averages_cp_pha] = self.num_averages_cp_pha
		self.expert_widget[self.data.mask_auto_set_kf_pow] = self.mask_auto_set_kf_pow
		self.expert_widget[self.data.mask_auto_set_kr_pow] = self.mask_auto_set_kr_pow
		self.expert_widget[self.data.mask_auto_set_cf_pow] = self.mask_auto_set_cf_pow
		self.expert_widget[self.data.mask_auto_set_cf_pow] = self.mask_auto_set_cf_pow
		self.expert_widget[self.data.mask_auto_set_cp_pow] = self.mask_auto_set_cp_pow
		self.expert_widget[self.data.mask_auto_set_kf_pha] = self.mask_auto_set_kf_pha
		self.expert_widget[self.data.mask_auto_set_kr_pha] = self.mask_auto_set_kr_pha
		self.expert_widget[self.data.mask_auto_set_cf_pha] = self.mask_auto_set_cf_pha
		self.expert_widget[self.data.mask_auto_set_cr_pha] = self.mask_auto_set_cr_pha
		self.expert_widget[self.data.mask_auto_set_cp_pha] = self.mask_auto_set_cp_pha
		self.expert_widget[self.data.mask_type_kf_pow] = self.mask_type_kf_pow
		self.expert_widget[self.data.mask_type_kr_pow] = self.mask_type_kr_pow
		self.expert_widget[self.data.mask_type_cf_pow] = self.mask_type_cf_pow
		self.expert_widget[self.data.mask_type_cf_pow] = self.mask_type_cf_pow
		self.expert_widget[self.data.mask_type_cp_pow] = self.mask_type_cp_pow
		self.expert_widget[self.data.mask_type_kf_pha] = self.mask_type_kf_pha
		self.expert_widget[self.data.mask_type_kr_pha] = self.mask_type_kr_pha
		self.expert_widget[self.data.mask_type_cf_pha] = self.mask_type_cf_pha
		self.expert_widget[self.data.mask_type_cr_pha] = self.mask_type_cr_pha
		self.expert_widget[self.data.mask_type_cp_pha] = self.mask_type_cp_pha
		self.expert_widget[self.data.mask_level_kf_pow] = self.mask_level_kf_pow
		self.expert_widget[self.data.mask_level_kr_pow] = self.mask_level_kr_pow
		self.expert_widget[self.data.mask_level_cf_pow] = self.mask_level_cf_pow
		self.expert_widget[self.data.mask_level_cf_pow] = self.mask_level_cf_pow
		self.expert_widget[self.data.mask_level_cp_pow] = self.mask_level_cp_pow
		self.expert_widget[self.data.mask_level_kf_pha] = self.mask_level_kf_pha
		self.expert_widget[self.data.mask_level_kr_pha] = self.mask_level_kr_pha
		self.expert_widget[self.data.mask_level_cf_pha] = self.mask_level_cf_pha
		self.expert_widget[self.data.mask_level_cr_pha] = self.mask_level_cr_pha
		self.expert_widget[self.data.mask_level_cp_pha] = self.mask_level_cp_pha
		self.expert_widget[self.data.mask_end_by_power_kf_pow] = self.mask_end_by_power_kf_pow
		self.expert_widget[self.data.mask_end_by_power_kr_pow] = self.mask_end_by_power_kr_pow
		self.expert_widget[self.data.mask_end_by_power_cf_pow] = self.mask_end_by_power_cf_pow
		self.expert_widget[self.data.mask_end_by_power_cf_pow] = self.mask_end_by_power_cf_pow
		self.expert_widget[self.data.mask_end_by_power_cp_pow] = self.mask_end_by_power_cp_pow
		self.expert_widget[self.data.mask_end_by_power_kf_pha] = self.mask_end_by_power_kf_pha
		self.expert_widget[self.data.mask_end_by_power_kr_pha] = self.mask_end_by_power_kr_pha
		self.expert_widget[self.data.mask_end_by_power_cf_pha] = self.mask_end_by_power_cf_pha
		self.expert_widget[self.data.mask_end_by_power_cr_pha] = self.mask_end_by_power_cr_pha
		self.expert_widget[self.data.mask_end_by_power_cp_pha] = self.mask_end_by_power_cp_pha
		self.expert_widget[self.data.mask_end_power_kf_pow] = self.mask_end_power_kf_pow
		self.expert_widget[self.data.mask_end_power_kr_pow] = self.mask_end_power_kr_pow
		self.expert_widget[self.data.mask_end_power_cf_pow] = self.mask_end_power_cf_pow
		self.expert_widget[self.data.mask_end_power_cf_pow] = self.mask_end_power_cf_pow
		self.expert_widget[self.data.mask_end_power_cp_pow] = self.mask_end_power_cp_pow
		self.expert_widget[self.data.mask_end_power_kf_pha] = self.mask_end_power_kf_pha
		self.expert_widget[self.data.mask_end_power_kr_pha] = self.mask_end_power_kr_pha
		self.expert_widget[self.data.mask_end_power_cf_pha] = self.mask_end_power_cf_pha
		self.expert_widget[self.data.mask_end_power_cr_pha] = self.mask_end_power_cr_pha
		self.expert_widget[self.data.mask_end_power_cp_pha] = self.mask_end_power_cp_pha
		self.expert_widget[self.data.saved_on_breakdown_event_kf_pow] = \
			self.saved_on_breakdown_event_kf_pow
		self.expert_widget[self.data.saved_on_breakdown_event_kr_pow] = \
			self.saved_on_breakdown_event_kr_pow
		self.expert_widget[self.data.saved_on_breakdown_event_cf_pow] = \
			self.saved_on_breakdown_event_cf_pow
		self.expert_widget[self.data.saved_on_breakdown_event_cf_pow] = \
			self.saved_on_breakdown_event_cf_pow
		self.expert_widget[self.data.saved_on_breakdown_event_cp_pow] = \
			self.saved_on_breakdown_event_cp_pow
		self.expert_widget[self.data.saved_on_breakdown_event_kf_pha] = \
			self.saved_on_breakdown_event_kf_pha
		self.expert_widget[self.data.saved_on_breakdown_event_kr_pha] = \
			self.saved_on_breakdown_event_kr_pha
		self.expert_widget[self.data.saved_on_breakdown_event_cf_pha] = \
			self.saved_on_breakdown_event_cf_pha
		self.expert_widget[self.data.saved_on_breakdown_event_cr_pha] = \
			self.saved_on_breakdown_event_cr_pha
		self.expert_widget[self.data.saved_on_breakdown_event_cp_pha] = \
			self.saved_on_breakdown_event_cp_pha
		self.expert_widget[self.data.saved_on_vac_spike_kf_pow] = self.saved_on_vac_spike_kf_pow
		self.expert_widget[self.data.saved_on_vac_spike_kr_pow] = self.saved_on_vac_spike_kr_pow
		self.expert_widget[self.data.saved_on_vac_spike_cf_pow] = self.saved_on_vac_spike_cf_pow
		self.expert_widget[self.data.saved_on_vac_spike_cf_pow] = self.saved_on_vac_spike_cf_pow
		self.expert_widget[self.data.saved_on_vac_spike_cp_pow] = self.saved_on_vac_spike_cp_pow
		self.expert_widget[self.data.saved_on_vac_spike_kf_pha] = self.saved_on_vac_spike_kf_pha
		self.expert_widget[self.data.saved_on_vac_spike_kr_pha] = self.saved_on_vac_spike_kr_pha
		self.expert_widget[self.data.saved_on_vac_spike_cf_pha] = self.saved_on_vac_spike_cf_pha
		self.expert_widget[self.data.saved_on_vac_spike_cr_pha] = self.saved_on_vac_spike_cr_pha
		self.expert_widget[self.data.saved_on_vac_spike_cp_pha] = self.saved_on_vac_spike_cp_pha
		self.expert_widget[self.data.drop_amplitude_kf_pow] = self.drop_amplitude_kf_pow
		self.expert_widget[self.data.drop_amplitude_kr_pow] = self.drop_amplitude_kr_pow
		self.expert_widget[self.data.drop_amplitude_cf_pow] = self.drop_amplitude_cf_pow
		self.expert_widget[self.data.drop_amplitude_cf_pow] = self.drop_amplitude_cf_pow
		self.expert_widget[self.data.drop_amplitude_cp_pow] = self.drop_amplitude_cp_pow
		self.expert_widget[self.data.drop_amplitude_kf_pha] = self.drop_amplitude_kf_pha
		self.expert_widget[self.data.drop_amplitude_kr_pha] = self.drop_amplitude_kr_pha
		self.expert_widget[self.data.drop_amplitude_cf_pha] = self.drop_amplitude_cf_pha
		self.expert_widget[self.data.drop_amplitude_cr_pha] = self.drop_amplitude_cr_pha
		self.expert_widget[self.data.drop_amplitude_cp_pha] = self.drop_amplitude_cp_pha
		self.expert_widget[self.data.streak_kf_pow] = self.streak_kf_pow
		self.expert_widget[self.data.streak_kr_pow] = self.streak_kr_pow
		self.expert_widget[self.data.streak_cf_pow] = self.streak_cf_pow
		self.expert_widget[self.data.streak_cf_pow] = self.streak_cf_pow
		self.expert_widget[self.data.streak_cp_pow] = self.streak_cp_pow
		self.expert_widget[self.data.streak_kf_pha] = self.streak_kf_pha
		self.expert_widget[self.data.streak_kr_pha] = self.streak_kr_pha
		self.expert_widget[self.data.streak_cf_pha] = self.streak_cf_pha
		self.expert_widget[self.data.streak_cr_pha] = self.streak_cr_pha
		self.expert_widget[self.data.streak_cp_pha] = self.streak_cp_pha
		self.expert_widget[self.data.breakdown_rate_aim] = self.breakdown_rate_aim
		self.expert_widget[self.data.breakdown_rate_aim_val] = self.breakdown_rate_aim_val
		self.expert_widget[self.data.expected_daq_rep_rate] = self.expected_daq_rep_rate
		self.expert_widget[self.data.expected_daq_rep_rate_val] = self.expected_daq_rep_rate_val
		self.expert_widget[self.data.daq_rep_rate_error] = self.daq_rep_rate_error
		self.expert_widget[self.data.daq_rep_rate_error_val] = self.daq_rep_rate_error_val
		self.expert_widget[self.data.number_of_pulses_in_history] = self.number_of_pulses_in_history
		self.expert_widget[self.data.number_of_pulses_in_history_val] = \
			self.number_of_pulses_in_history_val
		self.expert_widget[self.data.trace_buffer_size] = self.trace_buffer_size
		self.expert_widget[self.data.trace_buffer_size_val] = self.trace_buffer_size_val
		self.expert_widget[self.data.default_pulse_count] = self.default_pulse_count
		self.expert_widget[self.data.default_pulse_count_val] = self.default_pulse_count_val
		self.expert_widget[self.data.default_amp_increase] = self.default_amp_increase
		self.expert_widget[self.data.default_amp_increase_val] = self.default_amp_increase_val
		self.expert_widget[self.data.max_amp_increase] = self.max_amp_increase
		self.expert_widget[self.data.max_amp_increase_val] = self.max_amp_increase_val
		self.expert_widget[self.data.num_fit_points] = self.num_fit_points
		self.expert_widget[self.data.num_fit_points_val] = self.num_fit_points_val
		self.expert_widget[self.data.active_power] = self.active_power
		self.expert_widget[self.data.active_power_val] = self.active_power_val
		self.expert_widget[self.data.num_future_traces] = self.num_future_traces
		self.expert_widget[self.data.num_future_traces_val] = self.num_future_traces_val
		self.expert_widget[self.data.keep_valve_open] = self.keep_valve_open
		self.expert_widget[self.data.keep_valve_open_val] = self.keep_valve_open_val



