import sys

sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage')
from VELA_CLARA_enums import MACHINE_MODE
from VELA_CLARA_LLRF_Control import LLRF_TYPE
import VELA_CLARA_LLRF_Control
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QTextCursor
from src.view.OLD.rf_condition_view_base import Ui_rf_condition_mainWindow
import sys
import os

def fileno(file_or_fd):
    fd = getattr(file_or_fd, 'fileno', lambda: file_or_fd)()
    if not isinstance(fd, int):
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    return fd

class outlogger(object):

    def __init__(self,edit):
        #file.__init__(self)
        self.edit = edit
        self.piper, self.pipew = os.pipe()
        print('self.pipe = ', self.pipew)
        #self.pipew.write = self.write()

    def write(self, m):
        #os.write(self.pipew,m)
        #print a
        self.edit.moveCursor(QTextCursor.End)
        self.edit.insertPlainText( m )

    def flush(self, pipe):
        #os.write(self.pipew,m)
        #sys.stdout.flush()
        a = os.read(pipe,99999)
        self.edit.moveCursor(QTextCursor.End)
        self.edit.insertPlainText( a )

class rf_condition_view(QMainWindow, Ui_rf_condition_mainWindow):
    pass

        #
    # other attributes will be initialised in base-class
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_rf_condition_mainWindow.__init__(self)
        self.setupUi(self)




        print('222')
        #os.dup2(sio.pipew,  sys.stdout.fileno())
        print('333')
        # stdout_fd = sys.stdout.fileno()
        # stdout_fde = sys.stderr.fileno()

        prevOutFd = os.dup(1)
        prevInFd = os.dup(0)
        prevErrFd = os.dup(2)

        #sys.stdout = outlogger(self.message_pad)

        #fileno()

        print("PYTHON STANDARD OUT")

		#sys.stdout = OutLog(self.message_pad, os.dup(1))
        # sys.stdout = OutLog(self.message_pad, os.dup(2))




from PyQt4.QtGui import QApplication
class rf_condition(QApplication):
    def __init__(self, argv):
        #
	# you need this init line here to instantiate a QTApplication
#
		QApplication.__init__(self, argv)
		self.piper, self.pipew = os.pipe()
        os.dup2(sys.stdout.fileno(), self.pipew)
		#
		# only run if a config file was passed
		self.view = rf_condition_view()
		self.view.show()

        print('111')
        sys.stdout = outlogger(self.view.message_pad)

		QApplication.processEvents()
		self.llrf_init = VELA_CLARA_LLRF_Control.init()
		self.llrf_init.setQuiet()
		self.llrf_control = self.llrf_init.getLLRFController(MACHINE_MODE.PHYSICAL, LLRF_TYPE.L01)

		sys.stdout.flush()


		#raise Exception("sdddddddddddddddddddddddddddddddddddddddd"	)


if __name__ == '__main__':
    print('Starting rf_condition Application')
    app = rf_condition(sys.argv)
    sys.exit(app.exec_())

#libc = ctypes.oledll(None)

from contextlib import contextmanager
import io, sys, os

@contextmanager
def stdout_redirector(stream):
    old_stdout = sys.stdout
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = old_stdout



f = io.StringIO()

print fileno(f)
print fileno(f)
print fileno(f)
print fileno(f)

with stdout_redirector(f):
    print('foobar')
    print(12)
    print(12)
    #libc.puts(b'this comes from C')
    os.system('echo and this is from echo')
print('Got stdout: "{0}"'.format(f.getvalue()))

# import sys
# import os
# sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage')
# from VELA_CLARA_enums import MACHINE_MODE
# from VELA_CLARA_enums import MACHINE_AREA
# from VELA_CLARA_enums import CONTROLLER_TYPE
# from VELA_CLARA_LLRF_Control import LLRF_TYPE
# import VELA_CLARA_LLRF_Control


# from contextlib import contextmanager
# import ctypes
# import io
# import os, sys
# import tempfile

# libc = ctypes.CDLL(None)
# c_stdout = ctypes.c_void_p.in_dll(libc, 'stdout')

