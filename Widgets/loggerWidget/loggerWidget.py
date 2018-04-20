import sys
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
import logging
import os
# import rpyc
import zmq, time
# import threading
# from threading import Thread, Event, Timer

widgetLogger = logging.getLogger(__name__)

colournames = {
'aliceblue':            '#F0F8FF',
'antiquewhite':         '#FAEBD7',
'aqua':                 '#00FFFF',
'aquamarine':           '#7FFFD4',
'azure':                '#F0FFFF',
'beige':                '#F5F5DC',
'bisque':               '#FFE4C4',
'black':                '#000000',
'blanchedalmond':       '#FFEBCD',
'blue':                 '#0000FF',
'blueviolet':           '#8A2BE2',
'brown':                '#A52A2A',
'burlywood':            '#DEB887',
'cadetblue':            '#5F9EA0',
'chartreuse':           '#7FFF00',
'chocolate':            '#D2691E',
'coral':                '#FF7F50',
'cornflowerblue':       '#6495ED',
'cornsilk':             '#FFF8DC',
'crimson':              '#DC143C',
'cyan':                 '#00FFFF',
'darkblue':             '#00008B',
'darkcyan':             '#008B8B',
'darkgoldenrod':        '#B8860B',
'darkgray':             '#A9A9A9',
'darkgreen':            '#006400',
'darkkhaki':            '#BDB76B',
'darkmagenta':          '#8B008B',
'darkolivegreen':       '#556B2F',
'darkorange':           '#FF8C00',
'darkorchid':           '#9932CC',
'darkred':              '#8B0000',
'darksalmon':           '#E9967A',
'darkseagreen':         '#8FBC8F',
'darkslateblue':        '#483D8B',
'darkslategray':        '#2F4F4F',
'darkturquoise':        '#00CED1',
'darkviolet':           '#9400D3',
'deeppink':             '#FF1493',
'deepskyblue':          '#00BFFF',
'dimgray':              '#696969',
'dodgerblue':           '#1E90FF',
'firebrick':            '#B22222',
'floralwhite':          '#FFFAF0',
'forestgreen':          '#228B22',
'fuchsia':              '#FF00FF',
'gainsboro':            '#DCDCDC',
'ghostwhite':           '#F8F8FF',
'gold':                 '#FFD700',
'goldenrod':            '#DAA520',
'gray':                 '#808080',
'green':                '#008000',
'greenyellow':          '#ADFF2F',
'honeydew':             '#F0FFF0',
'hotpink':              '#FF69B4',
'indianred':            '#CD5C5C',
'indigo':               '#4B0082',
'ivory':                '#FFFFF0',
'khaki':                '#F0E68C',
'lavender':             '#E6E6FA',
'lavenderblush':        '#FFF0F5',
'lawngreen':            '#7CFC00',
'lemonchiffon':         '#FFFACD',
'lightblue':            '#ADD8E6',
'lightcoral':           '#F08080',
'lightcyan':            '#E0FFFF',
'lightgoldenrodyellow': '#FAFAD2',
'lightgreen':           '#90EE90',
'lightgray':            '#D3D3D3',
'lightpink':            '#FFB6C1',
'lightsalmon':          '#FFA07A',
'lightseagreen':        '#20B2AA',
'lightskyblue':         '#87CEFA',
'lightslategray':       '#778899',
'lightsteelblue':       '#B0C4DE',
'lightyellow':          '#FFFFE0',
'lime':                 '#00FF00',
'limegreen':            '#32CD32',
'linen':                '#FAF0E6',
'magenta':              '#FF00FF',
'maroon':               '#800000',
'mediumaquamarine':     '#66CDAA',
'mediumblue':           '#0000CD',
'mediumorchid':         '#BA55D3',
'mediumpurple':         '#9370DB',
'mediumseagreen':       '#3CB371',
'mediumslateblue':      '#7B68EE',
'mediumspringgreen':    '#00FA9A',
'mediumturquoise':      '#48D1CC',
'mediumvioletred':      '#C71585',
'midnightblue':         '#191970',
'mintcream':            '#F5FFFA',
'mistyrose':            '#FFE4E1',
'moccasin':             '#FFE4B5',
'navajowhite':          '#FFDEAD',
'navy':                 '#000080',
'oldlace':              '#FDF5E6',
'olive':                '#808000',
'olivedrab':            '#6B8E23',
'orange':               '#FFA500',
'orangered':            '#FF4500',
'orchid':               '#DA70D6',
'palegoldenrod':        '#EEE8AA',
'palegreen':            '#98FB98',
'paleturquoise':        '#AFEEEE',
'palevioletred':        '#DB7093',
'papayawhip':           '#FFEFD5',
'peachpuff':            '#FFDAB9',
'peru':                 '#CD853F',
'pink':                 '#FFC0CB',
'plum':                 '#DDA0DD',
'powderblue':           '#B0E0E6',
'purple':               '#800080',
'red':                  '#FF0000',
'rosybrown':            '#BC8F8F',
'royalblue':            '#4169E1',
'saddlebrown':          '#8B4513',
'salmon':               '#FA8072',
'sandybrown':           '#FAA460',
'seagreen':             '#2E8B57',
'seashell':             '#FFF5EE',
'sienna':               '#A0522D',
'silver':               '#C0C0C0',
'skyblue':              '#87CEEB',
'slateblue':            '#6A5ACD',
'slategray':            '#708090',
'snow':                 '#FFFAFA',
'springgreen':          '#00FF7F',
'steelblue':            '#4682B4',
'tan':                  '#D2B48C',
'teal':                 '#008080',
'thistle':              '#D8BFD8',
'tomato':               '#FF6347',
'turquoise':            '#40E0D0',
'violet':               '#EE82EE',
'wheat':                '#F5DEB3',
'white':                '#FFFFFF',
'whitesmoke':           '#F5F5F5',
'yellow':               '#FFFF00',
'yellowgreen':          '#9ACD32'}

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class colourNameError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

