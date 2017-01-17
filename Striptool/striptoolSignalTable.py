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

sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')
import VELA_CLARA_MagnetControl as mag
#
# elements=np.array(magnetcontroller.getMagnetNames());
# quads = filter(lambda name: magnetcontroller.isAQuad(name), elements)
# dipoles = filter(lambda name: magnetcontroller.isADip(name), elements)
# corrs =  filter(lambda name: magnetcontroller.isACor(name), elements)
# bpms = bpmcontroller.getBPMNames()

magnetcontroller = ''
quads = ['QUAD01', 'QUAD02', 'QUAD03', 'QUAD04', 'QUAD05', 'QUAD06', 'QUAD07', 'QUAD08', 'QUAD09', 'QUAD10', 'QUAD11', 'QUAD12', 'QUAD13', 'QUAD14', 'QUAD15']
dipoles = ['DIP01', 'DIP02', 'DIP03']
corrs = ['HCOR01', 'HCOR02', 'HCOR03', 'HCOR04', 'HCOR05', 'HCOR06', 'HCOR07', 'HCOR08', 'HCOR09', 'HCOR10', 'HCOR11', 'VCOR01', 'VCOR02', 'VCOR03', 'VCOR04', 'VCOR05', 'VCOR06', 'VCOR07', 'VCOR08', 'VCOR09', 'VCOR10', 'VCOR11']

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


class myTableWidget(QtGui.QTableWidget):

    def sizeHint(self):
        width = 0
        for i in range(self.columnCount()):
            width += self.columnWidth(i)

        width += self.verticalHeader().sizeHint().width()

        width += self.verticalScrollBar().sizeHint().width()
        width += self.frameWidth()*2

        return QtCore.QSize(width,self.height())

