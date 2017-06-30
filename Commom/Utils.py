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

def obj_dict(obj):
    return 

def encode_json(obj):
    if hasattr(obj, '__dict__'):
        return json.dumps(obj.__dict__)
    
    return json.dumps(obj)

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
help = 10

#reply_enum
FAIL = 0
SUCCESS = 1
REQUEST = 2


INTERFACE_NAME = 'wlp3s0'
#Server variables

STANDART_MULTICAST_MAC = '33:33:01:02:03:04'
SRC_MAC = '4c:eb:42:36:49:94'
SRC_IP6 = 'fe80::1c10:334e:4ab2:af3d'
SERVER_IP6 = 'fe80::42e6:72aa:2c16:5041'
