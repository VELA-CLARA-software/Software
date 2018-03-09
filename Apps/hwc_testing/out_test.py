import VELA_CLARA_Screen_Control as scr
import os
import sys

			
stdout_default = sys.stdout
log_file = 'log_file.txt'	

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

stdout_fd = sys.stdout.fileno()
with open(log_file, 'a') as f, stdout_redirected(f):
	print('redirected to a file')
	os.write(stdout_fd, b'it is redirected now\n')
	scr_init = scr.init()
	scr_init.setVerbose()	
	os.system('echo this is also redirected')
print('this is goes back to stdout')

			
			
def message(message):
	sys.stdout = stdout_default
	print message
	sys.stdout = open(log_file, 'a')
	print message
	# # always leave end stdout printing  to screen


message('Logging to file')

message('End Logging')
