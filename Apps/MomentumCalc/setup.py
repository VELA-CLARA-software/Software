from distutils.core import setup
import py2exe
setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True,"includes":["sip"]}},
    windows = [{'script': "MomentumApp.py"}],
    zipfile = None,
)
