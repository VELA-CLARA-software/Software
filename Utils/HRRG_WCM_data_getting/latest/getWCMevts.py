import json
import requests
import numpy
import os
import matplotlib.pyplot as plt

nev = 0
events = []
#searchfile = open("//fed.cclrc.ac.uk/org/NLab/ASTeC/Projects/VELA/Work/2019/02/07/2019-02-07-17-41-49/log.txt","r")
searchfile = open("log.txt","r")
for line in searchfile:
    if "OMED" in line: 
        print '****************************************************************************'
        print 'the whole line is'
        print line
        print 'Event timestamp is'    
        print line[0:10]    
        print line[-19:-6]
        ts = line[0:10]+"T"+line[-19:-6]+"Z"
        print ts
#        events.append(line[-19:-8])
        events.append(ts)
        nev = nev+1
searchfile.close()

#nm = searchfile.name
#dirnm = nm[-27:-8]
#print 'FILENAME', nm
#print 'ROOT', dirnm
print 'total number of events', nev
#print events

os.mkdir("WCM")
#outfilenm = dirnm+".txt"
output = open("WCM/wcmevents.txt","a")
output.write("The Log File has  "+str(nev)+" events\n")

pv_name = "EBT-B03-IOC-CS-04:FMC_1_ADC_0_READ"

for j in range(nev):

    time_from=events[j]

    print '****************************************************************************'
    print 'first event', time_from
    time_to = time_from
    url="http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv="+pv_name+"&from="+time_from+"&to="+time_to
    print(url)
    r= requests.get(url)
    data=r.json()
    print 'the data list length is', len(data[0]["data"])

    event = data[0]["data"][0]
    time = event["secs"]+event["nanos"]*1E-9
    yaxis = event["val"]
    ploo = []
    times = []
    i=0

    event1 = data[0]["data"][0]
    times.append(float(event1["secs"]+event["nanos"]*1E-9))
    yaxis1 = event1["val"]
    for x in yaxis1:
        if x<0 :
            yaxis1[i]=((x+2**16)*3.006381547039116e-05-0.984556575250828)*140
        else:
            yaxis1[i]=(x*3.006381547039116e-05-0.984556575250828)*140
#    if yaxis1[i] > 0.45 :
#        print 'HELLOO', yaxis1[i], ' a ', a, ' i ', i
        i=i+1  
    T= [j/240E03 for j in range(0,1024)]
    ploo.append((T,yaxis1))

#print ploo[0]   
    print "================================================================"


    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(ploo[0][0], ploo[0][1])
    plt.title(time_from)
    plt.ylabel("Current (mA)");
    plt.xlabel("Time (ms)")
#    plt.show()
    figname1 = str(time_from).replace(":","x")
#figname2 = str(figname1).replace(".","s")
    fig.savefig("WCM/"+str(figname1)+"fig.png") 


#output.write("Now the file has one more line! \n")
    output.write('\n')
    output.write("conditioning event at "+time_from)
    output.write('\n')
    output.write(str(event))
    output.write(str(ploo))
    output.write('\n')
    output.write('\n')
#    raw_input()
    
output.close()
