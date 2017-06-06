from Packet import *
class PacketBuilder:
    def __init__(self):
        self.p = Packet()

    def buildEth(self):
        return self

    def buildIp6(self):
        return self

    def buildUdp(self):
        return self

    def buildMsg(self, message):
        self.p.msg = message
        return self

    def unpack(self, pack):
        ethStart = 0
        ethEnd = 14

        ip6Start = 0
        ip6End = 14

        udpStart = 0
        udpEnd = 14

        msgStart = 0
        msgEnd = 14

        return self.p.unpack(pack[ethStart:ethEnd], pack[ip6Start:ip6End], pack[udpStart:udpEnd], pack[msgStart:msgEnd])

    def pack(self):
        return self.p.pack()