import socket, sys 
import netifaces
from PacketFilter import *
from PacketBuilder import *
class Socket:
    def __init__(self):
        self.s = None
        self.ip6 = None
        try:
            #s = socket.socket(socket.AF_INET6, socket.SOCK_RAW)
            #socket.ntohs(0x0003) --> ETH_P_ALL
            print socket.gethostbyname(socket.gethostname())
            self.s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        except socket.error, msg:
            print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

    def send(self, message, connection_info):
        #removed buildUdp, fixed packet
        data_pack = PacketBuilder()
        data_pack.buildEth(connection_info.src_mac, connection_info.dst_mac)
        data_pack.buildIp6(connection_info.src_ip, connection_info.dst_ip)
        #data_pack.buildMsg(message)
        data_pack = data_pack.pack()
        print data_pack#.encode('utf16')
        self.s.sendto(data_pack, ("enp4s0",0))

    def receive(self, packetFilter):
        network_data = self.s.recv(2048)
        builder = PacketBuilder()
        if network_data and packetFilter.filter(builder, network_data):
            #return PacketBuilder().unpack(network_data)

            return True
        return False
    def get_ip(self):
        if not self.ip6:
            self.ip6 = netifaces.ifaddresses('enp4s0')[netifaces.AF_INET6][0]['addr']
        return self.ip6
