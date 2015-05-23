import threading
import json

class NetEngine(object):
    def __init__(self, outgoing=('127.0.0.1', 8001), incoming=('127.0.0.1',8002)):
        self.ip_out, self.port_out = outgoing
        self.ip_in, self.port_in = incoming
        self.data = None

        self.create_sockets()

    def create_sockets(self):
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((self.ip_in, self.port_in))

    def daemon(self, event, code):
        def serve():
            while True:
                self.data = json.loads(self.read())
                print 'posting network event', self.data
                #event.post(event.Event(code + 100))
        self.thread = threading.Thread(target=serve)
        self.thread.setDaemon(True)
        self.thread.start()

    def read(self):
        data, addr = self.listener.recvfrom(1000)
        return data

    def write(self, s):
        self.sender.sendto(s, (self.ip_out, self.port_out))

if __name__ == '__main__':
    n = NetEngine()
    n.create_listener()
    data = n.read()
    print data
    while data:
        data = n.read()
        print data