#!/usr/bin/env python
#Change the  traces storage rate to 3600 secs
#See
#http://claraserv2/cssi_wiki/doku.php/archiver:scripting
import sys
import urllib
import urllib2
import json
import argparse
from ctypes import *

url = 'http://claraserv2:17665/mgmt/bpl/'

#Find PVs
data="/getAllPVs?pv=*:*:READTRACE*"

#Pause and Unpause REST command syntax
def pause(pv):
  return "/pauseArchivingPV?pv="+pv
def unpause(pv):
  return "/resumeArchivingPV?pv="+pv

#New archover period REST command syntax
def scan(pv):
  return "/changeArchivalParameters?pv="+pv+"&samplingmethod=SCAN&samplingperiod=3600"
  
##Start operations
#Scan archiver
req = urllib2.Request(url+data)
print "Submitting PVs to appliance archiver at ", url 
print req.get_full_url()
print req.get_method()
print req.get_data()
response = urllib2.urlopen(req)
the_page = response.read()
status = json.loads(the_page)

for pv in status:
 #Pause then Unpause
 print "unpause: "+unpause(pv)
 urllib2.urlopen(urllib2.Request(url+pause(pv)))
 req = urllib2.Request(url+unpause(pv))
 response = urllib2.urlopen(req)
 the_page = response.read()
 status = json.loads(the_page)
 if 'validation' in status:
  print "####Error:"+status["validation"]
 if 'status' in status:
  print status["status"]
  #Unpause worked so now try to update the scan rate
  req = urllib2.Request(url+scan(pv))
  response = urllib2.urlopen(req)
  the_page = response.read()
  status = json.loads(the_page)
  if 'status' in status and status['status']=="ok":
   print "New scan rate set"
  else:
   print "########Error"


#data = "pv=CLA-L01-LRF-CTRL-01:A:READTRACE:2&samplingmethod=SCAN&samplingperiod=3600"
#url = 'http://claraserv2:17665/mgmt/bpl/changeArchivalParameters?'
#req = urllib2.Request(url+data)
#print "Submitting PVs to appliance archiver at ", url 
#print req.get_full_url()
#print req.get_method()
#print req.get_data()
#response = urllib2.urlopen(req)
#the_page = response.read()
#status = json.loads(the_page)
#print status



#/resumeArchivingPV
#/getAllPVs
#changeArchivalParameters?