REM loop through all UI files and  run pyuic4 on them
for %%i in (*.ui) do C:\Python36\Scripts\pyuic5 %%i -o %%~ni.py