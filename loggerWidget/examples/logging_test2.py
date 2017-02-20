from PyQt4.QtCore import *
from PyQt4.QtGui import *
import loggerWidget as lw
import logging
import logger_subclass as logsub
import sys, time, os
import VELA_CLARA_MagnetControl as mag
# import velaINJBeamPositionMonitorControl as vbpmc

''' simple logger that takes the name of the current module '''
logger = logging.getLogger(__name__)
''' a second logger with a specified name '''
logger2 = logging.getLogger("A Logger")

import os
import sys
from contextlib import contextmanager

def fileno(file_or_fd):
    fd = getattr(file_or_fd, 'fileno', lambda: file_or_fd)()
    if not isinstance(fd, int):
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    return fd

@contextmanager
def stdout_redirected(to=os.devnull, stdout=None):
    if stdout is None:
       stdout = sys.stdout

    stdout_fd = fileno(stdout)
    # copy stdout_fd before it is overwritten
    #NOTE: `copied` is inheritable on Windows when duplicating a standard stream
    with os.fdopen(os.dup(stdout_fd), 'wb') as copied:
        stdout.flush()  # flush library buffers that dup2 knows nothing about
        try:
            os.dup2(fileno(to), stdout_fd)  # $ exec >&to
        except ValueError:  # filename
            with open(to, 'wb') as to_file:
                os.dup2(to_file.fileno(), stdout_fd)  # $ exec > to
        try:
            yield stdout # allow code to be run with the redirected stdout
        finally:
            # restore stdout to its previous value
            #NOTE: dup2 makes stdout_fd inheritable unconditionally
            stdout.flush()
            os.dup2(copied.fileno(), stdout_fd)  # $ exec >&copied

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
    print "this is a test"

    ''' Default PyQT exit handler '''
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
