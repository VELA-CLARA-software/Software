rem Compile the app to an EXE file
pyinstaller --onefile --clean -F -w --icon=".\resources\screen_status\screen_status_icon.ico" -n "screen_status" mainApp.pyw
