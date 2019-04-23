# Script for plotting many hours of archived data to look for WCM events
# or change PV for other applications
# Dave Dunning 7/2/19 based on code by Will Smith and Alex Brynes

import json
import requests
import numpy as np
import matplotlib
#matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
#import time

# Define the PV
#pv_name = "CLA-S01-DIA-WCM-01:Q"
pv_name = 'EBT-INJ-DIA-WCM-01:DI-MAX'

# Define the from and to times, usually several hours
time_from="2019-02-07T17:00:00.00Z"
time_to="2019-02-08T08:00:00.00Z"
# break data into smaller blocks for downloading and plotting
t_delta = timedelta(hours=1)

# convert to datetimes etc.
t_from = datetime.strptime(time_from, "%Y-%m-%dT%H:%M:%S.%fZ")
t_to = datetime.strptime(time_to, "%Y-%m-%dT%H:%M:%S.%fZ")
t1 = t_from
t2 = t_from + t_delta

# function to get data from the archiver
def get_data(t1, t2):
    url="http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv="+pv_name+"&from="+t1+"&to="+t2
    print(url)
    r= requests.get(url)
    data=r.json()
    yaxis = []
    t = []
    for event in data[0]["data"] :
      secs = event["secs"]
      nanos = event["nanos"]
      t0  = datetime.fromtimestamp(secs+nanos*1E-9)
      t1 = matplotlib.dates.date2num(t0)
      t.append(t1)
      yaxis.append(event["val"])
    return t, yaxis

# loop to get data chunks
ploo = []
while t1 < t_to:
    #print t1, 'to', t2, '...\n'
    time_1 = t1.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4]+'Z'
    time_2 = t2.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4]+'Z'
    t, yaxis = get_data(time_1, time_2)
    ploo.append((t,yaxis))
    t1 += t_delta
    t2 += t_delta

# function for changing plot panel on left/right key press
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
    ax1.cla()
    ax1.plot_date(ploo[curr_pos][0], ploo[curr_pos][1], '-', label='line')
    plt.xticks(rotation=90)
    ax1.xaxis.set_major_formatter(xfmt)
    plt.tight_layout()
    plt.title("(Index) "+str(curr_pos))
    fig.canvas.draw()

# plot figure etc.
fig = plt.figure()
fig.canvas.mpl_connect('key_press_event', key_event)
ax1 = plt.subplot(111)
xfmt = mdates.DateFormatter('%d-%m-%y %H:%M:%S.%f')
plt.plot_date(ploo[0][0], ploo[0][1], '-', label='line')
plt.xticks(rotation=90)
ax1.xaxis.set_major_formatter(xfmt)
plt.tight_layout()
plt.title("(Index) "+str(0))
#figManager = plt.get_current_fig_manager()
#figManager.window.showMaximized()
plt.show()
exit()
