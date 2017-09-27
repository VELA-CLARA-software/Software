from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject

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

class matlabImageLauncherViewUI(object):
    def setupUi(self, launcherWindow):
        #self.launcherWindow = launcherWindow
        launcherWindow.resize(410, 110)
        launcherWindow.setObjectName(_fromUtf8("Matlab image viewer launcher"))
        self.mainWidget = QtGui.QWidget(launcherWindow)
        self.mainWidget.resize(400,100)
        self.mainWidget.setObjectName(_fromUtf8("mainWidget"))
        self.panelHBox = QtGui.QHBoxLayout( self.mainWidget )
        self.launcherVBox = QtGui.QVBoxLayout()
        self.launcherButton = QtGui.QPushButton()
        self.launcherButton.setObjectName(_fromUtf8("launcherButton"))
        self.launcherButton.setText(_translate("mainWindow", "Launch Matlab image viewer", None))
        self.launcherLabel = QtGui.QLabel()
        self.infoLabel = QtGui.QLabel()
        self.launcherVBox.addWidget( self.launcherButton )
        self.launcherVBox.addWidget( self.launcherLabel )
        self.launcherVBox.addStretch()
        self.typesVBox = QtGui.QVBoxLayout()
        self.measurementTypesLabel = QtGui.QLabel()
        self.measurementTypesLabel.setObjectName(_fromUtf8("measurementTypesLabel"))
        self.measurementTypesLabel.setText(_translate("mainWindow", "Measurement Type?", None))
        self.measurementTypes = ["","Emittance","Energy spread"]
        self.measurementTypesComboBox = QtGui.QComboBox()
        self.measurementTypesComboBox.setObjectName(_fromUtf8("measurementTypesComboBox"))
        for i in self.measurementTypes:
            self.measurementTypesComboBox.addItem( i )
        self.typesVBox.addWidget( self.measurementTypesLabel )
        self.typesVBox.addWidget( self.measurementTypesComboBox )
        self.typesVBox.addStretch()
        self.panelHBox.addLayout( self.launcherVBox )
        self.panelHBox.addLayout( self.typesVBox )
        self.retranslateUi(launcherWindow)
        QtCore.QMetaObject.connectSlotsByName(launcherWindow)

    def retranslateUi(self, launcherWindow):
        launcherWindow.setWindowTitle(_translate("launcherWindow", "Matlab image viewer launcher", None))
        self.launcherLabelText = "Please select the appropriate measurement type."
        self.launcherLabel.setText(_translate("launcherWindow", self.launcherLabelText, None))
        self.infoLabel.setText(_translate("launcherWindow", "", None))
        #launcherWindow.setMinimumSize(QtCore.QSize(600,100))
