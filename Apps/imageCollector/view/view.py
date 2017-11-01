# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(214, 362)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("resources\imageCollector\icon.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.numImages_spinBox = QtGui.QSpinBox(self.centralwidget)
        self.numImages_spinBox.setMinimum(1)
        self.numImages_spinBox.setObjectName(_fromUtf8("numImages_spinBox"))
        self.gridLayout.addWidget(self.numImages_spinBox, 5, 1, 1, 1)
        self.cameraName_comboBox = QtGui.QComboBox(self.centralwidget)
        self.cameraName_comboBox.setObjectName(_fromUtf8("cameraName_comboBox"))
        self.gridLayout.addWidget(self.cameraName_comboBox, 1, 0, 1, 2)
        self.acquire_pushButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.acquire_pushButton.sizePolicy().hasHeightForWidth())
        self.acquire_pushButton.setSizePolicy(sizePolicy)
        self.acquire_pushButton.setMaximumSize(QtCore.QSize(16777215, 100))
        self.acquire_pushButton.setObjectName(_fromUtf8("acquire_pushButton"))
        self.gridLayout.addWidget(self.acquire_pushButton, 4, 0, 1, 2)
        self.save_pushButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_pushButton.sizePolicy().hasHeightForWidth())
        self.save_pushButton.setSizePolicy(sizePolicy)
        self.save_pushButton.setMaximumSize(QtCore.QSize(16777215, 100))
        self.save_pushButton.setObjectName(_fromUtf8("save_pushButton"))
        self.gridLayout.addWidget(self.save_pushButton, 6, 0, 1, 2)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)
        self.liveStream_pushButton = QtGui.QPushButton(self.centralwidget)
        self.liveStream_pushButton.setObjectName(_fromUtf8("liveStream_pushButton"))
        self.gridLayout.addWidget(self.liveStream_pushButton, 2, 0, 1, 2)
        self.label = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.getImages_pushButton = QtGui.QPushButton(self.centralwidget)
        self.getImages_pushButton.setObjectName(_fromUtf8("getImages_pushButton"))
        self.gridLayout.addWidget(self.getImages_pushButton, 7, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 214, 18))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Collector", None))
        self.acquire_pushButton.setText(_translate("MainWindow", "Acquire", None))
        self.save_pushButton.setText(_translate("MainWindow", "Collect and Save", None))
        self.label_2.setText(_translate("MainWindow", "Number of Images:", None))
        self.liveStream_pushButton.setText(_translate("MainWindow", "Live Steam", None))
        self.label.setText(_translate("MainWindow", "Selected Camera:", None))
        self.getImages_pushButton.setText(_translate("MainWindow", "Open Image Directory", None))
