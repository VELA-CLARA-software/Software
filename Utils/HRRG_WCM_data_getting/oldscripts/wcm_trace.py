import json
import requests
import numpy
import matplotlib.pyplot as plt

#Define the PV

pv_name = "EBT-B03-IOC-CS-04:FMC_1_ADC_0_READ"

#Define the from and to times

#time_from="2019-02-07T01:30:15.00Z"
#time_to="2019-02-07T01:30:30.00Z"
time_from="2019-02-07T20:40:04.20Z"
time_to="2019-02-07T20:40:04.30Z"

url="http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv="+pv_name+"&from="+time_from+"&to="+time_to

print(url)

r= requests.get(url)
data=r.json()
#print len(data[0]["data"])

event = data[0]["data"][0]
time = event["secs"]+event["nanos"]*1E-9
yaxis = event["val"]
ploo = []
times = []
i=0

#fix sign and apply scaling to go from ADC counts to mA
for a in range(0,len(data[0]["data"])-1):
    event1 = data[0]["data"][a]
    times.append(float(event1["secs"]+event["nanos"]*1E-9))
    yaxis1 = event1["val"]
    i=0
    for x in yaxis1:
      if x<0 :
        yaxis1[i]=((x+2**16)*3.006381547039116e-05-0.984556575250828)*140
      else:
        yaxis1[i]=(x*3.006381547039116e-05-0.984556575250828)*140
      #if yaxis1[i] > 0.45 :
        #print 'HELLOO', yaxis1[i], ' a ', a, ' i ', i
      i=i+1
    T= [j/240E03 for j in range(0,1024)]
    ploo.append((T,yaxis1))
#print(times)
#create time vector


#T= [j/240E3 for j in range(0,1024)]

curr_pos = 0

def key_event(e):
    global curr_pos

    if e.key == "right":
        curr_pos = curr_pos + 1
    elif e.key == "left":
        curr_pos = curr_pos - 1
    else:
        return
    curr_pos = curr_pos % len(ploo)

    ax.cla()
    ax.plot(ploo[curr_pos][0], ploo[curr_pos][1])
    plt.ylabel("Current (mA)");
    plt.xlabel("Time (ms)")
    plt.title(str(times[curr_pos])+" (index) "+str(curr_pos))
    fig.canvas.draw()

fig = plt.figure()
fig.canvas.mpl_connect('key_press_event', key_event)
ax = fig.add_subplot(111)
ax.plot(ploo[0][0], ploo[0][1])
plt.title(times[0])
plt.ylabel("Current (mA)");
plt.xlabel("Time (ms)")
plt.show()
