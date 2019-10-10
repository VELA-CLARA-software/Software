# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 10:35:48 2019

@author: qqi63789
"""

from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget

#=========================================================================================================================================================================
class MainWindow(object):
    '''The main GUI where user specifies 
        the sol, bsol and rf values'''
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.counter = 0
        
        self.Dialog = QtGui.QDialog()
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(390, 316)
        
        self.buttonBox_2 = QtGui.QDialogButtonBox(self.Dialog)
        self.buttonBox = QtGui.QDialogButtonBox(self.Dialog)
        
        self.buttonBox.setGeometry(QtCore.QRect(30, 270, 261, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        
        self.buttonBox_2.setGeometry(QtCore.QRect(30, 270, 341, 32))
        self.buttonBox_2.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_2.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox_2.setObjectName("buttonBox_2")
        
        self.l = QtGui.QLabel(self.Dialog)
        self.l.setGeometry(QtCore.QRect(20, 10, 211, 31))
        
        self.label = QtGui.QLabel(self.Dialog)
        self.label.setGeometry(QtCore.QRect(110, 10, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.gridLayoutWidget = QtGui.QWidget(self.Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(80, 120, 234, 86))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        
        self.label_7 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        
        # minimum sol- input
        min_sol = self.spinBox = QtGui.QSpinBox(self.gridLayoutWidget)
        min_sol.setMinimum(-300)
        min_sol.setMaximum(300)
        min_sol.setProperty("value", -1)
        min_sol.setObjectName("min_sol")
        self.gridLayout.addWidget(min_sol, 1, 1, 1, 1)
        self.min_sol = min_sol                                                 #defining a global variable in the class
        
        # maximum bsol- input
        max_bsol = self.spinBox_4 = QtGui.QSpinBox(self.gridLayoutWidget)
        max_bsol.setMinimum(-8)
        max_bsol.setMaximum(8)
        max_bsol.setProperty("value", 1)
        max_bsol.setObjectName("max_bsol")
        self.gridLayout.addWidget(max_bsol, 2, 3, 1, 1)
        self.max_bsol = max_bsol
        
        # step bsol- input
        step_bsol = self.spinBox_6 = QtGui.QSpinBox(self.gridLayoutWidget)
        step_bsol.setMinimum(1)
        step_bsol.setMaximum(17)
        step_bsol.setProperty("value", 2)
        step_bsol.setObjectName("step_bsol")
        self.gridLayout.addWidget(step_bsol, 2, 2, 1, 1)
        self.step_bsol = step_bsol
        
        # maximum sol- input
        max_sol = self.spinBox_2 = QtGui.QSpinBox(self.gridLayoutWidget)
        max_sol.setMinimum(-300)
        max_sol.setMaximum(300)
        max_sol.setProperty("value", 1)
        max_sol.setObjectName("max_sol")
        self.gridLayout.addWidget(max_sol, 1, 3, 1, 1)
        self.max_sol = max_sol
        
        # step sol- input
        step_sol = self.spinBox_5 = QtGui.QSpinBox(self.gridLayoutWidget)
        step_sol.setMinimum(1)
        step_sol.setMaximum(601)
        step_sol.setProperty("value", 2)
        step_sol.setObjectName("step_sol")
        self.gridLayout.addWidget(step_sol, 1, 2, 1, 1)
        self.step_sol = step_sol
        
        # minimum bsol- input
        min_bsol = self.spinBox_3 = QtGui.QSpinBox(self.gridLayoutWidget)
        min_bsol.setMinimum(-8)
        min_bsol.setMaximum(8)
        min_bsol.setProperty("value", -1)
        min_bsol.setObjectName("min_bsol")
        self.gridLayout.addWidget(min_bsol, 2, 1, 1, 1)
        self.min_bsol = min_bsol
        
        # minimum rf amplitude- input
        min_rf = self.spinBox_7 = QtGui.QSpinBox(self.gridLayoutWidget)
        min_rf.setMinimum(1)
        min_rf.setMaximum(100)
        min_rf.setProperty("value", 70)
        min_rf.setObjectName("min_rf")
        self.gridLayout.addWidget(min_rf, 3, 1, 1, 1)
        self.min_rf = min_rf
        
        # step rf amplitude- input
        step_rf = self.spinBox_8 = QtGui.QSpinBox(self.gridLayoutWidget)
        step_rf.setMinimum(1)
        step_rf.setMaximum(100)
        step_rf.setProperty("value", 1)
        step_rf.setObjectName("step_rf")
        self.gridLayout.addWidget(step_rf, 3, 2, 1, 1)
        self.step_rf = step_rf
        
        # maximum rf amplitude- input
        max_rf = self.spinBox_9 = QtGui.QSpinBox(self.gridLayoutWidget)
        max_rf.setMinimum(1)
        max_rf.setMaximum(100)
        max_rf.setProperty("value", 70)
        max_rf.setObjectName("max_rf")
        self.gridLayout.addWidget(max_rf, 3, 3, 1, 1)
        self.max_rf = max_rf
        
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)
        
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 3, 1, 1)
        
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        
        # sol [A]
        self.label_8 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 4, 1, 1)
        
        # bsol [A]
        self.label_9 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_9.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 2, 4, 1, 1)
        
        # rf [MV/m]
        self.label_10 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_10.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 3, 4, 1, 1)
        
        self.textBrowser = QtGui.QTextBrowser(self.Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(40, 50, 321, 41))
        self.textBrowser.setObjectName("textBrowser")
        
        # warning text at the bottom of the window
        self.warning = QtGui.QLabel(self.Dialog)
        self.warning.setGeometry(QtCore.QRect(30, 250, 310, 31))
        
        font.setPointSize(7)
        font.setBold(False)
        font.setWeight(75)
        self.warning.setFont(font)
        self.warning.setObjectName("warning")

        self.retranslateUi()
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
    
        self.Dialog.show()
        
        
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Dark Current Measurement"))
        self.l.setText(_translate("Dialog", "Start"))
        self.warning.setText(_translate("Dialog", "Please note that, after clicking OK, this window \n will freeze for approx. 20s"))
        self.label.setText(_translate("Dialog", "Dark current measurement"))
        self.label_6.setText(_translate("Dialog", "BSOL"))
        self.label_4.setText(_translate("Dialog", "# of samples"))
        self.label_3.setText(_translate("Dialog", "Max"))
        self.label_5.setText(_translate("Dialog", "SOL"))
        self.label_2.setText(_translate("Dialog", "Min"))
        self.label_7.setText(_translate("Dialog", "RF Amp"))
        self.label_8.setText(_translate("Dialog", "A"))
        self.label_9.setText(_translate("Dialog", "A"))
        self.label_10.setText(_translate("Dialog", "MV/m"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Pick the SOL, BSOL and RF amplitude values.</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> Note: SOL range +/- 300 A; BSOL range +/-8 A</p></body></html>"))
            
    def recurring_timer(self):
        self.counter +=1
        self.l.setText("Counter: %d" % self.counter)
 
#=========================================================================================================================================================================       
class classprogress(object):
    """ Window with life updates + progress bar """
    def __init__(self):
        self.Dialog = QtGui.QDialog()
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(411, 232)
        
        self.progressBar = QtGui.QProgressBar(self.Dialog)
        self.progressBar.setGeometry(QtCore.QRect(130, 160, 161, 31))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        
        self.gridLayoutWidget = QtGui.QWidget(self.Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(100, 30, 271, 81))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 1, 1, 1)
        
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        
        self.label_5 = QtGui.QLabel(self.Dialog)
        self.label_5.setGeometry(QtCore.QRect(170, 130, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        
        self.label_7 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 1, 1, 1)
        
    def show(self):
        self.Dialog.show()

    def retranslateUi(self, sol, bsol, rf):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Live", None))
        self.label.setText(_translate("Dialog", "SOL:", None))
        self.label_4.setText(_translate("Dialog", "%d A" % bsol, None))
        self.label_2.setText(_translate("Dialog", "BSOL:", None))
        self.label_3.setText(_translate("Dialog","%d A" % sol, None))
        self.label_5.setText(_translate("Dialog",'Loading...', None))
        self.label_6.setText(_translate("Dialog", "RF:", None))
        self.label_7.setText(_translate("Dialog", "%d MV/m" % rf, None))
    
    def finished(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_5.setText(_translate("Dialog",'Finished!', None))
        
    def progress_bar(self, percent):
        self.progressBar.setProperty("value", percent)

#=========================================================================================================================================================================       
class graph(object):
    
    def __init__(self):
        self.MainWindow = QtGui.QMainWindow()
        self.MainWindow.setObjectName("Graph")
        self.MainWindow.resize(650, 500)
        self.centralwidget = QtGui.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = GraphicsLayoutWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(100, 50, 461, 361))
        self.graphicsView.setObjectName("graphicsView")
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()

        self.dataplot = pg.PlotItem(labels = {'left': ('BSOL [A]'), 'bottom': ('SOL [A]')}, title = 'Charge')
        self.graphicsView.addItem(self.dataplot)
        self.colour_scale = pg.GradientLegend(size=(
                10,40), offset=(350, 20))
        self.colour_scale.setIntColorScale(-100,-18)
        self.colour_scale.setLabels({'':0, '':1})
        self.colour_scale.scale(1,1)  
        self.dataplot.addItem(self.colour_scale)

        self.s3 = pg.ScatterPlotItem(pxMode=False)   ## Set pxMode=False to allow spots to transform with the view
        self.dataplot.addItem(self.s3)
        
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
        
    def show(self):
        self.MainWindow.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("Graph", "Graph", None))
#
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    p = classprogress()
    p.retranslateUi(1,1,70)
    p.show()
    #g = graph()
    #g.show()
    #for i in range(20):
        #g.add_point(1,i,(i-2)*10)
    app.exec_()

