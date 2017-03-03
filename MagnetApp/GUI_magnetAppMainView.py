#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from Ui_magnetAppMainView import Ui_magnetAppMainView
from GUI_magnetWidget import GUI_magnetWidget

class GUI_magnetAppMainView(QtGui.QMainWindow, Ui_magnetAppMainView):
    closing = QtCore.pyqtSignal()# custom close signal to send to controller
    def __init__(self):
        QtGui.QWidget.__init__(self)
        # startup crap
        self.setupUi(self)
        self.setWindowTitle("VELA - CLARA Magnet App")
        self.logo  = QtGui.QPixmap(globals.claraIcon)
        self.scaledLogo =  self.logo.scaled(self.logoLabel.size(), QtCore.Qt.KeepAspectRatio)
        self.logoLabel.setPixmap(self.scaledLogo)
        self.setWindowIcon(QtGui.QIcon(globals.appIcon))
        self.appPixMap = QtGui.QPixmap(globals.appIcon)
        self.scaledAppPixMapo = self.appPixMap.scaled(self.logoLabel.size(), QtCore.Qt.KeepAspectRatio)
        self.iconLabel.setPixmap(self.scaledAppPixMapo)
        self.quadWidgets = {}
        self.solWidgets = {}
        self.dipWidgets = {}
        self.corWidgets = {}
        # ok so i set these like this... meh, just fixes the dimensions of the window
        # when we start with different machien areas this may neeed to be revisted
        self.maxNumQuadPerRow = 5
        self.maxNumCorPerRow  = 7
        self.quadCount = 0
        self.dipCount = 0
        self.solCount = 0
        self.corCount = 0
        self.currentQuadRow = -1
        self.currentCorRow  = -1
        self.currentQuadCol = 0
        self.currentCorCol  = 0
        # simple signals don't need to go back to the controller
        self.dipSelectAll.clicked.connect(   lambda:self.activateMags(self.dipWidgets,True  ) )
        self.dipSelectNone.clicked.connect(  lambda:self.activateMags(self.dipWidgets,False ) )
        self.solSelectAll.clicked.connect(   lambda:self.activateMags(self.solWidgets,True  ) )
        self.solSelectNone.clicked.connect(  lambda:self.activateMags(self.solWidgets,False ) )
        self.quadSelectAll.clicked.connect(  lambda:self.activateMags(self.quadWidgets,True ) )
        self.quadSelectNone.clicked.connect( lambda:self.activateMags(self.quadWidgets,False) )
        self.corSelectAll.clicked.connect(   lambda:self.activateMags(self.corWidgets,True  ) )
        self.corSelectNone.clicked.connect(  lambda:self.activateMags(self.corWidgets,False ) )
        self.mainSelectAll.clicked.connect( self.activateAll )
        self.selectNone.clicked.connect( self.deActivateAll )
        #self.closing.connect(self.close)

    def closeEvent(self,event):
        self.closing.emit()

    def updateMagnetWidgets(self):
        for mag in self.quadWidgets.values():
            mag.updateMagWidget()
        for mag in self.solWidgets.values():
            mag.updateMagWidget()
        for mag in self.dipWidgets.values():
            mag.updateMagWidget()
        for mag in self.corWidgets.values():
            mag.updateMagWidget()

    # add magnet widgets to the main view - dips and sol in one column ....
    def addDip(self, magnetObj):
        self.dipWidgets[magnetObj.name] = GUI_magnetWidget()
        self.dip_Grid_Box.addWidget(self.dipWidgets[magnetObj.name],self.dipCount,0)
        self.dipCount += 1
    def addSol(self, magnetObj):
        self.solWidgets[magnetObj.name] = GUI_magnetWidget()
        self.sol_Grid_Box.addWidget(self.solWidgets[magnetObj.name])
        self.solCount += 1
    # add magnet widgets to the main view - quads and cors in a grid ...
    def addQuad(self, magnetObj):
        self.quadWidgets[magnetObj.name] = GUI_magnetWidget()
        self.r = self.quadCount % self.maxNumQuadPerRow
        if self.r == 0:
            self.currentQuadRow += 1
            self.currentQuadCol = 0
        self.quad_Grid_Box.addWidget(self.quadWidgets[magnetObj.name], self.currentQuadRow, self.currentQuadCol)
        self.currentQuadCol += 1
        self.quadCount += 1
    def addCor(self, magnetObj ):
        self.corWidgets[magnetObj.name] = GUI_magnetWidget()
        self.r = self.corCount % self.maxNumCorPerRow
        if self.r == 0:
            self.currentCorRow += 1
            self.currentCorCol = 0
        self.cor_Grid_Box.addWidget(self.corWidgets[magnetObj.name], self.currentCorRow, self.currentCorCol)
        self.currentCorCol += 1
        self.corCount += 1
    # after adding magnet widgets add in a spacer to make things look a bit neater
    def mainResize(self):
        self.solFrameLayout.addItem(QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
        self.dipFrameLayout.addItem(QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
        self.quadFrameLayout.addItem(QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
        self.corFrameLayout.addItem(QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
    # set check boxes true or false
    def activateMags(self,magnets,value):
        for mag  in magnets.values():
            mag.mag_Active.setCheckState(value)
    def activateAll(self):
        self.activateMags(self.dipWidgets,True)
        self.activateMags(self.solWidgets,True)
        self.activateMags(self.corWidgets,True)
        self.activateMags(self.quadWidgets,True)
    def deActivateAll(self):
        self.activateMags(self.dipWidgets,False)
        self.activateMags(self.solWidgets,False)
        self.activateMags(self.corWidgets,False)
        self.activateMags(self.quadWidgets,False)
    # get names from active check boxes
    def getActiveQuads(self):
        self.returnmagnames= []
        for mag in self.quadWidgets:
            if self.quadWidgets[mag].isActive:
                self.returnmagnames.append(mag)
        return self.returnmagnames
    def getActiveDips(self):
        self.returnmagnames= []
        for mag in self.dipWidgets:
            if self.dipWidgets[mag].isActive:
                self.returnmagnames.append(mag)
        return self.returnmagnames
    def getActiveSols(self):
        self.returnmagnames= []
        for mag in self.solWidgets:
            if self.solWidgets[mag].isActive:
                self.returnmagnames.append(mag)
        return self.returnmagnames
    def getActiveNames(self):
        self.returnmagnames = self.getActiveQuads() + self.getActiveDips() + self.getActiveSols()
        return self.returnmagnames

