import socket
def to_net_addr( addr):
    return socket.inet_pton(socket.AF_INET6, addr)

def to_mac_str( addr):
    return addr.replace(':', '').decode('hex')

#actions
join = 1
check = 2
move = 3
take = 4
drop = 5
inventory = 6
use = 7
speak = 8
whisper = 9



INTERFACE_NAME = 'enp3s0'
#Server variables

SRC_MAC = '68:14:01:a6:42:8d'
SRC_IP6 = '2001:db8:c18:1:5ea4:fc54:d531:cb60'
