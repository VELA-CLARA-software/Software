# Code by Will Smith, 16/1/19
# http://claraserv2.dl.ac.uk/cssi_wiki/doku.php/archiver:pulling_data

import json
import requests
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt


#Define the PV

pv_name = 'EBT-INJ-DIA-WCM-01:DI-MAX'

#Define the from and to times

time_from="2019-02-07T01:00:00.00Z"
time_to="2019-02-07T01:02:00.00Z"

url="http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv="+pv_name+"&from="+time_from+"&to="+time_to

print(url)

r= requests.get(url)
data=r.json()

yaxis = []
time = []

for event in data[0]["data"] :
  time.append(event["secs"]+event["nanos"]*1E-9)
  yaxis.append(event["val"])

print(data[0]["meta"])

plt.plot(time,yaxis)
plt.ylabel(data[0]["meta"]["EGU"])
plt.xlabel("Time Since Epics Epoch")
plt.show()
