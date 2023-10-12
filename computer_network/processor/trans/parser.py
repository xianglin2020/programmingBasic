#! -*- encoding=utf-8 -*-
import struct


class TransParser:
    IP_HEADER_OFFSET = 20
    UDP_HEADER_LENGTH = 8
    TCP_HEADER_LENGTH = 20


def data2str(data):
    l = len(data)
    data = struct.unpack(l * 'B', data)
    string = ''
    for ch in data:
        if ch >= 127 or ch < 32:
            string += '.'
        else:
            string += chr(ch)
    return string


class UDPParser(TransParser):
    """
    16 位源端口 16 位目的端口
    16 位 UDP 长度 16 位校验和
    """

    @classmethod
    def parse_udp_header(cls, udp_header):
        udp_header = struct.unpack('>HHHH', udp_header)
        return {
            'src_port': udp_header[0],
            'dst_port': udp_header[1],
            'udp_length': udp_header[2],
            'udp_checksum': udp_header[3]
        }

    @classmethod
    def parse(cls, packet):
        udp_header = packet[cls.IP_HEADER_OFFSET:cls.IP_HEADER_OFFSET + cls.IP_HEADER_OFFSET]
        data = packet[cls.IP_HEADER_OFFSET + cls.IP_HEADER_OFFSET:]
        result = cls.parse_udp_header(udp_header)
        result['data'] = data2str(data)
        return result


class TCPParser(TransParser):
    """
    16 位源端口 16 位目的端口
    32 位序列号
    32 位确认号
    4 位数据偏移 6 位保留字段    6 位标志位   16 位窗口大小
    16 位校验和 16 位紧急指针
    """

    @classmethod
    def parse_tcp_header(cls, tcp_header):
        line1 = struct.unpack('>HH', tcp_header[:4])
        line2 = struct.unpack('>L', tcp_header[4:8])
        line3 = struct.unpack('>L', tcp_header[8:12])
        line4 = struct.unpack('>BBH', tcp_header[12:16])
        flag = line4[1] & int('00111111', 2)
        line5 = struct.unpack('>HH', tcp_header[16:20])
        return {
            'src_port': line1[0],
            'dst_port': line1[1],
            'seq_num': line2[0],
            'ack_num': line3[0],
            'data_offset': line4[0] >> 4,
            'flag': {
                'FIN': flag & 1,
                'SYN': (flag > 1) & 1,
                'RST': (flag > 2) & 1,
                'PSH': (flag > 3) & 1,
                'ACK': (flag > 4) & 1,
                'URG': (flag > 5) & 1
            },
            'win_size': line4[4],
            'checksum': line5[0],
            'urg_point': line5[1]
        }

    @classmethod
    def parse(cls, packet):
        tcp_header = packet[cls.IP_HEADER_OFFSET: cls.IP_HEADER_OFFSET + cls.TCP_HEADER_LENGTH]
        data = packet[cls.IP_HEADER_OFFSET + cls.TCP_HEADER_LENGTH:]
        result = cls.parse_tcp_header(tcp_header)
        result['data'] = data2str(data)
        return result