def getColour(label):
    return colournames[label.lower()]

class QPlainTextEditLogger(logging.Handler):
    def __init__(self, tableWidget, model):
        super(QPlainTextEditLogger, self).__init__()
        self.tableWidget = tableWidget
        self.debugColour = 'gray'
        self.infoColour = 'black'
        self.warningColour = 'deeppink'
        self.errorColour = 'red'
        self.criticalColor = 'red'
        self.dateColumnWidth = 160
        self.levelColumnWidth = 120
        self.logColumnWidth = 80
        self.logLength = 50
        self.model = model

    def emit(self, record, *args, **kwargs):
        while self.model.rowCount() >= self.logLength:
            self.model.removeRow(-1)
        newRowNumber = 0#self.model.rowCount()
        self.model.insertRow(newRowNumber)
        self.tableWidget.setShowGrid(True)
        self.model.setColumnCount(4)
        # self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setColumnWidth(0,self.dateColumnWidth)
        self.tableWidget.setColumnWidth(1,self.levelColumnWidth)
        self.tableWidget.setColumnWidth(2,self.logColumnWidth)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setWordWrap(True)
        msg = self.format(record)
        color = ''
        bold = False
        if(record.levelname == 'DEBUG'):
            color = getColour(self.debugColour)
        elif(record.levelname == 'INFO'):
            color = getColour(self.infoColour)
        elif(record.levelname == 'WARNING'):
            color = getColour(self.warningColour)
        elif(record.levelname == 'ERROR'):
            color = getColour(self.errorColour)
        elif(record.levelname == 'CRITICAL'):
            bold = True
            color = getColour(self.criticalColor)
        try:
            record.publisher
        except:
            record.publisher = ''
        if hasattr(record, 'networkname'):
            record.name = record.networkname
        logdata = [record.asctime, record.publisher+'('+record.name+')', record.levelname, record.message]
        font = QFont()
        font.setBold(bold)
        for i in range(4):
            # self.textbox = QPlainTextEdit()
            # self.textbox.setReadOnly(True)
            # self.textbox.appendHtml(color+str(logdata[i])+'</font>')
            # self.tableWidget.setIndexWidget(self.model.index(newRowNumber, i), self.textbox)
            standarditem = QStandardItem()
            standarditem.setText(str(logdata[i]))
            standarditem.setFont(font)
            standarditem.setForeground(QColor(color))
            self.model.setItem(newRowNumber,i, standarditem)
            # self.model.setData(self.model.index(newRowNumber,i), Qt.blue, Qt.BackgroundRole)

