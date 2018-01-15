# THE main_controller
# holds everything
from PyQt4.QtGui import QApplication
from controller_base import controller_base
from data_monitors.data_monitoring import data_monitoring
from gui.gui_conditioning import gui_conditioning
import data.rf_condition_data_base as dat
from data.rf_condition_data import rf_condition_data
import sys
import time
from VELA_CLARA_enums import STATE

class main_controller(controller_base):
	# whoami
	my_name = 'main_controller'
	#
	# all the data lives in here
	# to access data you have to "know" the keywords etc..
	data = rf_condition_data()
	#
	# all the data_monitoring lives here
	# pass in HWC and data to update
	data_monitor = data_monitoring(data)
	#
	# other attributes will be initiliased in base-class
	mask_set = False
	old_sp = 0

	def __init__(self, argv, config_file):
		controller_base.__init__(self, argv, config_file)
		self.data.llrf_type = self.llrf_type
		self.data_monitor.llrf_type = self.llrf_type
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
						   DC_param=self.DC_param
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
		# start data recording
		#
		self.data.start_logging(self.log_param)
		# everything now runs from the main_loop
		#
		#self.llrf_handler.check_masks()
		self.monitor_states = self.data.main_monitor_states

		self.main_loop()



	def main_loop(self):
		print(self.my_name + ' The RF Conditioning is Entering Main_Loop !')

		self.data_monitor.init_monitor_states()


		self.llrf_control.setAmpSP(500)
		# remove time.sleep(10 at you rperil
		time.sleep(1)
		self.mask_set = False

		self.llrf_control.setGlobalCheckMask(False)

		while self.mask_set == False:
			self.mask_set = self.llrf_handler.set_mask()

		print('entering mainloop')
		print('entering mainloop')

		# start the clock
		self.start_time()

		while True:
			QApplication.processEvents()

			#the GUI can overide this loop
			if self.gui.can_run:

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
						self.llrf_control.setGlobalCheckMask(True)
						# if there has been enough time since
						# the last increase get the new llrf sp
						if self.seconds_elapsed(self.llrf_param['TIME_BETWEEN_RF_INCREASES']):
							self.apply_new_amp()
							self.start_time()
				else:
					pass
					#print('not all good')
			else:
				print('press start ramp to continue')
				time.sleep(1)

	def check_vac(self):
		print'check_vac'

	def apply_new_amp(self):
		sp = self.llrf_control.getAmpSP()
		#????
		if sp < 30:#???
			pass # sp ???????
		else:
			new_amp = self.data.get_new_sp(self.llrf_param['RF_INCREASE_LEVEL'])  # MAGIC_STRING kw to increase by
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