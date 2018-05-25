import sys,os

os.environ['PATH']=os.environ['PATH']+';\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\'
#os.environ['PATH']=os.environ['PATH']+';\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin
# \\stage\\'
#os.environ['PATH']=os.environ['PATH']+';\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin
# \\Release\\root_v5.34.34\\bin\\'
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\model')
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\controller')
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\view')
# for i in sys.path:
#     print "hi"
#     print i
from PyQt4 import QtGui, QtCore
#import model.model as model
#import controller.controller as controller
import view.mainView as view


class App(QtGui.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.view = view.mainView()
        #self.MainWindow = QtGui.QMainWindow()
        #self.view.setupUi(self.MainWindow)
        #self.model = model.Model()
        print 'Creating Controller'
        #self.controller = controller.Controller(self.view, self.model)
        self.view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
