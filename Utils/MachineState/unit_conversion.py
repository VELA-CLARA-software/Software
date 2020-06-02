import numpy
import scipy.constants
import math

class UnitConversion(object):

	def __init__(self):
		object.__init__(self)
		self.my_name = "UnitConversion"
		speed_of_light = scipy.constants.speed_of_light / 1e6

	def getEnergyGain(self, rf_type, forward_power, phase, pulse_length, cavity_length):
		if (rf_type == "LRRG_GUN") or ("GUN" in rf_type):
			self.gun_energy_gain = self.getEnergyFromRF(forward_power, phase, pulse_length, cavity=rf_type)
			self.field_amplitude = float(self.gun_energy_gain / 0.0644)
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
			self.coeffs = numpy.append(field_integral_coefficients[:-1] * int(self.sign),
								field_integral_coefficients[-1])
			self.int_strength = numpy.polyval(self.coeffs, abs(current))
			self.effect = (scipy.constants.speed_of_light / 1e6) * self.int_strength / energy
			# self.update_widgets_with_values("lattice:" + key + ":k1l", effect / value['magnetic_length'])
			self.k1l = self.effect / (magnetic_length * 1000)
			magdict['k1l'] = float(self.k1l)
		elif (mag_type == 'SOL') or (mag_type == 'solenoid'):
			self.sign = numpy.copysign(1, current)
			self.coeffs = numpy.append(field_integral_coefficients[-4:-1] * int(self.sign), field_integral_coefficients[-1])
			self.int_strength = numpy.polyval(self.coeffs, abs(current))
			self.field_amplitude = self.int_strength / magnetic_length
			magdict['field_amplitude'] = float(self.field_amplitude)
		elif (mag_type == 'HCOR') or (mag_type == 'VCOR') or (mag_type == 'kicker'):
			self.sign = numpy.copysign(1, current)
			self.coeffs = numpy.append(field_integral_coefficients[:-1] * int(self.sign),
									   field_integral_coefficients[-1])
			self.int_strength = numpy.polyval(self.coeffs, abs(current))
			self.effect = (scipy.constants.speed_of_light / 1e6) * self.int_strength / energy
			magdict['angle'] = float(self.effect)
		elif (mag_type == 'DIP') or (mag_type == 'dipole'):
			self.sign = numpy.copysign(1, current)
			self.coeffs = numpy.append(field_integral_coefficients[:-1] * int(self.sign),
									   field_integral_coefficients[-1])
			self.int_strength = numpy.polyval(self.coeffs, abs(current))
			self.effect = (scipy.constants.speed_of_light / 1e6) * self.int_strength / energy
			self.angle = numpy.radians(self.effect / 1000)
			magdict['angle'] = float(self.angle)

	def getEnergyFromRF(self, forward_power, phase, pulse_length, cavity=None):
		if cavity == "LRRG_GUN":
			bestcase = 0.407615 + 1.94185 * (((1 - math.exp(-1.54427 * pulse_length)) * (
					0.0331869 + 6.05422 * 10 ** -7 * forward_power)) * numpy.cos(phase)) ** 0.5
			worstcase = 0.377 + 1.81689 * (((1 - math.exp(-1.54427 * pulse_length)) * (
					0.0331869 + 6.05422 * 10 ** -7 * forward_power)) * numpy.cos(phase)) ** 0.5
			return numpy.mean([bestcase, worstcase])
		elif cavity == "L01":
			return (numpy.sqrt(forward_power * 6.248 * 1e7) * 1e-6)

	def getPowerFromEnergy(self, energy_gain, phase, pulse_length, cavity=None):
		if (cavity == "LRRG_GUN") or ("GUN" in cavity):
			print(energy_gain)
			print(phase)
			print(pulse_length)
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
			print(numpy.mean([bestcase,worstcase]))
			return numpy.mean([bestcase, worstcase])
		elif (cavity == "L01") or ("L01" in cavity):
			return (1e12 * (energy_gain ** 2)/(6.248 * 1e7))