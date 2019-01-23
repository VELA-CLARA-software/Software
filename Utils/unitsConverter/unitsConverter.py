import os, sys
import scipy.constants as physics
import numpy as np
import math
sys.path.append("../../../")
import Software.Utils.getQuadK as quadK
from infi.systray import SysTrayIcon
degree = physics.pi/180.0
SPEED_OF_LIGHT = physics.constants.c / 1e6
import cherrypy

magprop = quadK.getMagnetProperties()

class Root(object):
    @cherrypy.expose
    def magnet(self, name=None, DBURT=None, momentum=None, current=None, *args, **kwargs):
        if DBURT is not None:
            magprop.loadDBURT(str(DBURT))
        if momentum is not None:
            if isinstance(momentum,(str, unicode)):
                magprop.momentum = magprop.calculateMomentumFromDipole(str(momentum))
            else:
                magprop.momentum = float(momentum)
        if name is not None:
            if current is not None:
                return str(magprop.getK(str(name), float(current)))
            else:
                return str(magprop.getK(str(name)))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getNamesK(self, DBURT=None, momentum=None, *args, **kwargs):
        if DBURT is not None:
            magprop.loadDBURT(str(DBURT))
        if momentum is not None:
            magprop.momentum = float(momentum)
        namesK = magprop.getNamesK()
        return namesK

def on_quit_callback(args):
    cherrypy.engine.exit()

if __name__ == "__main__":
    icon = 'unitsConverter.ico'
    hover_text = "unitsConverter"
    menu_options = ()
    systray = SysTrayIcon(icon, hover_text, menu_options,on_quit=on_quit_callback)
    systray.start()
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.quickstart(Root())
