from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
import threading
import sys
import time
import threads
import numpy as np
import pyqtgraph as pg
import epics
from epics import caget,caput


class Controller(QObject):

	def __init__(self, view, model):
		super(Controller, self).__init__()
		self.view = view
		self.model = model
		self.threads = threads
		self.threading = threading
		self.pool = []
		self.pvList = []
		self.lowerList = []
		self.upperList = []

		self.view.pushButton_2.clicked.connect(lambda: self.appendToList())
		self.view.pushButton_3.clicked.connect(lambda: self.addPVToList())
		self.view.pushButton.clicked.connect(lambda: self.setRandomPV())

	def setRandomPV(self):
		self.numShots = float(self.view.plainTextEdit_4.toPlainText())
		self.repRate = float(self.view.plainTextEdit_5.toPlainText())

		for i, j, k in zip(self.pvList, self.lowerList, self.upperList):
			self.thread = self.threading.Thread(target = self.threads.Worker(i, j, k, self.numShots, self.repRate).run)
			self.thread.daemon = True
			self.thread.start()
			print "thread " + i + " started"

	def appendToList(self):
		self.pvName = str(self.view.comboBox.currentText())
		self.lower = float(self.view.plainTextEdit.toPlainText())
		self.upper = float(self.view.plainTextEdit_2.toPlainText())
		self.pvList.append(self.pvName)
		self.lowerList.append(self.lower)
		self.upperList.append(self.upper)
		self.view.plainTextEdit1.insertPlainText(self.pvName+"\n")

	def addPVToList(self):
		self.pvList = []
		self.pvName = str(self.view.plainTextEdit_3.toPlainText())
		self.pvList.append(self.pvName)
		self.view.retranslateUi.comboBox.addItem(self.pvName)
		if self.view.radioButton.isChecked():
			self.model.numList.append(self.pvName)
		elif self.view.radioButton_2.isChecked():
			self.model.arrayList.append(self.pvName)
		self.view.comboBox.addItems(self.pvList)
