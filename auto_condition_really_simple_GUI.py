#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS automtic gun conditioning PROTOTYPING SCRIPT, march 2017
import epics, time, math, numpy, sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
sys.path.append('C:\\anaconda32\\Work\\Software\\striptool')
import striptool as stripTool
import pyqtgraph as pg
# import VELA_CLARA_MagnetControl as vmag
import  VELA_CLARA_General_Monitor as vgen
sys.path.append('C:\\anaconda32\\Work\\Software\\loggerwidget')
import logging
import loggerWidget as lw
logger = logging.getLogger(__name__)

class gun_condition(QObject):

	def __init__(self, parent = None):
		super(gun_condition, self).__init__()
		self.last_10_img_values = []
		# where to write the log
		self.log_file = "llrf_amp_kly_fwd_pwr_log.txt"

		# tweakable parameters
		self.normal_RF_increase = 1;  # RF step increment
		self.increase_wait_time = 2; # Time between RF step increments (in seconds)
		self.vac_spike_RF_drop = 50;   # RF step drop if spike
		self.permit_RF_drop    = 1000; # RF step drop if RF permit lost
		self.rf_upper_limit    = 16800 # AW suggestion
		self.maximum_pulse_width = 3; # Absolute mas pulse length
		self.nominal_pulse_width = 2.5; # Pulse width we should be at if all is well
		self.increase_wait_time_pulse_width = 4; # Time between RF pulse_width step increments (in seconds)
		self.vac_spike_RF_pulse_width_drop = 0.005; #pulse width amount to drop when IMG spike
		self.vac_spike_RF_pulse_width_increase = 0.005; #pulse width amount to increase after IMG spike (NB MUST BE >= 0.005)
		self.time_of_last_increase = self.time_of_last_increase_pulse_width = time.time()

		# ramp_pause_time times (seconds)
		self.ramp_pause_time = {
		'IMG_1'       : 2*60,  	# vac_spike_cooldown_time
		'RF_PERMIT'   : 5*60	# permit_cooldown_time
		}

		# timer reset cooldown  times (seconds)
		self.event_timer_cooldown = {
		'IMG_1'       : 0.1,  	# vac_spike_cooldown_time
		'RF_PERMIT'   : 30  	# permit_cooldown_time
		}

		# the PVs to "continuously" monitor (for now via acquisition)
		self.pv_to_monitor = {
		'RF_PERMIT' 			: epics.PV('CLA-GUN-RF-PROTE-01:Cmi'),
		'RF_TRIG' 				: epics.PV('CLA-GUNS-HRF-MOD-01:Sys:ErrorRead.SVAL'),
		'LLRF_CAVITY_REV_POWER' : epics.PV('CLA-GUNS-LRF-CTRL-01:ad1:ch4:power_remote.POWER'),
		'RF_PULSE_LENGTH' 	    : epics.PV('CLA-GUNS-LRF-CTRL-01:vm:feed_fwd:duration'),
		'IMG_1'        			: epics.PV('CLA-LRG1-VAC-IMG-01:P'),
		'RF_AMPLITUDE'  		: epics.PV('CLA-GUNS-LRF-CTRL-01:vm:dsp:sp_amp:amplitude'),
		}

		# these are the PVs that we sometimes get / set
		self.pv_to_use = {
		'LLRF_KLY_FWD_PWR' : epics.PV('CLA-GUNS-LRF-CTRL-01:ad1:ch1:power_remote.POWER'),
		'LLRF_CAV_FWD_PWR' : epics.PV('CLA-GUNS-LRF-CTRL-01:ad1:ch3:power_remote.POWER')
		}

		# not happy about repeating the keys...
		# if the current state IS NOT the value in this table the alarm should sound
		# RF rev power and vacuum are more complex as the ylook at arrays and changes from base-level
		self.pv_monitor_not_alarm_values= {
		'RF_PERMIT': 65535,
		'RF_TRIG': 'D000',
		'LLRF_CAVITY_REV_POWER': 500e3,
		'IMG_1': 0.5E-9
		}

		# keep a record of when the last alarm was
		self.pv_time_of_last_alarm = {
		'IMG_1' 				: time.time() - self.ramp_pause_time['IMG_1'],
		'RF_PERMIT' 			: time.time() - self.ramp_pause_time['RF_PERMIT'],
		'LLRF_CAVITY_REV_POWER' : time.time()
		}

		self.llrf_check_width =  0.4
		self.llrf_end_offest    =  0.05
		self.llrf_pulse_offset = 0.48 # usec from start of llrf trace until RF ramps on
		self.last_pulse_length = 0

		# to spot a vacuum spike we have a history buffer
		self.pre_spike_img_mean = epics.PV('CLA-LRG1-VAC-IMG-01:P').get()
		for i in range(11):
			self.last_10_img_values.append(self.pre_spike_img_mean)

	# Some utility functions
	def appendMessageToLog(self, message, log_file):
		# print message
		with open(log_file,"a") as logfile:
			self.logfile.write(str(message)+ '\n')

	def getCurrentValues(self, pv_dictionary ):
		returndict = {}
		for name,pv in pv_dictionary.iteritems():
			#print name, '  ', pv.get()
			returndict[name] = pv.get()
		return returndict

	def currentTimeStr(self):
		return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

	# check if the time since the last alarm is greater than the cool-down time, if so return True
	def is_not_in_cool_down(self, signal ):
		if time.time() - self.pv_time_of_last_alarm[signal] > self.event_timer_cooldown[signal]:
			return True
		else:
			return False

	# check if the time since the last alarm is greater than the cool-down time, if so return True
	def is_not_in_pause_ramp(self, signal ):
		if time.time() - self.pv_time_of_last_alarm[signal] > self.ramp_pause_time[signal]:
			return True
		else:
			return False

	def check_RF_permit_is_good(self, rf_permit_signal, rf_trig_signal, rf_amp_signal ):
		rf_dropped = False
		rf_permit_lost = False
		rf_trig_lost = False
		if (self.latest_values[ rf_permit_signal ] != self.pv_monitor_not_alarm_values[ rf_permit_signal ]):
			rf_dropped = True
			rf_permit_lost = True
		elif (self.latest_values[ rf_trig_signal ] != self.pv_monitor_not_alarm_values[ rf_trig_signal ]):
			rf_dropped = True
			rf_trig_lost = True
		if rf_dropped:
			if self.is_not_in_cool_down( rf_permit_signal ):
				self.pv_time_of_last_alarm[ rf_permit_signal ] =  time.time()
				if rf_permit_lost:
					logger.critical('RF Permit Lost, Dropping RF amplitude by ' + str(self.permit_RF_drop) + ' and pausing RF Amplitude Ramp for ' \
					+ str( self.ramp_pause_time[ rf_permit_signal ] ) + ' seconds')
					self.change_RF_amp(  self.latest_values[ rf_amp_signal ] -  self.permit_RF_drop )
			elif rf_trig_lost:
				self.pv_time_of_last_alarm[ rf_permit_signal ] =  time.time()
				logger.critical('RF Trig Lost - Please manually re-enable TRIG')

	def check_IMG_change_is_small(self, img_signal, rf_amp_signal, rf_pulse_width_signal):
		if len(self.last_10_img_values) > 10:
			self.last_10_img_values.pop(0)
		delta_IMG = self.latest_values[ img_signal ] - self.pre_spike_img_mean
		if delta_IMG > self.pv_monitor_not_alarm_values[ img_signal ]:
			logger.debug('delta_IMG = '+str(delta_IMG)+'  pre_spike_img_mean = '+str(self.pre_spike_img_mean))
			if self.is_not_in_cool_down( img_signal ):
				self.pv_time_of_last_alarm[ img_signal ] =  time.time()
				logger.warning('Vac Spike, Dropping RF pulse width to ' + str(self.latest_values[ rf_pulse_width_signal ] - self.vac_spike_RF_pulse_width_drop) + ' and pausing RF Ramp for ' \
				+ str( self.ramp_pause_time[ img_signal ] ) + ' seconds')
				# Changing RF Pulse Width
				self.change_RF_pulse_width(rf_pulse_width_signal, self.latest_values[ rf_pulse_width_signal ] - self.vac_spike_RF_pulse_width_drop)
				#last_10_img_values = [] # reset IMG values after spike
		else:
			#print 'new IMG mean'
			self.last_10_img_values.append( self.latest_values[ img_signal ] )
			self.pre_spike_img_mean = numpy.mean( self.last_10_img_values )

	def can_increase_rf(self):
		if not self.latest_values['RF_PULSE_LENGTH'] < self.nominal_pulse_width:
			if time.time() - self.pv_time_of_last_alarm[ 'IMG_1' ] > self.ramp_pause_time['IMG_1']:
				if time.time() - self.pv_time_of_last_alarm[ 'RF_PERMIT' ] > self.ramp_pause_time[ 'RF_PERMIT' ]:
					if time.time() - self.time_of_last_increase > self.increase_wait_time:
						return True
		return False

	def can_increase_rf_pulse_width(self):
		if time.time() - self.pv_time_of_last_alarm[ 'IMG_1' ] > self.ramp_pause_time['IMG_1']:
			if time.time() - self.pv_time_of_last_alarm[ 'RF_PERMIT' ] > self.ramp_pause_time[ 'RF_PERMIT' ]:
				if time.time() - self.time_of_last_increase_pulse_width > self.increase_wait_time_pulse_width:
					return True
		return False

	def change_RF_amp(self, anyrf_amp_signal, value ):
		# self.pv_to_monitor[ self.rf_amp_signal ].put( value )
		logger.info('increasing RF to '+str(value))

	def change_RF_pulse_width(self, rf_pulse_width_signal, value):
		if value > self.maximum_pulse_width:
			logger.critical('TRYING TO SET GREATER THAN MAX PULSE WIDTH - EXITING!')
			sys.exit()
		elif value > self.nominal_pulse_width:
			# self.pv_to_monitor[ self.rf_pulse_width_signal ].put( self.nominal_pulse_width )
			logger.error('setting nominal pulse width')
		elif value < 1.5:
			# self.pv_to_monitor[ self.rf_pulse_width_signal ].put( 1.5 )
			logger.error('setting minimum pulse width')
		else:
			logger.info('changing pulse width to: '+str(value))
			# self.pv_to_monitor[ self.rf_pulse_width_signal ].put( value )

	def log(self, lrf_index_start, llrf_index_stop, log_file):
		kly_power_data = pv_to_use[ 'LLRF_KLY_FWD_PWR' ].get()
		cav_power_data = pv_to_use[ 'LLRF_CAV_FWD_PWR' ].get()
		kly_power_cut   = self.kly_power_data[self.llrf_index_start:self.llrf_index_stop]
		cav_power_data = self.cav_power_data[self.llrf_index_start:self.llrf_index_stop]
		kly_power = numpy.mean( kly_power_cut )
		cav_power = numpy.mean( cav_power_data )
		message =  currentTimeStr() +  ' RF to ' + str( self.pv_to_monitor['RF_AMPLITUDE'].get( ) )	+ ' kly_fwd_power =  ' + str(kly_power) + ' cav_fwd_power =  ' + str(cav_power)
		appendMessageToLog( message, log_file)
		logger.info(message)

	# return the index (number of points) less than t form the LLRF time
	def get_LLRF_power_trace_index_at_time_t(self, t ):
		# the LLRF times
		self.llrf_time_pv = epics.PV('CLA-GUNS-LRF-CTRL-01:app:time_vector')
		return next( x[0] for x in enumerate( self.llrf_time_pv.get() ) if x[1] > t)

	def main_loop(self):

		self.latest_values = self.getCurrentValues( self.pv_to_monitor )

		if self.latest_values['RF_AMPLITUDE'] > self.rf_upper_limit:  #Upper RF limit
			self.change_RF_amp( 'RF_AMPLITUDE',  13000  ) # this is the value we re-start from when we raise the pulse length
			self.nominal_pulse_width = self.nominal_pulse_width + 0.1
			if self.nominal_pulse_width > self.maximum_pulse_width:
				sys.exit()

		if self.latest_values['RF_PULSE_LENGTH'] != self.last_pulse_length:
			self.llrf_time_stop   = self.llrf_pulse_offset + self.latest_values['RF_PULSE_LENGTH'] - self.llrf_end_offest
			self.llrf_time_start  = self.llrf_pulse_offset + self.latest_values['RF_PULSE_LENGTH'] - self.llrf_end_offest - self.llrf_check_width
			self.llrf_index_start = self.get_LLRF_power_trace_index_at_time_t( self.llrf_time_start )
			self.llrf_index_stop  = self.get_LLRF_power_trace_index_at_time_t( self.llrf_time_stop  )
			#print 'new RF pulse-length = ' + str( latest_values['RF_PULSE_LENGTH'] ) + ' micro-seconds'
			#print 'new LLRF trace start index ' + str( llrf_index_start ) + ' = ' + str(llrf_time_start) + ' micro-seconds'
			#print 'new LLRF trace stop  index ' + str( llrf_index_stop )  + ' = ' + str(llrf_time_stop)  + ' micro-seconds'

		self.check_RF_permit_is_good( 'RF_PERMIT', 'RF_TRIG', 'RF_AMPLITUDE' )


		self.check_IMG_change_is_small( 'IMG_1', 'RF_AMPLITUDE', 'RF_PULSE_LENGTH')

		if self.can_increase_rf_pulse_width() and self.latest_values['RF_PULSE_LENGTH'] < self.nominal_pulse_width:
				logger.info('can increase RF pulse width')
				logger.info('Increasing RF pulse width to: '+ str(self.latest_values[ 'RF_PULSE_LENGTH' ] + self.vac_spike_RF_pulse_width_increase))
				increase = self.latest_values[ 'RF_PULSE_LENGTH' ] + self.vac_spike_RF_pulse_width_increase
				self.change_RF_pulse_width('RF_PULSE_LENGTH', increase)
				self.time_of_last_increase_pulse_width = time.time()
				logger.info('No Events for ' + str( time.time() - self.time_of_last_increase ) + '  RF Amp = ' + str( increase ))
				log( self.llrf_index_start, self.llrf_index_stop, log_file)
		elif self.can_increase_rf():
			logger.info('can increase RF amplitude')
			increase = self.latest_values['RF_AMPLITUDE'] + self.normal_RF_increase
			self.change_RF_amp( 'RF_AMPLITUDE',  increase  )
			self.time_of_last_increase = time.time()
			logger.info('No Events for ' + str( time.time() - self.time_of_last_increase ) + '  RF Amp = ' + str( increase ))
			log( self.llrf_index_start, self.llrf_index_stop, log_file)
		# else:
			# print 'cannot increase RF '

		self.last_pulse_length = self.latest_values['RF_PULSE_LENGTH']

