#!/usr/bin/env python
# -*- coding: utf-8 -*-
# magnetAppGlobals.py
import sys
import os


sys.path.append(os.path.join(sys.path[0],'GUI'))
sys.path.append(os.path.join(sys.path[0],'control'))

dburtLocation = "\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Snapshots\\DBURT"
dburtLocation2 = "//fed.cclrc.ac.uk/org/NLab/ASTeC/Projects/VELA/Snapshots/DBURT/"
appIcon = 'assets\\magpic.jpg'
claraIcon = 'assets\\CLARA5.bmp'
sys.path.append('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stage\\')
# not sure we need a log and need to include JKJ logger widget if we do ??
logfile='magnetAppLog.log'
