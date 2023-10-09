#! -*- encoding=utf-8 -*-

import socket


def server():
    s = socket.socket()
    hots = "127.0.0.1"
    port = 6666
    s.bind((hots, port))
    s.listen(5)

    while True:
        c, addr = s.accept()
        print('connect Addr: ', addr)
        c.send('accept client yet!'.encode('utf-8'))
        c.close()


if __name__ == '__main__':
    server()
