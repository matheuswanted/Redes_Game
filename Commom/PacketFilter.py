import socket
import binascii
from struct import *
from ConnectionInfo import *
from Packet import *
from PacketBuilder import *
class PacketFilter:
    def __init__(self, connectionInfo):
        self.connection = connectionInfo

    def filter(self, pack_builder, network_data):
        pack_builder.unpack_eth(network_data)
        if not self.filter_ipv6(pack_builder.p.eth):
            return False

        pack_builder.unpack_ipv6(network_data)
        if not self.filter_dst_src(pack_builder.p.ip6):
            return False

        if not self.filter_udp(pack_builder.p.ip6):
            return False

        pack_builder.unpack_udp(network_data)
        if not self.filter_game_packet(pack_builder.p.udp):
            return False
        pack_builder.unpack_message(network_data)
        return True

    def filter_ipv6(self, ethernet):
        return ethernet.eth_type == 34525

    def filter_ipv4(self, ethernet):
        return ethernet.eth_type == 2048

    def filter_udp(self, ipv6):
        return ipv6.next_header == 17

    def filter_game_packet(self, udp):
        return udp.src_port == 16261 and udp.dst_port == 9309

    def filter_dst_src(self, ip6):
        to_me = self.connection.src_ip == ip6.dst_addr
        loopback_check = not self.connection.ignore_loop_back or ip6.src_addr != ip6.dst_addr
        return loopback_check and to_me and (self.connection.dst_ip == 0 or self.connection.dst_ip == ip6.src_addr)

    def filter_ping(self,pack_builder):
        protocol = unpack("!B", network_data[23])[0]
        #print protocol
        return  protocol == 0x001

