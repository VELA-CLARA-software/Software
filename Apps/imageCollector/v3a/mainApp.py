import sys
import os
import multiprocessing

os.environ['PATH'] = os.environ['PATH'] + r';\\apclara1.dl.ac.uk\ControlRoomApps\Controllers\bin\Release'
#os.environ['PATH']=os.environ['PATH']+';\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin
# \\stage\\'
os.environ['PATH'] = os.environ['PATH'] + r';\\apclara1.dl.ac.uk\ControlRoomApps\Controllers\bin\Release\root_v5.34.34\bin'
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\model')
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\controller')
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\view')
from PyQt4 import QtGui
import controller
import view

class App(QtGui.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.view = view.Ui_MainWindow()
        self.MainWindow = QtGui.QMainWindow()
        self.view.setupUi(self.MainWindow)
        print 'Creating Controller'
        self.controller = controller.Controller(self.view)
        self.MainWindow.show()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = App(sys.argv)
    sys.exit(app.exec_())
