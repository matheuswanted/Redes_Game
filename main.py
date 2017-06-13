from Commom.Socket import *
from Commom.Packet import *
from Commom.ConnectionInfo import *
from Commom.Debug import *
import socket

def to_net_addr(addr):
    return socket.inet_pton(socket.AF_INET6,addr)


def to_mac_str(addr):
    addr_str = ""
    for i in addr:
        addr_str = addr_str + unichr(i)
    return addr_str.encode('utf8')

def main():
    debug_print("Iniciado...")

    s = Socket()
    info = ConnectionInfo(to_mac_str([0xa4,0x1f,0x72,0xf5,0x90,0x14]), to_mac_str([0xa4,0x1f,0x72,0xf5,0x90,0x7f]), to_net_addr(s.get_ip()), to_net_addr("2001:db8:800:200c:8428:d09c:e238:cf6b"))
    filterObj = PacketFilter(info)

    debug_print("Socket criado...")
    debug_print("Recebendo dados...")
    s.send("teste",info)
    while True:
        if s.receive(filterObj):
            debug_print("Recebi PING")

    debug_print("Finalizado...")

if __name__ =="__main__":
    main()
