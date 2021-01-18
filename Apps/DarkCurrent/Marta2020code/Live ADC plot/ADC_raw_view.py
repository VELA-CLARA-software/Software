"""
View for the ADC raw live plot

@author: MFurmaniak
"""
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget

#=========================================================================================================================================================================       
class graph(object):
    '''Window with a graph'''
    
    def __init__(self):
        self.MainWindow = QtGui.QMainWindow()
        self.MainWindow.setObjectName("Graph")
        self.MainWindow.resize(1100, 430)
        self.centralwidget = QtGui.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = GraphicsLayoutWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(50, 50, 1000, 361))
        self.graphicsView.setObjectName("graphicsView")
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)
        
        self.text = QtGui.QLabel(self.MainWindow)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(100)
        self.text.setFont(font)
        self.text.setGeometry(QtCore.QRect(500, 10, 310, 31))

        self.retranslateUi()

        # creating a plot
        self.dataplot = pg.PlotItem(labels = {'left': ('ADC counts')}, title = 'Signal from the ADC')
        self.graphicsView.addItem(self.dataplot)
        
        # Set pxMode=False to allow spots to transform with the view
        self.s3 = pg.PlotDataItem(pxMode=False)   
        self.dataplot.addItem(self.s3)
        
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
        
    def show(self):
        self.MainWindow.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("Graph", "Graph", None))
        
    def retranslateUi_now(self, charge):
        _translate = QtCore.QCoreApplication.translate
        self.text.setText(_translate("Graph", "Charge: %d pC" % charge, None))