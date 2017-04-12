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

class scopeWriterUi_TabWidget(object):
    def setupUi(self, TabWidget, scopeCont):
        self.TabWidget = TabWidget
        #self.TabWidget.resize(1000, 402)
        self.scopeCont = scopeCont
        self.TabWidget.setObjectName(_fromUtf8("Scope EPICS Writer"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.mainBox = QtGui.QHBoxLayout(self.tab)
        self.channelsVBox = QtGui.QVBoxLayout()
        self.addChannel( self.TabWidget, self.channelsVBox, self.scopeCont )
        self.logVBox = QtGui.QVBoxLayout()
        self.labelBox = QtGui.QVBoxLayout()
        self.addToListButton = QtGui.QPushButton()
        self.addToListButton.setObjectName(_fromUtf8("addToListButton"))
        self.addToListButton.setMinimumSize(QtCore.QSize(100,100))
        self.startButton = QtGui.QPushButton()
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.startButton.setMinimumSize(QtCore.QSize(100,100))
        self.stopButton = QtGui.QPushButton()
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.stopButton.setMinimumSize(QtCore.QSize(100,100))
        self.tableRows = 1
        self.tableColumns = 2
        self.logTable = QtGui.QTableWidget( self.tableRows, self.tableColumns )
        self.logTable.setObjectName(_fromUtf8("logTable"))
        self.logTable.setItem(0, 0, QtGui.QTableWidgetItem("Timestamp"))
        self.logTable.setItem(0, 1, QtGui.QTableWidgetItem("Q"))
        self.logTable.setMinimumSize(QtCore.QSize(300,100))
        self.logVBox.addWidget( self.addToListButton )
        self.logVBox.addWidget( self.logTable )
        self.logVBox.addWidget( self.startButton )
        self.logVBox.addWidget( self.stopButton )
        self.titleLabel = QtGui.QLabel()
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.titleLabel.setMaximumSize(QtCore.QSize(300,200))
        self.infoLabel = QtGui.QLabel()
        self.infoLabel.setObjectName(_fromUtf8("infoLabel"))
        self.infoLabel.setMaximumSize(QtCore.QSize(300,200))
        self.labelBox.addWidget(self.titleLabel)
        self.labelBox.addWidget(self.infoLabel)
        self.mainBox.addLayout(self.labelBox)
        self.mainBox.addLayout(self.logVBox)
        self.mainBox.addLayout(self.channelsVBox)
        self.TabWidget.addTab(self.tab, _fromUtf8(""))

        self.retranslateUi(self.TabWidget)
        QtCore.QMetaObject.connectSlotsByName(self.TabWidget)

    def retranslateUi(self, TabWidget):
        self.TabWidget.setWindowTitle(_translate("TabWidget", "Scope charge writer", None))
        self.addToListButton.setText(_translate("TabWidget", "Add channel to list", None))
        self.startButton.setText(_translate("TabWidget", "Start logging to EPICS", None))
        self.stopButton.setText(_translate("TabWidget", "Abort", None))
        self.newFont = QtGui.QFont("Comic Sans", 20, QtGui.QFont.Bold)
        self.titleLabel.setFont(self.newFont)
        self.titleLabel.setText(_translate("TabWidget", "VELA/CLARA \nScope Logger", None))
        self.infoText = "Please select the BPMs to calibrate from the list using \nthe drop-down menu and the 'Calibrate BPM' button."
        self.infoLabel.setText(_translate("TabWidget", self.infoText, None))

    def addChannel(self, TabWidget, Layout, scopeCont):
        self.TabWidget = TabWidget
        self.Layout = Layout
        self.scopeCont = scopeCont
        self.hBox = QtGui.QHBoxLayout()
        self.chanVBox = QtGui.QVBoxLayout()
        self.channelNameLabel = QtGui.QLabel()
        self.channelNameLabel.setObjectName(_fromUtf8("channelNameLabel"))
        self.channelNameLabel.setText(_translate("TabWidget", "Scope channel", None))
        self.channels = ["C1", "C2", "C3", "C4"]
        self.chanComboBox = QtGui.QComboBox()
        self.chanComboBox.setObjectName(_fromUtf8("chanComboBox"))
        for i in self.channels:
            self.chanComboBox.addItem( i )
        self.chanVBox.addWidget( self.channelNameLabel )
        self.chanVBox.addWidget( self.chanComboBox )
        self.chanVBox.addStretch()
        self.epicsVBox = QtGui.QVBoxLayout()
        self.epicsNameLabel = QtGui.QLabel()
        self.epicsNameLabel.setObjectName(_fromUtf8("epicsNameLabel"))
        self.epicsNameLabel.setText(_translate("TabWidget", "EPICS PV Name", None))
        self.epicsPVs = ["P1", "P2", "P3", "P4"]
        self.epicsComboBox = QtGui.QComboBox()
        self.epicsComboBox.setObjectName(_fromUtf8("epicsComboBox"))
        self.scopeName = self.scopeCont.getScopeNames()[0]
        self.traceDataStruct = self.scopeCont.getScopeTraceDataStruct( self.scopeName )
        for i in self.epicsPVs:
            self.epicsPVName = self.traceDataStruct.pvRoot+":"+str(i)
            self.epicsComboBox.addItem( self.epicsPVName )
        self.epicsVBox.addWidget(self.epicsNameLabel)
        self.epicsVBox.addWidget(self.epicsComboBox)
        self.epicsVBox.addStretch()
        self.measurementVBox = QtGui.QVBoxLayout()
        self.measurementNameLabel = QtGui.QLabel()
        self.measurementNameLabel.setObjectName(_fromUtf8("measurementNameLabel"))
        self.measurementNameLabel.setText(_translate("TabWidget", "Measurement Type?", None))
        self.types = ["Area", "Max", "Min", "Peak-to-Peak"]
        self.measurementComboBox = QtGui.QComboBox()
        self.measurementComboBox.setObjectName(_fromUtf8("measurementComboBox"))
        for i in self.types:
            self.measurementComboBox.addItem( i )
        self.measurementVBox.addWidget( self.measurementNameLabel )
        self.measurementVBox.addWidget( self.measurementComboBox )
        self.measurementVBox.addStretch()
        self.noiseVBox = QtGui.QVBoxLayout()
        self.noiseHBox = QtGui.QHBoxLayout()
        self.noiseNameLabel = QtGui.QLabel()
        self.noiseNameLabel.setObjectName(_fromUtf8("noiseNameLabel"))
        self.noiseNameLabel.setText(_translate("TabWidget", "Noise subtraction region", None))
        self.lowerNoiseBound = QtGui.QPlainTextEdit()
        self.lowerNoiseBound.setObjectName(_fromUtf8("lowerNoiseBound"))
        self.lowerNoiseBound.setPlainText(_translate("TabWidget", "1", None))
        self.upperNoiseBound = QtGui.QPlainTextEdit()
        self.upperNoiseBound.setObjectName(_fromUtf8("upperNoiseBound"))
        self.upperNoiseBound.setPlainText(_translate("TabWidget", "100", None))
        self.lowerNoiseBound.setMaximumSize(QtCore.QSize(100,30))
        self.upperNoiseBound.setMaximumSize(QtCore.QSize(100,30))
        self.toLabel = QtGui.QLabel()
        self.toLabel.setObjectName(_fromUtf8("toLabel"))
        self.toLabel.setText(_translate("TabWidget", " to ", None))
        self.noiseHBox.addWidget( self.lowerNoiseBound )
        self.noiseHBox.addWidget( self.toLabel )
        self.noiseHBox.addWidget( self.upperNoiseBound )
        self.noiseVBox.addWidget( self.noiseNameLabel )
        self.noiseVBox.addLayout( self.noiseHBox )
        self.noiseVBox.addStretch()
        self.signalVBox = QtGui.QVBoxLayout()
        self.signalHBox = QtGui.QHBoxLayout()
        self.signalNameLabel = QtGui.QLabel()
        self.signalNameLabel.setObjectName(_fromUtf8("signalNameLabel"))
        self.signalNameLabel.setText(_translate("TabWidget", "Signal region", None))
        self.lowerSignalBound = QtGui.QPlainTextEdit()
        self.lowerSignalBound.setObjectName(_fromUtf8("lowerSignalBound"))
        self.lowerSignalBound.setPlainText(_translate("TabWidget", "600", None))
        self.upperSignalBound = QtGui.QPlainTextEdit()
        self.upperSignalBound.setObjectName(_fromUtf8("upperSignalBound"))
        self.upperSignalBound.setPlainText(_translate("TabWidget", "1000", None))
        self.lowerSignalBound.setMaximumSize(QtCore.QSize(100,30))
        self.upperSignalBound.setMaximumSize(QtCore.QSize(100,30))
        self.signalHBox.addWidget( self.lowerSignalBound )
        self.signalHBox.addWidget( self.toLabel )
        self.signalHBox.addWidget( self.upperSignalBound )
        self.signalVBox.addWidget( self.signalNameLabel )
        self.signalVBox.addLayout( self.signalHBox )
        self.signalVBox.addStretch()
        self.hBox.addLayout( self.chanVBox )
        self.hBox.addLayout( self.epicsVBox )
        self.hBox.addLayout( self.measurementVBox )
        self.hBox.addLayout( self.noiseVBox )
        self.hBox.addLayout( self.signalVBox )
        self.Layout.addLayout( self.hBox )
