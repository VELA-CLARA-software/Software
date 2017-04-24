from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject
import sys, os, threading
print os.getcwd()
#os.chdir(os.getcwd())
import scope_writer_main
import VELA_CLARA_Scope_Control as vcsc

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

class scopeWriterLauncherView(object):
    def setupUi(self, TabWidget):
        self.TabWidget = TabWidget
        #self.TabWidget.resize(1000, 402)
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.panelHBox = QtGui.QHBoxLayout( self.tab )
        self.launcherVBox = QtGui.QVBoxLayout()
        self.launcherButton = QtGui.QPushButton()
        self.launcherButton.setObjectName(_fromUtf8("launcherButton"))
        self.launcherButton.setText(_translate("TabWidget", "Launch ScopeWriter", None))
        self.launcherLabel = QtGui.QLabel()
        self.launcherVBox.addWidget( self.launcherButton )
        self.launcherVBox.addWidget( self.launcherLabel )
        self.launcherVBox.addStretch()
        self.typesVBox = QtGui.QVBoxLayout()
        self.controllerTypesLabel = QtGui.QLabel()
        self.controllerTypesLabel.setObjectName(_fromUtf8("controllerTypesLabel"))
        self.controllerTypesLabel.setText(_translate("TabWidget", "Controller Type?", None))
        self.controllerTypes = ["Physical", "Virtual", "Offline"]
        self.controllerTypesComboBox = QtGui.QComboBox()
        self.controllerTypesComboBox.setObjectName(_fromUtf8("controllerTypesComboBox"))
        for i in self.controllerTypes:
            self.controllerTypesComboBox.addItem( i )
        self.beamlineLabel = QtGui.QLabel()
        self.beamlineLabel.setObjectName(_fromUtf8("controllerTypesLabel"))
        self.beamlineLabel.setText(_translate("TabWidget", "Beamline?", None))
        self.beamlineTypes = ["CLARA_S01", "CLARA_S02", "VELA_INJ", "VELA_BA1", "VELA_BA2"]
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
        self.TabWidget.addTab(self.tab, _fromUtf8(""))

        self.retranslateUi(self.TabWidget)
        QtCore.QMetaObject.connectSlotsByName(self.TabWidget)

    def retranslateUi(self, TabWidget):
        self.TabWidget.setWindowTitle(_translate("TabWidget", "Scope charge writer", None))
        self.infoText = "Please select the appropriate beamline and controller types.\n"
        self.infoText1 = self.infoText+"Note - currently only EBT-INJ exists...."
        self.launcherLabel.setText(_translate("TabWidget", self.infoText1, None))
        self.TabWidget.setMinimumSize(QtCore.QSize(600,100))

class scopeWriterLauncherController(QObject):

    def __init__(self, view):
        super(scopeWriterLauncherController, self).__init__()
        self.view = view
        self.view.launcherButton.clicked.connect(lambda: self.launchScopeWriterThread())
        self.beamlines = {"VELA_INJ":  vcsc.MACHINE_AREA.VELA_INJ,
                          "VELA_BA1":  vcsc.MACHINE_AREA.VELA_BA1,
                          "VELA_BA1":  vcsc.MACHINE_AREA.VELA_BA2,
                          "CLARA_S01": vcsc.MACHINE_AREA.CLARA_S01}
        self.modes = {"Physical": vcsc.MACHINE_MODE.PHYSICAL,
                      "Virtual":  vcsc.MACHINE_MODE.VIRTUAL,
                      "Offline":  vcsc.MACHINE_MODE.OFFLINE}

    def searchInDict(self, myDict, lookup):
        self.myDict = myDict
        self.lookup = lookup
        for key, value in self.myDict.items():
            if self.lookup == key:
                print type(value)
                return value

    def launchScopeWriter(self):
        #self.blineName = self.searchInDict(self.beamlines, str(self.view.beamlineTypesComboBox.currentText()))
        #self.contTypeName = self.searchInDict(self.modes, str(self.view.controllerTypesComboBox.currentText()))
        #scope_writer_main.scopeWriterApp( self.contTypeName, self.blineName )
		os.system("python scope_writer_main.py "+str(self.view.controllerTypesComboBox.currentText())+" "+str(self.view.beamlineTypesComboBox.currentText()))

    def launchScopeWriterThread(self):
        self.scopeWriterThread = threading.Thread(target = self.launchScopeWriter)
        self.scopeWriterThread.daemon = True
        self.scopeWriterThread.start()

class scopeWriterLauncherApp(QtGui.QApplication):
    def __init__(self, sys_argv):
        #This file simply loads up the GUI and links in the controller, which connects the buttons to the BPM apps
        super(scopeWriterLauncherApp, self).__init__(sys_argv)
        self.view = scopeWriterLauncherView()
        self.MainWindow = QtGui.QTabWidget()
        self.view.setupUi(self.MainWindow)
        self.controller = scopeWriterLauncherController(self.view)
        self.MainWindow.show()

if __name__ == '__main__':
    app = scopeWriterLauncherApp(sys.argv)
    sys.exit(app.exec_())