class signalOnOffCheckBox(QtGui.QCheckBox):
    def __init__(self, comboID, mainForm):
        super(signalOnOffCheckBox, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm

        self.connect(self, QtCore.SIGNAL("stateChanged (int)"), self.stateChanged)

    def stateChanged(self, ind):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.emit(QtCore.SIGNAL("checkboxChanged(PyQt_PyObject,PyQt_PyObject)"), self.__comboID, ind)

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

class deleteRowButton(QtGui.QPushButton):
    def __init__(self, comboID, mainForm):
        super(deleteRowButton, self).__init__()
        self.__comboID = comboID
        self.__mainForm = mainForm
        self.connect(self, QtCore.SIGNAL("clicked ()"), self.buttonPushed)

    def buttonPushed(self):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.emit(QtCore.SIGNAL("deleteRowButtonPushed(PyQt_PyObject)"), self.__comboID)

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
    def __init__(self, parent = None):
        super(signalTable, self).__init__(parent)
        self.magInit = mag.init()
        self.magnets = self.magInit.virtual_VELA_INJ_Magnet_Controller()
        self.stripTool = parent
        self.rowNumber = -1
        self.penColors = {}
        self.rowWidgets = {}
        self.deleteicon  = QtGui.QIcon('icons/delete.png')
        for i in range(len(Qtableau20)):
            self.penColors[i] = Qtableau20[2*i % 20]
        ''' create selectionBox '''
        self.selectBox = self.selectionBox()
        ''' create tableWidget and pushButton '''
        self.tableWidget = myTableWidget()
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(True)
        header = self.tableWidget.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)
        header.setResizeMode(4, QtGui.QHeaderView.Stretch)
        header.setResizeMode(5, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(6, QtGui.QHeaderView.ResizeToContents)
        self.pushButton = QtGui.QPushButton()
        self.pushButton.setText("Add row")
        vBoxlayoutParameters = QGridLayout()
        vBoxlayoutParameters.addWidget(self.selectBox,       0, 0, 1, 1)
        vBoxlayoutParameters.addWidget(self.tableWidget,       1, 0, 6, 1)
        vBoxlayoutParameters.addWidget(self.pushButton,        8, 0, 1, 1)
        self.setLayout(vBoxlayoutParameters)
        # self.tableWidget.resizeRowsToContents()
        # self.tableWidget.resizeColumnsToContents()
        self.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.addRow)
        self.connect(self, QtCore.SIGNAL("firstColumnComboBoxChanged(PyQt_PyObject, PyQt_PyObject)"), self.changeSecondCombo)
        self.connect(self, QtCore.SIGNAL("firstColumnComboBoxChanged(PyQt_PyObject, PyQt_PyObject)"), self.changeThirdComboFromFirst)
        self.connect(self, QtCore.SIGNAL("deleteRowButtonPushed(PyQt_PyObject)"), self.deleteTableRow)
        self.connect(self, QtCore.SIGNAL("colourPickerButtonPushed(PyQt_PyObject)"), self.colorPicker)
        # self.connect(self, QtCore.SIGNAL("signalRateChanged(PyQt_PyObject, PyQt_PyObject)"), self.updateSignalTimer)

    def addRow(self, combo1index, combo2index, combo3index, combo4index, colourpickercolour):
        self.rowNumber += 1
        newRowNumber = self.tableWidget.rowCount()
        self.tableWidget.insertRow(newRowNumber)
        checkbox=signalOnOffCheckBox(self.rowNumber, self)
        checkbox.setChecked(True)
        checkbox.setFixedWidth(20)
        combo1=QtGui.QTableWidgetItem()
        combo2=QtGui.QTableWidgetItem()
        combo3=QtGui.QTableWidgetItem()
        combo4=QtGui.QTableWidgetItem()
        deleteButton = deleteRowButton(self.rowNumber, self)
        deleteButton.setFixedWidth(50)
        deleteButton.setIcon(self.deleteicon)
        combo1text = ('Off','Quads','Dipoles','Correctors','BPMs')[combo1index]
        combo1.setText(combo1text)
        combo2.setText(magnets[combo1text]['Names'][combo2index])
        combo3.setText(magnets[combo1text]['PVs'].keys()[combo3index])
        combo4.setText(('1','5','10','25','50','100')[combo4index])
        colorbox = pg.ColorButton()
        colorbox.setMinimumWidth(60)
        colorbox.setFlat(True)
        colorbox.setColor(colourpickercolour)
        # colorbox.sigColorChanged.connect(lambda x: self.changePenColor(x))
        # colorbox.sigColorChanging.connect(lambda x: self.changePenColor(x))
        self.tableWidget.setCellWidget(newRowNumber, 0, checkbox)
        self.tableWidget.setItem(newRowNumber, 1, combo1)
        self.tableWidget.setItem(newRowNumber, 2, combo2)
        self.tableWidget.setItem(newRowNumber, 3, combo3)
        self.tableWidget.setItem(newRowNumber, 4, combo4)
        self.tableWidget.setCellWidget(newRowNumber, 5, colorbox)
        self.tableWidget.setCellWidget(newRowNumber, 6, deleteButton)
        name=magnets[combo1text]['Names'][combo2index]+'.'+magnets[combo1text]['PVs'].keys()[combo3index]
        freq = int(('1','5','10','25','50','100')[combo4index])
        functionForm = magnets[combo1text]['PVs'][str(combo3.text())]
        if functionForm[0] == '':
            functionName = functionForm[1]
        else:
            functionName = '.'.join(functionForm)
        # functionName = 'createRandomSignal'
        # testFunction = lambda: globals()[functionName](-0.5)
        print self.magnets
        testFunction = lambda: getattr(self.magnets,functionName)(magnets[combo1text]['Names'][combo2index])
        # print getattr(magnets,'getRI')
        self.stripTool.addSignal(name=name,pen=colourpickercolour, function=testFunction, timer=1.0/freq)
        # self.emit(QtCore.SIGNAL("newSignalAdded(PyQt_PyObject,PyQt_PyObject)"), name, pen, )

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
        combo2.setEditable(True)
        combo2.lineEdit().setReadOnly(True);
        combo2.lineEdit().setAlignment(Qt.AlignCenter);
        combo2.setMinimumWidth(80)
        combo3.setEditable(True)
        combo3.lineEdit().setReadOnly(True);
        combo3.lineEdit().setAlignment(Qt.AlignCenter);
        combo3.setMinimumWidth(80)
        combo4.setEditable(True)
        combo4.lineEdit().setReadOnly(True);
        combo4.lineEdit().setAlignment(Qt.AlignCenter);
        combo4.setCurrentIndex(2)
        combo4.setMinimumWidth(80)
        colorbox = pg.ColorButton()
        colorbox.setMinimumWidth(60)
        colorbox.setFlat(True)
        if(self.rowNumber < 0):
            colorbox.setColor(self.penColors[0])
        else:
            colorbox.setColor(self.penColors[self.rowNumber])
        self.selectionBoxlayout.addWidget(combo1,2)
        self.selectionBoxlayout.addWidget(combo2,3)
        self.selectionBoxlayout.addWidget(combo3,2)
        self.selectionBoxlayout.addWidget(combo4,1)
        self.selectionBoxlayout.addWidget(colorbox,1)
        self.selectionBoxlayout.addWidget(self.addButton,1)
        widget.setLayout(self.selectionBoxlayout)
        return widget

    def changePenColor(self, widget):
        self.penColors[self.rowNumber] = widget._color

    def deleteTableRow(self, idnumber):
        row = self.tableWidget.indexAt(QApplication.focusWidget().pos()).row()
        self.tableWidget.cellWidget(row, 0).setChecked(False)
        self.tableWidget.removeRow(row)

    def addTableRow(self):
        row = self.rowNumber
        combo1index = self.selectBox.children()[1].currentIndex()
        combo2index = self.selectBox.children()[2].currentIndex()
        combo3index = self.selectBox.children()[3].currentIndex()
        combo4index = self.selectBox.children()[4].currentIndex()
        colourpickercolour = self.selectBox.children()[5]._color
        if combo1index > 0:
            self.addRow(combo1index, combo2index, combo3index, combo4index, colourpickercolour)

    def changeSecondCombo(self, idnumber, ind):
        combo2 = self.selectBox.children()[2]
        if combo2 != None:
            combo2.clear()
            combo2.addItems(magnets["%s"%(ind)]['Names'])
        # self.tableWidget.resizeRowsToContents()
        # self.tableWidget.resizeColumnsToContents()

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

# def main():
#     app = QApplication(sys.argv)
#     app.setStyle(QStyleFactory.create("GTK+"))
#     ex = combodemo()
#     ex.show()
#     print "starting..."
#
#     sys.exit(app.exec_())
#
# if __name__ == '__main__':
#    main()
