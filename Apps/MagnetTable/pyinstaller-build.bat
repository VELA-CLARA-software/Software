rem Use pyinstaller to bundle everything into one EXE file
rem  --onefile: make a single executable
rem  --noconfirm: overwrite things without confirming
rem  -i: use a custom icon file
rem  --windowed: don't show a console window

pyinstaller --onefile --noconfirm -i resources\magnetTable\Icons\magnet.ico MagnetTable.py

rem Copy files in the resources tree to dist
rem  /d: only copy newer files
rem  /s: copy directory structure
rem  /y: force overwrite
xcopy /d /s /y resources dist\resources

rem Copy dist tree to apclara1
xcopy /d /s /y dist \\apclara1\ControlRoomApps\Release
