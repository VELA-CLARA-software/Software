import collections
import os, sys
import numpy
sys.path.append('E://VELA-CLARA-software//OnlineModel')
import SimulationFramework.Framework as Fw
import SimulationFramework.Modules.read_beam_file as read_beam_file
import SimulationFramework.Modules.read_twiss_file as read_twiss_file
sys.path.append(os.path.realpath(__file__)+'/../../../../')

class GetDataFromSimFrame(object):

	def __init__(self):
		object.__init__(self)
		self.my_name = "GetDataFromSimFrame"
		self.parameterDict = collections.OrderedDict()
		self.lattices = ['INJ', 'S01', 'L01', 'S02', 'C2V', 'VELA', 'BA1']
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
		self.allDataDict.update({"INJ": {}})
		self.allDataDict.update({"S01": {}})
		self.allDataDict.update({"L01": {}})
		self.allDataDict.update({"S02": {}})
		self.allDataDict.update({"C2V": {}})
		self.allDataDict.update({"BA1": {}})
		self.allDataDict.update({"VELA": {}})
		self.allDataDict.update({"simulation": {}})
		self.allDataDict.update({"generator": {}})
		self.setSimulationDictDefaults(self.allDataDict)
		self.allbeamfiles = {}
		self.beam = read_beam_file.beam()
		self.twiss = read_twiss_file.twiss()
		self.my_name = "GetDataFromSimFrame"

	def setSimulationDictDefaults(self, datadict):
		datadict.update({"generator": {}})
		datadict['generator'].update({'dist_x': {}})
		datadict['generator']['dist_x'].update({'type': 'generator'})
		datadict['generator']['dist_x'].update({'catap_type': 'pil'})
		datadict['generator']['dist_x'].update({'value': '2DGaussian'})
		datadict['generator'].update({'dist_y': {}})
		datadict['generator']['dist_y'].update({'type': 'generator'})
		datadict['generator']['dist_y'].update({'catap_type': 'pil'})
		datadict['generator']['dist_y'].update({'value': '2DGaussian'})
		datadict['generator'].update({'dist_z': {}})
		datadict['generator']['dist_z'].update({'type': 'generator'})
		datadict['generator']['dist_z'].update({'catap_type': 'pil'})
		datadict['generator']['dist_z'].update({'value': 'g'})
		datadict['generator'].update({'sig_x': {}})
		datadict['generator']['sig_x'].update({'type': 'generator'})
		datadict['generator']['sig_x'].update({'catap_type': 'pil'})
		datadict['generator']['sig_x'].update({'value': 0.25})
		datadict['generator'].update({'sig_y': {}})
		datadict['generator']['sig_y'].update({'type': 'generator'})
		datadict['generator']['sig_y'].update({'catap_type': 'pil'})
		datadict['generator']['sig_y'].update({'value': 0.25})
		datadict['generator'].update({'spot_size': {}})
		datadict['generator']['spot_size'].update({'type': 'generator'})
		datadict['generator']['spot_size'].update({'catap_type': 'pil'})
		datadict['generator']['spot_size'].update({'value': 0.25})
		datadict['generator'].update({'sig_clock': {}})
		datadict['generator']['sig_clock'].update({'type': 'generator'})
		datadict['generator']['sig_clock'].update({'catap_type': 'pil'})
		datadict['generator']['sig_clock'].update({'value': 0.85e-3})
		datadict['generator'].update({'charge': {}})
		datadict['generator']['charge'].update({'type': 'generator'})
		datadict['generator']['charge'].update({'catap_type': 'charge'})
		datadict['generator']['charge'].update({'PV': 'CLA-S01-DIA-WCM-01'})
		datadict['generator']['charge'].update({'PV_suffixes': 'Q'})
		datadict['generator']['charge'].update({'value': 0.25})
		datadict['generator'].update({'number_of_particles': {}})
		datadict['generator']['number_of_particles'].update({'type': 'generator'})
		datadict['generator']['number_of_particles'].update({'value': 51})

		datadict.update({"simulation": {}})
		datadict['simulation'].update({'astra_run_number': {}})
		datadict['simulation']['astra_run_number'].update({'astra_run_number': 101})
		datadict['simulation']['astra_run_number'].update({'type': 'generator'})
		datadict['simulation'].update({'directory': './test/'})
		datadict['simulation'].update({'injector_space_charge': True})
		datadict['simulation'].update({'rest_of_line_space_charge': True})
		datadict['simulation'].update({'starting_lattice': 'Generator'})
		datadict['simulation'].update({'final_lattice': 'S02'})
		datadict['simulation'].update({'track': False})
		datadict['simulation'].update({'bsol_tracking': False})

		datadict['simulation'].update({'space_charge': {}})
		datadict['simulation']['space_charge'].update({'type': 'generator'})
		datadict['simulation']['space_charge'].update({'value': False})

		datadict['simulation'].update({'tracking_code': {}})
		datadict['simulation']['tracking_code'].update({'BA1': 'Elegant'})
		datadict['simulation']['tracking_code'].update({'C2V': 'Elegant'})
		datadict['simulation']['tracking_code'].update({'S02': 'Elegant'})
		datadict['simulation']['tracking_code'].update({'VELA': 'Elegant'})
		# self.allDataDict['simulation']['tracking_code'].update({'INJ': 'ASTRA'})

		datadict['simulation'].update({'csr': {}})
		datadict['simulation'].update({'csr_bins': {}})
		datadict['simulation'].update({'lsc': {}})
		datadict['simulation'].update({'lsc_bins': {}})
		datadict['simulation']['csr'].update({'BA1': True})
		datadict['simulation']['csr'].update({'C2V': True})
		datadict['simulation']['csr'].update({'S02': True})
		datadict['simulation']['csr'].update({'VELA': True})
		datadict['simulation']['csr_bins'].update({'BA1': 200})
		datadict['simulation']['csr_bins'].update({'C2V': 200})
		datadict['simulation']['csr_bins'].update({'S02': 200})
		datadict['simulation']['csr_bins'].update({'VELA': 200})
		datadict['simulation']['lsc'].update({'BA1': True})
		datadict['simulation']['lsc'].update({'C2V': True})
		datadict['simulation']['lsc'].update({'S02': True})
		datadict['simulation']['lsc'].update({'VELA': True})
		datadict['simulation']['lsc_bins'].update({'BA1': 200})
		datadict['simulation']['lsc_bins'].update({'C2V': 200})
		datadict['simulation']['lsc_bins'].update({'S02': 200})
		datadict['simulation']['lsc_bins'].update({'VELA': 200})

	def loadFramework(self, dtory, clea=False, verb=True):
		self.Framework = Fw.Framework(directory=dtory, clean=clea, verbose=verb)

	def getFramework(self):
		return self.Framework

	def loadLattice(self, lattice):
		self.Framework.loadSettings(lattice)

	def initialiseData(self):
		# [self.runParameterDict.update({key: value}) for key, value in zip(data_keys, data_v)]
		[self.generatorDict.update({key: value}) for key, value in self.laser_values.items()]
		[self.generatorDict.update({key: value}) for key, value in self.charge_values.items()]
		[self.generatorDict.update({key: value}) for key, value in self.number_of_particles.items()]
		[self.generatorDict.update({key: value}) for key, value in self.cathode.items()]
		[self.simulationDict.update({key: value}) for key, value in self.space_charge.items()]
		[self.simulationDict.update({key: value}) for key, value in self.astra_run_number.items()]
		[self.simulationDict.update({key: value}) for key, value in self.tracking_code.items()]
		[[self.allDataDict[l].update({key: value}) for key, value in self.dip_values.items() if l in key] for l in
		 self.lattices]
		[[self.allDataDict[l].update({key: value}) for key, value in self.cor_values.items() if l in key] for l in
		 self.lattices]
		[[self.allDataDict[l].update({key: value}) for key, value in self.quad_values.items() if l in key] for l in
		 self.lattices]
		[self.allDataDict['INJ'].update({key: value}) for key, value in self.rf_values.items() if 'LRG1' in key]
		[self.allDataDict['L01'].update({key: value}) for key, value in self.rf_values.items() if 'L01' in key]
		[self.allDataDict['generator'].update({key: value}) for key, value in self.laser_values.items()]
		[self.allDataDict['generator'].update({key: value}) for key, value in self.charge_values.items()]
		[self.allDataDict['generator'].update({key: value}) for key, value in self.number_of_particles.items()]
		[self.allDataDict['generator'].update({key: value}) for key, value in self.cathode.items()]
		[self.allDataDict['simulation'].update({key: value}) for key, value in self.space_charge.items()]
		[self.allDataDict['simulation'].update({key: value}) for key, value in self.astra_run_number.items()]
		[self.allDataDict['simulation'].update({key: value}) for key, value in self.tracking_code.items()]

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

		for quad in self.Framework.getElementType('quadrupole'):
			self.quad_values.update({quad['objectname']: {}})
			self.quad_values[quad['objectname']].update({'type': quad['objecttype']})
			self.quad_values[quad['objectname']].update({'k1l': quad['k1l']})
			self.quad_values[quad['objectname']].update({'field_integral_coefficients': quad['field_integral_coefficients']})
			self.quad_values[quad['objectname']].update({'magnetic_length': quad['length']})
			self.quad_values[quad['objectname']].update({'PV_suffixes': "SETI"})
			self.quad_values[quad['objectname']].update({'PV': quad['objectname']})
		for dip in self.Framework.getElementType('dipole'):
			self.dip_values.update({dip['objectname']: {}})
			self.dip_values[dip['objectname']].update({'type': dip['objecttype']})
			self.dip_values[dip['objectname']].update({'angle': dip['angle']})
			self.dip_values[dip['objectname']].update({'field_integral_coefficients': dip['field_integral_coefficients']})
			self.dip_values[dip['objectname']].update({'magnetic_length': dip['length']})
			self.dip_values[dip['objectname']].update({'PV_suffixes': "SETI"})
			self.dip_values[dip['objectname']].update({'PV': dip['objectname']})
		for cor in self.Framework.getElementType('kicker'):
			self.cor_values.update({cor['objectname']: {}})
			self.cor_values[cor['objectname']].update({'type': cor['objecttype']})
			self.cor_values[cor['objectname']].update({'angle': cor['angle']})
			self.cor_values[cor['objectname']].update({'field_integral_coefficients': cor['field_integral_coefficients']})
			self.cor_values[cor['objectname']].update({'magnetic_length': cor['length']})
			self.cor_values[cor['objectname']].update({'PV_suffixes': "SETI"})
			self.cor_values[cor['objectname']].update({'Horizontal_PV': cor['Horizontal_PV']})
			self.cor_values[cor['objectname']].update({'Vertical_PV': cor['Vertical_PV']})
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
		self.charge_values['charge'].update({'catap_type': 'charge'})
		self.charge_values['charge'].update({'value': self.Framework.generator.charge})
		self.charge_values['charge'].update({'PV': 'CLA-S01-DIA-WCM-01'})
		self.charge_values['charge'].update({'PV_suffixes': 'Q'})
		self.number_of_particles.update({'number_of_particles': collections.OrderedDict()})
		self.number_of_particles['number_of_particles'].update({'value': int(self.Framework.generator.particles/10)})
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
		self.laser_values['dist_x'].update({'catap_type': 'pil'})
		self.laser_values['dist_x'].update({'value': self.Framework.generator.parameters['dist_x']})
		self.laser_values.update({'dist_y': {}})
		self.laser_values['dist_y'].update({'type': 'generator'})
		self.laser_values['dist_y'].update({'catap_type': 'pil'})
		self.laser_values['dist_y'].update({'value': self.Framework.generator.parameters['dist_y']})
		self.laser_values.update({'dist_z': {}})
		self.laser_values['dist_z'].update({'type': 'generator'})
		self.laser_values['dist_z'].update({'catap_type': 'pil'})
		self.laser_values['dist_z'].update({'value': self.Framework.generator.parameters['dist_z']})
		self.laser_values.update({'sig_x': {}})
		self.laser_values['sig_x'].update({'type': 'generator'})
		self.laser_values['sig_x'].update({'catap_type': 'pil'})
		self.laser_values['sig_x'].update({'value': self.Framework.generator.parameters['sig_x']})
		self.laser_values.update({'sig_y': {}})
		self.laser_values['sig_y'].update({'type': 'generator'})
		self.laser_values['sig_y'].update({'catap_type': 'pil'})
		self.laser_values['sig_y'].update({'value': self.Framework.generator.parameters['sig_y']})
		self.laser_values.update({'spot_size': {}})
		self.laser_values['spot_size'].update({'type': 'generator'})
		self.laser_values['spot_size'].update({'catap_type': 'pil'})
		self.laser_values['spot_size'].update({'value': self.Framework.generator.parameters['sig_x']})
		self.laser_values.update({'sig_clock': {}})
		self.laser_values['sig_clock'].update({'type': 'generator'})
		self.laser_values['sig_clock'].update({'catap_type': 'pil'})
		self.laser_values['sig_clock'].update({'value': self.Framework.generator.parameters['sig_clock']})

	def getAllBeamFiles(self, directory):
		for file in os.listdir(directory):
			if file.endswith(".hdf5"):
				self.beam.read_HDF5_beam_file(os.path.join(directory, file))
				self.beamdata = {}
				self.beamdata.update({'filename': os.path.join(directory, file)})
				self.beamdata.update({'x': {}})
				self.beamdata['x'].update({'mean': numpy.mean(getattr(self.beam, 'x'))})
				self.beamdata['x'].update({'dist': getattr(self.beam, 'x')})
				self.beamdata.update({'y': {}})
				self.beamdata['y'].update({'mean': numpy.mean(getattr(self.beam, 'y'))})
				self.beamdata['y'].update({'dist': getattr(self.beam, 'y')})
				self.beamdata.update({'z': {}})
				self.beamdata['z'].update({'mean': numpy.mean(getattr(self.beam, 'z'))})
				self.beamdata['z'].update({'dist': getattr(self.beam, 'z')})
				self.beamdata.update({'px': {}})
				self.beamdata['px'].update({'mean': numpy.mean(getattr(self.beam, 'px'))})
				self.beamdata['px'].update({'dist': getattr(self.beam, 'px')})
				self.beamdata.update({'py': {}})
				self.beamdata['py'].update({'mean': numpy.mean(getattr(self.beam, 'py'))})
				self.beamdata['py'].update({'dist': getattr(self.beam, 'py')})
				self.beamdata.update({'pz': {}})
				self.beamdata['pz'].update({'mean': numpy.mean(getattr(self.beam, 'pz'))})
				self.beamdata['pz'].update({'dist': getattr(self.beam, 'pz')})
				self.beamdata.update({'t': {}})
				self.beamdata['t'].update({'mean': numpy.mean(getattr(self.beam, 't'))})
				self.beamdata['t'].update({'dist': getattr(self.beam, 't')})
				# self.beamdata.update({'q': {}})
				# self.beamdata['q'].update({'total': (-1) * (10 ** 12) * numpy.sum(getattr(self.beam, 'charge'))})
				# self.beamdata['q'].update({'dist': (-1) * (10 ** 12) * getattr(self.beam, 'charge')})
				self.separator = '.'
				self.pvname = file.split(self.separator, 1)[0]
				self.allbeamfiles.update({self.pvname: self.beamdata})
		return self.allbeamfiles