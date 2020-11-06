rem Compile the app to an EXE file
rem pyinstaller --onefile --clean -F -w --icon=".\resources\Valve_Status\valve.ico" -n "Valve_Status" mainApp.py
pyinstaller Valve_Status.spec