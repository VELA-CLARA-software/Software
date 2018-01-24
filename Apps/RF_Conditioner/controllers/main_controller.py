# THE main_controller
# holds everything
from PyQt4.QtGui import QApplication
from controller_base import controller_base
from gui.gui_conditioning import gui_conditioning
import data.rf_condition_data_base as dat
import sys
import time
from VELA_CLARA_enums import STATE

class main_controller(controller_base):
	# whoami
	my_name = 'main_controller'
	#
	# other attributes will be initiliased in base-class
	old_sp = 0

	def __init__(self, argv, config_file):
		#super(controller_base,self).__init__()
		controller_base.__init__(self,argv, config_file)

		controller_base.data.llrf_type = self.llrf_type
		controller_base.data_monitor.llrf_type = self.llrf_type

		# more set-up after config read
		#self.data.llrf_param= self.llrf_param
		self.data.init_after_config_read()

		#
		# start monitoring data
		self.data_monitor.start_monitors()
		# build the gui and pass in the data
		#
		# build the gui and pass in the data
		self.gui = gui_conditioning()
		self.gui.closing.connect(self.connectCloseEvents)
		self.gui.show()
		self.gui.activateWindow()
		QApplication.processEvents()

		# more set-up after controller built
		controller_base.llrf_control.addPulseCountOffset(self.data.values[dat.log_active_pulse_count])


		print(self.my_name + ' setting pulse length to last previous log value = ' +\
			  str(controller_base.config.llrf_config['PULSE_LENGTH_START']))


		self.llrf_handler.set_pulse_length(self.data.values[dat.log_pulse_length] )
		QApplication.processEvents()

		# set dat llrf parm, so dat can work out the
		# amplitude increase step size
		print controller_base.config.llrf_config['RF_INCREASE_RATE']
		#controller_base.data.llrf_param = self.llrf_param
		controller_base.data.power_increase_set_up()
		QApplication.processEvents()

		# everything now runs from the main_loop
		#
		#self.llrf_handler.check_masks()
		self.monitor_states = self.data.main_monitor_states
		QApplication.processEvents()

		# start data recording
		#
		self.data.start_logging()
		QApplication.processEvents()

		self.main_loop()



	def main_loop(self):
		print(self.my_name + ' The RF Conditioning is Entering Main_Loop !')

		self.data_monitor.init_monitor_states()

		#self.llrf_control.setPulseCountOffset(410000)
		#self.llrf_control.setAmpHP(0)
		# remove time.sleep(10 at your peril
		time.sleep(1)
		self.mask_set = False

		self.llrf_control.trigExt()


		print(self.my_name + ' entering mainloop')

		# start the clock
		#self.start_time()

		values = controller_base.data.values

		self.llrf_control.setGlobalCheckMask(False)

		self.llrf_handler.set_amp(values[dat.next_sp_decrease])
		self.data.clear_last_sp_history()
		self.continue_ramp()

		controller_base.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
		controller_base.logger.header('ENTERING MAIN LOOP')
		i = 0
		self.llrf_control.setGlobalCheckMask(False)

		while 1:
			QApplication.processEvents()

			# update main monitor states

			self.data_monitor.update_states()
			#
			# # if new_bad drop SP
			if controller_base.data_monitor.new_bad():
				controller_base.llrf_control.setGlobalCheckMask(False)
				if controller_base.data_monitor.vac_new_bad():
					controller_base.logger.message('MAIN-LOOP New VAC BAD State dropping amp = 5', True)

				if controller_base.data_monitor.dc_new_bad():
					controller_base.logger.message('MAIN-LOOP New DC BAD State dropping amp = 6', True)

			elif controller_base.data_monitor.new_good_no_bad():

				if values[dat.breakdown_rate_hi]:
					self.ramp_down()
				else:
					self.continue_ramp()


			# if everything is good carry on increasing
			if controller_base.data_monitor.all_good():
				#print('all good')
							# set the masks
				if self.llrf_handler.mask_set == False:
					#print('main loop mask not set')
					self.llrf_handler.set_mask()
					# if GOOD set checking for breakdowns
				else:
					#print('main loop setting global check mask = TRUE')
					self.llrf_control.setGlobalCheckMask(True)
					# if there has been enough time since
					# the last increase get the new llrf sp
					# we use dto updat ebased on time elapsed
					#if self.seconds_elapsed(self.llrf_param['TIME_BETWEEN_RF_INCREASES']):
					# now we update base do npulses
					if values[dat.event_pulse_count] > values[dat.required_pulses]: # check this number in the look up
						if self.gui.can_ramp:
							if values[dat.breakdown_rate_hi]:
								if i > 0:
									self.logger.message('MAIN LOOP allgood, but breakdown rate too high ' + str(values[dat.breakdown_rate]))
									i = 1
							else:
								self.ramp_up()
								i = 0
						else:
							pass
							#self.logger.message('MAIN LOOP allgood, pulse count good gui in pause ramp mode')
					else:
						pass
						#self.logger.message('MAIN LOOP all good, but pulse count low, ' + str(values[dat.event_pulse_count]) +' \ '+ str(values[dat.required_pulses]))

			else:
				pass
				#print('not all good')

	def check_vac(self):
		print'check_vac'


	def continue_ramp(self):
		print('continue_ramp ' + str(self.data.amp_sp_history[-1]))
		# apply the old settings
		self.llrf_handler.set_amp(self.data.amp_sp_history[-1])
		self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
		self.llrf_control.resetAverageTraces()
		self.data.add_to_pulse_breakdown_log()


	def ramp_up(self):
		new_amp = self.data.get_new_set_point( self.data.values[dat.next_power_increase]  )
		if new_amp:
			self.llrf_handler.set_amp(new_amp)
			self.data.values[dat.next_sp_decrease] = dat.rf_condition_data_base.amp_sp_history[-2]
			self.data.ramp_up()
		else:
			self.llrf_handler.set_amp(self.llrf_control.getAmpSP() + controller_base.config.llrf_config['DEFAULT_RF_INCREASE_LEVEL'])
		self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
		#  YES, for now
		self.data.add_to_pulse_breakdown_log()
		self.llrf_control.resetAverageTraces()

	def ramp_down(self):
		self.llrf_handler.set_amp(self.data.amp_sp_history[-2])
		self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
		self.data.clear_last_sp_history()
		self.data.ramp_down()
		self.llrf_control.resetAverageTraces()
		self.data.add_to_pulse_breakdown_log()




	def apply_new_amp(self):
		sp = self.llrf_control.getAmpSP()
		#????
		if sp < 30:#???
			pass # sp ???????
		else:
			new_amp = self.data.get_new_sp()
			if new_amp:
				self.llrf_handler.set_amp(new_amp)
			else:
				self.llrf_handler.set_amp(sp + self.llrf_param['DEFAULT_RF_INCREASE_LEVEL'])
			# after increase SP the mask is out of date
			self.mask_set = False
		self.old_sp = sp





		# hi = self.llrfObj[0].trace_data['LRRG_CAVITY_REVERSE_POWER'].high_mask
		# lo = self.llrfObj[0].trace_data['LRRG_CAVITY_REVERSE_POWER'].low_mask
		# av = self.llrfObj[0].trace_data['LRRG_CAVITY_REVERSE_POWER'].rolling_average
		#
		# with open('test.txt', 'w') as f:
		# 	for i in range(0,len(hi)):
		# 		if hi[i] != hi[0]:
		# 			print i,hi[i],lo[i],av[i]
		# 			f.write(str(i) + ',' + str(hi[i]) + ',' + str(lo[i]) + ','+ str(av[i]) + ',\n' )
		#

	# the load and save dburt windows can't be closed until this function is called
	def connectCloseEvents(self):
		self.gui.close()
		self.data.close()
		print 'Fin - RF condtioning closing down, goodbye.'
		sys.exit()