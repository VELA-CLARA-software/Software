import epics
import numpy as np
import time
import velaBPMGlobals as vbpmg


class BPMMonitor(object):
    def __init__(self):
        # This is the main hash table of bpmObjects
        print 'Initialising BPM objects'
        self.bpmObjects = {bpmName: bpmRawData(bpmName) for bpmName in vbpmg.globalBPMNames.values()}


    def monitorBPMForNCounts( self, bpm, N ):
        print 'Monitoring BPM for ', N, ' counts'
        if bpm in self.bpmObjects.keys(): 
            self.bpmObjects[ bpm ].isBusy = True

            self.bpmObjects[ bpm ].clearData()
            self.bpmObjects[ bpm ].appendingData = True
            self.bpmObjects[ bpm ].printing = False
            
            while self.bpmObjects[ bpm ].isBusy: 
                if self.bpmObjects[ bpm ].currentDataSize() == N:
                    self.bpmObjects[ bpm ].appendingData = False
                    self.bpmObjects[ bpm ].isBusy = False
                    print 'Acquired ', N, ' shots'
            
            self.bpmObjects[ bpm ].printing = False
            
        else:
            print 'ERROR in monitorBPMForNCounts'

    def setX(self, bpm, val):
        if bpm in self.bpmObjects.keys():
            self.bpmObjects[bpm].pvDict[vbpmg.X].put(val)
        else:
            return 'BPM Does not Exist'

    def setY(self, bpm, val):
        if bpm in self.bpmObjects.keys():
            self.bpmObjects[bpm].pvDict[vbpmg.Y].put(val)
        else:
            return 'BPM Does not Exist'

    def getX(self, bpm):
        if bpm in self.bpmObjects.keys():
            return self.bpmObjects[bpm].X
        else:
            return 'BPM Does not Exist'

    def getY(self, bpm):
        if bpm in self.bpmObjects.keys():
            return self.bpmObjects[bpm].Y
        else:
            return 'BPM Does not Exist'

    def getAllPositionData(self, bpm):
        if bpm in self.bpmObjects.keys():
            print 'Getting position data for', bpm
            return [self.bpmObjects[bpm].X, self.bpmObjects[bpm].Y]
            
    def isBusy(self, bpm):
        if bpm in self.bpmObjects.keys():
            return self.bpmObjects[bpm].isBusy
        else:
            return 'BPM Does not Exist'

class bpmRawData(object):

    def __init__(self, epicsName):
        
        print 'Initialising BPM raw data'
        self.epicsName = epicsName
        self.SA1 = -1
        self.SA2 = -1
        self.RA1 = -1
        self.RA2 = -1
        self.X = []
        self.Y = []
        self.bufferSize = 1000
        self.PU1 = []
        self.PU2 = []
        self.PU3 = []
        self.PU4 = []
        self.ped1 = -1
        self.ped2 = -1
        self.C2 = -1
        self.C1 = -1

        self.isBusy = False
        self.appendingData = True
        self.printing = False

        # The BPM object can also hold its epics.PV parameters in a dictionary
        self.pvDict = {}
        self.callBackDict = {}
        
        for suf in zip(vbpmg.globalBPMMonitorType, vbpmg.globalBPMPVsuffix):
            print 'Creating ', suf[0], ' = ', self.epicsName + suf[1]
            self.pvDict[suf[0]] = epics.PV(self.epicsName + suf[1], self.callback(suf[0]))
    
    def onDatChange(self, pvname=None, value=None, char_value=None, **kw  ):
        str.format('{0:.15f}', kw[ 'timestamp' ] )

    def onRA1Change(self, pvname=None, value=None, char_value=None, **kw):
        # print 'PV Changed! ', pvname, char_value, str.format('{0:.15f}', kw[
        # 'timestamp' ] )
        self.RA1 = value
        # print 'self.RA1 = ', self.RA1

    def onRA2Change(self, pvname=None, value=None, char_value=None, **kw):
        # print 'PV Changed! ', pvname, char_value, str.format('{0:.15f}', kw[
        # 'timestamp' ] )
        self.RA2 = value
        #print 'self.RA2 = ', self.RA2

    def onSA1Change(self, pvname=None, value=None, char_value=None, **kw):
        # print 'PV Changed! ', pvname, char_value, str.format('{0:.15f}', kw[
        # 'timestamp' ] )
        self.SA1 = value
        #print 'self.SA1 = ', self.SA1

    def onSA2Change(self, pvname=None, value=None, char_value=None, **kw):
        # print 'PV Changed! ', pvname, char_value, str.format('{0:.15f}', kw[
        # 'timestamp' ] )
        self.SA2 = value
        # print 'self.SA2 = ', self.SA2

    def onXChange(self, pvname=None, value=None, char_value=None, **kw):
        if self.appendingData:
            self.X.append(value)
        #print 'x = ', self.X
        
    def onYChange(self, pvname=None, value=None, char_value=None, **kw):
        if self.appendingData:
            self.Y.append(value)
        #print 'y = ', self.Y
  
    def currentDataSize( self ):
        return len( self.X )
    
    # function to key the callback functions (!?) not entirely happy about this, 
    def callback(self, x ):
        return {vbpmg.SA1 : self.onSA1Change, 
        vbpmg.SA2 : self.onSA2Change, 
        vbpmg.RA1 : self.onRA1Change, 
        vbpmg.RA2 : self.onRA2Change,
        vbpmg.X : self.onXChange,
        vbpmg.Y : self.onYChange,
        vbpmg.DAT : self.onDatChange}[x]

    def stopDataCallback( self ):
        print 'Stopping Data Callback for ', self.epicsName + vbpmg.DATs
        self.pvDict[ vbpmg.DAT ].remove_callback( )
        
    def startDataCallback( self ):
        print 'Starting  Data Callback for ', self.epicsName
        self.pvDict[ vbpmg.DAT ].add_callback( )        
       
    def clearData(self):
        self.X = []
        self.Y = []
        
        
        
