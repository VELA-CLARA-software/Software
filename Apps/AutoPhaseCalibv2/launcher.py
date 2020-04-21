import os,sys
sys.path.append("../../../")
import Software.Procedures.qt as qt
from mainApp import *
# if (float(qt.QT_VERSION_STR.split('.')[0]) < 5.0):
from launcherUI_4 import *
# else:
    # from launcherUI import *

class launcherUI(qt.QObject):
    def __init__(self, *sys_argv):
        super(launcherUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        self.ui.pushButton.clicked.connect(self.launch)

    def launch(self):
        # print 'launching!'
        # os.system("python mainApp.py "+str(self.comboBox.currentText())+' '+str(self.comboBox_2.currentText())+' '+str(self.comboBox_3.currentText()))
        self.workerThread = runMainApp(self, str(self.ui.comboBox.currentText()), str(self.ui.comboBox_2.currentText()), str(self.ui.comboBox_3.currentText()))
        MainWindow.hide()
        self.workerThread.finished.connect(MainWindow.show)
        self.workerThread.start()

class runMainApp(qt.QThread):
    def __init__(self, *sys_argv):
        super(runMainApp, self).__init__()
        self.args = sys_argv

    def start(self):
        global app
        self.appObject = App(app, self.args)

if __name__ == "__main__":
    import sys
    global app
    app = qt.QApplication(sys.argv)
    MainWindow = qt.QMainWindow()
    launcher = launcherUI()
    MainWindow.show()
    sys.exit(app.exec_())
