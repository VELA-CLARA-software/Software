REM After creating a new machine status table, or updating an existing one, run this file to
REM copy the files over to apsv2. You will need the appropriate permissions, so it probably
REM needs to be done by Ben Shepherd.

REM The /d flag ensures only newer files are copied
xcopy /y /d machine-status\machineStatusServer.py \\apsv2\bjs54\machine-status
xcopy /y /d machine-status\status.* \\apsv2\bjs54\machine-status
xcopy /y /d scripts\ckeditor\plugins\vela\icons\*.png \\apsv2\elog2\scripts\ckeditor\plugins\vela\icons
xcopy /y /d scripts\ckeditor\plugins\vela\plugin.js \\apsv2\elog2\scripts\ckeditor\plugins\vela
xcopy /y /d scripts\ckeditor\contents.css \\apsv2\elog2\scripts\ckeditor
xcopy /y /d themes\default\default.css \\apsv2\elog2\themes\default
