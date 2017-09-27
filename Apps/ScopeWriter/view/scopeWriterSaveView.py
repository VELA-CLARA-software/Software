#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from scopeWriterSaveUI import scopeWriterSaveUI
import datetime
import scopeWriterGlobals as globals

class scopeWriterSaveView(QtGui.QMainWindow, scopeWriterSaveUI):
    fileName = QtCore.pyqtSignal(str)
    def __init__(self  ):
        QtGui.QMainWindow.__init__(self)
        # startup crap
        self.setupUi(self)
        self.addComboKeywords()
        self.now = datetime.datetime.now()
        #type(self.now.month)
        self.controller_type = "";
        self.cancelButton_2.clicked.connect(self.handle_fileSaveCancel)
        self.canWindowClose = False

    def setFileName(self):
        self.filename = globals.scopeSetupLocation + \
                        str(self.now.year)  + '-' + \
                        '{:02d}'.format(self.now.month) + '-' + \
                        '{:02d}'.format(self.now.day  ) + '-' + \
                        '{:02d}'.format(self.now.hour ) + \
                        '{:02d}'.format(self.now.minute)+ \
                        '.lss'
        self.file_name_entry.setText(self.filename)
        print self.filename
        self.fileName.emit(self.filename)
        return self.filename

    def getComboBoxEntries(self):
        self.keywords = str(self.areaCombo.currentText())
        return self.keywords
    # this event is inherited and we overlaod it so the GUI_FileSave
    # is never deleted, (until we call close on the entire program)
    def closeEvent(self, evnt):
        if self.canWindowClose:
            super(scopeWriterSaveView, self).closeEvent(evnt)
        else:
            evnt.ignore()
            self.hide()
    # cancel button
    def handle_fileSaveCancel(self):
        self.hide()
    # when we decide keywords we'll add more here...
    def addComboKeywords(self):
        self.list1 = [
            self.tr('VELA  INJ'),
            self.tr('CLARA INJ'),
            self.tr('VELA  BA1'),
            self.tr('VELA  BA2')]
        self.areaCombo.addItems(self.list1)