class zmqPublishLogger(QObject):
    def __init__(self, logger=None, *args, **kwargs):
        super(zmqPublishLogger,self).__init__()
        self.networkLogger = zmqPublishLoggerHandler(*args, **kwargs)
        if(logger != None):
            if(isinstance(logger, list)):
                for log in logger:
                    self.addLogger(log)
            else:
                self.addLogger(logger)
        self.networkLogger.setFormatter(logging.Formatter(' %(asctime)s - %(name)s - %(publisher)s - %(levelno)s - %(message)s'))
        self.addLogger(widgetLogger)

    def addLogger(self, logger):
        logger.addHandler(self.networkLogger)
        logger.setLevel(logging.DEBUG)

    def setLogName(self, name):
        self.networkLogger.publisher = name

    def setIPAddress(self, ipaddress):
        self.networkLogger.setIPAddress(ipaddress=ipaddress)

class zmqPublishLoggerHandler(logging.Handler):
    def __init__(self, logName=__name__, *args, **kwargs):
        super(zmqPublishLoggerHandler, self).__init__()
        self.context = zmq.Context()
        self.connect(*args, **kwargs)
        self.publisher = logName
        time.sleep(0.2)

    def connect(self, ipaddress='127.0.0.1', port=5556):
        self.socket = self.context.socket(zmq.PUSH)
        self.ipaddress = str(ipaddress)
        self.port = str(port)
        self.socket.connect("tcp://%s:%s" % (self.ipaddress, self.port))

    def setIPAddress(self, ipaddress):
        self.connect(ipaddress=ipaddress, port=self.port)

    def emit(self, record, *args, **kwargs):
        self.socket.send_pyobj([self.publisher, record.name, record.levelno, record.message])

class zmqReceiverLogger(QObject):
    def __init__(self, *args, **kwargs):
        super(zmqReceiverLogger,self).__init__()
        self.thread = zmqReceiverLoggerThread(*args, **kwargs)
        self.thread.start()

class zmqReceiverLoggerThread(QThread):

    def __init__(self, port=5556):
        super(zmqReceiverLoggerThread, self).__init__()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.port = port

    def run(self):
        self.socket.bind("tcp://*:%s" % (self.port))

        while True:
            string = self.socket.recv_pyobj()
            publisher, name, level, message = string
            widgetLogger.log(level, message, extra={'networkname': name, 'publisher': publisher})

