from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage
import sys,os
import testview as view
import numpy as np
import pyqtgraph as pg
import scanner
#import matplotlib.pyplot as plt
#import controller
#import striptool

class Worker(QRunnable):
    '''
    Worker thread
    '''

    @pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        print("Thread start") 
        time.sleep(5)
        print("Thread complete")





class testclassforsignals(QtCore.QObject): 
# A test class that emits signals 
# It could do anything and emit signals which
# for example can make a graph change on a UI. 
# I want it to know nothing about the UI, so
# that it could be a completely separate, encapsulated piece of code 
# To emit signals it has to inherit from QObject
#
# create signals    
    changedval = pyqtSignal(int, int, int)
# function which changes the values of the signals
    def generate(self):
        print("Hello!!! You've pushed the button")  
        col = 0    
        for i in range(5):
            for j in range(5):
                col = col + 1
                xval = i
                yval = j
                charge = col*10   
                self.changedval.emit(xval,yval,charge)
 
class App(QtGui.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.view = view.Ui_MainWindow()
        self.MainWindow = QtGui.QMainWindow()
        self.view.setupUi(self.MainWindow)
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
# application which creates a gui and graph 
# and button. The button starts the test class which generates the signal
# the graph then updates from the signal 
#
# first connect the test signal class function to button on gui        
        self.mygenerator = testclassforsignals()
        self.view.pushButton.clicked.connect(self.mygenerator.generate)  
        self.myscanner = scanner.chargescanner()

        self.view.pushButton.clicked.connect(self.fn_worker) 
  		
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
       
#        self.mygenerator.changedval.connect(self.get_data_vals)
        self.myscanner.changedval.connect(self.get_data_values)    
        self.myscanner.changedlogtxt.connect(self.get_text_output)    
 
    
 
 
        self.MainWindow.show()
        self.processEvents() # otherwise gui window will freeze/hang during data collection

        
    @pyqtSlot(int, int, int)
    def get_data_vals(self,arg1,arg2,arg3):
        myspot = []
        ch = 250
        revarg3 =  300 - 70 - ch
        myspot.append({'pos': (arg1, arg2), 'size': 0.5, 'pen': {'color': 'w', 'width': 2}, 'brush':pg.intColor(revarg3, 300)}) 
        self.s3.addPoints(myspot)
        print9("Hiya", arg1, arg2, arg3, revarg3) 
 
    @pyqtSlot(float, float, float,float)
    def get_data_values(self,arg1,arg2,arg3,arg4):
        myspot = []
        revarg3 = int(300 - 70 - arg3) 
        myspot.append({'pos': (arg1, arg2), 'size': 0.5, 'pen': {'color': 'w', 'width': 2}, 'brush':pg.intColor(revarg3, 300)}) 
        self.s3.addPoints(myspot)
        print("Hiya", arg1, arg2, arg3, revarg3, arg4)
        self.processEvents()
        
    @pyqtSlot(str)
    def get_text_output(self, arg1):
        self.view.textBrowser.append(arg1)
        self.processEvents() 
  
    def fn_worker()
        worker = Worker()
		self.threadpool.start(worker)
		
        self.myscanner.doscan(\
              self.view.doubleSpinBox.value(),\
              self.view.doubleSpinBox_2.value(),\
              int(self.view.doubleSpinBox_3.value()),\
              self.view.doubleSpinBox_6.value(),\
              self.view.doubleSpinBox_4.value(),\
              int(self.view.doubleSpinBox_5.value()) )


        
if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
