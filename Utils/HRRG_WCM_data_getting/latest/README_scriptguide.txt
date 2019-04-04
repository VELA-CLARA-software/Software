GitHub\Software\Utils\HRRG_WCM_data_getting.
README file describing how to use the script
============================================

The getWCMevts.py file is to be run in the CLARA work folder where the HRRG conditioning data logs are kept. For example

\\fed.cclrc.ac.uk\org\NLab\ASTeC\Projects\VELA\Work\2019\02\07\2019-02-07-17-41-49\

where the "log.txt" file is created by the conditiong script. It contains the times of each conditioning 'event'. 

The getWCMevts.py script reads the log.txt file, gets the timestamp of the 'event', and uses this timestamp to pull the WCM trace data from the EPICS archive. It plots and saves the WCM trace (as pngs) at that timestamp, and also saves the trace data in ascii format to wcmevents.txt. It creates a WCM folder and puts the plots and wcmevents.txt file in it.   