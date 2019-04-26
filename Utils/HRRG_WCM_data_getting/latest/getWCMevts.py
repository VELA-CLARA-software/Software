#-----------------------------------------------------------------------
# Script to read HRRG conditioning log files, get the times of the 
# conditioning events, then for each event time:
# -retrieve the WCM raw trace data for that
#-----------------------------------------------------------------------

import json
import requests
import numpy
import os
import matplotlib.pyplot as plt
import time
import datetime
from datetime import timedelta

print '*******************************************' 
print 'Script to read HRRG conditioning log files' 
print 'Press Enter to continue' 
raw_input()
print "First I'll get the times of the events from the log.txt file. Press Enter to continue "
raw_input()


nev = 0
events = []
tevents = []
#searchfile = open("//fed.cclrc.ac.uk/org/NLab/ASTeC/Projects/VELA/Work/2019/02/07/2019-02-07-17-41-49/log.txt","r")

##########################################
# Loop to get the event times from log.txt
########################################## 
searchfile = open("log.txt","r")
for line in searchfile:
    if "OMED" in line: # conditioning event times in conditiong logs found by searching for 'OMED'   

        ts = line[0:10]+"T"+line[-19:-4]+"Z" # ts, the time of the event in format needed for EPICS archive web interface, to the nearest 1 microsecond
       
        tr = datetime.datetime(int(line[0:4]),int(line[5:7]),int(line[8:10]),int(line[-19:-17]),int(line[-16:-14]),int(line[-13:-11]),int(line[-10:-4])) # tr, the time of the event in python time format, to the nearest 1 microsecond  

        events.append(ts)
        tevents.append(tr)        
        nev = nev+1
        print 'This is the ', nev, ' event in this conditioning log file'
        print 'Event time, EPICS archive format:',ts
        print 'Event time, python time format:',tr
        print 'Press Enter to continue'
        raw_input()
searchfile.close()
print 'Total number of conditioning events in the log file ', nev
print 'Press Enter to continue'
raw_input()


#####################################################
# Create WCM folder, ascii file to save WCM data in 
#####################################################
os.mkdir("WCM")
#outfilenm = dirnm+".txt"
output = open("WCM/wcmevents.txt","a")
output.write("The Log File has  "+str(nev)+" events\n")
pv_name = "EBT-B03-IOC-CS-04:FMC_1_ADC_0_READ"




print "Now I'll get the WCM data for each event time from the EPICS archive"
print 'Press Enter to continue'
raw_input()
##############################################################
# For each event, get the WCM data from the EPICS archive
# Retrieve the following data for each event:
# -the trace data 0.01 second BEFORE the event time
# -the trace data AT the event time (to the nearest micro second)
# -the trace data 0.01 second AFTER the event time
##############################################################
for j in range(nev):
    tzero = events[j]
    print "\n\n"   
    print 'EVENT', j+1, ' of ', nev, ' ***********************'
    print 'CENTRAL TIME OF EVENT', tzero
#    time_to = time_from
    
    
    time_fromt = str(tevents[j]-datetime.timedelta(seconds=0.01)) # get the event time 0.01 seconds BEFORE the event time
    
    time_tot = str(tevents[j]+datetime.timedelta(seconds=0.01))  # get the event time 0.01 seconds AFTER the event time   
    
    print 'event time (python)', tevents[j]
    print 'time from ', time_fromt
    print 'time to ', time_tot
 
    # times in EPICS archive format
    time_from = time_fromt[0:10]+"T"+time_fromt[11:26]+"Z"
    time_to = time_tot[0:10]+"T"+time_tot[11:26]+"Z"
    
    print 'EPICS time from ', time_from
    print 'EPICS time to ', time_to
    url="http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv="+pv_name+"&from="+time_from+"&to="+time_to
    print 'EPICS archive http call ', url
    r= requests.get(url)
    data=r.json()
    lendat = len(data[0]["data"])
    print 'The data pulled from EPICS for this event has ', lendat, ' WCM traces ' # should be 3

    event = data[0]["data"][0]
    time = event["secs"]+event["nanos"]*1E-9
    yaxis = event["val"]
    times = []

    #
    # Get each event in the to_ from_ interval 
    #
    for a in range(0,lendat):
        i = 0
        ploo = []
        print 'Event ', j+1, ' trace ', a+1, ' of ', lendat
        event1 = data[0]["data"][a]
        times.append(float(event1["secs"]+event1["nanos"]*1E-9))
        print " Archive time of event ", times[a]
        yaxis1 = event1["val"]
        for x in yaxis1:
            if x<0 :
                yaxis1[i]=((x+2**16)*3.006381547039116e-05-0.984556575250828)*140
            else:
                yaxis1[i]=(x*3.006381547039116e-05-0.984556575250828)*140
            i=i+1  
        T= [jj/240E03 for jj in range(0,1024)]
        ploo.append((T,yaxis1))

#        print ploo[0]   
        print "================================================================"


        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(ploo[0][0], ploo[0][1])

        plt.title("Logged event central time "+tzero+"\n evt "+str(a+1)+" of "+str(lendat)+"\n archive time "+str(format(times[a],'.6f')))
        plt.ylabel("Current (mA)");
        plt.xlabel("Time (ms)")
#        plt.show()

        print 'time ....', times
        figname1 = str(tzero+"_"+str(a)).replace(":","x")
        fig.savefig("WCM/"+str(figname1)+"fig.png") 

        output.write('\n')
        output.write("conditioning event at "+tzero)
        output.write('\n')
        output.write(str(event1))
        output.write(str(ploo))
        output.write('\n')
        output.write('\n')
        
        print 'Press Enter to Continue' 
        raw_input()
    print 'Finished processing event ', j+1, ' of ', nev
    print 'Press Enter to Continue'
    raw_input()    
output.close()
