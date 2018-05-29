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
from controller.controller import controller
from model.model import model
from view.mainView import mainView as view


class App(QtGui.QApplication):
    def __init__(self, sys_argv):
        QtGui.QWidget.__init__(self, sys_argv)
        self.model = model()
        self.view = view()
        print 'Creating Controller'
        self.control = controller(sys_argv, view = self.view, model= self.model)
        #self.view.show()
        print 'Running'


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
