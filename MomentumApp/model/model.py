from epics import caget,caput
import os,sys
import time
import generalMomentumFunctions as general
sys.path.append('C:\\Users\\wln24624\\Documents\\VELA-CLARA-Controllers\\Controllers\\VELA\INJECTOR\\velaINJMagnets\\bin\\Release')
import logging
#import velaINJMagnetControl as vimc


class Model():
	def __init__(self, view):
		self.PL = logging.getLogger("P")
		self.PSL = logging.getLogger("PS")
		self.deets = logging.getLogger("P/PS")
		self.momentum = 0
		self.momentumSpread = 0
		self.predictedMomentum = 0
		self.func = general.Functions()
		#self.magnets =	vimc.velaINJMagnetController(False,False,False)
		self.view = view
		print("Model Made")

	def LogTest(self):
		self.PSL.info('Llama')
		self.PSL.debug('Llama')
		self.PSL.warning('Llama')
		self.PSL.error('Llama')
		self.PSL.critical('Llama')
	def measureMomentum(self):
		"""1. Align Beam through Dipole"""
		if self.view.checkBox_2.isChecked()==True:
			self.PL.info('2. Aligning Beam through Dipole')
			for i in range(3):
				self.func.align('HCOR01','BPM01', self.deets)
				self.func.align('HCOR02','BPM02', self.deets)

		"""2. Centre in Spectrometer Line"""
		if self.view.checkBox_3.isChecked()==True:
			self.PL.info('3. Center Down Spectrometer Line')
			self.func.bendBeam('DIP01','BPM03', self.deets)

		"""3. Convert Current to Momentum"""
		if self.view.checkBox_4.isChecked()==True:
			self.PL.info('4. Calculate Momentum')

	def measureMomentumSpread(self):
		"""1. Minimize Beta"""

		"""2. Set Dispersion Size"""

		"""3. Find Dispersion """
