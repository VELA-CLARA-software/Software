rem Compile the app to an EXE file
pyinstaller --onefile --clean -F -w --workpath="\\claraserv3.dl.ac.uk\claranet\temp" --distpath="\\claraserv3.dl.ac.uk\claranet\temp" --icon=.\resources\gun_solenoid_adjuster\gun_solenoid_adjuster.ico -n "gun_solenoid_adjuster" mainApp.py
