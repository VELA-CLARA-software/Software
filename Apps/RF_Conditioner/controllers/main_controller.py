# THE main_controller
# holds everything
from PyQt4.QtGui import QApplication
from controller_base import controller_base
from gui.gui_conditioning import gui_conditioning
import data.rf_condition_data_base as dat
import sys
import time
from timeit import default_timer as timer


class main_controller(controller_base):
	# whoami
	my_name = 'main_controller'
	#
	# other attributes will be initiliased in base-class

	def __init__(self, argv, config_file):
		controller_base.__init__(self,argv, config_file)
		#
		# set base class llrf_types
		controller_base.data.llrf_type = self.llrf_type
		controller_base.data_monitor.llrf_type = self.llrf_type
		#
		# more set-up after config read
		self.data.init_after_config_read()
		#
		# start monitoring data
		self.data_monitor.start_monitors()
		# build the gui and pass in the data
		#
		# build the gui
		self.gui = gui_conditioning()
		QApplication.processEvents()
		self.gui.closing.connect(self.connectCloseEvents)
		QApplication.processEvents()
		self.gui.show()
		self.gui.activateWindow()
		QApplication.processEvents()

		# more set-up after controller built
		controller_base.llrf_control.addPulseCountOffset(self.data.values[dat.log_active_pulse_count])


		print(self.my_name + ' setting pulse length to last previous log value = ' +\
			  str(controller_base.config.llrf_config['PULSE_LENGTH_START']))


		controller_base.llrf_handler.set_pulse_length(self.data.values[dat.log_pulse_length] )
		QApplication.processEvents()

		#controller_base.data.power_increase_set_up()
		QApplication.processEvents()
		#
		#controller_base.llrf_handler.check_masks()
		self.monitor_states = self.data.main_monitor_states
		QApplication.processEvents()
		#
		# start data recording
		self.data.start_logging()
		QApplication.processEvents()
		#
		# everything now runs from the main_loop
		self.main_loop()



	def main_loop(self):
		self.logger.header(self.my_name + ' The RF Conditioning is Preparing to Entering Main_Loop !',True)

		#
		i = 0
		self.llrf_control.setGlobalCheckMask(False)


		# this sets up main monitors, based on what was successfully connected
		# they are,vac, dc, breakdown, rf_on?
		self.data_monitor.init_monitor_states()
		#
		# remove time.sleep(1) at your peril
		time.sleep(1)
		#
		# self.llrf_control.setGlobalCheckMask(False)
		#
		# set the 2nd last amplitude from log file, and delete last entry
		#controller_base.llrf_handler.set_amp( controller_base.data.values[dat.next_sp_decrease])
		self.data.clear_last_sp_history()
		# continue the ramp
		self.continue_ramp()

		controller_base.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()

		controller_base.logger.header('ENTERING MAIN LOOP')

		self.set_epoch()

		while 1:
			#start = timer()
			# ...
			# reset trigger
			controller_base.llrf_handler.enable_trigger()

			QApplication.processEvents()

			# update main monitor states

			controller_base.data_monitor.update_states()
			#
			# # if new_bad drop SP
			if controller_base.data_monitor.new_bad():
				controller_base.llrf_handler.mask_set = False
				# disable checking masks,(precautionary)
				controller_base.llrf_handler.set_global_check_mask(False)
				# check if spike was vac or DC
				controller_base.data_monitor.check_if_new_bad_is_vac_or_DC()

			elif controller_base.data_monitor.new_good_no_bad():

				if controller_base.data.values[dat.breakdown_rate_hi]:
					self.ramp_down()
				else:
					self.continue_ramp()
				if controller_base.llrf_handler.mask_set == False:
					controller_base.llrf_handler.set_mask()
					self.set_epoch()
				controller_base.llrf_handler.set_global_check_mask(True)

			# if everything is good carry on increasing
			elif controller_base.data_monitor.all_good():
				#print('all good')
							# set the masks
				#else:
				if self.seconds_passed(5):#magic number, rest masks every now and then if lal good?
					controller_base.llrf_handler.set_mask()
					self.set_epoch()

				#print('main loop setting global check mask = TRUE')
				#self.llrf_control.setGlobalCheckMask(True)
				# controller_base.llrf_handler.set_global_check_mask(True)
				# if there has been enough time since
				# the last increase get the new llrf sp
				# we use dto updat ebased on time elapsed
				#if self.seconds_elapsed(self.llrf_param['TIME_BETWEEN_RF_INCREASES']):
				# now we update base do npulses
				if controller_base.data.reached_min_pulse_count_for_this_step(): # check this number in the look up
					controller_base.llrf_handler.set_global_check_mask(True)
					if self.gui.can_ramp:
						if controller_base.data.values[dat.breakdown_rate_hi]:
							if i > 0:
								self.logger.message('MAIN LOOP allgood, but breakdown rate too high ' + str(controller_base.data.values[dat.breakdown_rate]))
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
			# end = timer()
			# print(end - start)


	def continue_ramp(self):
		self.logger.message('continue_ramp ' + str(controller_base.data.amp_sp_history[-1]))
		# apply the old settings
		controller_base.llrf_handler.set_amp(controller_base.data.amp_sp_history[-1])
		controller_base.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
		self.data.add_to_pulse_breakdown_log(controller_base.llrfObj[0].amp_sp)
		self.llrf_control.resetAverageTraces()


	def ramp_up(self):
		self.data.add_to_pulse_breakdown_log(controller_base.llrfObj[0].amp_sp)
		new_amp = controller_base.data.get_new_set_point( controller_base.data.values[dat.next_power_increase]  )
		if new_amp:
			controller_base.llrf_handler.set_amp(new_amp)
			controller_base.data.values[dat.next_sp_decrease] = dat.rf_condition_data_base.amp_sp_history[-2]
			controller_base.data.ramp_up()
		else:
			controller_base.llrf_handler.set_amp(self.llrf_control.getAmpSP() + controller_base.config.llrf_config['DEFAULT_RF_INCREASE_LEVEL'])
		self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
		#  YES, for now
		self.llrf_control.resetAverageTraces()

	def ramp_down(self):
		if len(self.data.amp_sp_history) > 1:
				controller_base.llrf_handler.set_amp(self.data.amp_sp_history[-2])
		else:
			controller_base.llrf_handler.set_amp(self.data.amp_sp_history[0])
		self.data.add_to_pulse_breakdown_log(controller_base.llrfObj[0].amp_sp)
		self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
		self.data.clear_last_sp_history()
		self.data.ramp_down()
		self.llrf_control.resetAverageTraces()


	# over load close
	def connectCloseEvents(self):
		self.gui.close()
		self.data.close()
		print 'Fin - RF condtioning closing down, goodbye.'
		sys.exit()

	def set_epoch(self):
		self.epoch = time.time()

	def seconds_passed(self,secs):
		return time.time() - self.epoch >= secs