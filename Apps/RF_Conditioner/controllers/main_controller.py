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
	mask_set = False
	old_sp = 0

	def __init__(self, argv, config_file):
		controller_base.__init__(self, argv, config_file)
		self.data.llrf_type = self.llrf_type
		self.data_monitor.llrf_type = self.llrf_type

		# more set-up after config read
		self.data.llrf_param= self.llrf_param
		self.data.init_after_config_read()

		#
		# start monitoring data
		self.data_monitor.start_monitors(
		                   prot_control=self.prot_control,
		                   rfprot_param=self.rfprot_param,
		                   valve_control=self.valve_control,
		                   vac_valve_param=self.vac_valve_param,
		                   mod_control=self.mod_control,
		                   mod_param=self.mod_param,
		                   cavity_temp_param=self.cavity_temp_param,
		                   water_temp_param=self.water_temp_param,
		                   vac_param=self.vac_param,
		                   llrf_control=self.llrf_control,
		                   llrf_param=self.llrf_param,
						   breakdown_param=self.breakdown_param,
						   log_param=self.log_param,
						   DC_param=self.DC_param,
						   logger = self.logger
						)
		# build the gui and pass in the data
		#
		# build the gui and pass in the data
		self.gui = gui_conditioning(
				data=self.data,
				update_time=self.gui_param['GUI_UPDATE_TIME']#MAGIC_STRING
			)
		self.gui.closing.connect(self.connectCloseEvents)
		self.gui.show()
		self.gui.activateWindow()

		# more set-up after controller built
		self.llrf_control.addPulseCountOffset(self.data.values[dat.log_active_pulse_count])
		print(self.my_name + ' setting pulse length to last previous log value = ' + str(self.llrf_param['PULSE_LENGTH_START']))
		self.llrf_handler.set_pulse_length( self.llrf_param['PULSE_LENGTH_START'] )
		# set dat llrf parm, so dat can work out the
		# amplitude increase step size
		print self.llrf_param['RF_INCREASE_RATE']
		self.data.llrf_param = self.llrf_param
		self.data.power_increase_set_up()
		# everything now runs from the main_loop
		#
		#self.llrf_handler.check_masks()
		self.monitor_states = self.data.main_monitor_states
		# start data recording
		#
		self.data.start_logging(self.log_param)

		self.main_loop()



	def main_loop(self):
		print(self.my_name + ' The RF Conditioning is Entering Main_Loop !')

		self.data_monitor.init_monitor_states()

		#self.llrf_control.setPulseCountOffset(410000)
		self.llrf_control.setAmpSP(500)
		# remove time.sleep(10 at your peril
		time.sleep(1)
		self.mask_set = False

		self.llrf_control.setGlobalCheckMask(False)

		while self.mask_set == False:
			self.mask_set = self.llrf_handler.set_mask()

		print(self.my_name + ' entering mainloop')

		# start the clock
		self.start_time()

		i = 0

		while 1:
			QApplication.processEvents()

			#the GUI can overide omcreasing the power
			if self.gui.can_ramp:

			# update main monitor states

				self.data_monitor.update()
				#
				# # if new_bad drop SP
				if self.data_monitor.new_bad():
					print('MAIN-LOOP New Bad State droppingng SP=0')
					self.llrf_control.setGlobalCheckMask(False)
					if self.data_monitor.vac_new_bad():
						self.llrf_handler.set_amp( 5 ) # vac amp set value
					if self.data_monitor.dc_new_bad():
						self.llrf_handler.set_amp( 6 ) # DC amp set value

				if 	self.data_monitor.new_good_no_bad():
					m = max([i[0] for i in self.data.sp_pwr_hist])
					print(self.my_name +' new good, seting amp_sp = ' + str(m ))

					# if breakdown rate is good set previous max value (should this be max?
					self.llrf_handler.set_amp( m  )
					# if breakdown rate is bd, go to previous power and wait for breakdown_rate to recover
					# if anothe breakdown occurs then drop down agaain
					print('restart main_loop clock')
					self.start_time()


				# if everything is good carry on increasing
				if self.data_monitor.all_good():
					#print('all good')

								# set the masks
					if self.mask_set == False:
						#print('main loop mask not set')
						self.mask_set = self.llrf_handler.set_mask()
						# if GOOD set checking for breakdowns
					else:
						#print('main loop setting global check mask = TRUE')
						if i == 0:
							self.llrf_control.setGlobalCheckMask(True)
							i = 1
						# if there has been enough time since
						# the last increase get the new llrf sp
						# we use dto updat ebased on time elapsed
						#if self.seconds_elapsed(self.llrf_param['TIME_BETWEEN_RF_INCREASES']):
						# now we update base do npulses
						if self.data.values['event_pulse_count'] > 150: # check this number in the look up table / index
							self.apply_new_amp()
							self.start_time()
							self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
				else:
					pass
					#print('not all good')
			else:
				#print('press start ramp to continue')
				time.sleep(1)

	def check_vac(self):
		print'check_vac'

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