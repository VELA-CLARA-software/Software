import sys, os
import numpy

class WriteDataToCATAP(object):

    def __init__(self):
        object.__init__(self)
        self.my_name = "WriteDataToCATAP"
        self.diagnosticTypes = ['bpm', 'charge', 'camera', 'pil']

    def writeMachineStateToCATAP(self, mode, datadict, allbeamfiles, catap):
        for key, value in datadict.items():
            # if value['type'] in self.diagnosticTypes:
            if isinstance(value, dict):
                if 'type' in value.keys():
                    if value['type'] == 'bpm':
                        if key in allbeamfiles.keys():
                            datadict[key]['x'] = numpy.mean(allbeamfiles[key]['x']['mean'])
                            datadict[key]['y'] = numpy.mean(allbeamfiles[key]['y']['mean'])
                            catap['BPM'][key].setX() = datadict[key]['x']
                    if value['type'] == 'charge':
                        datadict[key]['q'] = value['q']
            # if value['type'] == "magnet":
            #     datadict[key]['READI'] = value['READI']
            # if value['type'] == "screen":
            #     datadict[key].state = value['state']
