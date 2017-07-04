import socket
import sys
import netifaces
from uuid import getnode as get_mac
from PacketFilter import *
from PacketBuilder import *
from Utils import *

class Socket:
    def __init__(self):
        self.s = None
        self.ip6 = False
        self.mac = False

        try:
            self.s = socket.socket(
                socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        except socket.error, msg:
            print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

    def send(self, message, connection_info):
        data_pack = PacketBuilder()

        data_pack.buildEth(connection_info.src_mac, connection_info.dst_mac)

        data_pack.buildIp6(connection_info.src_ip, connection_info.dst_ip)
        
        data_pack.buildMsg(message)

        data_pack = data_pack.pack()

        self.s.sendto(data_pack, (INTERFACE_NAME, 0))

    def receive(self, packetFilter):
        network_data = self.s.recv(2048)
        encoded = network_data.encode('hex')
        src_mac = encoded[12:24]
        # if src_mac == '080027c08ead':
        #     x = src_mac
        builder = PacketBuilder()
        if network_data and packetFilter.filter(builder, network_data):
            return builder.get_message(), builder.get_connection_info()

        return False

    def get_ip_mac(self):
       if not self.ip6:
           self.mac = netifaces.ifaddresses(INTERFACE_NAME)[netifaces.AF_LINK][0]['addr']
           ip6 = netifaces.ifaddresses(INTERFACE_NAME)[netifaces.AF_INET6]

           for i in ip6:
               if 'fe80' in i['addr']:
                self.ip6 = i['addr']
                self.ip6 = self.ip6[:self.ip6.index('%')]
                break
       return self.ip6, self.mac
