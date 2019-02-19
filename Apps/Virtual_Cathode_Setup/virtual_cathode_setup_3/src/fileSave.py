#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS 2018
#
from PyQt4 import QtGui, QtCore
from Ui_FileSave import Ui_FileSave
import datetime
import magnetAppGlobals as globals


class GUI_FileSave(QtGui.QMainWindow, Ui_FileSave):
    def __init__(self  ):
        QtGui.QMainWindow.__init__(self)
        # startup crap
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(globals.appIcon))
        self.appPixMap = QtGui.QPixmap(globals.appIcon)
        self.commentsSection.appendPlainText("Some Interesting Comments...")
        self.now = datetime.datetime.now()
        #type(self.now.month)
        self.controller_type = ""
        self.cancelButton_2.clicked.connect(self.handle_fileSaveCancel)
        self.canWindowClose = False

    def setFileName(self):
        self.now = datetime.datetime.now()
        self.filename = globals.dburtLocation2 + \
                        self.controller_type + "_" + \
                        str(self.now.year)  + '-' + \
                        '{:02d}'.format(self.now.month) + '-' + \
                        '{:02d}'.format(self.now.day  ) + '-' + \
                        '{:02d}'.format(self.now.hour ) + \
                        '{:02d}'.format(self.now.minute)+ \
                        '.dburt'
        self.file_name_entry.setText(self.filename)
        ##print 'SAVE FIILENAME = ' + self.filename

    def getComboBoxEntries(self):
        self.keywords = str(self.areaCombo.currentText()) + '\t' +\
                        str(self.comboBox1.currentText()) + '\t' +\
                        str(self.comboBox2.currentText()) + '\t' +\
                        str(self.comboBox3.currentText()) + '\t'
        return self.keywords
    # this event is inherited and we overload it so the GUI_FileSave
    # is never deleted, (until we call close on the entire program)
    def closeEvent(self, evnt):
        if self.canWindowClose:
            super(GUI_FileSave, self).closeEvent(evnt)
        else:
            evnt.ignore()
            self.hide()
    # cancel button
    def handle_fileSaveCancel(self):
        self.hide()
    # when we decide keywords we'll add more here...
    def addComboKeywords(self,controller_type):
        list1 = [
            self.tr(controller_type),
            self.tr('AREA   51'),
            self.tr('Cheyenne ')]
        self.areaCombo.addItems(list1)



