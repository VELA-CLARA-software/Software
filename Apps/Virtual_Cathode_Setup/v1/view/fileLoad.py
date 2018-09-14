#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS 2017
# part of VIRTUAL_CATHDOE_INTERFACE
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from viewSource.Ui_FileLoad import Ui_FileLoad
import datetime



class GUI_FileLoad(QDialog, Ui_FileLoad):
    def __init__(self, window_name = "", root = "/" ):
        QDialog.__init__(self)
        self.setupUi(self)
        self.canWindowClose = False
        #self.root = QDir(root)
        self.root = root
        self.root = QString("//fed.cclrc.ac.uk/org/NLab/ASTeC/Projects/VELA/")
        self.snapshots = QString("//fed.cclrc.ac.uk/org/NLab/ASTeC/Projects/VELA/Snapshots")
        self.dburtpath = QString("//fed.cclrc.ac.uk/org/NLab/ASTeC/Projects/VELA/Snapshots/DBURT/")
        self.quadMagnets.toggled.connect(lambda: self.handle_magRadio(self.quadMagnets))
        self.corrMagnets.toggled.connect(lambda: self.handle_magRadio(self.corrMagnets))
        self.allMagnets.toggled.connect(lambda: self.handle_magRadio(self.allMagnets))
        self.dburtType = self.allMagnets

        self.dirModel = QFileSystemModel()
        self.dirModel.setFilter(QDir.NoDotAndDotDot|QDir.Dirs)
        self.rootPathIndex = self.dirModel.setRootPath(self.root)
        self.treeView.setModel(self.dirModel)
        self.treeView.setRootIndex(self.rootPathIndex)
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.setColumnWidth(0,250)
        self.treeView.setColumnWidth(3,250)
        self.treeView.setCurrentIndex(self.dirModel.index(self.dburtpath))
        snapshotindex = self.dirModel.index(self.snapshots)
        #self.treeView.expand(self.dirModel.index(self.dburtpath))
        self.treeView.setExpanded(snapshotindex, True)
        self.treeView.scrollTo(snapshotindex, QAbstractItemView.PositionAtCenter)

        self.filesModel = QFileSystemModel()
        self.filesModel.setFilter(QDir.NoDotAndDotDot|QDir.Files)
        self.dburtpathIndex = self.filesModel.setRootPath(self.dburtpath)
        self.listView.setModel(self.filesModel)
        self.listView.setRootIndex(self.dburtpathIndex)
        self.dirModel.directoryLoaded.connect(self.handle_directoryLoaded)
        self.filesModel.directoryLoaded.connect(self.handle_filesLoaded)
        self.cancelButton.clicked.connect(self.handle_fileLoadCancel)
        # The select button is handled in the magnetAppController.handle_fileLoadSelect()
        #self.selectButton.clicked.connect(self.handle_fileLoadSelect)
        #self.on_treeView_clicked(self.dirModel.index(self.dburtpath))
        self.viewButton.clicked.connect(self.handle_fileLoadView)
        self.selectedDirPath = self.dburtpath
        self.selectedFile = ""
        self.selectedFilePath = ""
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(self.dburtpath)
        self.watcher.directoryChanged.connect(self.handle_fileDirectoryChanged)
#        self.selectedDirPathselectedDirPath
        #self.dirModel.dataChanged[QModelIndex,QModelIndex].connect(self.handle_fileDirectoryChanged2)
        self.textWindowList = []

    def burtLoadFailed(self):
        self.label.setText(
                "<font color='red'>)-: !!WARNING!! CLARA did not accept requested "
                "magnet current settings try re-applying or check file !!WARNING!! :-( </font>")

    def burtLoadSuccess(self):
        self.label.setText(
                "<font color='green'>!!Success!! CLARA did not accept all settings :)  </font>")

    def handle_fileLoadSelect(self):
        print 'handle_fileLoadSelect'

    def handle_fileDirectoryChanged(self):
        print 'watcher handle_fileDirectoryChanged'
        print 'self.selectedDirPath  = ' + str(self.selectedDirPath)
        self.dburtpathIndex = self.filesModel.setRootPath(self.selectedDirPath)
        self.listView.setRootIndex(self.dburtpathIndex)

    def handle_directoryLoaded(self):
        print 'handle_directoryLoaded'

    def handle_filesLoaded(self):
        print 'handle_filesLoaded'
        index = self.filesModel.index(self.filesModel.rowCount(),0)
        self.listView.scrollTo(index, QAbstractItemView.PositionAtCenter)

    def on_treeView_clicked(self, index):
        print("on_treeView_clicked")
        self.indexItem = self.dirModel.index(index.row(), 0, index.parent())
        self.dburtFile = str(self.dirModel.fileName(self.indexItem))
        self.selectedDirPath = self.dirModel.filePath(self.indexItem)
        print 'self.selectedDirPath ' + str(self.selectedDirPath)
        self.rootPathIndex = self.filesModel.setRootPath(self.selectedDirPath)
        self.listView.setRootIndex(self.rootPathIndex)
        self.watcher.removePaths(self.watcher.directories())
        print 'Watching ' + str(self.selectedDirPath)
        self.watcher.addPath(QString(self.selectedDirPath))

    def on_listView_clicked(self, index):
        indexItem = self.filesModel.index(index.row(), 0, index.parent())
        self.selectedFile = str(self.filesModel.fileName(indexItem))
        self.selectedFilePath = self.selectedDirPath + self.selectedFile
        print 'on_listView_clicked = ' + self.selectedFilePath

    def handle_magRadio(self, r):
        if r.isChecked() == True:
            self.dburtType = r

    # This window only dies when the entire app closes
    # top do this we call hide()
    def closeEvent(self, evnt):
        print 'GUI_FileLoad  close event called'
        if self.canWindowClose:
            super(GUI_FileLoad, self).closeEvent(evnt)
        else:
            evnt.ignore()
            self.hide()

    def handle_fileLoadCancel(self):
        self.done(0)

    def handle_fileLoadView(self):
        if self.selectedFilePath != "":
            textWindow = QPlainTextEdit()
            print 'opening file'
            fileText = open(self.selectedFilePath).read()
            textWindow.setPlainText(fileText)
            textWindow.resize(500, 700)
            textWindow.selectAll()
            font = QFont()
            font.setPointSize(16)
            textWindow.setFont(font)
            tc = QTextCursor()
            tc.setPosition(textWindow.document().characterCount())
            textWindow.setTextCursor(tc)
            textWindow.setWindowTitle(self.selectedFile)
            textWindow.setWindowIcon(QIcon('magpic.jpg'))

            self.textWindowList.append(textWindow)

            self.textWindowList[-1].show()
        else:
            print "can't open file "

