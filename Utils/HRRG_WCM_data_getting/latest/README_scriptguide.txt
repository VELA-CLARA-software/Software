GitHub\Software\Utils\HRRG_WCM_data_getting.
README file describing how to use the script
============================================

The getWCMevts.py file is to be run in the CLARA work folder where the HRRG conditioning data logs are kept. For example

\\fed.cclrc.ac.uk\org\NLab\ASTeC\Projects\VELA\Work\2019\02\07\2019-02-07-17-41-49\

where the "log.txt" file is created by the conditiong script. It contains the times of each conditioning 'event'. 

The getWCMevts.py script reads the log.txt file, gets the timestamp of the 'event' (to the microsecond), and uses this timestamp to pull the WCM trace data from the EPICS archive.

For each event timestamp, the following WCM trace data is extracted from the archive:
-the trace 0.01 seconds BEFORE the timestamp, 
-the trace AT the timestamp
-the trace 0.01 seconds AFTER the timestamp, 

(0.01 seconds becuase the gun was conditioned at 100 Hz)

The traces are saved both as plots (with titles which indicate the timestamp) and as also ascii format to wcmevents.txt. 

It creates a WCM folder and puts the plots and wcmevents.txt file in it.   