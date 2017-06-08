from Commom.Socket import *
from Commom.Packet import *
from Commom.ConnectionInfo import *
from Commom.Debug import *

def main():
    debug_print("Iniciado...")

    info = ConnectionInfo("", "", "192.168.15.32", "192.168.15.34")
    filterObj = PacketFilter(filter, info)
    s = Socket()
    debug_print("Socket criado...")

    debug_print("Recebendo dados...")
    while True:
        if s.receive(filterObj):
            debug_print("Recebi PING")

    debug_print("Finalizado...")

if __name__ =="__main__":
    main()
