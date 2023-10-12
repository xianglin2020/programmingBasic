#! -*- encoding=utf-8 -*-
import json
import socket

from computer_network.processor.net.parser import IPParser
from computer_network.processor.trans.parser import UDPParser, TCPParser
from operate_system.Pool import ThreadPool
from operate_system.Task import AsyncTask


class ProcessTask(AsyncTask):
    def __init__(self, packet, *args, **kwargs):
        self.packet = packet
        super().__init__(self.process, *args, **kwargs)

    def process(self):
        ip_header = IPParser.parse(self.packet)
        transport_header = None
        if ip_header['protocol'] == 17:
            transport_header = UDPParser.parse(self.packet)
        elif ip_header['protocol'] == 6:
            transport_header = TCPParser.parse(self.packet)
        return {
            'network_header': ip_header,
            'transport_header': transport_header
        }


class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        self.sock.bind(('192.168.31.113', 8888))
        self.sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        self.pool = ThreadPool(10)
        self.pool.start()

    def loop_serve(self):
        while True:
            packet, addr = self.sock.recvfrom(65535)
            task = ProcessTask(packet)
            self.pool.put(task)
            result = task.get_result()
            result = json.dumps(result, indent=4)
            print(result)


if __name__ == '__main__':
    server = Server()
    server.loop_serve()
