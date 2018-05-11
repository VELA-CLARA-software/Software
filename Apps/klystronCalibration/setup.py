from distutils.core import setup
import py2exe
import sys, os

sys.path.append(r"C:\anaconda32\envs\py2qt4min\Lib\site-packages\scipy\extra-dll")
sys.path.append(r"C:\anaconda32\envs\py2qt4min\Lib\site-packages\numpy\.libs")

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True,"includes":["sip"]}},
    windows = [{'script': "klystronCalibrate.py"}],
    zipfile = None,
)
