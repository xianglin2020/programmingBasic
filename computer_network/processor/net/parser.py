#! -*- encoding=utf-8 -*-
from computer_network import socket_demo
import struct


class IPParser:
    IP_HEADER_LENGTH = 20

    @classmethod
    def parser_ip_header(cls, ip_header):
        """
        4 位版本  4 位首部长度    8 位服务类型    16 位总长度
        16 位标识符 标记位 偏移
        8 位TTL 8 位协议  16 位校验和
        32 位源地址
        32 位目的地址
        :param ip_header:
        :return:
        """
        line1 = struct.unpack('>BBH', ip_header[:4])
        line3 = struct.unpack('>BBH', ip_header[8:12])
        line4 = struct.unpack('>4s', ip_header[12:16])
        line5 = struct.unpack('>4s', ip_header[16:20])
        return {
            'ip_version': line1[0] >> 4,
            'iph_length': line1[0] & 15 * 4,
            'packet_length': line1[2],
            'TTL': line3[0],
            'protocol': line3[1],
            'iph_checksum': line3[2],
            'src_ip': socket_demo.inet_ntoa(line4[0]),
            'dst_ip': socket_demo.inet_ntoa(line5[0])
        }

    @classmethod
    def parse(cls, packet):
        ip_header = packet[:20]
        return cls.parser_ip_header(ip_header)
