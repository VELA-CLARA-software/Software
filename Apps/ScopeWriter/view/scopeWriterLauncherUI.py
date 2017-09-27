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

class scopeWriterLauncherUI(object):
    def setupUi(self, launcherWindow):
        #self.launcherWindow = launcherWindow
        launcherWindow.resize(410, 110)
        launcherWindow.setObjectName(_fromUtf8("Scope writer launcher"))
        self.mainWidget = QtGui.QWidget(launcherWindow)
        self.mainWidget.resize(400,100)
        self.mainWidget.setObjectName(_fromUtf8("mainWidget"))
        self.panelHBox = QtGui.QHBoxLayout( self.mainWidget )
        self.launcherVBox = QtGui.QVBoxLayout()
        self.launcherButton = QtGui.QPushButton()
        self.launcherButton.setObjectName(_fromUtf8("launcherButton"))
        self.launcherButton.setText(_translate("mainWindow", "Launch ScopeWriter", None))
        self.launcherLabel = QtGui.QLabel()
        self.infoLabel = QtGui.QLabel()
        self.launcherVBox.addWidget( self.launcherButton )
        self.launcherVBox.addWidget( self.launcherLabel )
        self.launcherVBox.addStretch()
        self.typesVBox = QtGui.QVBoxLayout()
        self.controllerTypesLabel = QtGui.QLabel()
        self.controllerTypesLabel.setObjectName(_fromUtf8("controllerTypesLabel"))
        self.controllerTypesLabel.setText(_translate("mainWindow", "Controller Type?", None))
        self.controllerTypes = ["","Physical", "Virtual", "Offline"]
        self.controllerTypesComboBox = QtGui.QComboBox()
        self.controllerTypesComboBox.setObjectName(_fromUtf8("controllerTypesComboBox"))
        for i in self.controllerTypes:
            self.controllerTypesComboBox.addItem( i )
        self.beamlineLabel = QtGui.QLabel()
        self.beamlineLabel.setObjectName(_fromUtf8("controllerTypesLabel"))
        self.beamlineLabel.setText(_translate("mainWindow", "Beamline?", None))
        self.beamlineTypes = ["","CLARA_S01", "CLARA_S02", "VELA_INJ", "VELA_BA1", "VELA_BA2"]
        self.beamlineTypesComboBox = QtGui.QComboBox()
        self.beamlineTypesComboBox.setObjectName(_fromUtf8("beamlineTypesComboBox"))
        for i in self.beamlineTypes:
            self.beamlineTypesComboBox.addItem( i )
        self.typesVBox.addWidget( self.controllerTypesLabel )
        self.typesVBox.addWidget( self.controllerTypesComboBox )
        self.typesVBox.addWidget( self.beamlineLabel )
        self.typesVBox.addWidget( self.beamlineTypesComboBox )
        self.typesVBox.addStretch()
        self.panelHBox.addLayout( self.launcherVBox )
        self.panelHBox.addLayout( self.typesVBox )
        self.retranslateUi(launcherWindow)
        QtCore.QMetaObject.connectSlotsByName(launcherWindow)

    def retranslateUi(self, launcherWindow):
        launcherWindow.setWindowTitle(_translate("launcherWindow", "Scope charge writer launcher", None))
        self.launcherLabelText = "Please select the appropriate beamline and controller types.\n"
        self.launcherLabelText1 = self.launcherLabelText+"Note - currently only EBT-INJ exists...."
        self.launcherLabel.setText(_translate("launcherWindow", self.launcherLabelText1, None))
        self.infoLabel.setText(_translate("launcherWindow", "", None))
        #launcherWindow.setMinimumSize(QtCore.QSize(600,100))
