import numpy
import scipy.constants

class UnitConversion(object):

	def __init__(self):
		object.__init__(self)
		self.my_name = "UnitConversion"
		speed_of_light = scipy.constants.speed_of_light / 1e6

	def getEnergyGain(self, rf_type, forward_power, phase, pulse_length, cavity_length):
		if rf_type == "GUN10":
			self.gun_energy_gain = self.getEnergyFromRF(forward_power, phase, pulse_length, cavity=rf_type)
			self.field_amplitude = float(self.gun_energy_gain * numpy.cos(phase) / cavity_length)
			return [self.gun_energy_gain, self.field_amplitude]
		elif rf_type == "L01":
			self.l01_energy_gain = self.getEnergyFromRF(forward_power, phase, pulse_length, cavity=rf_type)*1e-6
			self.field_amplitude = float(self.l01_energy_gain * numpy.cos(phase) / cavity_length)
			return [self.l01_energy_gain, self.field_amplitude]

	def currentToK(self, mag_type, current, field_integral_coefficients, magnetic_length, energy):
		if mag_type == 'QUAD':
			self.coeffs = numpy.append(field_integral_coefficients[:-1],
								field_integral_coefficients[-1])
			self.int_strength = numpy.polyval(self.coeffs, current)
			self.effect = speed_of_light * self.int_strength / energy
			# self.update_widgets_with_values("lattice:" + key + ":k1l", effect / value['magnetic_length'])
			self.k1l = self.effect / (magnetic_length * 1000)
			return self.k1l
		elif mag_type == 'SOL':
			self.sign = numpy.copysign(1, self.current)
			self.coeffs = numpy.append(field_integral_coefficients[-4:-1] * int(self.sign),
								field_integral_coefficients[-1])
			self.int_strength = numpy.polyval(self.coeffs, current)
			self.effect = self.int_strength / (magnetic_length * 1000)
			self.field_amplitude = float(self.effect / (magnetic_length * 1000))
			return self.field_amplitude


	def getEnergyFromRF(self, forward_power, phase, pulse_length, cavity=None):
		if cavity == "GUN10":
			bestcase = 0.407615 + 1.94185 * (((1 - math.exp((-1.54427 * 10 ** 6 * pulse_length * 10 ** -6))) * (
						0.0331869 + 6.05422 * 10 ** -7 * forward_power)) * numpy.cos(phase)) ** 0.5
			worstcase = 0.377 + 1.81689 * (((1 - math.exp((-1.54427 * 10 ** 6 * pulse_length * 10 ** -6))) * (
						0.0331869 + 6.05422 * 10 ** -7 * forward_power)) * numpy.cos(phase)) ** 0.5
			return numpy.mean([bestcase, worstcase])
		elif cavity == "L01":
			return numpy.sqrt(forward_power*6.248*1e7)