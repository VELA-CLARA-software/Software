#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class GUI_FileLoad(QWidget):
    def __init__(self, window_name = "", root = "/" ):
        super(GUI_FileLoad, self).__init__()
        # never got the below line to do what i hoped it might: close window with parent
        #self.setAttribute(Qt.WA_DeleteOnClose,True)
        self.resize(600, 600)
        self.setWindowTitle(window_name)
        # file browser tree view
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
        self.groupBox = QGroupBox()
        # which magnets to apply to
        self.groupBox.setFont(self.font)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.allMagnets = QRadioButton(self.groupBox)
        self.allMagnets.setObjectName("allMagnets")
        self.horizontalLayout.addWidget(self.allMagnets)
        self.quadMagnets = QRadioButton(self.groupBox)
        self.quadMagnets.setObjectName("quadMagnets")
        self.horizontalLayout.addWidget(self.quadMagnets)
        self.corrMagnets = QRadioButton(self.groupBox)
        self.corrMagnets.setObjectName("corrMagnets")
        self.horizontalLayout.addWidget(self.corrMagnets)
        self.groupBox.setTitle  ( "Which Magnets To Apply File To ")
        self.allMagnets.setText (  "All" )
        self.quadMagnets.setText(  "Quads " )
        self.corrMagnets.setText(  "Correctors" )
        self.groupBox.setTitle("Which Magnets To Apply File To?")
        self.treeView.hideColumn(1)
        self.treeView.setColumnWidth (0,250)
        self.treeView.setColumnWidth (2,100)
        self.treeView.setColumnWidth (3,250)
        self.treeView.setSortingEnabled(True)
        self.quadMagnets.toggled.connect( lambda:self.handle_magRadio(self.quadMagnets) )
        self.corrMagnets.toggled.connect( lambda:self.handle_magRadio(self.corrMagnets) )
        self.allMagnets.toggled.connect ( lambda:self.handle_magRadio(self.allMagnets ) )
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
        self.browserLayout.addWidget(self.groupBox)
        self.browserLayout.addWidget(self.label)
        self.browserLayout.addWidget(self.treeView)
        self.browserLayout.addWidget(self.buttonFrame)
        self.setLayout(self.browserLayout)
        self.dburtFile = ""
        self.allMagnets.setChecked(True)
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

    def handle_magRadio(self, r):
        if r.isChecked() == True:
            self.dburtType  = r
    def handle_fileLoadView(self):
        if self.dburtPathAndFile != "":
            self.textWindow = QPlainTextEdit()
            print 'opening file'
            self.fileText = open(self.dburtPathAndFile).read()
            self.textWindow.setPlainText(self.fileText)
            self.textWindow.resize(350, 700)
            self.textWindow.setWindowTitle(self.dburtFile)
            self.textWindow.setWindowIcon(QIcon('magpic.jpg'))
            self.textWindow.show()
        else:
            print "can't open file "

    def on_treeView_clicked(self, index):
        self.indexItem = self.fileSystemModel.index(index.row(), 0, index.parent())
        self.dburtFile = str(self.fileSystemModel.fileName(self.indexItem))
        self.dburtPathAndFile = self.fileSystemModel.filePath(self.indexItem)
        print  self.dburtFile
        print  self.dburtPathAndFile

