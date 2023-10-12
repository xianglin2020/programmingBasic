#! -*- encoding=utf-8 -*-

from computer_network import socket_demo


def server():
    s = socket_demo.socket()
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
