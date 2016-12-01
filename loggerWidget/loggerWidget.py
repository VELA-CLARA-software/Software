import sys
from PyQt4 import QtCore, QtGui
import logging
import os
widgetLogger = logging.getLogger(__name__)

class QPlainTextEditLogger(logging.Handler):
    def __init__(self, tableWidget):
        super(QPlainTextEditLogger, self).__init__()
        self.tableWidget = tableWidget

    def emit(self, record):
        newRowNumber = self.tableWidget.rowCount()
        self.tableWidget.insertRow(newRowNumber)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setColumnWidth(0,140)"""TIM EDIT"""
        self.tableWidget.setColumnWidth(1,40)"""TIM EDIT"""
        self.tableWidget.setColumnWidth(2,40)""" TIM EDIT"""
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setWordWrap(True)
        msg = self.format(record)
        color = ''
        if(record.levelname == 'DEBUG'):
            color = '<font color=\"Grey\">'
        elif(record.levelname == 'INFO'):
            color = '<font color=\"Green\">'
        elif(record.levelname == 'WARNING'):
            color = '<font color=\"DeepPink\">'
        elif(record.levelname == 'ERROR'):
            color = '<font color=\"RED\">'
        elif(record.levelname == 'CRITICAL'):
            color = '<font style="font-weight:bold" color=\"RED\">'
        logdata = [record.asctime, record.name, record.levelname, record.message]
        for i in range(4):
            self.textbox = QtGui.QPlainTextEdit()
            self.textbox.setReadOnly(True)
            self.textbox.appendHtml(color+str(logdata[i])+'</font>')
            self.tableWidget.setCellWidget(newRowNumber, i, self.textbox)

class loggerWidget(QtGui.QWidget):
    def __init__(self, logger=None, parent=None):
        super(loggerWidget,self).__init__(parent)
        self.tablewidget = QtGui.QTableWidget()
        layout = QtGui.QGridLayout()
        saveButton = QtGui.QPushButton('Save Log')
        saveButton.setFixedSize(74,20)
        saveButton.setFlat(True)
        saveButton.clicked.connect(self.saveLog)
        layout.addWidget(self.tablewidget,0,0,10,3)
        layout.addWidget(saveButton,10,1,1,1)
        self.logTextBox = QPlainTextEditLogger(self.tablewidget)
        self.setLayout(layout)
        if(logger != None):
            if(isinstance(logger, list)):
                for log in logger:
                    self.addLogger(log)
            else:
                self.addLogger(logger)
        self.logTextBox.setFormatter(logging.Formatter(' %(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.addLogger(widgetLogger)

    def addLogger(self, logger):
        logger.addHandler(self.logTextBox)
        logger.setLevel(logging.DEBUG)

    def setLoggerLevel(self, logger, level):
        logger.setLevel(level)

    def saveLog(self):
        rows = self.tablewidget.rowCount()
        saveData = range(rows);
        for r in range(rows):
            row = range(4)
            for i in range(4):
                widg = self.tablewidget.cellWidget(r, i)
                row[i] = widg.toPlainText()
            saveData[r] = row
        # print saveData
        saveFileName = str(QtGui.QFileDialog.getSaveFileName(self, 'Save Log', filter="TXT files (*.txt);;", selectedFilter="TXT files (*.txt)"))
        filename, file_extension = os.path.splitext(saveFileName)
        if file_extension == '.txt':
        #     print "csv!"
            fmt='%s \t %s \t %s \t %s'
            target = open(saveFileName,'w')
            for row in saveData:
                target.write((fmt % tuple(row))+'\n')
        widgetLogger.info('Log Saved to '+saveFileName)
