# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_mainView3.ui'
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

class Ui_mainView(object):
    def setupUi(self, mainView):
        mainView.setObjectName(_fromUtf8("mainView"))
        mainView.resize(1134, 846)
        self.centralwidget = QtGui.QWidget(mainView)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.y_proj = GraphicsLayoutWidget(self.centralwidget)
        self.y_proj.setObjectName(_fromUtf8("y_proj"))
        self.gridLayout_2.addWidget(self.y_proj, 0, 0, 1, 1)
        self.graphicsView = GraphicsLayoutWidget(self.centralwidget)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout_2.addWidget(self.graphicsView, 0, 1, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.reset_mean_pushButton = QtGui.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.reset_mean_pushButton.setFont(font)
        self.reset_mean_pushButton.setObjectName(_fromUtf8("reset_mean_pushButton"))
        self.verticalLayout.addWidget(self.reset_mean_pushButton)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.average_cbox = QtGui.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.average_cbox.setFont(font)
        self.average_cbox.setObjectName(_fromUtf8("average_cbox"))
        self.horizontalLayout.addWidget(self.average_cbox)
        self.useROI_cbox = QtGui.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.useROI_cbox.setFont(font)
        self.useROI_cbox.setObjectName(_fromUtf8("useROI_cbox"))
        self.horizontalLayout.addWidget(self.useROI_cbox)
        self.useBackground_cbox = QtGui.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.useBackground_cbox.setFont(font)
        self.useBackground_cbox.setObjectName(_fromUtf8("useBackground_cbox"))
        self.horizontalLayout.addWidget(self.useBackground_cbox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.setRef_button = QtGui.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.setRef_button.setFont(font)
        self.setRef_button.setObjectName(_fromUtf8("setRef_button"))
        self.horizontalLayout_2.addWidget(self.setRef_button)
        self.clearRef_button = QtGui.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.clearRef_button.setFont(font)
        self.clearRef_button.setObjectName(_fromUtf8("clearRef_button"))
        self.horizontalLayout_2.addWidget(self.clearRef_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(65, 25))
        self.label.setMaximumSize(QtCore.QSize(5555, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.cam_name_text = QtGui.QTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cam_name_text.sizePolicy().hasHeightForWidth())
        self.cam_name_text.setSizePolicy(sizePolicy)
        self.cam_name_text.setMinimumSize(QtCore.QSize(100, 25))
        self.cam_name_text.setMaximumSize(QtCore.QSize(100, 25))
        self.cam_name_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.cam_name_text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.cam_name_text.setObjectName(_fromUtf8("cam_name_text"))
        self.gridLayout.addWidget(self.cam_name_text, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setMinimumSize(QtCore.QSize(65, 25))
        self.label_4.setMaximumSize(QtCore.QSize(5555, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.max_text = QtGui.QTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.max_text.sizePolicy().hasHeightForWidth())
        self.max_text.setSizePolicy(sizePolicy)
        self.max_text.setMinimumSize(QtCore.QSize(100, 25))
        self.max_text.setMaximumSize(QtCore.QSize(100, 25))
        self.max_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.max_text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.max_text.setObjectName(_fromUtf8("max_text"))
        self.gridLayout.addWidget(self.max_text, 1, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setMinimumSize(QtCore.QSize(65, 25))
        self.label_6.setMaximumSize(QtCore.QSize(5555, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.max_pos_text = QtGui.QTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.max_pos_text.sizePolicy().hasHeightForWidth())
        self.max_pos_text.setSizePolicy(sizePolicy)
        self.max_pos_text.setMinimumSize(QtCore.QSize(100, 25))
        self.max_pos_text.setMaximumSize(QtCore.QSize(100, 25))
        self.max_pos_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.max_pos_text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.max_pos_text.setObjectName(_fromUtf8("max_pos_text"))
        self.gridLayout.addWidget(self.max_pos_text, 2, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setMinimumSize(QtCore.QSize(65, 25))
        self.label_5.setMaximumSize(QtCore.QSize(5555, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.fwhm_text = QtGui.QTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fwhm_text.sizePolicy().hasHeightForWidth())
        self.fwhm_text.setSizePolicy(sizePolicy)
        self.fwhm_text.setMinimumSize(QtCore.QSize(100, 25))
        self.fwhm_text.setMaximumSize(QtCore.QSize(100, 25))
        self.fwhm_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.fwhm_text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.fwhm_text.setObjectName(_fromUtf8("fwhm_text"))
        self.gridLayout.addWidget(self.fwhm_text, 3, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.x_proj = GraphicsLayoutWidget(self.centralwidget)
        self.x_proj.setObjectName(_fromUtf8("x_proj"))
        self.verticalLayout_3.addWidget(self.x_proj)
        self.x_proj_2 = GraphicsLayoutWidget(self.centralwidget)
        self.x_proj_2.setObjectName(_fromUtf8("x_proj_2"))
        self.verticalLayout_3.addWidget(self.x_proj_2)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 1, 1, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 15)
        self.gridLayout_2.setRowStretch(0, 25)
        self.gridLayout_2.setRowStretch(1, 1)
        self.graphicsView.raise_()
        self.y_proj.raise_()
        mainView.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainView)
        QtCore.QMetaObject.connectSlotsByName(mainView)

    def retranslateUi(self, mainView):
        mainView.setWindowTitle(_translate("mainView", "MainWindow", None))
        self.reset_mean_pushButton.setText(_translate("mainView", "Reset Mean", None))
        self.average_cbox.setText(_translate("mainView", "AVG", None))
        self.useROI_cbox.setText(_translate("mainView", "ROI", None))
        self.useBackground_cbox.setText(_translate("mainView", "BCK", None))
        self.setRef_button.setText(_translate("mainView", "Set Ref", None))
        self.clearRef_button.setText(_translate("mainView", "Clear Ref", None))
        self.label.setText(_translate("mainView", "Camera:", None))
        self.cam_name_text.setHtml(_translate("mainView", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Cam Name</span></p></body></html>", None))
        self.label_4.setText(_translate("mainView", "MAX:", None))
        self.max_text.setHtml(_translate("mainView", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">max</span></p></body></html>", None))
        self.label_6.setText(_translate("mainView", "Max Pos:", None))
        self.max_pos_text.setHtml(_translate("mainView", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">max</span></p></body></html>", None))
        self.label_5.setText(_translate("mainView", "FWHM:", None))
        self.fwhm_text.setHtml(_translate("mainView", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">fwhm</span></p></body></html>", None))

from pyqtgraph import GraphicsLayoutWidget