class loggerWidget(QWidget):
    def __init__(self, logger=None, networkLogger=False, parent=None):
        super(loggerWidget,self).__init__(parent)
        self.tablewidget = QTableView()

        layout = QGridLayout()
        self.model = QStandardItemModel(0, 4)
        self.model.setHorizontalHeaderLabels(['Date', 'Logger', 'Severity', 'VALUE'])

        # filter proxy model
        self.filter_proxy_model = QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterKeyColumn(2) # third column

        # # line edit for filtering
        # layout = QVBoxLayout()
        filterbox = QComboBox()
        filterbox.addItems(['All', 'Info','Warning','Error','Critical'])
        filterbox.setMinimumWidth(100)
        filterbox.currentIndexChanged.connect(lambda x: self.filter_proxy_model.setFilterRegExp(self.filterLogs(x)))
        layout.addWidget(filterbox,0,1,1,1)
        clearButton = QPushButton('Clear Log')
        clearButton.setFixedSize(74,20)
        clearButton.setFlat(True)
        clearButton.clicked.connect(self.clearLog)
        layout.addWidget(clearButton,0,2,1,1)
        self.tablewidget.setModel(self.filter_proxy_model)
        saveButton = QPushButton('Save Log')
        saveButton.setFixedSize(74,20)
        saveButton.setFlat(True)
        saveButton.clicked.connect(self.saveLog)
        layout.addWidget(self.tablewidget,1,0,10,5)
        layout.addWidget(saveButton,0,3,1,1)
        self.logTextBox = QPlainTextEditLogger(self.tablewidget, self.model)
        self.setLayout(layout)
        if(logger != None):
            if(isinstance(logger, list)):
                for log in logger:
                    self.addLogger(log)
            else:
                self.addLogger(logger)
        self.logTextBox.setFormatter(logging.Formatter(' %(asctime)s - %(name)s - %(levelno)s - %(message)s'))
        self.addLogger(widgetLogger)
        if networkLogger:
            self.networkLogThread = networkLogThread()
            global logWidget
            logWidget = self

    def filterLogs(self, level):
        if level == 0:
            return ''
        elif level == 1:
            return r'INFO|WARNING|ERROR|CRITICAL'
        elif level == 2:
            return r'WARNING|ERROR|CRITICAL'
        elif level == 3:
            return r'ERROR|CRITICAL'
        elif level == 4:
            return r'CRITICAL'
        #lambda x: self.filter_proxy_model.setFilterRegExp(filterbox.itemText(x))

    def setColumnWidths(self,dateWidth=160, levelWidth=120, logWidth=80):
        self.logTextBox.dateColumnWidth = dateWidth
        self.logTextBox.levelColumnWidth = levelWidth
        self.logTextBox.logColumnWidth = logWidth

    def setDateColumnWidth(self, dateWidth=160):
        self.logTextBox.dateColumnWidth = dateWidth

    def setLevelColumnWidth(self, levelWidth=120):
        self.logTextBox.levelColumnWidth = levelWidth

    def setDebugColour(self, colour):
        try:
            getColour(colour)
        except:
            colour = 'gray'
        finally:
            self.logTextBox.debugColour = colour

    def setInfoColour(self, colour):
        try:
            getColour(colour)
        except:
            colour = 'black'
        finally:
            self.logTextBox.infoColour = colour

    def setWarningColour(self, colour):
        try:
            getColour(colour)
        except:
            colour = 'deeppink'
        finally:
            self.logTextBox.warningColour = colour

    def setErrorColour(self, colour):
        try:
            getColour(colour)
        except:
            colour = 'red'
        finally:
            self.logTextBox.errorColour = colour

    def setCriticalColour(self, colour):
        try:
            getColour(colour)
        except:
            colour = 'red'
        finally:
            self.logTextBox.criticalColor = colour

    def setLogColours(self, debugcolour='gray', infocolour='black', warningcolour='deeppink', errorcolour='red',criticalcolour='red'):
        self.setDebugColour(debugcolour)
        self.setInfoColour(infocolour)
        self.setWarningColour(warningcolour)
        self.setErrorColour(errorcolour)
        self.setCriticalColour(criticalcolour)

    def addLogger(self, logger, level=logging.DEBUG):
        logger.addHandler(self.logTextBox)
        logger.setLevel(level)

    def setLoggerLevel(self, logger, level=logging.DEBUG):
        logger.setLevel(level)

    def saveLog(self):
        rows = self.model.rowCount()
        saveData = range(rows);
        for r in range(rows):
            row = range(4)
            for i in range(4):
                widg = self.model.item(r, i)
                row[i] = widg.text()
            saveData[r] = row
        # print saveData
        saveFileName = str(QFileDialog.getSaveFileName(self, 'Save Log', filter="TXT files (*.txt);;", selectedFilter="TXT files (*.txt)"))
        filename, file_extension = os.path.splitext(saveFileName)
        if file_extension == '.txt':
        #     print "csv!"
            fmt='%s \t %s \t %s \t %s'
            target = open(saveFileName,'w')
            for row in saveData:
                target.write((fmt % tuple(row))+'\n')
        widgetLogger.info('Log Saved to '+saveFileName)

    def setLogLength(self, length):
        self.logTextBox.logLength = length

    def clearLog(self):
        numrows = self.model.rowCount()
        for i in reversed(range(numrows)):
            self.model.removeRow(i)

class redirectLogger(object):
    """File-like object to log text using the `logging` module."""

    def __init__(self, widget=None, name=None):
        self.logger = logging.getLogger(name)
        widget.addLogger(self.logger)

    def write(self, msg, level=logging.INFO):
        if msg != '\n':
            self.logger.log(level, msg)

    def flush(self):
        for handler in self.logger.handlers:
            handler.flush()

    def __getattr__(self, attr):
        return getattr(self.logger, attr)
