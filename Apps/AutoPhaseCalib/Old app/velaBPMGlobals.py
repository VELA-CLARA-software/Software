#This script holds all the info about referencing a VELA data object

#    /// http://projects.astec.ac.uk/VELAManual/index.php/BPMs

#   The data array comes with 10 values... 
#    //0 - number of columns
#    //1 - number of turns
#    //2 - first pickup voltage = PU1
#    //3 - second pickup voltage  = PU2
#    //4 - "c1"
#    //5 - pedestal 1 (to be subtracted from first and second pickup voltages)
#    //6 - third pickup voltage  =  PU3
#    //7 - fourth pickup voltage =  PU4
#    //8 - "c2"
#    //9 - pedestal 2 (to be subtracted from third and fourth pickup voltages) 


#globalBPMNames are the 'prefix' names of BPM process variables
#globalBPMPVsuffix are the suffixes that create a real PV (when added onto the end with a colon)
#globalBPMMonitorType are keywords to reference different monitors

#note: last two are basically the same thing...




bpmDict = { 0: 'BPM1', 
            1: 'BPM2', 
            2: 'BPM3',  
            3: 'BPM4', 
            4: 'BPM5'}
 
scopeDict = { 0: 'WCM' }

screenDict = {  0: 'YAG1',
                1: 'YAG2', 
                2: 'YAG3', 
                3: 'YAG4', 
                4: 'YAG5'}

globalBPMNames = { 0: 'EBT-INJ-DIA-BPMC-02', 
                   1: 'EBT-INJ-DIA-BPMC-04', 
                   2: 'EBT-INJ-DIA-BPMC-06',  
                   3: 'EBT-INJ-DIA-BPMC-10',
                   4: 'EBT-INJ-DIA-BPMC-12'}
                   
globalScopeNames = { 0: 'EBT-INJ-SCOPE-01' } 

globalScreenNames = {   0: 'EBT-INJ-DIA-YAG01',
                        1: 'EBT-INJ-DIA-YAG02',
                        2: 'EBT-INJ-DIA-YAG03',
                        3: 'EBT-INJ-DIA-YAG04',
                        4: 'EBT-INJ-DIA-YAG05'}

SA1 = 'SA1'
SA2 = 'SA2'
RA1 = 'RA1'
RA2 = 'RA2'
DAT = 'DAT'
X = 'X'
Y = 'Y'
P1 = 'P1'
Sta = 'Sta'
On = 'On'
Off = 'Off'

SA1s = ':' + SA1
SA2s = ':' + SA2
RA1s = ':' + RA1
RA2s = ':' + RA2
DATs = ':DATA:B2V.VALA'
Xs = ':' + X
Ys = ':' + Y
P1s = ':' + P1
Stas = ':' + Sta
Ons = ':' + On
Offs = ':' + Off


globalBPMPVsuffix = [ SA1s, SA2s, RA1s, RA2s, DATs, Xs, Ys ] 

globalScopePVsuffix = [ P1s ]

globalScreenPVSuffix = [Stas, Ons, Offs]

globalBPMMonitorType = [ SA1, SA2, RA1, RA2, DAT, X, Y ]

globalScopeMonitorType = [ P1 ]

globalScreenMonitorType = [Sta, On, Off]










