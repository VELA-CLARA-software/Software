import numpy
import scipy.constants
import scipy.stats
import math
import aliases

class UnitConversion(object):

	def __init__(self):
		object.__init__(self)
		self.my_name = "UnitConversion"
		self.alias_names = aliases.alias_names
		self.type_alias = aliases.type_alias
		speed_of_light = scipy.constants.speed_of_light / 1.0e6
		self.lattices = ['EBT-BA1', 'INJ', 'CLA-S01', 'CLA-S02', 'L01', 'CLA-C2V', 'VCA']
		self.gun_pulse_length = 2.5
		self.linac_pulse_length = 0.75
		self.energy = {}
		self.gun_position = 0.17  # MAGIC NUMBER (BUT IT WON'T CHANGE)
		self.l01_position = 3.2269  # MAGIC NUMBER (BUT IT WON'T CHANGE)

	def getLattices(self):
		return self.lattices

	def getDefaultGunPulseLength(self):
		return self.gun_pulse_length

	def getDefaultL01PulseLength(self):
		return self.linac_pulse_length

	def getGunPosition(self):
		return self.gun_position

	def getL01Position(self):
		return self.l01_position

	def getEnergyGain(self, rf_type, forward_power, phase, pulse_length, cavity_length):
		if (rf_type == "LRRG_GUN") or ("GUN" in rf_type):
			self.gun_energy_gain = self.getEnergyFromRF(forward_power, phase, pulse_length, cavity=rf_type)
			self.energy_gain = self.getEnergyFromRF(forward_power, 0.0, pulse_length, cavity=rf_type)
			self.field_amplitude = float(self.energy_gain / 0.0644)
			return [self.gun_energy_gain, self.field_amplitude]
		elif (rf_type == "L01") or ("L01" in rf_type):
			self.l01_energy_gain = self.getEnergyFromRF(forward_power, phase, pulse_length, cavity=rf_type)
			self.field_amplitude = float(self.l01_energy_gain / cavity_length)
			return [self.l01_energy_gain, self.field_amplitude]

	def getPowerFromFieldAmplitude(self, rf_type, field_amplitude, phase, pulse_length, cavity_length):
		if rf_type == "LRRG_GUN":
			self.energy_gain = float(field_amplitude * 0.0644)
			self.forward_power = self.getPowerFromEnergy(self.energy_gain, phase, pulse_length, cavity=rf_type)
			return self.forward_power
		elif rf_type == "L01":
			self.energy_gain = float(field_amplitude * cavity_length)
			self.forward_power = self.getPowerFromEnergy(self.energy_gain, phase, pulse_length, cavity=rf_type)
			return self.forward_power

	def currentToK(self, mag_type, current, field_integral_coefficients, magnetic_length, energy, magdict):
		if (mag_type == 'QUAD') or (mag_type == 'quadrupole'):
			self.sign = numpy.copysign(1, current)
			self.ficmod = [i * int(self.sign) for i in field_integral_coefficients[:-1]]
			self.coeffs = numpy.append(self.ficmod,
									   field_integral_coefficients[-1])
			self.int_strength = numpy.polyval(self.coeffs, abs(current))
			self.effect = (scipy.constants.speed_of_light / 1.0e6) * self.int_strength / energy
			# self.update_widgets_with_values("lattice:" + key + ":k1l", effect / value['magnetic_length'])
			self.k1 = self.effect / (magnetic_length)
			magdict.update({'k1': float(self.k1)})
		elif (mag_type == 'SOL') or (mag_type == 'solenoid'):
			self.sign = numpy.copysign(1, current)
			self.ficmod = [i * int(self.sign) for i in field_integral_coefficients[-4:-1]]
			self.coeffs = numpy.append(self.ficmod,
									   field_integral_coefficients[-1])
			self.int_strength = numpy.polyval(self.coeffs, abs(current))
			self.field_amplitude = self.int_strength / magnetic_length
			magdict.update({'field_amplitude': float(int(self.sign) * self.field_amplitude)})
		elif (mag_type == 'HCOR') or (mag_type == 'VCOR') or (mag_type == 'kicker'):
			self.sign = numpy.copysign(1, current)
			self.ficmod = [i * int(self.sign) for i in field_integral_coefficients[:-1]]
			self.coeffs = numpy.append(self.ficmod,
									   field_integral_coefficients[-1])
			self.int_strength = numpy.polyval(self.coeffs, abs(current))
			self.effect = (scipy.constants.speed_of_light / 1.0e6) * self.int_strength / energy
			magdict.update({'angle': float(self.effect)})
		elif (mag_type == 'DIP') or (mag_type == 'dipole'):
			self.sign = numpy.copysign(1.0, current)
			self.ficmod = [i * int(self.sign) for i in field_integral_coefficients[:-1]]
			self.coeffs = numpy.append(self.ficmod,
									   field_integral_coefficients[-1])
			self.int_strength = numpy.polyval(self.coeffs, abs(current))
			self.effect = (scipy.constants.speed_of_light / 1.0e6) * self.int_strength / energy
			self.angle = numpy.radians(self.effect / 1000.0)
			magdict.update({'angle': float(self.angle)})

	def kToCurrent(self, mag_type, k, field_integral_coefficients, magnetic_length, energy):
		if (mag_type == 'QUAD') or (mag_type == 'quadrupole'):
			self.effect = magnetic_length * k  # * magnetic_length
			self.int_strength = self.effect * energy / (scipy.constants.speed_of_light / 1e6)
			self.sign = numpy.copysign(1, k)
			self.ficmod = [i * int(self.sign) for i in field_integral_coefficients[:-1]]
			self.coeffs = numpy.append(self.ficmod, field_integral_coefficients[-1])
			self.roots = numpy.roots(self.coeffs)
			self.current = self.roots[1].real * self.int_strength
			return self.current
		elif (mag_type == 'SOL') or (mag_type == 'solenoid'):
			self.int_strength = k * magnetic_length
			self.sign = int(numpy.copysign(1, self.int_strength - field_integral_coefficients[-1]))
			fic1 = [x * int(self.sign) for x in field_integral_coefficients[-4:-1]]
			self.coeffs = numpy.append(fic1, field_integral_coefficients[-1])
			self.coeffs[-1] -= self.int_strength  # Need to find roots of polynomial, i.e. a1*x + a0 - y = 0
			self.roots = numpy.roots(self.coeffs)
			self.current = numpy.copysign(self.roots[-1].real,
										  self.sign)  # last root is always x value (#TODO: can prove this?)
			return self.current
		elif (mag_type == 'HCOR') or (mag_type == 'VCOR') or (mag_type == 'kicker'):
			self.effect = k
			self.int_strength = self.effect * energy / (scipy.constants.speed_of_light / 1e6)
			if field_integral_coefficients[0] == 0:
				return 0
			self.sign = int(numpy.copysign(1, self.int_strength - field_integral_coefficients[-1]))
			fic1 = [x * int(self.sign) for x in field_integral_coefficients[:-1]]
			self.coeffs = numpy.append(fic1, [field_integral_coefficients[-1]])
			self.coeffs[-1] -= self.int_strength  # Need to find roots of polynomial, i.e. a1*x + a0 - y = 0
			self.roots = numpy.roots(self.coeffs)
			self.current = numpy.copysign(self.roots[-1].real,
										  self.sign)  # last root is always x value (#TODO: can prove this?)
			return self.current
		elif (mag_type == 'DIP') or (mag_type == 'dipole'):
			self.effect = numpy.radians(k) * 1000
			self.int_strength = self.effect * energy / (scipy.constants.speed_of_light / 1e6)
			if field_integral_coefficients[0] == 0:
				return 0
			self.sign = numpy.copysign(1, self.int_strength - field_integral_coefficients[-1])
			fic1 = [x * int(self.sign) for x in field_integral_coefficients[:-1]]
			self.coeffs = numpy.append(fic1, [field_integral_coefficients[-1]])
			self.coeffs[-1] -= self.int_strength  # Need to find roots of polynomial, i.e. a1*x + a0 - y = 0
			self.roots = numpy.roots(self.coeffs)
			self.current = numpy.copysign(self.roots[-1].real,
										  self.sign)  # last root is always x value (#TODO: can prove this?)
			return self.current

	def getEnergyFromRF(self, forward_power, phase, pulse_length, cavity=None):
		if (cavity == "LRRG_GUN") or ("GUN" in cavity):
			bestcase = 0.407615 + 1.94185 * (((1 - math.exp(-1.54427 * pulse_length)) * (
					0.0331869 + 6.05422 * 10 ** -7 * forward_power)) * abs(numpy.cos(phase))) ** 0.5
			worstcase = 0.377 + 1.81689 * (((1 - math.exp(-1.54427 * pulse_length)) * (
			 		0.0331869 + 6.05422 * 10 ** -7 * forward_power)) * abs(numpy.cos(phase))) ** 0.5
			return numpy.mean([bestcase, worstcase])
		elif (cavity == "L01") or ("L01" in cavity):
			return (numpy.sqrt(forward_power * 6.248 * 1e7) * 1e-6)

	def getPowerFromEnergy(self, energy_gain, phase, pulse_length, cavity=None):
		if (cavity == "LRRG_GUN") or ("GUN" in cavity):
			w1 = ((energy_gain - 0.377) / 1.81689) ** 2
			w2 = 1 / (1 - math.exp(-1.54427 * pulse_length))
			w3 = 1 / numpy.cos(phase)
			w4 = -0.0331869
			w5 = 1 / (6.05422 * (10 ** -7))
			worstcase = ((w1 * w2 * w3) - w4) * w5
			b1 = ((energy_gain - 0.407615) / 1.94185) ** 2
			b2 = 1 / (1 - math.exp(-1.54427 * pulse_length))
			b3 = 1 / numpy.cos(phase)
			b4 = -0.0331869
			b5 = 1 / (6.05422 * (10 ** -7))
			bestcase = ((b1 * b2 * b3) - b4) * b5
			return numpy.mean([bestcase, worstcase])
		elif (cavity == "L01") or ("L01" in cavity):
			return (1e12 * (energy_gain ** 2)/(6.248 * 1e7))

	def gaussianFit(self, data):
		mu, std = scipy.stats.norm.fit(data)
		return [mu, std]