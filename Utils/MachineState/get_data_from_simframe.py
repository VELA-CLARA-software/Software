import collections
import os, sys
import numpy
sys.path.append('E://VELA-CLARA-software//OnlineModel')
import SimulationFramework.Framework as Fw

class GetDataFromSimFrame(object):

	def __init__(self):
		object.__init__(self)
		self.my_name = "GetDataFromSimFrame"
		self.parameterDict = collections.OrderedDict()
		self.lattices = ['INJ', 'S02', 'C2V', 'EBT', 'BA1']
		[self.parameterDict.update({l:collections.OrderedDict()}) for l in self.lattices]
		# self.latticeDict = self.parameterDict['lattice']
		self.parameterDict['scan'] = collections.OrderedDict()
		self.scanDict = self.parameterDict['scan']
		self.scanDict['parameter_scan'] = False
		self.parameterDict['simulation'] = collections.OrderedDict()
		self.simulationDict = self.parameterDict['simulation']
		self.parameterDict['generator'] = collections.OrderedDict()
		self.generatorDict = self.parameterDict['generator']
		self.scannableParametersDict = collections.OrderedDict()
		self.allDataDict = {}
		self.my_name = "GetDataFromSimFrame"

	def loadFramework(self, dtory, clea=False, verb=True):
		self.Framework = Fw.Framework(directory=dtory, clean=clea, verbose=verb)

	def getFramework(self):
		return self.Framework

	def loadLattice(self, lattice):
		self.Framework.loadSettings(lattice)

	def initialiseData(self):
		# [self.runParameterDict.update({key: value}) for key, value in zip(data_keys, data_v)]
		[[self.parameterDict[l].update({key: value}) for key, value in self.quad_values.items() if l in key] for l in
		 self.lattices]
		[[self.parameterDict[l].update({key: value}) for key, value in self.dip_values.items() if l in key] for l in
		 self.lattices]
		[[self.parameterDict[l].update({key: value}) for key, value in self.cor_values.items() if l in key] for l in
		 self.lattices]
		[[self.parameterDict[l].update({key: value}) for key, value in self.quad_values.items() if l in key] for l in
		 self.lattices]
		[self.parameterDict['INJ'].update({key: value}) for key, value in self.rf_values.items()]
		[self.generatorDict.update({key: value}) for key, value in self.laser_values.items()]
		[self.generatorDict.update({key: value}) for key, value in self.charge_values.items()]
		[self.generatorDict.update({key: value}) for key, value in self.number_of_particles.items()]
		[self.generatorDict.update({key: value}) for key, value in self.cathode.items()]
		[self.simulationDict.update({key: value}) for key, value in self.space_charge.items()]
		[self.simulationDict.update({key: value}) for key, value in self.astra_run_number.items()]
		[self.simulationDict.update({key: value}) for key, value in self.tracking_code.items()]
		[[self.allDataDict.update({key: value}) for key, value in self.quad_values.items() if l in key] for l in
		 self.lattices]
		[[self.allDataDict.update({key: value}) for key, value in self.dip_values.items() if l in key] for l in
		 self.lattices]
		[[self.allDataDict.update({key: value}) for key, value in self.cor_values.items() if l in key] for l in
		 self.lattices]
		[[self.allDataDict.update({key: value}) for key, value in self.quad_values.items() if l in key] for l in
		 self.lattices]
		[self.allDataDict.update({key: value}) for key, value in self.rf_values.items()]
		[self.allDataDict.update({key: value}) for key, value in self.laser_values.items()]
		[self.allDataDict.update({key: value}) for key, value in self.charge_values.items()]
		[self.allDataDict.update({key: value}) for key, value in self.number_of_particles.items()]
		[self.allDataDict.update({key: value}) for key, value in self.cathode.items()]
		[self.allDataDict.update({key: value}) for key, value in self.space_charge.items()]
		[self.allDataDict.update({key: value}) for key, value in self.astra_run_number.items()]
		[self.allDataDict.update({key: value}) for key, value in self.tracking_code.items()]

	def getDataDict(self):
		return self.allDataDict

	def getElementLength(self, dict, key):
		length = self.Framework.getElement(key)['position_end'][2] - self.Framework.getElement(key)['position_start'][2]
		dict[key].update({'length': length})

	def getRunData(self):
		self.scan_values = {}
		self.scan_parameter = {}
		self.quad_values = {}
		self.rf_values = {}
		self.dip_values = {}
		self.cor_values = {}
		self.screen_values = {}
		self.solenoid_values = {}
		self.charge_values = {}
		self.laser_values = {}
		self.number_of_particles = {}
		self.cathode = {}
		self.space_charge = {}
		self.astra_run_number = {}
		self.tracking_code = {}

		self.tracking_code.update({'tracking_code': {}})

		for quad in self.Framework.getElementType('quadrupole'):
			self.quad_values.update({quad['objectname']: {}})
			self.quad_values[quad['objectname']].update({'type': quad['objecttype']})
			self.quad_values[quad['objectname']].update({'k1l': quad['k1l']})
			self.quad_values[quad['objectname']].update({'field_integral_coefficients': quad['field_integral_coefficients']})
			self.quad_values[quad['objectname']].update({'magnetic_length': quad['length']})
			self.quad_values[quad['objectname']].update({'PV_suffixes': "SETI"})
			self.quad_values[quad['objectname']].update({'PV': quad['objectname']})
		for dip in self.Framework.getElementType('dipole'):
			self.dip_values.update({quad['objectname']: {}})
			self.dip_values[quad['objectname']].update({'type': dip['objecttype']})
			self.dip_values[quad['objectname']].update({'angle': dip['angle']})
			self.dip_values[quad['objectname']].update({'field_integral_coefficients': dip['field_integral_coefficients']})
			self.dip_values[quad['objectname']].update({'magnetic_length': dip['length']})
			self.dip_values[quad['objectname']].update({'PV_suffixes': "SETI"})
			self.dip_values[quad['objectname']].update({'PV': dip['objectname']})
		for cor in self.Framework.getElementType('kicker'):
			self.cor_values.update({quad['objectname']: {}})
			self.cor_values[quad['objectname']].update({'type': cor['objecttype']})
			self.cor_values[quad['objectname']].update({'angle': cor['angle']})
			self.cor_values[quad['objectname']].update({'field_integral_coefficients': cor['field_integral_coefficients']})
			self.cor_values[quad['objectname']].update({'magnetic_length': cor['length']})
			self.cor_values[quad['objectname']].update({'PV_suffixes': "SETI"})
			self.cor_values[quad['objectname']].update({'PV': cor['objectname']})
		for cavity in self.Framework.getElementType('cavity'):
			self.rf_values.update({cavity['objectname']: {}})
			self.rf_values[cavity['objectname']].update({'type': cavity['objecttype']})
			self.rf_values[cavity['objectname']].update({'phase': cavity['phase']})
			self.rf_values[cavity['objectname']].update({'pv_root_alias': cavity['PV']})
			self.rf_values[cavity['objectname']].update({'controller_name': cavity['Controller_Name']})
			self.getElementLength(self.rf_values, cavity['objectname'])
			self.rf_values[cavity['objectname']].update({'field_amplitude': cavity['field_amplitude']})
			self.rf_values[cavity['objectname']].update({'PV_suffixes': cavity['PV_suffixes']})
			self.rf_values[cavity['objectname']].update({'PV': cavity['PV_root']})
			for key, value in cavity['sub_elements'].items():
				if value['type'] == "solenoid":
					self.rf_values.update({key: {}})
					self.rf_values[key].update({'type': 'solenoid'})
					self.rf_values[key].update({'cavity': cavity['objectname']})
					self.rf_values[key].update({'field_amplitude': value['field_amplitude']})
					self.rf_values[key].update({'magnetic_length': value['length']})
					self.rf_values[key].update({'field_integral_coefficients': value['field_integral_coefficients']})
					self.rf_values[key].update({'PV_suffixes': "SETI"})
					self.rf_values[key].update({'PV': key})
		self.charge_values.update({'charge': {}})
		self.charge_values['charge'].update({'type': 'generator'})
		self.charge_values['charge'].update({'value': self.Framework.generator.charge})
		self.charge_values['charge'].update({'PV': 'CLA-S01-DIA-WCM-01'})
		self.charge_values['charge'].update({'PV_suffixes': 'Q'})
		self.number_of_particles.update({'number_of_particles': collections.OrderedDict()})
		self.number_of_particles['number_of_particles'].update({'value': self.Framework.generator.particles})
		self.number_of_particles['number_of_particles'].update({'type': 'generator'})
		self.cathode.update({'cathode': {}})
		self.cathode['cathode'].update({'type': 'generator'})
		self.cathode['cathode'].update({'value': self.Framework.generator.parameters['cathode']})
		self.space_charge.update({'space_charge': {}})
		self.space_charge['space_charge'].update({'type': 'generator'})
		self.space_charge['space_charge'].update({'value': False})
		self.astra_run_number.update({'astra_run_number': {}})
		self.astra_run_number['astra_run_number'].update({'type': 'generator'})
		self.astra_run_number['astra_run_number'].update({'astra_run_number': 101})
		self.laser_values.update({'dist_x': {}})
		self.laser_values['dist_x'].update({'type': 'generator'})
		self.laser_values['dist_x'].update({'value': self.Framework.generator.parameters['dist_x']})
		self.laser_values.update({'dist_y': {}})
		self.laser_values['dist_y'].update({'type': 'generator'})
		self.laser_values['dist_y'].update({'value': self.Framework.generator.parameters['dist_y']})
		self.laser_values.update({'dist_z': {}})
		self.laser_values['dist_z'].update({'type': 'generator'})
		self.laser_values['dist_z'].update({'value': self.Framework.generator.parameters['dist_z']})
		self.laser_values.update({'sig_x': {}})
		self.laser_values['sig_x'].update({'type': 'generator'})
		self.laser_values['sig_x'].update({'value': self.Framework.generator.parameters['sig_x']})
		self.laser_values.update({'sig_y': {}})
		self.laser_values['sig_y'].update({'type': 'generator'})
		self.laser_values['sig_y'].update({'value': self.Framework.generator.parameters['sig_y']})
		self.laser_values.update({'spot_size': {}})
		self.laser_values['spot_size'].update({'type': 'generator'})
		self.laser_values['spot_size'].update({'value': self.Framework.generator.parameters['sig_x']})
		self.laser_values.update({'sig_clock': {}})
		self.laser_values['sig_clock'].update({'type': 'generator'})
		self.laser_values['sig_clock'].update({'value': self.Framework.generator.parameters['sig_clock']})
		self.tracking_code.update({'tracking_code':  {}, 'csr':  {}, 'csr_bins':  {},
			'lsc':  {}, 'lsc_bins':  {}})