class gun_condition_edit_widget(QObject):

	def __init__(self, param, label, gc, parent=None):
		super(gun_condition_edit_widget, self).__init__(parent)
		self.param = param
		self.label = label
		self.gc = gc
		self.labelWidget = QLabel(label[0])
		self.editWidget = QLineEdit(str(getattr(self.gc,param)))
		self.editWidget.setMaximumWidth(100)
		self.editWidget.setToolTip(label[1])
		# self.editWidget.editingFinished.connect(self.parameterChange)

	def widgets(self):
		return self.labelWidget, self.editWidget

	def applySetting(self):
		val = self.editWidget.text()
		# print 'before = ', getattr(self.gc, self.param)
		setattr(self.gc, self.param, val)
		# print 'after = ', getattr(self.gc, self.param)

class gun_condition_window(QMainWindow):

	applySettingsSignal = pyqtSignal()

	def __init__(self, parent = None):
		super(gun_condition_window, self).__init__()
		self.gc = gun_condition()
		timer = QTimer()
		timer.timeout.connect(self.gc.main_loop)
		# timer.start(100)
		self.centralWidget = QWidget()
		self.setCentralWidget(self.centralWidget)
		self.centralLayout = QHBoxLayout()
		self.centralWidget.setLayout(self.centralLayout)

		self.centralSplitter = QSplitter()
		self.centralLayout.addWidget(self.centralSplitter)

		self.gunlogTab = QTabWidget()
		self.centralSplitter.addWidget(self.gunlogTab)

		self.logwidget = lw.loggerWidget(logger)
		# self.logwidget.setMinimumWidth(500)
		self.gunParametersWidget = QWidget()
		self.gunlogTab.addTab(self.logwidget,'Log')
		self.gunlogTab.addTab(self.gunParametersWidget,'RF Params')

		self.gunParametersWidgetLayout = QGridLayout()
		self.gunParametersWidget.setLayout(self.gunParametersWidgetLayout)

		self.gunParameters = {'nominal_pulse_width': ['Pulse Width Start','Starting RF pulse width'],
		'vac_spike_RF_pulse_width_drop': ['Pulse Width Drop','Step reduction in RF pulse width on vacuum spike'],
		'vac_spike_RF_pulse_width_increase': ['Pulse Width Raise','Step increase in RF pulse width after vacuum spike'],
		'increase_wait_time_pulse_width': ['Pulse width Wait','Time to wait between RF pulse width increments'],
		'normal_RF_increase': ['Power Step','Step increase in RF power'],
		'increase_wait_time': ['Power Wait','Time to wait between RF power increments'],
		'permit_RF_drop': ['Power Drop on Trip','Step reduction in RF power after RF trip'],
		}

		self.plotParameters = {'CLA-GUNS-LRF-CTRL-01:vm:dsp:ff_amp:amplitude':{'pen':'r', 'name':'KLY FWD PWR', 'freq': 10.0, 'logscale': True},
		}

		row = 0
		for param, label in self.gunParameters.iteritems():
			gunwidget = gun_condition_edit_widget(param, label, self.gc, self)
			self.applySettingsSignal.connect(gunwidget.applySetting)
			l, e = gunwidget.widgets()
			self.gunParametersWidgetLayout.addWidget(gunwidget.labelWidget,row,0)
			self.gunParametersWidgetLayout.addWidget(gunwidget.editWidget,row,1)
			row += 1
		self.applyButton = QPushButton('Apply')
		self.applyButton.clicked.connect(self.applySettings)
		self.gunParametersWidgetLayout.addWidget(self.applyButton,row,1)

		self.general = vgen.init()
		self.pvids = []

		self.sp = stripTool.stripPlot(plotRateBar=False,crosshairs=True)
		self.sp.start()
		self.sp.pausePlotting(False)
		self.sp.setPlotScale(60)
		self.centralSplitter.addWidget(self.sp)
		for pv, pvparams in self.plotParameters.iteritems():
			self.generalPVFunction(pv,pvparams)

	def generalPVFunction(self, pvname, pvproperties):
		# global general
		pv = epics.PV(pvname)
		logger.debug('pv = '+str(pv))
		self.pvids.append(pv)
		testFunction = lambda: pv.get()
		logger.debug('pv value = '+str(testFunction()))
		self.sp.addSignal(name=pvproperties['name'],pen=pvproperties['pen'], function=testFunction, timer=1.0/pvproperties['freq'], logscale=pvproperties['logscale'])

	def applySettings(self):
		self.applySettingsSignal.emit()

def main():
	app = QApplication(sys.argv)
	pg.setConfigOptions(antialias=True)
	pg.setConfigOption('background', 'w')
	pg.setConfigOption('foreground', 'k')
	# app.setStyle(QStyleFactory.create("plastique"))
	gc = gun_condition_window()
	gc.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
   main()
