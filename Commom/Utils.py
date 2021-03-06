import socket
import json
from collections import namedtuple
from Server.room import *
from Server.item import *
import copy

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

def get_command(com):
    if com == 'EXAMINAR':
        return check
    elif com == 'MOVER':
        return move
    elif com == 'PEGAR':
        return take
    elif com == 'LARGAR':
        return drop
    elif com == 'INVENTARIO':
        return inventory
    elif com == 'USAR':
        return use
    elif com ==  'FALAR':
        return speak
    elif com == 'COCHICHAR':
        return whisper
    elif com == 'AJUDA':
        return help
    else:
        return -1

def get_rooms():

    rooms = []

    r = Room("Calabouco")
    r.add_item(Item(100, "Porta Norte", False, None, 1, 3))
    r.add_item(Item(1, "Cama com colchao", False, Item(33, "Mapa", True, None)))
    r.add_item(Item(2, "Jarro de agua", True, Item(3, "Chave sala 1", True, None), False, 4))
    r.add_item(Item(4, "Copo de plastico", True, None))
    rooms.append(copy.copy(r))

    r = Room("Sala de Tortura")
    r.add_item(Item(101, "Porta Sul", False, None, 0, 11))
    r.add_item(Item(5, "Cadeira de ferro", False, None))
    r.add_item(Item(6, "Equipamento de choque", True, None))
    r.add_item(Item(7, "Saco de roupas sujas", True, Item(32, "Mapa", True, None)))
    r.add_item(Item(8, "Balde vazio", True, Item(34, "Mapa", True, None)))
    r.add_item(Item(9, "Garrafa quebrada", True, None))
    r.add_item(Item(102, "Porta Oeste", False, None, 2, 11))
    r.add_item(Item(10, "Caixa de fosforos", True, Item(11, "Chave sala 2", True, None)))
    r.add_item(Item(12, "Vela acesa", True, None))
    r.add_item(Item(13, "Martelo", True, None))
    rooms.append(copy.copy(r))

    r = Room("Sala de Jandar")
    r.add_item(Item(103, "Porta Leste", False, None, 1, 18))
    r.add_item(Item(14, "Mesa com pratos quebrados", False, None))
    r.add_item(Item(15, "Lustre de velas", False, None))
    r.add_item(Item(16, "Parede cheia de quadros", False, None))
    r.add_item(Item(104, "Porta Norte", False, None, 3, 18))
    r.add_item(Item(17, "Cristaleira com portas cadeadas", False, Item(18, "Chave sala 3", True, None), False, 19)) #machado quebra cristaleira
    r.add_item(Item(19, "Machado", True, None))
    rooms.append(copy.copy(r))

    r = Room("Cozinha")
    r.add_item(Item(105, "Porta Sul", False, None, 2, 26))
    r.add_item(Item(20, "Fogao a lenha", False, None))
    r.add_item(Item(21, "Pilha de lenha no canto da sala", False, None))
    r.add_item(Item(106, "Porta Leste", False, None, 4, 26))
    r.add_item(Item(22, "Facas espalhadas pelo chao", False, None))
    r.add_item(Item(23, "Garfos fincados em frutas em cima da mesa", False, None))
    r.add_item(Item(24, "Uma chaleira em cima do fogao a lenha", True, None))
    r.add_item(Item(25, "Uma gaveta entreaberta", False, Item(26, "Chave sala 4", True, None)))

    rooms.append(copy.copy(r))

    r = Room("Jardim dos Fundos do Castelo")
    r.add_item(Item(107, "Porta Oeste", False, None, 3, 28))
    r.add_item(Item(27, "Fonte com a estatua de anjos sem cabeca", False, Item(28, "Chave sala 5", True, None), False, 31))
    r.add_item(Item(29, "Uma caixa de ferramentas", True, None))
    r.add_item(Item(30, "Uma arvore sem folhas", False, None))
    r.add_item(Item(31, "Um limpador de piscina", True, None))
    r.add_item(Item(108, "Porta Sul", False, None, 5, 28))
    rooms.append(copy.copy(r))

    return rooms

# timeout para resposta do servidor
TIMEOUT_RESPONSE = 4

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
feedback = 11

#reply_enum
FAIL = 0
SUCCESS = 1
REQUEST = 2
RESPONSE = 3

INTERFACE_NAME = 'wlp3s0' #'enp4s0'

MULTICAST_MAC = '33:33:00:00:00:01'
MULTICAST_IPV6 = 'ff02::1'

#Server variables
#SRC_MAC = '4c:eb:42:36:49:94'
#SRC_IP6 = 'fe80::1c10:334e:4ab2:af3d'