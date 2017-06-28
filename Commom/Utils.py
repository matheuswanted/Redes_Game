import socket
import json
from collections import namedtuple
def to_net_addr( addr):
    return socket.inet_pton(socket.AF_INET6, addr)

def to_mac_str( addr):
    return addr.replace(':', '').decode('hex')

def to_str_addr(addr):
    return socket.inet_ntop(socket.AF_INET6, addr)
def decoder(d):
    return namedtuple('X', d.keys())(*d.values())
def decode_json(json_str):
    return json.loads(json_str, object_hook=decoder)

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

#reply_enum
FAIL = 0
SUCCESS = 1
REQUEST = 2


INTERFACE_NAME = 'wlp2s0'
#Server variables

STANDART_MULTICAST_MAC = '33:33:01:02:03:04'
SRC_MAC = '68:14:01:a6:42:8d'
SRC_IP6 = '2804:7f4:c380:9133:3ff:dc8c:47f5:885b'
SERVER_IP6 = '2804:7f4:c380:7e61:52fc:b035:1a43:6154'
