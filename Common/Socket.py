import socket, sys 
from PacketFilter import *
from PacketBuilder import *

class Socket:
    def __init__(self):
        self.s = None
        try:
            s = socket.socket(socket.AF_INET6, socket.SOCK_RAW)
        except socket.error, msg:
            print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

    def send(self, message, dest):
        pack = PacketBuilder().buildEth().buildIp6().buildUdp().buildMsg(message).pack()
        self.s.sendto(pack, (dest, 0))

    def receive(self, packetFilter):
        pack = PacketBuilder().unpack(self.s.recv(2048))
        if not packetFilter.filter(pack):
            return pack
        return None
