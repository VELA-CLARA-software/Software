REM loop through all UI files and  run pyuic4 on them
for %%i in (*.ui) do C:\Python27\python.exe -c"import PyQt4.uic.pyuic" %%i -o %%~ni.py