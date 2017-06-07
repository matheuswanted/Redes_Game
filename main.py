from Common.Socket import *
from Common.Packet import *
from Common.ConnectionInfo import *

def filter(packet):
    packet = Packet()
    return packet.ip6 == ""

def main():
    info = ConnectionInfo("", "", "", "")
    filterObj = PacketFilter(filter)
    socket = Socket()

if __name__ =="__main__":
    main()
