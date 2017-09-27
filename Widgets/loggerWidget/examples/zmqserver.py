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

def test():
    ''' This will create some error messages for the logger '''
    logger.debug('damn, a bug')
    logger.info('something to remember')
    logger.warning('that\'s not right')
    logger.error('foobar')
    logger.critical('really foobar')

def main():
    ''' Initiate PyQT application '''
    app = QApplication(sys.argv)

    ''' initialise an instance of logging widget with a logger '''
    logwidget1 = lw.loggerWidget(logger)
    zmqlog1 = lw.zmqPublishLogger(logger, port=5556, ipaddress='148.79.112.154', logName='network')
    zmqlog1.setLogName('differentName')
    zmqlog1.setIPAddress(ipaddress='148.79.112.153')

    tab = QTabWidget()
    tab.resize(800,500)
    tab.addTab(logwidget1,"Single Log")
    widget = QWidget()
    layout = QVBoxLayout()
    button = QPushButton("test logs")
    button.clicked.connect(test)
    layout.addWidget(button)
    widget.setLayout(layout)
    tab.addTab(widget,"Another Tab")

    ''' Display the Qt App '''
    tab.show()

    ''' Default PyQT exit handler '''
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
