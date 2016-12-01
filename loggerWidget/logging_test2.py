from PyQt4.QtCore import *
from PyQt4.QtGui import *
import loggerWidget as lw
import logging
import logger_subclass as logsub
import sys, time
''' simple logger that takes the name of the current module '''
logger = logging.getLogger(__name__)
''' a second logger with a specified name '''
logger2 = logging.getLogger("A Logger")

def test():
    ''' This will create some error messages for the logger '''
    logger.debug('damn, a bug')
    logger2.debug('Logger2 in action')
    logger.info('something to remember')
    logger.warning('that\'s not right')
    logger.error('foobar')
    logger.critical('really foobar')
    logger2.critical('logger2 is also really foobar')

def main():
    ''' Initiate PyQT application '''
    app = QApplication(sys.argv)

    ''' Reference to the logger from the subclass '''
    subclasslog = logsub.logger

    ''' initialise an instance of logging widget with a logger '''
    logwidget1 = lw.loggerWidget(logger)
    logwidget1.setDebugColour('red')
#    zmqlog1 = lw.loggerNetwork(logger, port=5556, ipaddress='148.79.112.153')
    sys.stdout = lw.redirectLogger(logwidget1, 'stdout')

    ''' initialise an instance of the logging Widget  and add loggers'''
    logwidget2 = lw.loggerWidget()
    ''' set colours of different log levels '''
    logwidget2.setLogColours(debugcolour='blue',infocolour='green',warningcolour='black',errorcolour='orange',criticalcolour='brown')
    logwidget2.setDateColumnWidth(160)
    logwidget2.setLevelColumnWidth(100)
    logwidget2.addLogger(logger)
    logwidget2.addLogger(logger2)
    logwidget2.addLogger(subclasslog)

    ''' or we can initialise with a list of loggers '''
    logwidget3 = lw.loggerWidget([logger, logger2, subclasslog])
    logwidget3.setColumnWidths(200,300,400)

    tab = QTabWidget()
    tab.resize(800,500)
    tab.addTab(logwidget1,"Single Log")
    tab.addTab(logwidget2,"2 Logs added")
    tab.addTab(logwidget3,"Initialised with 2 Logs")
    layout = QWidget()
    tab.addTab(layout,"Another Tab")

    ''' Display the Qt App '''
    tab.show()

    ''' Output some logging info! '''
    test()
    logsub.test()

    ''' Default PyQT exit handler '''
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
