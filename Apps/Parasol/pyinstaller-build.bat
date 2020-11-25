rem It seems to be necessary to use the latest pyinstaller version
rem (otherwise you run into problems where it can't import scipy)
rem To get this, use
rem python -m pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip

rem Use pyinstaller to bundle everything into one EXE file
rem  --onefile: make a single executable
rem  --noconfirm: overwrite things without confirming
rem  -i: use a custom icon file
rem  --windowed: don't show a console window

rem Recreate the spec file. Only do this if imports have changed.
rem pyi-makespec --onefile -i resources\parasol\Icons\parasol.ico --windowed parasol.py
rem If you've done this, reinsert the code from remove-dlls.py into the spec file.
rem remove-dlls.py saves about 2MB (of 28MB) - it may not be worth bothering!

pyinstaller --noconfirm parasol.spec

rem Copy files in the resources tree to dist
rem  /d: only copy newer files
rem  /s: copy directory structure
rem  /y: force overwrite
xcopy /d /s /y resources dist\resources

rem Copy dist tree to apclara1
xcopy /d /s /y dist \\apclara1\ControlRoomApps\Release
