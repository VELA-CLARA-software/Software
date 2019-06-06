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
import win32gui
import win32con

class StdRedirector(object):
    """Redirects stdout/stderr to a GUI text box."""
    def __init__(self, stdout):
        self.stdout = stdout
        self.text_space = None
        self.text_log = ''

    def setWidget(self, text_widget):
        self.text_space = text_widget
        self.text_space.insertPlainText(self.text_log)

    def write(self, string):
        self.stdout.write(string)
        if self.text_space:
            self.text_space.moveCursor(QtGui.QTextCursor.End)
            self.text_space.insertPlainText(string)
            self.text_space.moveCursor(QtGui.QTextCursor.End)
        else:  # save up text for when a text widget becomes available
            self.text_log += string

    def flush(self):
        self.stdout.flush()


class App(QtGui.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.view = view.Ui_MainWindow()
        self.MainWindow = QtGui.QMainWindow()
        self.view.setupUi(self.MainWindow)
        print 'Creating Controller'
        self.controller = controller.Controller(self.view)
        if getattr(sys, 'frozen', False):  # are we bundled with PyInstaller?
            fg_window = win32gui.FindWindow(None, sys.executable)
            if win32gui.GetWindowText(fg_window) == sys.executable:
                win32gui.ShowWindow(fg_window, win32con.SW_HIDE)
        self.MainWindow.show()


if __name__ == '__main__':
    sys.stdout = StdRedirector(sys.stdout)
    sys.stderr = StdRedirector(sys.stderr)
    multiprocessing.freeze_support()
    app = App(sys.argv)
    sys.exit(app.exec_())
