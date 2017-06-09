from Commom.Socket import *
from Commom.Packet import *
from Commom.ConnectionInfo import *
from Commom.Debug import *

def to_net_addr(addr):
    return socket.inet_pton(socket.AF_INET6,addr)

def main():
    debug_print("Iniciado...")

    info = ConnectionInfo("", "", to_net_addr("2001:db8:800:200c:a046:eabe:fa9d:23c7"), to_net_addr("2001:db8:800:200c:a046:eabe:fa9d:23c8"))
    filterObj = PacketFilter(info)
    s = Socket()
    debug_print("Socket criado...")

    debug_print("Recebendo dados...")
    while True:
        if s.receive(filterObj):
            debug_print("Recebi PING")

    debug_print("Finalizado...")

if __name__ =="__main__":
    main()
