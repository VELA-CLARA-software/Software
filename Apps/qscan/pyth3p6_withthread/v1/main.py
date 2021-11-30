from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage
from PyQt5.QtCore import *
import sys,os
import testview as view
import numpy as np
import pyqtgraph as pg
import doingmodule

         
 
class App(QtGui.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.view = view.Ui_MainWindow()
        self.MainWindow = QtGui.QMainWindow()
        self.view.setupUi(self.MainWindow)
# application which creates a gui with button 
# and graph and text box. 

# the app will be threaded so that the 'doing stuff' part of the code can run 
# without the GUI becoming unresponsive      
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        
# connect the 'doing function' to button on gui                
#        self.view.pushButton.clicked.connect(self.doingfunction)

        
        self.view.pushButton.clicked.connect(self.doingfunction)


# add a plot to the window
        self.s3 = pg.ScatterPlotItem(pxMode=False)   ## Set pxMode=False to allow spots to transform with the view        
        self.dataplot = self.view.graphicsView.addPlot(title="My Data")        
        self.dataplot.addItem(self.s3)
        self.dataplot.addLegend()        
        self.view.label.setPixmap(QtGui.QPixmap("legend2.png").scaled(300,300))
        
# Start with some text in the text browser.         
        self.view.textBrowser.append("Scan Log Commencing:");
        		
	 
        self.MainWindow.show()

         

# This is just an interface function to the class which actually does the stuff.
# Within this function the signals are connected to the GUI
# and the execution of the 'doing stuff' code is threaded. 
# the threading relies on mechanics from the 'Worker class' pattern ...
#(... Martin Fitzpatrick, 'Multithreading PyQt applications with QThreadPool' ...
# ... https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool/)
# most of the threading mechanics are containied in the module that 'does stuff'  
    def doingfunction(self):
        # print('hello in mainapp:scanfunction')
        mydoingclass = doingmodule.doingclass()
#        mydoingclass.setparams(2,4,2,1,3,2) 
        mydoingclass.setparams(\
            self.view.doubleSpinBox.value(),\
            self.view.doubleSpinBox_2.value(),\
            int(self.view.doubleSpinBox_3.value()),\
            self.view.doubleSpinBox_6.value(),\
            self.view.doubleSpinBox_4.value(),\
            int(self.view.doubleSpinBox_5.value()) )  
        mydoingclass.changedval.connect(self.get_data_values) 
        mydoingclass.changedlogtxt.connect(self.get_text_output)   
        doingworker = doingmodule.Worker(mydoingclass.domystuff)
        self.threadpool.start(doingworker)
     
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
