import sys,os
import pyqtgraph as pg
sys.path.append("../../../")
import Software.Procedures.qt as qt
import time
import yaml
import string as string
import colours as colours
from collections import OrderedDict

_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

def dict_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())

def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))

yaml.add_representer(OrderedDict, dict_representer)
yaml.add_constructor(_mapping_tag, dict_constructor)

class signalTypeComboBox(qt.QComboBox):
    def __init__(self, comboID, mainForm):
        super(signalTypeComboBox, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm
        self.currentIndexChanged.connect(self.indexChanged)

    def indexChanged(self, ind):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.firstColumnComboBoxChanged.emit(self.__comboID, self.currentText())

class signalElementComboBox(qt.QComboBox):
    def __init__(self, comboID, mainForm):
        super(signalElementComboBox, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm
        self.currentIndexChanged.connect(self.indexChanged)

    def indexChanged(self, ind):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.secondColumnComboBoxChanged.emit(self.__comboID, self.currentText())

class signalPVComboBox(qt.QComboBox):
    def __init__(self, comboID, mainForm):
        super(signalPVComboBox, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm
        self.currentIndexChanged.connect(self.indexChanged)

    def indexChanged(self, ind):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.thirdColumnComboBoxChanged.emit(self.__comboID, self.currentText())

class signalRateComboBox(qt.QComboBox):
    def __init__(self, comboID, mainForm):
        super(signalRateComboBox, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm
        self.currentIndexChanged.connect(self.indexChanged)

    def indexChanged(self, ind):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.signalRateChanged.emit(self.__comboID, self.currentText())

class colourPickerButton(qt.QPushButton):
    def __init__(self, comboID, mainForm):
        super(colourPickerButton, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm
        self.clicked.connect(self.buttonPushed)

    def buttonPushed(self):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.colourPickerButtonPushed.emit(self.__comboID)

class createNormalSelectionBox(qt.QWidget):

    def __init__(self, parent=None, custom=False):
        super(createNormalSelectionBox, self).__init__(parent=parent)
        self.parent = parent
        self.custom = custom
        self.selectionBoxlayout = qt.QHBoxLayout()
        self.combo1=signalTypeComboBox(0, self.parent)
        self.combo2=signalElementComboBox(0, self.parent)
        self.combo3=signalPVComboBox(0, self.parent)
        self.combo4=signalRateComboBox(0, self.parent)
        self.addButton = qt.QPushButton('Add Signal')
        self.addButton.setFixedWidth(100)
        if self.custom:
            self.addButton.clicked.connect(self.parent.addTableRowCustom)
        else:
            self.addButton.clicked.connect(self.parent.addTableRow)
        self.logTickBox = qt.QCheckBox('Log Scale')
        self.combo1.addItems(self.parent.headings)
        if not self.custom:
            self.combo2.addItems(self.parent.magnetnames['Off']['Names'])
            self.combo3.addItems(self.parent.magnetnames['Off']['PVs'].keys())
        self.combo4.addItems([str(i) + ' Hz'for i in self.parent.frequencies])
        self.combo1.setEditable(True)
        self.combo1.lineEdit().setReadOnly(True);
        self.combo1.lineEdit().setAlignment(qt.Qt.AlignCenter);
        self.combo1.setMinimumWidth(100)
        self.combo1.setMaximumWidth(150)
        if not self.custom:
            self.combo2.setEditable(True)
            self.combo2.lineEdit().setReadOnly(True);
            self.combo2.lineEdit().setAlignment(qt.Qt.AlignCenter);
            self.combo2.setMinimumWidth(100)
            self.combo2.setMaximumWidth(150)
            self.combo3.setEditable(True)
            self.combo3.lineEdit().setReadOnly(True);
            self.combo3.lineEdit().setAlignment(qt.Qt.AlignCenter);
            self.combo3.setMinimumWidth(80)
            self.combo3.setMaximumWidth(100)
        self.combo4.setEditable(True)
        self.combo4.lineEdit().setReadOnly(True);
        self.combo4.lineEdit().setAlignment(qt.Qt.AlignCenter);
        self.combo4.setCurrentIndex(2)
        self.combo4.setMinimumWidth(100)
        self.combo4.setMaximumWidth(100)
        self.pvtextedit = qt.QLineEdit()
        self.pvtextedit.setMinimumWidth(240)
        self.pvtextedit.setMaximumWidth(300)
        self.colorbox = pg.ColorButton()
        self.colorbox.setMinimumWidth(60)
        self.colorbox.setMaximumWidth(80)
        self.colorbox.setFlat(True)
        if(self.parent.rowNumber < 0):
            self.colorbox.setColor(self.parent.penColors[0])
        else:
            self.colorbox.setColor(self.parent.penColors[self.parent.rowNumber])
        self.selectionBoxlayout.addWidget(self.combo1,2)
        if self.custom:
            self.selectionBoxlayout.addWidget(self.pvtextedit,5)
        else:
            self.selectionBoxlayout.addWidget(self.combo2,3)
            self.selectionBoxlayout.addWidget(self.combo3,2)
        self.selectionBoxlayout.addWidget(self.combo4,1)
        self.selectionBoxlayout.addWidget(self.logTickBox,1)
        self.selectionBoxlayout.addWidget(self.colorbox,1)
        self.selectionBoxlayout.addWidget(self.addButton,1)
        self.setLayout(self.selectionBoxlayout)
        self.setMaximumHeight(100)

    def resetHeadings(self):
        self.combo1.clear()
        self.combo1.addItems(self.parent.headings)
        if not self.custom:
            self.combo2.clear()
            self.combo2.addItems(self.parent.magnetnames['Off']['Names'])
            self.combo3.clear()
            self.combo3.addItems(self.parent.magnetnames['Off']['PVs'].keys())

class customPVFunction(qt.QObject):
    def __init__(self, parent = None, pvid=None, GeneralController=None):
        super(customPVFunction, self).__init__(parent)
        self.pvid = pvid
        self.general = GeneralController

    def getValue(self):
        return float(self.general.getValue(self.pvid))


class signalTable(qt.QWidget):

    firstColumnComboBoxChanged = qt.pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')
    secondColumnComboBoxChanged = qt.pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')
    thirdColumnComboBoxChanged = qt.pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')
    signalRateChanged = qt.pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')
    colourPickerButtonPushed = qt.pyqtSignal('PyQt_PyObject')

    def __init__(self, parent = None, VELAMagnetController=None, CLARAMagnetController=None, VELABPMController=None, CLARABPMController=None, GeneralController=None):
        super(signalTable, self).__init__(parent)
        self.setMaximumHeight(100)
        self.stream = open('striptool.yaml', 'r')
        self.settings = yaml.load(self.stream)
        self.stream.close()
        self.magnetnames = self.settings['magnets']
        self.headings = self.settings['headings']
        self.frequencies = self.settings['frequencies']
        self.VELAMagnets = VELAMagnetController
        self.CLARAMagnets = CLARAMagnetController
        self.VELAbpms = VELABPMController
        self.CLARAbpms = CLARABPMController
        self.general = GeneralController
        self.stripTool = parent
        self.rowNumber = 0
        self.penColors = {}
        self.rowWidgets = {}
        for i in range(len(colours.Qtableau20)):
            self.penColors[i] = colours.Qtableau20[2*i % 20]
        ''' create selectionBox '''
        self.customPVInput = False
        self.normalSelectionBox = createNormalSelectionBox(parent=self)
        self.customSelectionBox = createNormalSelectionBox(parent=self, custom=True)
        ''' create tableWidget and pushButton '''
        vBoxlayoutParameters = qt.QVBoxLayout()
        vBoxlayoutParameters.addWidget(self.normalSelectionBox,1)
        vBoxlayoutParameters.addWidget(self.customSelectionBox,1)
        self.normalSelectionBox.show()
        self.customSelectionBox.hide()
        self.setLayout(vBoxlayoutParameters)
        self.firstColumnComboBoxChanged.connect(self.changeSecondCombo)
        self.firstColumnComboBoxChanged.connect(self.changeThirdComboFromFirst)
        self.colourPickerButtonPushed.connect(self.colorPicker)
        self.stripTool.signalAdded.connect(self.updateColourBox)
        self.pvids = []

    def reloadSettings(self):
        self.stream = open('striptool.yaml', 'r')
        self.settings = yaml.load(self.stream)
        self.stream.close()
        self.magnetnames = self.settings['magnets']
        self.headings = self.settings['headings']
        self.frequencies = self.settings['frequencies']
        self.firstColumnComboBoxChanged.disconnect(self.changeSecondCombo)
        self.firstColumnComboBoxChanged.disconnect(self.changeThirdComboFromFirst)
        self.normalSelectionBox.resetHeadings()
        self.customSelectionBox.resetHeadings()
        self.firstColumnComboBoxChanged.connect(self.changeSecondCombo)
        self.firstColumnComboBoxChanged.connect(self.changeThirdComboFromFirst)


    def addRow(self, name, functionForm, functionArgument, freq, colourpickercolour, logScale=False, **kwargs):
        if functionForm == 'custom':
            pvtype="DBR_DOUBLE"
            # print ('functionArgument = ', functionArgument)
            pvid = self.general.connectPV(str(functionArgument))
            if pvid is not 'FAILED':
                self.pvids.append(pvid)
                testFunction = customPVFunction(parent=self, pvid=pvid, GeneralController=self.general).getValue
                time.sleep(0.01)
                testFunction()
            else:
                print('Is this a valid PV? - ', functionArgument)
        # elif functionForm[0] == '':
        #     functionName = functionForm[1]
        #     testFunction = lambda: getattr(self.magnets,functionName)(functionArgument)
        else:
            functionName = functionForm[1]
            function = eval(functionForm[0])
            # print('functionName = ', functionName)
            # print('functionForm = ', functionForm)
            testFunction = lambda: getattr(function,functionName)(functionArgument)
        self.stripTool.addSignal(name=name, pen=colourpickercolour, function=testFunction, timer=1.0/freq, logScale=logScale)
        self.stripTool.records[name]['record'].start()

    def updateColourBox(self):
        self.rowNumber = self.rowNumber + 1
        self.normalSelectionBox.colorbox.setColor(self.penColors[self.rowNumber])
        self.customSelectionBox.colorbox.setColor(self.penColors[self.rowNumber])

    def addTableRow(self):
        row = self.rowNumber
        combo1index = str(self.normalSelectionBox.combo1.currentText())
        combo1text = str(self.normalSelectionBox.combo1.currentText())
        combo2index = self.normalSelectionBox.combo2.currentIndex()
        combo3index = self.normalSelectionBox.combo3.currentIndex()
        combo3text = str(self.normalSelectionBox.combo3.currentText())
        combo4index = self.normalSelectionBox.combo4.currentIndex()
        if isinstance(self.magnetnames[combo1text]['Names'][combo2index], (tuple, list, set)):
            functionArgument = self.magnetnames[combo1text]['Names'][combo2index][0]
        else:
            functionArgument = self.magnetnames[combo1text]['Names'][combo2index]
        name = functionArgument+'.'+self.magnetnames[combo1index]['PVs'].keys()[combo3index]
        freq = int(self.frequencies[combo4index])
        functionForm = self.magnetnames[combo1index]['PVs'][combo3text]
        colourpickercolour = self.normalSelectionBox.colorbox._color
        logScale = self.normalSelectionBox.logTickBox.isChecked()
        if combo1index > 0:
            self.addRow(name, functionForm, functionArgument, freq, colourpickercolour, logScale=logScale)

    def addTableRowCustom(self):
        row = self.rowNumber
        combo4index = self.customSelectionBox.combo4.currentIndex()
        name = str(self.customSelectionBox.pvtextedit.displayText())
        freq = int(self.frequencies[combo4index])
        functionForm = 'custom'
        colourpickercolour = self.customSelectionBox.colorbox._color
        logScale = self.customSelectionBox.logTickBox.isChecked()
        self.addRow(string.replace(name,"_","$"), functionForm, name, freq, colourpickercolour, logScale=logScale)

    def changeSecondCombo(self, idnumber, ind):
        # print('ind = ', ind)
        if ind == 'Custom':
            self.customSelectionBox.combo1.setCurrentIndex(self.normalSelectionBox.combo1.currentIndex())
            self.customPVInput = True
            self.normalSelectionBox.hide()
            self.customSelectionBox.show()
        else:
            if self.normalSelectionBox.isVisible():
                self.customSelectionBox.combo1.setCurrentIndex(self.normalSelectionBox.combo1.currentIndex())
            else:
                self.normalSelectionBox.combo1.setCurrentIndex(self.customSelectionBox.combo1.currentIndex())
            combo2 = self.normalSelectionBox.combo2
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
            combo1 = self.normalSelectionBox.combo1
            combo2 = self.normalSelectionBox.combo2
            combo3 = self.normalSelectionBox.combo3
            if combo3 != None:
                signalType = str(combo1.currentText())
                signalName = str(combo2.currentText())
                signalPVName = str(combo3.currentText())
                if not(signalPVName in self.magnetnames["%s"%(signalType)]['PVs'].keys()):
                    combo3.clear()
                    combo3.addItems(self.magnetnames["%s"%(signalType)]['PVs'].keys())

    def changeThirdComboFromSecond(self, idnumber, ind):
        if not self.customPVInput:
            combo3 = self.normalSelectionBox.combo3
            combo1 = self.normalSelectionBox.combo1
            if combo3 != None:
                signalType = combo1.currentText()
                combo3.clear()
                combo3.addItems(self.magnetnames["%s"%(signalType)]['PVs'].keys())

    def colorPicker(self):
        row = self.tableWidget.indexAt(qt.QApplication.focusWidget().pos()).row()
        signalIndex = self.rowWidgets.keys()[self.rowWidgets.values().index(self.tableWidget.cellWidget(row,5))]
        color = qt.QColorDialog.getColor(colours.Qtableau20[2*signalIndex % 20])
        self.tableWidget.cellWidget(row, 5).setStyleSheet("border: none; background-color: %s" % color.name())
        self.penColors[signalIndex] = color