# @contextmanager
# def stdout_redirector(stream):
    # # The original fd stdout points to. Usually 1 on POSIX systems.
    # original_stdout_fd = sys.stdout.fileno()

    # def _redirect_stdout(to_fd):
        # """Redirect stdout to the given file descriptor."""
        # # Flush the C-level buffer stdout
        # libc.fflush(c_stdout)
        # # Flush and close sys.stdout - also closes the file descriptor (fd)
        # sys.stdout.close()
        # # Make original_stdout_fd point to the same file as to_fd
        # os.dup2(to_fd, original_stdout_fd)
        # # Create a new sys.stdout that points to the redirected fd
        # sys.stdout = io.TextIOWrapper(os.fdopen(original_stdout_fd, 'wb'))

    # # Save a copy of the original stdout fd in saved_stdout_fd
    # saved_stdout_fd = os.dup(original_stdout_fd)
    # try:
        # # Create a temporary file and redirect stdout to it
        # tfile = tempfile.TemporaryFile(mode='w+b')
        # _redirect_stdout(tfile.fileno())
        # # Yield to caller, then redirect stdout back to the saved fd
        # yield
        # _redirect_stdout(saved_stdout_fd)
        # # Copy contents of temporary file to the given stream
        # tfile.flush()
        # tfile.seek(0, io.SEEK_SET)
        # stream.write(tfile.read())
    # finally:
        # tfile.close()
        # os.close(saved_stdout_fd)


# f = io.BytesIO()

# with stdout_redirector(f):
    # print('foobar')
    # print(12)
    # libc.puts(b'this comes from C')
    # os.system('echo and this is from echo')
# print('Got stdout: "{0}"'.format(f.getvalue().decode('utf-8')))



# import time
# from PyQt4.QtGui import QTextCursor
# class OutLog:
    # def __init__(self, edit, out=None, color=None):
        # """(edit, out=None, color=None) -> can write stdout, stderr to a
        # QTextEdit.
        # edit = QTextEdit
        # out = alternate stream ( can be the original sys.stdout )
        # color = alternate color (i.e. color stderr a different color)
        # """
        # self.edit = edit
        # self.out = out
        # self.color = color

    # def write(self, m):
	# """This is an overload of the stdout write method"""
        # if self.color:
            # tc = self.edit.textColor()
            # self.edit.setTextColor(self.color)

        # self.edit.moveCursor(QTextCursor.End)
        # self.edit.insertPlainText( m )

        # if self.color:
            # self.edit.setTextColor(tc)

        # if self.out:
            # self.out.write(m)
        # QApplication.processEvents()


# from PyQt4.QtGui import QMainWindow
# from PyQt4.QtGui import QColor
# from src.view.rf_condition_view_base import Ui_rf_condition_mainWindow
# class rf_condition_view(QMainWindow, Ui_rf_condition_mainWindow):
    # pass

        # #
    # # other attributes will be initialised in base-class
    # def __init__(self):
        # QMainWindow.__init__(self)
        # Ui_rf_condition_mainWindow.__init__(self)
        # self.setupUi(self)

        # # stdout_fd = sys.stdout.fileno()
        # # stdout_fde = sys.stderr.fileno()

        # prevOutFd = os.dup(1)
        # prevInFd = os.dup(0)
        # prevErrFd = os.dup(2)

        # # os.dup2(sys.stdout.fileno(), prevOutFd)
        # # # os.dup2(sys.stderr, stdout_fd)
        # sys.stdout = OutLog(self.message_pad )
        # #sys.stderr = OutLog(self.message_pad, color = QColor(255,0,0))


        # fileno(sys.stdout)

        # print("PYTHON STANDARD OUT")

		# #sys.stdout = OutLog(self.message_pad, os.dup(1))
        # # sys.stdout = OutLog(self.message_pad, os.dup(2))

# from PyQt4.QtGui import QApplication
# class rf_condition(QApplication):
    # def __init__(self, argv):
        # #
	# # you need this init line here to instantiate a QTApplication
		# QApplication.__init__(self, argv)
		# #
		# # only run if a config file was passed

		# self.view = rf_condition_view()
		# self.view.show()
		# QApplication.processEvents()

		# self.llrf_init = VELA_CLARA_LLRF_Control.init()
		# self.llrf_init.setQuiet()

		# self.llrf_control = self.llrf_init.getLLRFController(MACHINE_MODE.PHYSICAL, LLRF_TYPE.L01)

		# #raise Exception("sdddddddddddddddddddddddddddddddddddddddd"	)


# if __name__ == '__main__':
    # print('Starting rf_condition Application')
    # app = rf_condition(sys.argv)
    # sys.exit(app.exec_())