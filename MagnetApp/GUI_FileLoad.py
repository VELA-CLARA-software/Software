#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4.QtGui import *

class GUI_FileLoad(QWidget):
    def __init__(self, window_name = "", root = "/" ):
        super(GUI_FileLoad, self).__init__()
        self.resize(700, 600)
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

        self.quadMagnets.toggled.connect(lambda:self.handle_magRadio(self.quadMagnets) )
        self.corrMagnets.toggled.connect(lambda:self.handle_magRadio(self.corrMagnets) )
        self.allMagnets.toggled.connect( lambda:self.handle_magRadio(self.allMagnets)  )


        # choose file label
        self.label = QLabel()
        self.label.setText( "Choose File To Load Magnet Settings" )
        #
        self.buttonFrame = QFrame()
        self.horizontalLayout2 = QHBoxLayout(self.buttonFrame)
        self.selectButton = QPushButton( self.buttonFrame )
        self.cancelButton = QPushButton( self.buttonFrame )
        self.horizontalLayout2.addWidget(self.selectButton)
        self.horizontalLayout2.addWidget(self.cancelButton)
        self.selectButton.setText( "Select" )
        self.cancelButton.setText( "Cancel" )
        self.cancelButton.setFont(self.font)
        self.selectButton.setFont(self.font)


        self.browserLayout.addWidget(self.groupBox)
        self.browserLayout.addWidget(self.label)
        self.browserLayout.addWidget(self.treeView)
        self.browserLayout.addWidget(self.buttonFrame)
        self.setLayout(self.browserLayout)

        self.dburtType = None
        self.dburtFile = ""
        self.allMagnets.setChecked(True)

    def handle_magRadio(self, r):
        if r.isChecked() == True:
            self.dburtType  = r

    def on_treeView_clicked(self, index):
        self.dburtFile = self.fileSystemModel.index(index.row(), 0, index.parent())
        #self.fileName = self.fileSystemModel.fileName( self.indexItem )
        #self.filePath = self.fileSystemModel.filePath( self.indexItem )