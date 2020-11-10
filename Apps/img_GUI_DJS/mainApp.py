from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from control.control import control
from procedure.procedure import procedure as procedure
from View.view import view as view
import sys


class App(QApplication):
    def __init__(self, sys_argv):
        QWidget.__init__(self, sys_argv)
        self.procedure = procedure()
        self.view = view()
        print( 'Creating Controller')
        self.control = control(sys_argv, view = self.view, procedure= self.procedure)
        print('Running')


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
