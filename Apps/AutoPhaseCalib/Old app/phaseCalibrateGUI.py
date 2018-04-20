from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub         
import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
        FigureCanvasWxAgg as FigureCanvas, \
        NavigationToolbar2WxAgg as NavigationToolbar

import velaBPMGlobals as vbpmg 


class RedirectText(object):
    def __init__(self, aWxTextCtrl):
        self.out=aWxTextCtrl
    
    def write(self, string):
        self.out.WriteText(string)
        
# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class mainFrame
###########################################################################

class mainFrame ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 537,673 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        vertSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.mainNotebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Main = wx.Panel( self.mainNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        vertSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.startButton = wx.Button( self.Main, wx.ID_ANY, u"START", wx.DefaultPosition, wx.DefaultSize, 0 )
        vertSizer1.Add( self.startButton, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.resultsTxt = wx.TextCtrl( self.Main, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY )
        vertSizer1.Add( self.resultsTxt, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        self.Main.SetSizer( vertSizer1 )
        self.Main.Layout()
        vertSizer1.Fit( self.Main )
        self.mainNotebook.AddPage( self.Main, u"Main", False )
        self.Settings = wx.Panel( self.mainNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"Expert" )
        vertSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        horizSizer2 = wx.BoxSizer( wx.HORIZONTAL )
        
        gridSizer2 = wx.GridSizer( 0, 2, 0, 0 )
        
        self.momentumLabel = wx.StaticText( self.Settings, wx.ID_ANY, u"Momentum (MeV/c)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.momentumLabel.Wrap( -1 )
        gridSizer2.Add( self.momentumLabel, 0, wx.ALL, 5 )
        
        self.momentumTxt = wx.TextCtrl( self.Settings, wx.ID_ANY, u"4.5", wx.DefaultPosition, wx.DefaultSize, 0 )
        gridSizer2.Add( self.momentumTxt, 0, wx.ALL, 5 )
        
        self.shotsLabel = wx.StaticText( self.Settings, wx.ID_ANY, u"Number of Shots", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.shotsLabel.Wrap( -1 )
        gridSizer2.Add( self.shotsLabel, 0, wx.ALL, 5 )
        
        self.shotsTxt = wx.TextCtrl( self.Settings, wx.ID_ANY, u"10", wx.DefaultPosition, wx.DefaultSize, 0 )
        gridSizer2.Add( self.shotsTxt, 0, wx.ALL, 5 )
        
        self.degreesLabel = wx.StaticText( self.Settings, wx.ID_ANY, u"Degrees from crest (degrees)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.degreesLabel.Wrap( -1 )
        gridSizer2.Add( self.degreesLabel, 0, wx.ALL, 5 )
        
        self.degreesTxt = wx.TextCtrl( self.Settings, wx.ID_ANY, u"0.0", wx.DefaultPosition, wx.DefaultSize, 0 )
        gridSizer2.Add( self.degreesTxt, 0, wx.ALL, 5 )
        
        self.rangeLabel = wx.StaticText( self.Settings, wx.ID_ANY, u"Range of phase to scan over (Degrees)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.rangeLabel.Wrap( -1 )
        gridSizer2.Add( self.rangeLabel, 0, wx.ALL, 5 )
        
        self.rangeTxt = wx.TextCtrl( self.Settings, wx.ID_ANY, u"20", wx.DefaultPosition, wx.DefaultSize, 0 )
        gridSizer2.Add( self.rangeTxt, 0, wx.ALL, 5 )
        
        self.degaussBSOLCheck = wx.CheckBox( self.Settings, wx.ID_ANY, u"Degauss BSOL", wx.DefaultPosition, wx.DefaultSize, 0 )
        gridSizer2.Add( self.degaussBSOLCheck, 0, wx.ALL, 5 )
        
        self.degaussSOLCheck = wx.CheckBox( self.Settings, wx.ID_ANY, u"Degauss SOL", wx.DefaultPosition, wx.DefaultSize, 0 )
        gridSizer2.Add( self.degaussSOLCheck, 0, wx.ALL, 5 )
        
        self.degaussDIP01Check = wx.CheckBox( self.Settings, wx.ID_ANY, u"Degauss DIP01", wx.DefaultPosition, wx.DefaultSize, 0 )
        gridSizer2.Add( self.degaussDIP01Check, 0, wx.ALL, 5 )
        
        self.degaussQUAD01Check = wx.CheckBox( self.Settings, wx.ID_ANY, u"Degauss QUAD01", wx.DefaultPosition, wx.DefaultSize, 0 )
        gridSizer2.Add( self.degaussQUAD01Check, 0, wx.ALL, 5 )
        
        self.degaussQUAD02Check = wx.CheckBox( self.Settings, wx.ID_ANY, u"Degauss QUAD02", wx.DefaultPosition, wx.DefaultSize, 0 )
        gridSizer2.Add( self.degaussQUAD02Check, 0, wx.ALL, 5 )
        
        self.degaussQUAD03Check = wx.CheckBox( self.Settings, wx.ID_ANY, u"Degauss QUAD03", wx.DefaultPosition, wx.DefaultSize, 0 )
        gridSizer2.Add( self.degaussQUAD03Check, 0, wx.ALL, 5 )
        
        self.degaussQUAD04Check = wx.CheckBox( self.Settings, wx.ID_ANY, u"Degauss QUAD04", wx.DefaultPosition, wx.DefaultSize, 0 )
        gridSizer2.Add( self.degaussQUAD04Check, 0, wx.ALL, 5 )
        
        self.quadsCheck = wx.CheckBox( self.Settings, wx.ID_ANY, u"Turn quads (QUAD01, 02, 03, 04, 05, 06) off", wx.DefaultPosition, wx.DefaultSize, 0 )
        gridSizer2.Add( self.quadsCheck, 0, wx.ALL, 5 )
        
        self.correctorsCheck = wx.CheckBox( self.Settings, wx.ID_ANY, u"Turn correctors (H/VCOR03, 04, 05, 06) off", wx.DefaultPosition, wx.DefaultSize, 0 )
        gridSizer2.Add( self.correctorsCheck, 0, wx.ALL, 5 )
        
        
        horizSizer2.Add( gridSizer2, 1, wx.EXPAND, 5 )
        
        
        vertSizer2.Add( horizSizer2, 0, wx.EXPAND, 5 )
        
        
        self.Settings.SetSizer( vertSizer2 )
        self.Settings.Layout()
        vertSizer2.Fit( self.Settings )
        self.mainNotebook.AddPage( self.Settings, u"Settings", True )
        
        vertSizer.Add( self.mainNotebook, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        self.SetSizer( vertSizer )
        self.Layout()
        self.menuBar = wx.MenuBar( 0 )
        self.SetMenuBar( self.menuBar )
        
        self.statusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.startButton.Bind( wx.EVT_BUTTON, self.startCalibrate )
        
        #redirect text to the gui
        redir=RedirectText( self.resultsTxt )
        sys.stdout=redir
        sys.stderr=redir
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def startCalibrate( self, event ):
        event.Skip()

        
"""
Subclass the form created by wxFormBuilder.  We use the generated output
from wxFormBuilder verbatim and add all of the functionality here.
"""
class MyFrameSub( mainFrame ):

    def __init__(self, parent):
        # If we overload __init__ we still need to make sure the parent is initialized.
        # This also sets up GUI elements with in self namespace
        mainFrame.__init__(self, parent)
 
        # Events can also be bound in the GUI builder arguably is easier because you don't have to remember the WX events.
        # The gui builder will bind the events and generate a virtual method that we can override in the derived class.
 
        #self.m_Calculate.Bind(wx.EVT_BUTTON, self.OnCalculate)
        #self.CreatePlot()
        self.widgetNames = ['Momentum','Shots', 'Degrees', 'Range', 'QuadsOFF', 'CorrectorsOFF', 'DegaussBSOL', 'DegaussSOL', 'DegaussDIP01', 'DegaussQUAD01', 'DegaussQUAD02', 'DegaussQUAD03', 'DegaussQUAD04']
    
    # Virtual event handlers, override them in your derived class
    def startCalibrate( self, event ):

        self.widgetValues = {}

        self.widgetValues[ self.widgetNames[ 0 ] ] = self.getMomentum()
        self.widgetValues[ self.widgetNames[ 1 ] ] = self.getShots() 
        self.widgetValues[ self.widgetNames[ 2 ] ] = self.getDegrees()
        self.widgetValues[ self.widgetNames[ 3 ] ] = self.getRange()
        self.widgetValues[ self.widgetNames[ 4 ] ] = self.getQuadsOFF()
        self.widgetValues[ self.widgetNames[ 5 ] ] = self.getCorrectorsOFF()
        
        self.degausslist = np.array(self.getDegauss(), dtype=bool)
        for i in range(7):
            print 'Setting ', self.widgetNames[ i + 6 ], '=', self.degausslist[i]
            self.widgetValues[ self.widgetNames[ i + 6 ] ] = self.degausslist[i]

        # check input values are positive
        self.carryOn = True
        if self.widgetValues[ self.widgetNames[ 0 ] ] > -1:
            1
        else:
            self.carryOn = False 
        if self.widgetValues[ self.widgetNames[ 1 ] ] > -1:
            1
        else:
            self.carryOn = False
        if self.carryOn: 
            pub.sendMessage("startCalibrate", self.widgetValues)
        else:
            print 'CANNOT INPUT NEGATIVE VALUES'  


    def getMomentum(self):
        return self.getTextEntry(self.momentumTxt)

    def getShots(self):
        return self.getTextEntry(self.shotsTxt)
    
    def getDegrees(self):
        return self.getTextEntry(self.degreesTxt)    
        
    def getRange(self):
        return self.getTextEntry(self.rangeTxt)

    def getDegauss(self):
        return [self.degaussBSOLCheck.GetValue(), self.degaussSOLCheck.GetValue(), self.degaussDIP01Check.GetValue(), self.degaussQUAD01Check.GetValue(), self.degaussQUAD02Check.GetValue(), self.degaussQUAD03Check.GetValue(), self.degaussQUAD04Check.GetValue()]
        
    def getQuadsOFF(self):
        return self.quadsCheck.GetValue()
    
    def getCorrectorsOFF(self):
        return self.correctorsCheck.GetValue()
   
    def getTextEntry(self, textBox ):
        raw_value = textBox.GetValue().strip()
        # check they're all numbers
        if all(x in '0123456789.-' for x in raw_value):
            # convert to float and limit to decimal numbers
            try:
                self.value = float( raw_value )
                textBox.ChangeValue( str( self.value ) )
            except:
                textBox.ChangeValue( "Number only" )
                self.value = - 1            
        else:
            textBox.ChangeValue( "Number only" )
            self.value = - 1
        return self.value