class scopeMonitor (object):
    #EBT-INJ-SCOPE-01:PI
    def __init__(self):
        print 'Initialising scope monitoring'
        self.scopeObjects = {scopeName: scopeRawData(scopeName) for scopeName in vbpmg.globalScopeNames.values()}
    
    def monitorScopeForNCounts( self, scope, N ):
        print 'Monitoring charge for ', N, ' counts'
        if scope in self.scopeObjects.keys(): 
            self.scopeObjects[ scope ].isBusy = True

            self.scopeObjects[ scope ].clearData()
            self.scopeObjects[ scope ].appendingData = True
            self.scopeObjects[ scope ].printing = False
            

            while self.scopeObjects[ scope ].isBusy: 
                if self.scopeObjects[ scope ].currentDataSize() == N:
                    self.scopeObjects[ scope ].appendingData = False
                    self.scopeObjects[ scope ].isBusy = False
                    print 'Acquired ', N, ' shots'
            
            self.scopeObjects[ scope ].printing = False
            
        else:
            print 'ERROR in monitorScopeForNCounts'
    
    def getChargeData(self, scope):
        if scope in self.scopeObjects.keys():
            print 'Getting charge data for', scope
            return self.scopeObjects[scope].P1
            
    def isBusy(self, scope):
        if scope in self.scopeObjects.keys():
            return self.scopeObjects[scope].isBusy
        else:
            return 'Scope Does not Exist'        
            
class scopeRawData(object):

    def __init__(self, epicsName):
        
        print 'Initialising scope raw data'
        self.epicsName = epicsName
        self.P1 = []
        self.bufferSize = 1000


        self.isBusy = False
        self.appendingData = True
        self.printing = False

        # The object can also hold its epics.PV parameters in a dictionary
        self.pvDict = {}
        self.callBackDict = {}
       
        
        for suf in zip(vbpmg.globalScopeMonitorType, vbpmg.globalScopePVsuffix):
            print 'Creating ', suf[0], ' = ', self.epicsName + suf[1]
            self.pvDict[suf[0]] = epics.PV(self.epicsName + suf[1], self.callback(suf[0]))
    
    def onDatChange(self, pvname=None, value=None, char_value=None, **kw  ):
        str.format('{0:.15f}', kw[ 'timestamp' ] )
    
    def onP1Change(self, pvname=None, value=None, char_value=None, **kw):
        if self.appendingData:
            self.P1.append(value)
        #print 'P1 = ', self.P1
  
    def currentDataSize( self ):
        return len( self.P1 )
    
    # function to key the callback functions (!?) not entirely happy about this, 
    def callback(self, x ):
        return {vbpmg.P1 : self.onP1Change}[x]
    
    def stopDataCallback( self ):
        print 'Stopping Data Callback for ', self.epicsName + vbpmg.P1s
        self.pvDict[ vbpmg.P1 ].remove_callback( )
        
    def startDataCallback( self ):
        print 'Starting  Data Callback for ', self.epicsName
        self.pvDict[ vbpmg.P1 ].add_callback( )        
       
    def clearData(self):
        self.P1 = []          
            
class screenMonitor(object):
    
    def __init__(self, epicsName):
        print 'Initialising screen raw data'
        self.epicsName = epicsName
        self.Sta = []
        self.On = []
        self.Off = []
        self.bufferSize = 1000


        self.isBusy = False
        self.appendingData = True
        self.printing = False  

        # The object can also hold its epics.PV parameters in a dictionary
        self.pvDict = {}
        self.callBackDict = {}   
        
                
        for suf in zip(vbpmg.globalScreenMonitorType, vbpmg.globalScreenPVsuffix):
            print 'Creating ', suf[0], ' = ', self.epicsName + suf[1]
            self.pvDict[suf[0]] = epics.PV(self.epicsName + suf[1], self.callback(suf[0]))
            
    def onStaChange(self, pvname=None, value=None, char_value=None, **kw):
        if self.appendingData:
            self.Sta.append(value)
    
    def onOnChange(self, pvname=None, value=None, char_value=None, **kw):
        if self.appendingData:
            self.On.append(value)

    def onOffChange(self, pvname=None, value=None, char_value=None, **kw):
        if self.appendingData:
            self.Off.append(value)          
    
    def currentDataSize( self ):
        return len( self.Sta )
    
    #function to key the callback functions (!?) not entirely happy about this, 
    def callback(self, x ):
        return {vbpmg.Sta : self.onStaChange, 
                vbpmg.On : self.onOnChange,
                vbpmg.Off : self.onOffChange}[x]
           
    def clearData(self):
        self.Sta = [] 
        self.On = []
        self.Off = []
            
            
            
            
            
            
            
            
            
            
