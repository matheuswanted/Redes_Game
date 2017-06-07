import socket, sys 
from PacketFilter import *
from PacketBuilder import *

class Socket:
    def __init__(self):
        self.s = None
        try:
            #s = socket.socket(socket.AF_INET6, socket.SOCK_RAW)
            #socket.ntohs(0x0003) --> ETH_P_ALL
            s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        except socket.error, msg:
            print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

    def send(self, message, connection_info):
        #removed buildUdp, fixed packet
        data_pack = PacketBuilder()
        data_pack = data_pack.buildEth(connection_info.src_mac, connection_info.dst_mac)
        data_pack = data_pack.buildIp6(connection_info.src_ip, connection_info.dst_ip)
        data_pack = data_pack.buildMsg(message)
        data_pack = data_pack.pack()
        self.s.sendto(pack, connection_info.dst_ip)

    def receive(self, packetFilter):
        pack = PacketBuilder().unpack(self.s.recv(2048))
        if not packetFilter.filter(pack):
            return pack
        return None
