# import os
# import sys
# import ctypes, ctypes.util
#
# kernel32 = ctypes.WinDLL('kernel32')
#
# STD_OUTPUT_HANDLE = -11
#
# if sys.version_info < (3, 5):
#     libc = ctypes.CDLL(ctypes.util.find_library('c'))
# else:
#     if hasattr(sys, 'gettotalrefcount'): # debug build
#         libc = ctypes.CDLL('ucrtbased')
#     else:
#         libc = ctypes.CDLL('api-ms-win-crt-stdio-l1-1-0')
#
#     # VC 14.0 doesn't implement printf dynamically, just
#     # __stdio_common_vfprintf. This take a va_array arglist,
#     # which I won't implement, so I escape format specificiers.
#
#     class _FILE(ctypes.Structure):
#         """opaque C FILE type"""
#
#     libc.__acrt_iob_func.restype = ctypes.POINTER(_FILE)
#
#     def _vprintf(format, arglist_ignored):
#         options = ctypes.c_longlong(0) # no legacy behavior
#         stdout = libc.__acrt_iob_func(1)
#         format = format.replace(b'%%', b'\0')
#         format = format.replace(b'%', b'%%')
#         format = format.replace(b'\0', b'%%')
#         arglist = locale = None
#         return libc.__stdio_common_vfprintf(
#             options, stdout, format, locale, arglist)
#
#     def _printf(format, *args):
#         return _vprintf(format, args)
#
#     libc.vprintf = _vprintf
#     libc.printf = _printf
#
# def do_print(label):
#     print("%s: python print" % label)
#     s = ("%s: libc _write\n" % label).encode('ascii')
#     libc._write(1, s, len(s))
#     s = ("%s: libc printf\n" % label).encode('ascii')
#     libc.printf(s)
#     libc.fflush(None) # flush all C streams
#
from PyQt4.QtGui import QTextCursor
import sys
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
            self.text_space.moveCursor(QTextCursor.End)
            self.text_space.insertPlainText(string)
            self.text_space.moveCursor(QTextCursor.End)
        else:  # save up text for when a text widget becomes available
            self.text_log += string

    def flush(self):
        self.stdout.flush()


#
#
# if __name__ == '__main__':
#     # save POSIX stdout and Windows StandardOutput
#     fd_stdout = os.dup(1)
#     hStandardOutput = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
#
#     do_print("begin")
#
#     # redirect POSIX and Windows
#     with open("TEST.TXT", "w") as test:
#         os.dup2(test.fileno(), 1)
#         kernel32.SetStdHandle(STD_OUTPUT_HANDLE, libc._get_osfhandle(1))
#
#     do_print("redirected")
#
#     # restore POSIX and Windows
#     os.dup2(fd_stdout, 1)
#     kernel32.SetStdHandle(STD_OUTPUT_HANDLE, hStandardOutput)
#
#     do_print("end")
#
