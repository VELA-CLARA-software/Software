# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled1.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import pyqtgraph, qrangeslider

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TabWidget(object):
    def setupUi(self, TabWidget):
        self.TabWidget = TabWidget
        self.TabWidget.setObjectName(_fromUtf8("TabWidget"))
        self.TabWidget.resize(699, 602)
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.pushButton_2 = QtGui.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 0, 91, 41))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.plainTextEdit = QtGui.QPlainTextEdit(self.tab)
        self.plainTextEdit.setGeometry(QtCore.QRect(260, 80, 151, 171))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.pushButton = QtGui.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(20, 90, 221, 161))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        #self.graphicsView = pyqtgraph.GraphicsView(self.tab)
        #self.graphicsView.setGeometry(QtCore.QRect(440, 20, 441, 261))
        #self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        #self.glayoutOutput = pyqtgraph.GraphicsLayout(border = (400,400,400))
        #self.graphicsView.setCentralItem(self.glayoutOutput)
        self.comboBox = QtGui.QComboBox(self.tab)
        self.comboBox.setGeometry(QtCore.QRect(8, 10, 231, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(260, 50, 111, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        #self.graphicsView_2 = pyqtgraph.GraphicsView(self.tab)
        #self.graphicsView_2.setGeometry(QtCore.QRect(440, 290, 441, 261))
        #self.graphicsView_2.setObjectName(_fromUtf8("graphicsView_2"))
        #self.glayoutOutput_2 = pyqtgraph.GraphicsLayout(border = (400,400,400))
        #self.graphicsView_2.setCentralItem(self.glayoutOutput_2)
        self.groupBox = QtGui.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(20, 270, 231, 131))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 20, 191, 101))
        self.label_4.setText(_fromUtf8(""))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.plainTextEdit_4 = QtGui.QPlainTextEdit(self.tab)
        self.plainTextEdit_4.setGeometry(QtCore.QRect(100, 50, 61, 31))
        self.plainTextEdit_4.setObjectName(_fromUtf8("plainTextEdit_4"))
        self.plainTextEdit_6 = QtGui.QPlainTextEdit(self.tab)
        self.plainTextEdit_6.setGeometry(QtCore.QRect(130, 450, 30, 30))
        self.plainTextEdit_6.setObjectName(_fromUtf8("plainTextEdit_6"))
        self.plainTextEdit_7 = QtGui.QPlainTextEdit(self.tab)
        self.plainTextEdit_7.setGeometry(QtCore.QRect(180, 450, 30, 30))
        self.plainTextEdit_7.setObjectName(_fromUtf8("plainTextEdit_7"))
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(40, 60, 46, 13))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_7 = QtGui.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(20, 450, 90, 30))
        self.label_7.setObjectName(_fromUtf8("label_4"))
        self.label_8 = QtGui.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(130, 420, 30, 30))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.tab)
        self.label_9.setGeometry(QtCore.QRect(180, 420, 30, 30))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.TabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName(_fromUtf8("tab1"))
        self.tabList = []
        self.graphicsViews = []
        self.graphicsViews_2 = []
        self.glayoutOutputs = []
        self.glayoutOutputs_2 = []

        self.retranslateUi(self.TabWidget)
        QtCore.QMetaObject.connectSlotsByName(self.TabWidget)

    def retranslateUi(self, TabWidget):
        self.TabWidget.setWindowTitle(_translate("TabWidget", "TabWidget", None))
        self.pushButton_2.setText(_translate("TabWidget", "Calibrate BPM", None))
        self.pushButton.setText(_translate("TabWidget", "Calibrate Delays", None))
        self.comboBox.setItemText(0, _translate("TabWidget", "BPM01", None))
        self.comboBox.setItemText(1, _translate("TabWidget", "BPM02", None))
        self.comboBox.setItemText(2, _translate("TabWidget", "BPM03", None))
        self.comboBox.setItemText(3, _translate("TabWidget", "BPM04", None))
        self.comboBox.setItemText(4, _translate("TabWidget", "BPM05", None))
        self.comboBox.setItemText(5, _translate("TabWidget", "BPM06", None))
        self.label_5.setText(_translate("TabWidget", "BPM List", None))
        self.groupBox.setTitle(_translate("TabWidget", "New BPM Delay Values", None))
        self.plainTextEdit_4.setPlainText(_translate("TabWidget", "2", None))
        self.label_3.setText(_translate("TabWidget", "# Shots", None))
        self.label_7.setText(_translate("TabWidget", "ATT Scan Range", None))
        self.label_8.setText(_translate("TabWidget", "Lower Bound", None))
        self.label_9.setText(_translate("TabWidget", "Upper Bound", None))
        self.plainTextEdit_6.setPlainText(_translate("TabWidget", "2", None))
        self.plainTextEdit_7.setPlainText(_translate("TabWidget", "10", None))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab), _translate("TabWidget", "Settings", None))
        #self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab1), _translate("TabWidget", "Tab 2", None))

    def addPlotTab(self, TabWidget, pvName):
        self.pvName = pvName
        self.TabWidget = TabWidget
        self.TabWidget.setObjectName(_fromUtf8("TabWidget"))
        self.TabWidget.resize(699, 602)
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName(_fromUtf8("tab"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab1), _translate("TabWidget", self.pvName, None))
        self.graphicsView = pyqtgraph.GraphicsView(self.tab1)
        self.graphicsView.setGeometry(QtCore.QRect(140, 20, 441, 261))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.glayoutOutput = pyqtgraph.GraphicsLayout(border = (400,400,400))
        self.graphicsView.setCentralItem(self.glayoutOutput)
        self.graphicsView_2 = pyqtgraph.GraphicsView(self.tab1)
        self.graphicsView_2.setGeometry(QtCore.QRect(140, 290, 441, 261))
        self.graphicsView_2.setObjectName(_fromUtf8("graphicsView_2"))
        self.glayoutOutput_2 = pyqtgraph.GraphicsLayout(border = (400,400,400))
        self.graphicsView_2.setCentralItem(self.glayoutOutput_2)
        self.tabList.append(self.tab1)
        self.glayoutOutputs.append(self.glayoutOutput)
        self.glayoutOutputs_2.append(self.glayoutOutput_2)
        self.TabWidget.addTab(self.tab1, _fromUtf8(self.pvName))
        self.TabWidget.setObjectName(_fromUtf8(self.pvName))
