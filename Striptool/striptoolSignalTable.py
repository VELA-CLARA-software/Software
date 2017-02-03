import sys,os
# import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import time
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
import yaml

stream = file('settings.yaml', 'r')
magnets = yaml.load(stream)

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

Qtableau20 = [QColor(i,j,k) for (i,j,k) in tableau20]

def createRandomSignal(offset=0):
    signalValue = np.sin(2*2*np.pi*time.time()+0.05)+np.sin(1.384*2*np.pi*time.time()-0.1)+0.5*np.random.normal()
    return signalValue+offset

class signalTypeComboBox(QtGui.QComboBox):
    def __init__(self, comboID, mainForm):
        super(signalTypeComboBox, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm
        self.connect(self, QtCore.SIGNAL("currentIndexChanged (const QString&)"), self.indexChanged)

    def indexChanged(self, ind):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        print 'comboID = ', self.__comboID, 'ind = ', ind
        self.__mainForm.emit(QtCore.SIGNAL("firstColumnComboBoxChanged(PyQt_PyObject,PyQt_PyObject)"), self.__comboID, ind)

class signalElementComboBox(QtGui.QComboBox):
    def __init__(self, comboID, mainForm):
        super(signalElementComboBox, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm
        self.connect(self, QtCore.SIGNAL("currentIndexChanged (const QString&)"), self.indexChanged)

    def indexChanged(self, ind):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.emit(QtCore.SIGNAL("secondColumnComboBoxChanged(PyQt_PyObject,PyQt_PyObject)"), self.__comboID, ind)

class signalPVComboBox(QtGui.QComboBox):
    def __init__(self, comboID, mainForm):
        super(signalPVComboBox, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm

        self.connect(self, QtCore.SIGNAL("currentIndexChanged (const QString&)"), self.indexChanged)

    def indexChanged(self, ind):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.emit(QtCore.SIGNAL("thirdColumnComboBoxChanged(PyQt_PyObject,PyQt_PyObject)"), self.__comboID, ind)

class signalRateComboBox(QtGui.QComboBox):
    def __init__(self, comboID, mainForm):
        super(signalRateComboBox, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm

        self.connect(self, QtCore.SIGNAL("currentIndexChanged (const QString&)"), self.indexChanged)

    def indexChanged(self, ind):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.emit(QtCore.SIGNAL("signalRateChanged(PyQt_PyObject,PyQt_PyObject)"), self.__comboID, ind)

class colourPickerButton(QtGui.QPushButton):
    def __init__(self, comboID, mainForm):
        super(colourPickerButton, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm
        self.connect(self, QtCore.SIGNAL("clicked ()"), self.buttonPushed)

    def buttonPushed(self):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.emit(QtCore.SIGNAL("colourPickerButtonPushed(PyQt_PyObject)"), self.__comboID)

class signalTable(QWidget):
    def __init__(self, parent = None, MagnetController=None, BPMController=None):
        super(signalTable, self).__init__(parent)
        self.setMaximumHeight(100)
        self.magnets = MagnetController
        self.bpms = BPMController
        self.stripTool = parent
        self.rowNumber = 0
        self.penColors = {}
        self.rowWidgets = {}
        for i in range(len(Qtableau20)):
            self.penColors[i] = Qtableau20[2*i % 20]
        ''' create selectionBox '''
        self.selectBox = self.selectionBox()
        ''' create tableWidget and pushButton '''
        vBoxlayoutParameters = QVBoxLayout()
        vBoxlayoutParameters.addWidget(self.selectBox,       1)
        self.setLayout(vBoxlayoutParameters)
        self.connect(self, QtCore.SIGNAL("firstColumnComboBoxChanged(PyQt_PyObject, PyQt_PyObject)"), self.changeSecondCombo)
        self.connect(self, QtCore.SIGNAL("firstColumnComboBoxChanged(PyQt_PyObject, PyQt_PyObject)"), self.changeThirdComboFromFirst)
        self.connect(self, QtCore.SIGNAL("colourPickerButtonPushed(PyQt_PyObject)"), self.colorPicker)
        self.stripTool.signalAdded.connect(self.updateColourBox)

    def addRow(self, name, functionForm, functionArgument, freq, colourpickercolour):
        if functionForm[0] == '':
            functionName = functionForm[1]
            testFunction = lambda: getattr(self.magnets,functionName)(functionArgument)
        else:
            functionName = functionForm[1]
            function = eval(functionForm[0])
            testFunction = lambda: getattr(function,functionName)(functionArgument)
        # functionName = 'createRandomSignal'
        # testFunction = lambda: globals()[functionName](-0.5)

        self.stripTool.addSignal(name=name,pen=colourpickercolour, function=testFunction, timer=1.0/freq)
        self.stripTool.handleSplitterButton(False)
        self.stripTool.handleSplitterButton(False)

    def updateColourBox(self):
        self.rowNumber = self.rowNumber + 1
        self.colorbox.setColor(self.penColors[self.rowNumber])

    def selectionBox(self):
        self.selectionBoxlayout = QHBoxLayout()
        widget = QtGui.QWidget()
        combo1=signalTypeComboBox(0, self)
        combo2=signalElementComboBox(0, self)
        combo3=signalPVComboBox(0, self)
        combo4=signalRateComboBox(0, self)
        self.addButton = QPushButton('Add Signal')
        self.addButton.setFixedWidth(100)
        self.addButton.clicked.connect(self.addTableRow)
        combo1.addItems(('Off','Quads','Dipoles','Correctors','BPMs'))
        combo2.addItems(magnets['Off']['Names'])
        combo3.addItems(magnets['Off']['PVs'].keys())
        combo4.addItems([i + ' Hz'for i in ('1','5','10','25','50','100')])
        combo1.setEditable(True)
        combo1.lineEdit().setReadOnly(True);
        combo1.lineEdit().setAlignment(Qt.AlignCenter);
        combo1.setMinimumWidth(80)
        combo1.setMaximumWidth(100)
        combo2.setEditable(True)
        combo2.lineEdit().setReadOnly(True);
        combo2.lineEdit().setAlignment(Qt.AlignCenter);
        combo2.setMinimumWidth(80)
        combo2.setMaximumWidth(100)
        combo3.setEditable(True)
        combo3.lineEdit().setReadOnly(True);
        combo3.lineEdit().setAlignment(Qt.AlignCenter);
        combo3.setMinimumWidth(80)
        combo3.setMaximumWidth(100)
        combo4.setEditable(True)
        combo4.lineEdit().setReadOnly(True);
        combo4.lineEdit().setAlignment(Qt.AlignCenter);
        combo4.setCurrentIndex(2)
        combo4.setMinimumWidth(80)
        combo4.setMaximumWidth(100)
        self.colorbox = pg.ColorButton()
        self.colorbox.setMinimumWidth(60)
        self.colorbox.setMaximumWidth(80)
        self.colorbox.setFlat(True)
        if(self.rowNumber < 0):
            self.colorbox.setColor(self.penColors[0])
        else:
            self.colorbox.setColor(self.penColors[self.rowNumber])
        self.selectionBoxlayout.addWidget(combo1,2)
        self.selectionBoxlayout.addWidget(combo2,3)
        self.selectionBoxlayout.addWidget(combo3,2)
        self.selectionBoxlayout.addWidget(combo4,1)
        self.selectionBoxlayout.addWidget(self.colorbox,1)
        self.selectionBoxlayout.addWidget(self.addButton,1)
        widget.setLayout(self.selectionBoxlayout)
        widget.setMaximumHeight(100)
        return widget

    def addTableRow(self):
        row = self.rowNumber
        combo1index = str(self.selectBox.children()[1].currentText())
        combo1text = str(self.selectBox.children()[1].currentText())
        combo2index = self.selectBox.children()[2].currentIndex()
        combo3index = self.selectBox.children()[3].currentIndex()
        combo3text = str(self.selectBox.children()[3].currentText())
        combo4index = self.selectBox.children()[4].currentIndex()
        functionArgument = magnets[combo1text]['Names'][combo2index]
        name = magnets[combo1index]['Names'][combo2index]+'.'+magnets[combo1index]['PVs'].keys()[combo3index]
        freq = int(('1','5','10','25','50','100')[combo4index])
        functionForm = magnets[combo1index]['PVs'][combo3text]
        colourpickercolour = self.selectBox.children()[5]._color
        if combo1index > 0:
            self.addRow(name, functionForm, functionArgument, freq, colourpickercolour)

    def changeSecondCombo(self, idnumber, ind):
        combo2 = self.selectBox.children()[2]
        if combo2 != None:
            combo2.clear()
            combo2.addItems(magnets["%s"%(ind)]['Names'])

    def changeThirdComboFromFirst(self, idnumber, ind):
        combo1 = self.selectBox.children()[1]
        combo2 = self.selectBox.children()[2]
        combo3 = self.selectBox.children()[3]
        if combo3 != None:
            signalType = str(combo1.currentText())
            signalName = str(combo2.currentText())
            signalPVName = str(combo3.currentText())
            if not(signalPVName in magnets["%s"%(signalType)]['PVs'].keys()):
                combo3.clear()
                combo3.addItems(magnets["%s"%(signalType)]['PVs'].keys())

    def changeThirdComboFromSecond(self, idnumber, ind):
        combo3 = self.selectBox.children()[3]
        combo1 = self.selectBox.children()[1]
        if combo3 != None:
            signalType = combo1.currentText()
            combo3.clear()
            combo3.addItems(magnets["%s"%(signalType)]['PVs'].keys())

    def colorPicker(self):
        row = self.tableWidget.indexAt(QApplication.focusWidget().pos()).row()
        signalIndex = self.rowWidgets.keys()[self.rowWidgets.values().index(self.tableWidget.cellWidget(row,5))]
        color = QtGui.QColorDialog.getColor(Qtableau20[2*signalIndex % 20])
        self.tableWidget.cellWidget(row, 5).setStyleSheet("border: none; background-color: %s" % color.name())
        self.penColors[signalIndex] = color
