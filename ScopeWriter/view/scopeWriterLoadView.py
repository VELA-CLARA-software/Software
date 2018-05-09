#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class scopeWriterLoadView(QWidget):
    fileName = pyqtSignal(str)
    def __init__(self, window_name = "", root = "/" ):
        super(scopeWriterLoadView, self).__init__()
        self.resize(600, 600)
        self.setWindowTitle(window_name)
        # file browser tree ui
        self.treeView = QTreeView()
        self.fileSystemModel = QFileSystemModel(self.treeView)
        self.fileSystemModel.setReadOnly(True)
        self.rootPath = self.fileSystemModel.setRootPath(root)
        self.treeView.setModel(self.fileSystemModel)
        self.treeView.setRootIndex( self.rootPath )
        self.treeView.clicked.connect(self.on_treeView_clicked)
        self.browserLayout = QVBoxLayout(self)
        self.font = QFont()
        self.font.setPointSize(12)
        self.treeView.hideColumn(1)
        self.treeView.setColumnWidth (0,250)
        self.treeView.setColumnWidth (2,100)
        self.treeView.setColumnWidth (3,250)
        self.treeView.setSortingEnabled(True)
        self.label = QLabel()
        self.label.setText( "Choose File To Load Magnet Settings" )
        self.buttonFrame = QFrame()
        self.horizontalLayout2 = QHBoxLayout(self.buttonFrame)
        self.selectButton = QPushButton( self.buttonFrame )
        self.cancelButton = QPushButton( self.buttonFrame )
        self.viewFiButton = QPushButton( self.buttonFrame )
        self.horizontalLayout2.addWidget(self.selectButton)
        self.horizontalLayout2.addWidget(self.cancelButton)
        self.horizontalLayout2.addWidget(self.viewFiButton)
        self.selectButton.setText( "Select" )
        self.cancelButton.setText( "Cancel" )
        self.viewFiButton.setText( "View" )
        self.cancelButton.setFont(self.font)
        self.selectButton.setFont(self.font)
        self.viewFiButton.setFont(self.font)
        self.browserLayout.addWidget(self.label)
        self.browserLayout.addWidget(self.treeView)
        self.browserLayout.addWidget(self.buttonFrame)
        self.setLayout(self.browserLayout)
        self.setupFile = ""
        self.cancelButton.clicked.connect(self.handle_fileLoadCancel)
        self.viewFiButton.clicked.connect(self.handle_fileLoadView)
        self.canWindowClose = False

    def closeEvent(self, evnt):
        print 'GUI_FileLoad  close event called'
        if self.canWindowClose:
            super(GUI_FileLoad, self).closeEvent(evnt)
        else:
            evnt.ignore()
            self.hide()
            #self.setWindowState(QtCore.Qt.WindowMinimized)

    def handle_fileLoadCancel(self):
        self.hide()

    def handle_fileLoadView(self):
        if self.setupPathAndFile != "":
            self.textWindow = QPlainTextEdit()
            print 'opening file'
            self.fileText = open(self.setupPathAndFile).read()
            self.textWindow.setPlainText(self.fileText)
            self.textWindow.resize(350, 700)
            self.textWindow.setWindowTitle(self.setupFile)
            self.textWindow.setWindowIcon(QIcon('magpic.jpg'))
            self.textWindow.show()
        else:
            print "can't open file "

    def on_treeView_clicked(self, index):
        self.indexItem = self.fileSystemModel.index(index.row(), 0, index.parent())
        self.setupPath = str(self.fileSystemModel.fileName(self.indexItem))
        self.setupPathAndFile = self.fileSystemModel.filePath(self.indexItem)
        self.fileName.emit(self.setupPathAndFile)
        print  self.setupPath
        print  self.setupPathAndFile

