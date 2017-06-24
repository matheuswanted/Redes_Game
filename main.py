from Commom.Socket import *
from Commom.Packet import *
from Commom.ConnectionInfo import *
from Commom.Debug import *
import socket

def to_net_addr(addr):
    return socket.inet_pton(socket.AF_INET6, addr)

def to_mac_str(addr):
    return addr.replace(':', '').decode('hex')

def main(argv):
    debug_print("Iniciado...")

    s = Socket()
    info = ConnectionInfo(to_mac_str('4c:eb:42:36:49:94'), to_mac_str('08:00:27:c0:8e:ad'), to_net_addr("fe80::1c10:334e:4ab2:af3d"), to_net_addr("fe80::42e6:72aa:2c16:5041"))
    #info = ConnectionInfo(to_mac_str('08:00:27:c0:8e:ad'), to_mac_str('4c:eb:42:36:49:94'), to_net_addr("fe80::42e6:72aa:2c16:5041"), to_net_addr("fe80::1c10:334e:4ab2:af3d"))

    filterObj = PacketFilter(info)

    debug_print("Socket criado...")
    debug_print("Recebendo dados...")

    # enviando
    #s.send("teste",info)

    #recebendo
    while True:
        data = s.receive(filterObj)
        if data:
            print data

    debug_print("Finalizado...")

if __name__ =="__main__":
    main(sys.argv)
