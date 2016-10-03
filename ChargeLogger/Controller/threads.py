from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread, pyqtSignal

import win32com.client
import time

class logChargeThread( QThread ):
	def __init__( self, model, trName, wfType ):
		QtCore.QThread.__init__( self )
		self.model = model
		self.trName = trName
		self.wfType = wfType

	def __del__(self):
		self.wait()
	
	def run( self ):
		self.model.recordChannel( self.trName, self.wfType )
		self.model.writeToEPICS( self.trName, self.wfType )
	
		self.terminate()
	# def writeToEPICS( self, trName, wfType ):
		# self.model.writeToEPICS( trName, wfType )
		
	# def recordTraces( self, trName ):
		# self.model.recordTraces( trName )
		
	# def recordNums( self, numName ):
		# self.model.recordNums( numName )
