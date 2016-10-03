from PyQt4 import QtGui, QtCore

import sys
import time
import numpy as np
# import threads

class Controller():

	def __init__(self, view, model):
		self.view = view
		self.model = model
		# self.threads = threads
		#self.graph = self.view.glayout.addPlot()
		#self.curve = self.graph.plot()
		#self.graph.addItem(self.curve)
		#connecttions
		self.sPool = []
		self.view.pushButton.clicked.connect(self.startScript)
		self.radiobuttons = [ self.view.radioButton, 
							  self.view.radioButton_2,
							  self.view.radioButton_3,
							  self.view.radioButton_4,
							  self.view.radioButton_5,
							  self.view.radioButton_6,
							  self.view.radioButton_7,
							  self.view.radioButton_8 ]
		# self.comboBoxes = [ self.view.comboBox,
							# self.view.comboBox_2, 
							# self.view.comboBox_3, 
							# self.view.comboBox_4 ]
							
	def startScript( self ):
		self.conditions = [ self.view.checkBox.isChecked(),
							self.view.checkBox_2.isChecked(),
							self.view.checkBox_3.isChecked(),
							self.view.checkBox_4.isChecked() ]
		
		# for i in range( len( self.comboBoxes ) ):
			# self.model.writeDiagType( self.model.traceNames[ i ] , str( self.comboBoxes[ i ].currentText()))
			# self.model.writeDiagType( self.model.numNames[ i ] , str( self.comboBoxes[ i ].currentText()))
		
		while True:
			start = time.clock()
			for i in range( len( self.conditions ) ):
				if self.conditions[ i ] == True:
					#self.model.getAndResetScale( i )
					if self.radiobuttons[ ( 2*i ) ].isChecked():
						self.model.recordChannel( ( i + 1 ), "trace" )
						self.model.writeToEPICS( i + 1, "trace" )
					elif self.radiobuttons[ ( 2*i ) + 1 ].isChecked():
						self.model.recordChannel( ( i + 1 ), "num" )
						self.model.writeToEPICS( i + 1, "num" )
					else:
						print "Please select either full waveforms or P values for all channels"

			while time.clock() - start < 0.1:
				time.sleep(0.0001)
			print time.clock() - start
			
