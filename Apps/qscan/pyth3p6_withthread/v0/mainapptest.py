from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage
from PyQt5.QtCore import *
import sys,os
import testview as view
import numpy as np
import pyqtgraph as pg
import scanner
#import matplotlib.pyplot as plt
#import controller
#import striptool
         
#class Worker(QRunnable):
#    '''
#    Worker thread
#    '''
#
#    @pyqtSlot()
#    def run(self):
#        '''
#        Your code goes in this function
#        '''
#        print("Thread start") 
#        time.sleep(5)
#        print("Thread complete")         
         
 
class App(QtGui.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.view = view.Ui_MainWindow()
        self.MainWindow = QtGui.QMainWindow()
        self.view.setupUi(self.MainWindow)
# application which creates a gui and graph 
# and button. The button starts the test class which generates the signal
# the graph then updates from the signal 
#
# first connect the test signal class function to button on gui        
 #       self.mygenerator = testclassforsignals()
 #       self.view.pushButton.clicked.connect(self.mygenerator.generate)  
#        self.myscanner = scanner.chargescanner()
#        self.view.pushButton.clicked.connect(self.myscanner.generatedummydata)  # testing: generate fake data without operating machine
        
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        
        self.view.pushButton.clicked.connect(self.scanfunction)
#        print("****TEST********",self.view.doubleSpinBox.value())
#        self.myscanner.setxrange(self.view.doubleSpinBox.value(),self.view.doubleSpinBox_2.value(),int(self.view.doubleSpinBox_3.value()))
#        self.myscanner.setxrange(self.view.doubleSpinBox_4.value(),self.view.doubleSpinBox_5.value(),int(self.view.doubleSpinBox_6.value()))
#        self.view.pushButton.clicked.connect(self.myscanner.doscan)
#        theval = self.view.doubleSpinBox.value()
#        self.view.pushButton.clicked.connect(lambda: self.myscanner.doscan(float(theval)))  		
#        self.view.pushButton.clicked.connect(\
#		   lambda: self.myscanner.doscan(\
#              self.view.doubleSpinBox.value(),\
#			  self.view.doubleSpinBox_2.value(),\
#			  int(self.view.doubleSpinBox_3.value()),\
#			  self.view.doubleSpinBox_6.value(),\
#			  self.view.doubleSpinBox_4.value(),\
#			  int(self.view.doubleSpinBox_5.value()) ) )  
# add a plot to the window
        self.s3 = pg.ScatterPlotItem(pxMode=False)   ## Set pxMode=False to allow spots to transform with the view
        
        self.dataplot = self.view.graphicsView.addPlot(title="My Data")        
        self.dataplot.addItem(self.s3)
        self.dataplot.addLegend()
        
        self.view.label.setPixmap(QtGui.QPixmap("legend2.png").scaled(300,300))
        
        self.view.textBrowser.append("Scan Log Commencing:");
        
#        print("THIS!!!!!!!!",self.view.doubleSpinBox_5.value())
		
#		self.myscanner.setxmin(self.view.doubleSpinBox_5.value())
		
		
#        exit()
		
#        self.textbox = self.textBrowser
       
#        self.myscanner.changedval.connect(self.get_data_values)   
#        self.myscanner.changedlogtxt.connect(self.get_text_output)    
 
    
 
 
        self.MainWindow.show()
        print("OK I've shown the windows")
#        self.processEvents() # This is redudnant I think 
         

    def scanfunction(self):
        print('hello in mainapp:scanfunction')
        myscanner = scanner.chargescanner()
        myscanner.changedval.connect(self.get_data_values) 
        myscanner.changedlogtxt.connect(self.get_text_output)   
        scworker = scanner.Worker(myscanner.domyscan)
        print('mainapp:scanfunction: Ive instantiated the worker class')
#        scworker.signals.result.connect(scworker.print_output)        
        self.threadpool.start(scworker)
     
    @pyqtSlot(int, int, int)
    def get_data_vals(self,arg1,arg2,arg3):
        myspot = []
        ch = 250
        revarg3 =  300 - 70 - ch
        myspot.append({'pos': (arg1, arg2), 'size': 0.5, 'pen': {'color': 'w', 'width': 2}, 'brush':pg.intColor(revarg3, 300)}) 
        self.s3.addPoints(myspot)
        print("Hiya", arg1, arg2, arg3, revarg3) 
 
    @pyqtSlot(float, float, float,float)
    def get_data_values(self,arg1,arg2,arg3,arg4):
        myspot = []
        revarg3 = int(300 - 70 - arg3) 
        myspot.append({'pos': (arg1, arg2), 'size': 0.5, 'pen': {'color': 'w', 'width': 2}, 'brush':pg.intColor(revarg3, 300)}) 
        self.s3.addPoints(myspot)
        print("Hiya", arg1, arg2, arg3, revarg3, arg4)
#        self.processEvents() # to get continually updated gui 
        
    @pyqtSlot(str)
    def get_text_output(self, arg1):
        self.view.textBrowser.append(arg1)
#        self.processEvents() # to get continually updated gui 
        
if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
