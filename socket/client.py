#! -*- encoding=utf-8 -*-

import socket


def client(i):
    s = socket.socket()
    s.connect(('127.0.0.1', 6666))
    print('receive msg %s, client %d' % (s.recv(1024), i))
    s.close()


if __name__ == '__main__':
    for i in range(10):
        client(i)
