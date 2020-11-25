import zmq
import json

class zmqClient(object):
    def __init__(self, port=5556, host='apws24.dl.ac.uk'):
        super(zmqClient, self).__init__()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.linger = 0
        self.socket.connect ("tcp://%s:%s" % (host, port))

    def request(self, **kwargs):
        self.socket.send_pyobj(kwargs)
        message = json.loads(self.socket.recv())
        # print "Received reply ", kwargs, "[", message, "]"
        return message

    def magnet(self, **kwargs):
        return self.request(type='magnet', **kwargs)

    def getNamesK(self, **kwargs):
        return self.request(type='getNamesK', **kwargs)

if __name__ == "__main__":
    client = zmqClient()
    print client.magnet(name='S02-DIP01', DBURT='CLARA_2_BA1_BA2_2018-11-20-1951.dburt')
    # print client.getNamesK(DBURT='CLARA_2_BA1_BA2_2018-11-20-1951.dburt')
    # print client.magnet(name='S02-DIP01')
    # print client.getNamesK()
