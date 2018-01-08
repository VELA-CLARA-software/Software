set PATH=

set PATH=c:\anaconda32\envs\py2qt4;c:\anaconda32\envs\py2qt4\Library\mingw-w64\bin;c:\anaconda32\envs\py2qt4\Library\usr\bin;c:\anaconda32\envs\py2qt4\Library\bin;c:\anaconda32\envs\py2qt4\Scripts;c:\anaconda32\envs\py2qt4\bin;c:\anaconda32;c:\anaconda32\Library\mingw-w64\bin;c:\anaconda32\Library\usr\bin;c:\anaconda32\Library\bin;c:\anaconda32\Scripts;c:\anaconda32\bin;C:\anaconda32\Work\Software\Apps\Striptool2

pyinstaller -yF -n Striptool2Epics striptool_epics.py --noupx --hidden-import=scipy._lib.messagestream --hidden-import=PyQt4.QtCore --hidden-import=PyQt4.QtGui --paths=c:\anaconda32\Work --hidden-import=scipy.interpolate --hidden-import=scipy.optimize --hidden-import=scipy.integrate --hidden-import=scipy.special