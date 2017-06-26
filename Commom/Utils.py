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
