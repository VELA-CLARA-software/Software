# holds everything
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import pyqtSlot
import os
import sys
import time
from state import state

if os.environ['COMPUTERNAME'] == "DJS56PORT2":
	print 'port'
	sys.path.append(os.getcwd())
else:
	print 'desk'
	sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage')

# Hardware Controllers (.pyd)
import VELA_CLARA_General_Monitor
import VELA_CLARA_LLRF_Control
# import VELA_CLARA_RF_Modulator_Control
# Python Classes that do work
import LLRF_monitor
import mask_setter
import vacuum_monitor
import config_reader
#import gun_modulator
import libera_interlocks
import break_down_monitor
import gui_conditioning

#os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
#os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
#os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"


class master(object):
	# whoami
	my_name = 'master'
	# general monitoring for parameters with no controller
	# or just 1 parameter such as mod-status
	# the master will handle ALL gen mon connections
	# it will then paxss of keys and objects to monitor classes
	gen_mon = VELA_CLARA_General_Monitor.init()
	# every key from gen_mon will be stored here
	gen_mon_keys = {}
	# we can make some reasonable guesses as to what will be included
	vac_id = 'VAC_ID'
	dc_id  = 'DC_ID'
	mod_id = 'MOD_ID'
	cavity_temp_id = 'CAVITY_TEMP_ID'
	water_temp_id  = 'WATER_TEMP_ID'
	all_id = [vac_id,dc_id,mod_id,cavity_temp_id,water_temp_id]
	[gen_mon_keys.update({x:None}) for x in all_id]

	# explicit flags for possible monitors & monitors states
	# below

	# flags for known monitors
	# these are used to determine if monitoring these items is happening
	# they're not for defining vacuum good, / bad etc.
	modulator_monitoring 	= "modulator_monitoring"
	DC_monitoring 			= "DC_monitoring"
	rf_prot_monitoring 		= "rf_prot_monitoring"
	vacuum_monitoring 		= "vacuum_monitoring"
	breakdown_monitoring 	= "breakdown_monitoring"
	water_temp_monitoring 	= "water_temp_monitoring"
	cavity_temp_monitoring 	= "cavity_temp_monitoring"
	monitoring_flags = {}
	all_monitors = [modulator_monitoring,DC_monitoring,rf_prot_monitoring,
						 vacuum_monitoring,breakdown_monitoring,water_temp_monitoring,
					     cavity_temp_monitoring]
	[monitoring_flags.update({x:False})for x in all_monitors]


	# which things are monitored
	vacuum_state="vacuum_state"
	dc_state="dc_state"
	breakdown_rate_state = "breakdown_rate_state"
	rf_prot_state = "rf_prot_state"
	modulator_state = "modulator_state"
	all_state_names = [vacuum_state, dc_state, breakdown_rate_state]
	all_states={}
	[all_states.update({x:state.UNKNOWN})for x in all_state_names]


	# gui value dict
	vacuum_level = 'vacuum_level'
	all_gui_values = [vacuum_level]
	gui_values={}
	[gui_values.update({x:0})for x in all_gui_values]


	# Create Specific Hardware Controllers
	# THE The Gun LLRF
	# Change physical_VELA_LRRG_LLRF_Controller for different Gun / RF structure
	#llrf_controller     = llrf_init.physical_VELA_HRRG_LLRF_Controller()
	# The Gun Modulator
	#gun_mod_controller = rf_mod_init.physical_GUN_MOD_Controller()

	# create Python monitoring / control classes
	#llrf = LLRF_monitor.LLRF_monitor(llrf_controller)



	#libera_interlocks = libera_interlocks.libera_interlocks(llrf_controller)
	#gun_modulator = gun_modulator.gun_modulator(gun_mod_controller)

	def __init__(self, argv, config_file, vac_pv = 'EBT-HRG1-VAC-IMG-01:PRES'):
		#QObject.__init__(self)
		# create Python monitoring / control classes

		#self.init_vac_monitor(vac_pv)

		# mask_setter monitoring
		# self.mask_setter = mask_setter.mask_setter( llrf_controller = self.llrf_controller )
		# self.mask_setter.start()

		# break_down monitoring
		# self.break_down_monitor = break_down_monitor.break_down_monitor(self.llrf_controller)
		# self.break_down_monitor.newBreakDownSignal.connect(self.new_break_down)


		# read a config
		self.get_config(config_file)
		self.init_vac_monitor()

		# build a gui
		self.init_gui()



	def get_config(self,fn):
		reader = config_reader.config_reader(fn)
		self.have_config = reader.get_config()

		self.vac_param = reader.get_vac_parameter()

		if self.have_config:
			self.config = reader.config
		return self.have_config


	def init_gui(self):
		self.gui = gui_conditioning.gui_conditioning()
		self.gui.show()







	def init_vac_monitor(self):
		if bool(self.vac_param):
			# NOT HAPPY ABOUT HARDCODED STRINGS...
			if self.connectPV(self.vac_id,self.vac_param.get('VAC_PV')):
				self.vac_param[self.vac_id] = self.gen_mon_keys[self.vac_id]
				# Vacuum monitoring requires a vacuum PV
				self.vacuum = vacuum_monitor.vacuum_monitor(self.gen_mon, self.vac_param,self.all_states,self.gui_values)
				# connect the signal, OLD DEPRICATED
				#self.vacuum.vac_signal.connect(self.vac_signal)
				if self.vacuum.set_success:
					self.vacuum.start()
					self.monitoring_flags[self.vacuum_monitoring] = True

	@pyqtSlot()
	def new_break_down(self):
		print('Received new break down signal')
		# record current state
		# set powers accordingly
		# set a timer
		# or just set some flags that are handled in main loop?



	# connect to process variable pv
	def connectPV(self, pvKey, pvValue):
		connected = False
		if pvValue is not None:
			id = self.gen_mon.connectPV(pvValue)
			if id != 'FAILED':
				connected = True
				print('Connected to PV = ', pvValue, ' with ID = ', id, ' acquiring data')
				self.gen_mon_keys[pvKey] = id
			else:
				print('Failed to connect to PV = ',pvValue, ' ID = ', id, ' NOT acquiring data')
		return connected

	def main_loop(self):

		print('The RF Conditioning Master is Entering Main_Loop ')

		i = 0

		self.llrf.set_klystron_forward_power_trace_mean_range(71, 201)


		while i < 10:

			print self.llrf.get_mean_klystron_foward_power()


			# if self.gun_modulator.is_gun_modulator_in_Trig:
			# 	print 'modulator trig'
			# else:
			# 	print 'modulator NOT IN trig'

			# if self.vacuum_monitor.is_good:
			# 	print 'vacuum_monitor good'
			# else:
			# 	print 'vacuum_monitor bad'

			print 'self.llrf.get_mean_klystron_foward_power()'
			print self.llrf.get_mean_klystron_foward_power()



			#QApplication.processEvents()
			time.sleep(0.1)
			i += 1
			print(' i = ', i)


	def check_breakdown(self):
		print('checking for a break down')






	# OLD AND DEPRICATED
	# slot for vacuum monitor signal to connect to
	# @pyqtSlot()
	# def vac_signal(self,val):
	# 	if val:
	# 		self.all_states[self.vacuum_state] = self.state.GOOD
	# 		print(self.my_name,': Vacuum is good!')
	# 	elif not val:
	# 		self.all_states[self.vacuum_state] = self.state.BAD
	# 		print(self.my_name,': Vacuum is bad!')
	# 	else:
	# 		self.all_states[self.vacuum_state] = self.state.UNKNOWN
	# 		print(self.my_name, ': Vacuum is in UNKNOWN STATE')

