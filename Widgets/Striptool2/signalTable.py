import sys,os
# import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
# from PyQt5.QtCore import QtCore.QObject, QtCore.pyqtSignal, Qt
# from PyQt5.QtGui import QtGui.QHBoxLayout, QtGui.QVBoxLayout
# from PyQt5.QtWidgets import QtGui.QWidget, QPushButton, QLineEdit, QCheckBox
from PyQt4 import QtCore, QtGui
import time
import yaml
import string as string
import Software.Widgets.Striptool2.colours as colours

class signalTypeComboBox(QtGui.QComboBox):
    def __init__(self, comboID, mainForm):
        super(signalTypeComboBox, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm
        self.currentIndexChanged.connect(self.indexChanged)

    def indexChanged(self, ind):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.firstColumnComboBoxChanged.emit(self.__comboID, self.currentText())

class signalElementComboBox(QtGui.QComboBox):
    def __init__(self, comboID, mainForm):
        super(signalElementComboBox, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm
        self.currentIndexChanged.connect(self.indexChanged)

    def indexChanged(self, ind):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.secondColumnComboBoxChanged.emit(self.__comboID, self.currentText())

class signalPVComboBox(QtGui.QComboBox):
    def __init__(self, comboID, mainForm):
        super(signalPVComboBox, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm
        self.currentIndexChanged.connect(self.indexChanged)

    def indexChanged(self, ind):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.thirdColumnComboBoxChanged.emit(self.__comboID, self.currentText())

class signalRateComboBox(QtGui.QComboBox):
    def __init__(self, comboID, mainForm):
        super(signalRateComboBox, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm
        self.currentIndexChanged.connect(self.indexChanged)

    def indexChanged(self, ind):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.signalRateChanged.emit(self.__comboID, self.currentText())

class colourPickerButton(QtGui.QPushButton):
    def __init__(self, comboID, mainForm):
        super(colourPickerButton, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm
        self.clicked.connect(self.buttonPushed)

    def buttonPushed(self):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.colourPickerButtonPushed.emit(self.__comboID)

class customPVFunction(QtCore.QObject):
    def __init__(self, parent = None, pvid=None, GeneralController=None):
        super(customPVFunction, self).__init__(parent)
        self.pvid = pvid
        self.general = GeneralController

    def getValue(self):
        return float(self.general.getValue(self.pvid))

class signalTable(QtGui.QWidget):

    firstColumnComboBoxChanged = QtCore.pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')
    secondColumnComboBoxChanged = QtCore.pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')
    thirdColumnComboBoxChanged = QtCore.pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')
    signalRateChanged = QtCore.pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')
    colourPickerButtonPushed = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, parent = None, VELAMagnetController=None, CLARAMagnetController=None, BPMController=None, GeneralController=None):
        super(signalTable, self).__init__(parent)
        self.setMaximumHeight(100)
        self.stream = open('settings.yaml', 'r')
        self.settings = yaml.load(self.stream)
        self.stream.close()
        self.magnetnames = self.settings['magnets']
        self.headings = self.settings['headings']
        self.frequencies = self.settings['frequencies']
        self.VELAMagnets = VELAMagnetController
        self.CLARAMagnets = CLARAMagnetController
        self.bpms = BPMController
        self.general = GeneralController
        self.stripTool = parent
        self.rowNumber = 0
        self.penColors = {}
        self.rowWidgets = {}
        for i in range(len(colours.Qtableau20)):
            self.penColors[i] = colours.Qtableau20[2*i % 20]
        ''' create selectionBox '''
        self.customPVInput = False
        self.normalSelectionBox = self.createNormalSelectionBox()
        self.customSelectionBox = self.createCustomSelectionBox()
        ''' create tableWidget and pushButton '''
        vBoxlayoutParameters = QtGui.QVBoxLayout()
        vBoxlayoutParameters.addWidget(self.normalSelectionBox,1)
        vBoxlayoutParameters.addWidget(self.customSelectionBox,1)
        self.normalSelectionBox.show()
        self.customSelectionBox.hide()
        self.setLayout(vBoxlayoutParameters)
        self.firstColumnComboBoxChanged.connect(self.changeSecondCombo)
        self.secondColumnComboBoxChanged.connect(self.changeThirdComboFromSecond)
        self.colourPickerButtonPushed.connect(self.colorPicker)
        self.stripTool.signalAdded.connect(self.updateColourBox)
        self.pvids = []

    def addRow(self, name, functionForm, functionArgument, freq, colourpickercolour, logScale=False, **kwargs):
        if functionForm == 'custom':
            pvtype="DBR_DOUBLE"
            pvid = self.general.connectPV(str(functionArgument))
            if pvid is not 'FAILED':
                self.pvids.append(pvid)
                testFunction = customPVFunction(parent=self, pvid=pvid, GeneralController=self.general).getValue
                time.sleep(0.01)
                testFunction.getValue()
            else:
                print('Is this a valid PV? - ', functionArgument)
        # elif functionForm[0] == '':
        #     functionName = functionForm[1]
        #     testFunction = lambda: getattr(self.magnets,functionName)(functionArgument)
        else:
            functionName = functionForm[1]
            function = eval(functionForm[0])
            print('functionName = ', functionName)
            print('functionForm = ', functionForm)
            testFunction = lambda: getattr(function,functionName)(functionArgument)
        self.stripTool.addSignal(name=name, pen=colourpickercolour, function=testFunction, timer=1.0/freq, logScale=logScale)
        self.stripTool.records[name]['record'].start()

    def updateColourBox(self):
        self.rowNumber = self.rowNumber + 1
        self.normalcolorbox.setColor(self.penColors[self.rowNumber])
        self.customcolorbox.setColor(self.penColors[self.rowNumber])

    def createNormalSelectionBox(self):
        self.selectionBoxlayout = QtGui.QHBoxLayout()
        normalwidget = QtGui.QWidget()
        combo1=signalTypeComboBox(0, self)
        combo2=signalElementComboBox(0, self)
        combo3=signalPVComboBox(0, self)
        combo4=signalRateComboBox(0, self)
        addButton = QtGui.QPushButton('Add Signal')
        addButton.setFixedWidth(100)
        addButton.clicked.connect(self.addTableRow)
        combo1.addItems(self.headings)
        combo2.addItems(self.magnetnames['Off']['Names'])
        combo3.addItems(self.magnetnames['Off']['PVs'].keys())
        combo4.addItems([str(i) + ' Hz'for i in self.frequencies])
        combo1.setEditable(True)
        combo1.lineEdit().setReadOnly(True);
        combo1.lineEdit().setAlignment(QtCore.Qt.AlignCenter);
        combo1.setMinimumWidth(80)
        combo1.setMaximumWidth(100)
        combo2.setEditable(True)
        combo2.lineEdit().setReadOnly(True);
        combo2.lineEdit().setAlignment(QtCore.Qt.AlignCenter);
        combo2.setMinimumWidth(80)
        combo2.setMaximumWidth(100)
        combo3.setEditable(True)
        combo3.lineEdit().setReadOnly(True);
        combo3.lineEdit().setAlignment(QtCore.Qt.AlignCenter);
        combo3.setMinimumWidth(80)
        combo3.setMaximumWidth(100)
        combo4.setEditable(True)
        combo4.lineEdit().setReadOnly(True);
        combo4.lineEdit().setAlignment(QtCore.Qt.AlignCenter);
        combo4.setCurrentIndex(2)
        combo4.setMinimumWidth(80)
        combo4.setMaximumWidth(100)
        pvtextedit = QtGui.QLineEdit()
        pvtextedit.setMinimumWidth(240)
        pvtextedit.setMaximumWidth(300)
        self.normalcolorbox = pg.ColorButton()
        self.normalcolorbox.setMinimumWidth(60)
        self.normalcolorbox.setMaximumWidth(80)
        self.normalcolorbox.setFlat(True)
        if(self.rowNumber < 0):
            self.normalcolorbox.setColor(self.penColors[0])
        else:
            self.normalcolorbox.setColor(self.penColors[self.rowNumber])
        self.selectionBoxlayout.addWidget(combo1,2)
        self.selectionBoxlayout.addWidget(combo2,3)
        self.selectionBoxlayout.addWidget(combo3,2)
        self.selectionBoxlayout.addWidget(combo4,1)
        self.selectionBoxlayout.addWidget(self.normalcolorbox,1)
        self.selectionBoxlayout.addWidget(addButton,1)
        normalwidget.setLayout(self.selectionBoxlayout)
        normalwidget.setMaximumHeight(100)
        return normalwidget

    def createCustomSelectionBox(self):
        self.pvEditlayout = QtGui.QHBoxLayout()
        customwidget = QtGui.QWidget()
        combo1=signalTypeComboBox(0, self)
        combo4=signalRateComboBox(0, self)
        addButton = QtGui.QPushButton('Add Signal')
        addButton.setFixedWidth(100)
        addButton.clicked.connect(self.addTableRowCustom)
        self.logTickBox = QtGui.QCheckBox('Log Scale')
        combo1.addItems(self.headings)
        combo4.addItems([str(i) + ' Hz'for i in self.frequencies])
        combo1.setEditable(True)
        combo1.lineEdit().setReadOnly(True);
        combo1.lineEdit().setAlignment(QtCore.Qt.AlignCenter);
        combo1.setMinimumWidth(80)
        combo1.setMaximumWidth(100)
        combo4.setEditable(True)
        combo4.lineEdit().setReadOnly(True);
        combo4.lineEdit().setAlignment(QtCore.Qt.AlignCenter);
        combo4.setCurrentIndex(2)
        combo4.setMinimumWidth(80)
        combo4.setMaximumWidth(100)
        pvtextedit = QtGui.QLineEdit()
        pvtextedit.setMinimumWidth(230)
        pvtextedit.setMaximumWidth(290)
        self.customcolorbox = pg.ColorButton()
        self.customcolorbox.setMinimumWidth(60)
        self.customcolorbox.setMaximumWidth(80)
        self.customcolorbox.setFlat(True)
        if(self.rowNumber < 0):
            self.customcolorbox.setColor(self.penColors[0])
        else:
            self.customcolorbox.setColor(self.penColors[self.rowNumber])
        self.pvEditlayout.addWidget(combo1,2)
        self.pvEditlayout.addWidget(pvtextedit,5)
        self.pvEditlayout.addWidget(combo4,1)
        self.pvEditlayout.addWidget(self.logTickBox,1)
        self.pvEditlayout.addWidget(self.customcolorbox,1)
        self.pvEditlayout.addWidget(addButton,1)
        customwidget.setLayout(self.pvEditlayout)
        customwidget.setMaximumHeight(100)
        return customwidget

    def addTableRow(self):
        row = self.rowNumber
        combo1index = str(self.normalSelectionBox.children()[1].currentText())
        combo1text = str(self.normalSelectionBox.children()[1].currentText())
        combo2index = self.normalSelectionBox.children()[2].currentIndex()
        combo3index = self.normalSelectionBox.children()[3].currentIndex()
        combo3text = str(self.normalSelectionBox.children()[3].currentText())
        combo4index = self.normalSelectionBox.children()[4].currentIndex()
        if isinstance(self.magnetnames[combo1text]['Names'][combo2index], (tuple, list, set)):
            functionArgument = self.magnetnames[combo1text]['Names'][combo2index][0]
        else:
            functionArgument = self.magnetnames[combo1text]['Names'][combo2index]
        name = functionArgument+'.'+self.magnetnames[combo1index]['PVs'].keys()[combo3index]
        freq = int(self.frequencies[combo4index])
        functionForm = self.magnetnames[combo1index]['PVs'][combo3text]
        colourpickercolour = self.normalSelectionBox.children()[5]._color
        if combo1index > 0:
            self.addRow(name, functionForm, functionArgument, freq, colourpickercolour)

    def addTableRowCustom(self):
        row = self.rowNumber
        combo3index = self.pvEditlayout.itemAt(1).widget().currentIndex()
        name = str(self.pvEditlayout.itemAt(0).widget().displayText())
        freq = int(self.frequencies[combo3index])
        functionForm = 'custom'
        colourpickercolour = self.customcolorbox._color
        logScale = self.logTickBox.isChecked()
        self.addRow(string.replace(name,"_","$"), functionForm, name, freq, colourpickercolour, logScale=logScale)

    def changeSecondCombo(self, idnumber, ind):
        print('ind = ', ind)
        if ind == 'Custom':
            self.pvEditlayout.itemAt(0).widget().setCurrentIndex(self.selectionBoxlayout.itemAt(0).widget().currentIndex())
            self.customPVInput = True
            self.normalSelectionBox.hide()
            self.customSelectionBox.show()
        else:
            if self.normalSelectionBox.isVisible():
                self.pvEditlayout.itemAt(0).widget().setCurrentIndex(self.selectionBoxlayout.itemAt(0).widget().currentIndex())
            else:
                self.selectionBoxlayout.itemAt(0).widget().setCurrentIndex(self.pvEditlayout.itemAt(0).widget().currentIndex())
            combo2 = self.normalSelectionBox.children()[2]
            self.customPVInput = False
            self.normalSelectionBox.show()
            self.customSelectionBox.hide()
            if combo2 != None:
                combo2.clear()
                for name in self.magnetnames["%s"%(ind)]['Names']:
                    if isinstance(name, (tuple, list, set)):
                        combo2.addItem(name[1])
                    else:
                        combo2.addItem(name)

    def changeThirdComboFromFirst(self, idnumber, ind):
        if not self.customPVInput or not ind == 'Custom':
            combo1 = self.normalSelectionBox.children()[1]
            combo2 = self.normalSelectionBox.children()[2]
            combo3 = self.normalSelectionBox.children()[3]
            if combo3 != None:
                signalType = str(combo1.currentText())
                signalName = str(combo2.currentText())
                signalPVName = str(combo3.currentText())
                if not(signalPVName in self.magnetnames["%s"%(signalType)]['PVs'].keys()):
                    combo3.clear()
                    combo3.addItems(self.magnetnames["%s"%(signalType)]['PVs'].keys())

    def changeThirdComboFromSecond(self, idnumber, ind):
        if not self.customPVInput:
            combo3 = self.normalSelectionBox.children()[3]
            combo1 = self.normalSelectionBox.children()[1]
            if combo3 != None:
                signalType = combo1.currentText()
                combo3.clear()
                combo3.addItems(self.magnetnames["%s"%(signalType)]['PVs'].keys())

    def colorPicker(self):
        row = self.tableWidget.indexAt(QApplication.focusWidget().pos()).row()
        signalIndex = self.rowWidgets.keys()[self.rowWidgets.values().index(self.tableWidget.cellWidget(row,5))]
        color = QtGui.QColorDialog.getColor(colours.Qtableau20[2*signalIndex % 20])
        self.tableWidget.cellWidget(row, 5).setStyleSheet("border: none; background-color: %s" % color.name())
        self.penColors[signalIndex] = color
