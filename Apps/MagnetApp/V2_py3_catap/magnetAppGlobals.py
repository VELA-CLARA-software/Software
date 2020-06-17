#!/usr/bin/env python
# -*- coding: utf-8 -*-
# magnetAppGlobals.py
import sys
import os


sys.path.append(os.path.join(sys.path[0],'GUI'))
sys.path.append(os.path.join(sys.path[0],'control'))

#dburtLocation = "\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Snapshots\\DBURT"
dburtLocation = "\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\DJS_TEST_AREA"
dburtLocation2 = "C:/Users/djs56/Documents/CATAP_DBURT_TEST/"
appIcon = 'resources\\magnetApp\\magpic.jpg'
claraIcon = 'resources\\magnetApp\\CLARA5.bmp'
#sys.path.append('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software
# \\VELA_CLARA_PYDs\\bin\\stage\\')
#sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release\\')
#sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\')
#sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release\\')
# not sure we need a log and need to include JKJ logger widget if we do ??
logfile='magnetAppLog.log'


#for i in sys.path:
#	print i