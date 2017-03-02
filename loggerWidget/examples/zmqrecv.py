import sys
import zmq



import sys, time, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
sys.path.append("..")
import loggerWidget as lw
import logging
import logger_subclass as logsub
import VELA_CLARA_MagnetControl as mag
# import velaINJBeamPositionMonitorControl as vbpmc

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
    zmqreceiver = lw.zmqReceiverLogger(port=5556)
    logwidget1.setDebugColour('red')

    tab = QTabWidget()
    tab.resize(800,500)
    tab.addTab(logwidget1,"Single Log")

    ''' Display the Qt App '''
    tab.show()

    ''' Default PyQT exit handler '''
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
