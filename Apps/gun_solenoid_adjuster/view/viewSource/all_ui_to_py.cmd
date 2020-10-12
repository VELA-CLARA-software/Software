REM loop through all UI files and  run pyuic4 on them
for %%i in (*.ui) do C:\Python27\Lib\site-packages\PyQt4\pyuic4 %%i -o %%~ni.py