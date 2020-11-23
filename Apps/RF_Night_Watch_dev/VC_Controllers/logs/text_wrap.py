




import VELA_CLARA_Vac_Valve_Control


class OutLog:
    def __init__(self, edit, out=None, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        self.edit = edit
        self.out = None
        self.color = color

    def write(self, m):
	"""This is an overload of the stdout write method"""
        if self.color:
            tc = self.edit.textColor()
            self.edit.setTextColor(self.color)

        self.edit.moveCursor(QTextCursor.End)
        self.edit.insertPlainText( m )

        if self.color:
            self.edit.setTextColor(tc)

        if self.out:
            self.out.write(m)

from rf_condition_view_base import Ui_rf_condition_mainWindow
class rf_condition_view(QMainWindow, Ui_rf_condition_mainWindow):
    pass

        #
    # other attributes will be initialised in base-class
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_rf_condition_mainWindow.__init__(self)
        self.setupUi(self)

        # stdout_fd = sys.stdout.fileno()
        # stdout_fde = sys.stderr.fileno()

        prevOutFd = os.dup(1)
        prevInFd = os.dup(0)
        prevErrFd = os.dup(2)

        # os.dup2(sys.stdout.fileno(), prevOutFd)
        # os.dup2(sys.stderr, stdout_fd)
        sys.stdout = OutLog(self.message_pad, os.dup(0))
        sys.stdout = OutLog(self.message_pad, os.dup(1))
        sys.stdout = OutLog(self.message_pad, os.dup(2))
		
class rf_condition(QtGui.QApplication):
    def __init__(self, argv):
        #
        # you need this init line here to instantiate a QTApplication
        QtGui.QApplication.__init__(self, argv)
        #
        # only run if a config file was passed
		
        self.view = rf_condition_view()
		
		self.llrf_init = VELA_CLARA_LLRF_Control.init()
		self.llrf_init.setQuiet()
        
		self.llrf_control = self.llrf_init.getLLRFController(MACHINE_MODE.PHYSICAL, rf_structure)
		
		
		
if __name__ == '__main__':
    print('Starting rf_condition Application')
    app = rf_condition(sys.argv)
    sys.exit(app.exec_())