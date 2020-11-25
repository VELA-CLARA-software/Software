rem Use pyinstaller to bundle everything into one EXE file
rem  --onefile: make a single executable
rem  --noconfirm: overwrite things without confirming
rem  -i: use a custom icon file
rem  --windowed: don't show a console window

pyinstaller --onefile --noconfirm -i resources\magnetTable\Icons\magnet.ico MagnetTable.py

rem Rename EXE file including today's date - in an attempt to avoid "sharing violation" errors
set exe=MagnetTable.exe
set exeyyyymmdd=MagnetTable.%date:~8,2%%date:~3,2%%date:~0,2%.exe
ren dist\%exe% %exeyyyymmdd%

rem Copy files in the resources tree to dist
rem  /d: only copy newer files
rem  /s: copy directory structure
rem  /y: force overwrite
xcopy /d /s /y resources dist\resources

rem Copy dist tree to apclara1
set destdir=\\apclara1\ControlRoomApps\Release
xcopy /d /s /y dist %destdir%

rem Keep trying to copy that temp file
:repeat
copy %destdir%\%exeyyyymmdd% %destdir%\%exe% || goto :repeat
del %destdir%\%exeyyyymmdd%
