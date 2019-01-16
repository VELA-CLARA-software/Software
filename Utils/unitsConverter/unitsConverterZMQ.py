import os, sys
import time
import zmq
sys.path.append("../../../")
import Software.Utils.getQuadK as quadK  
import threading
import signal
import cherrypy

magprop = quadK.getMagnetProperties()

class zmqServer(threading.Thread):

    def __init__(self, port=5556):
        super(zmqServer, self).__init__()
        self.event = threading.Event()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.linger = 0
        self.port = port

    def run(self):
        self.socket.bind("tcp://*:%s" % (self.port))
        self.socket.linger = 0
        while not self.event.is_set():
            msg = self.socket.recv_pyobj()
            if 'type' in msg:
                if msg['type'] == 'magnet':
                    ans = magnet(**msg)
                if msg['type'] == 'getNamesK':
                    ans = getNamesK(**msg)
                    self.socket.send_pyobj(ans)

    def stop(self):
        print 'stopping server...'
        self.event.set()
        self.socket.close()
        self.context.destroy()

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


class zmqClient(object):
    def __init__(self, port=5556):
        super(zmqClient, self).__init__()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.linger = 0
        self.socket.connect ("tcp://localhost:%s" % port)

    def request(self, **kwargs):
        self.socket.send_pyobj(kwargs)
        message = self.socket.recv_pyobj()
        # print "Received reply ", kwargs, "[", message, "]"
        return message

    def magnet(self, **kwargs):
        return self.request(type='magnet', **kwargs)

    def getNamesK(self, **kwargs):
        return self.request(type='getNamesK', **kwargs)

def magnet(name=None, DBURT=None, momentum=None, current=None, *args, **kwargs):
    print 'name = ', name
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
            return magprop.getK(str(name))

def getNamesK(DBURT=None, momentum=None, *args, **kwargs):
    if DBURT is not None:
        magprop.loadDBURT(str(DBURT))
    if momentum is not None:
        magprop.momentum = float(momentum)
    namesK = magprop.getNamesK()
    return namesK

def stop(*args):
    server.stop()
    cherrypy.engine.exit()
    # sys.exit(0)

if __name__ == "__main__":
    from infi.systray import SysTrayIcon
    icon = 'unitsConverter.ico'
    hover_text = "unitsConverter"
    menu_options = ()
    systray = SysTrayIcon(icon, hover_text, menu_options,on_quit=stop)
    systray.start()
    server = zmqServer()
    server.start()
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.quickstart(Root())
