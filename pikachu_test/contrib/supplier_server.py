__author__ = '4ikist'

import socket
from pikachu_test.properties import *
from pikachu_test.contrib import environment_manager


def process():
    host = supplier_server_host
    port = supplier_server_port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    sock, address = s.accept()
    while True:
        buf = sock.recv(1024)
        print '<<', buf
        if buf == 'start':
            environment_manager.supplier_start_old_peers()
            sock.send('started')
        elif buf == 'stop':
            environment_manager.supplier_stop_old_peers()
            sock.send('stopped')
        elif buf == 'end':
            sock.send('ended')
            break
        else:
            sock.send(buf)
    sock.close()


if __name__ == '__main__':
    process()