__author__ = '4ikist'

import socket
from pikachu_test.properties import *


class SupplierSender(object):
    def __init__(self):
        host = supplier_server_host
        port = supplier_server_port

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.s.send('hi')
        print '<<', self.s.recv(100)

    def start_supplier(self):
        print 'send start'
        self.s.send('start')
        print '<<', self.s.recv(100)

    def stop_supplier(self):
        print 'send stop'
        self.s.send('stop')
        print '<<', self.s.recv(100)

    def __del__(self):
        self.s.send('end')
        print '<<', self.s.recv(100)
        self.s.close()


if __name__ == '__main__':
    ss = SupplierSender()
    ss.stop_supplier()
    ss.start_supplier()
    ss.stop_supplier()