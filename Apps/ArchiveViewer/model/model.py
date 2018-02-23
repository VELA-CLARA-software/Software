import numpy as np
import urllib2
import urlparse
import json
class Model():
    def __init__(self):
        self.comment = 'Hello World!!    and the Llamas in the Universe :)'
        print("Model Initialized")
        self.sec = []
        self.vals = []

    def getData(self, pv, dateFrom, timeFrom, dateTo, timeTo):
        #print dateFrom.day()
        #print dateTo.day()

        # CLA-GUN-RF-LRRG-01%3ART&from=2018-01-17T14%3A43%3A00.000Z&to=2018-01-17T14%3A46%3A00.000Z
        pv = pv.replace(':', '%3A')
        urlString = ("getData.json?pv=" + str(pv) +
                     "&from=" + str(dateFrom.year()) +
                     "-" + str(dateFrom.month()) + '-' +
                     str(dateFrom.day()) + 'T' +
                     str(timeFrom.hour()) + '%3A' +
                     str(timeFrom.minute()) + '%3A00.000Z' +
                     "&to=" + str(dateTo.year()) + '-' +
                     str(dateTo.month()) + '-' +
                     str(dateTo.day()) + 'T' +
                     str(timeTo.hour()) + '%3A' +
                     str(timeTo.minute()) + '%3A00.000Z')

        hi = urlparse.urljoin("http://claraserv2.dl.ac.uk:17668/retrieval/data/",
                              urlString)
        print hi
        req = urllib2.urlopen(hi)
        data = json.load(req)
        self.secs = [x['secs'] for x in data[0]['data']]
        self.vals = [x['val'] for x in data[0]['data']]
        #print self.vals[:5]
