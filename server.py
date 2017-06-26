from Server.player import *
from Server.room import *
from Server.item import *
from Commom.Socket import *
from Commom.Packet import *
from Commom.ConnectionInfo import *
from Commom.Utils import *
from Queue import *
import thread 
import threading
import copy

SRC_MAC = '4c:eb:42:36:49:94'
SRC_IP6 = '2999::68c6:3003:ea12:59cb'
class Server:

    def __init__(self):
        self.rooms = []
        self.players = dict()

        self.init_rooms()

        self.queue = Queue()
        self.s = Socket()
        self.exiting = False
        self.lock = threading.Lock()

    def start(self):
        thread.start_new_thread(self.receiver,())
        while True:
            if self.queue.qsize() < 1:
                continue

            message, info = self.queue.get(True)
            self.queue.task_done()
            self.handle(message, info)

    def exit(self):
        self.lock.acquire()
        self.exiting = True
        self.lock.release()

    def is_exiting(self):
        self.lock.acquire()
        ex = self.exiting
        self.lock.release()
        return ex

    def receiver(self):
        s = Socket()
        info = ConnectionInfo(to_mac_str(SRC_MAC), 0, to_net_addr(SRC_IP6), 0)
        filterObj = PacketFilter(info)
        while True:
            if self.is_exiting():
                thread.exit()
                
            data = s.receive(filterObj)
            if data:
                self.queue.put_nowait(data)

    def handle(self, message, info):
        message = ''
        player = self.get_player(message.ip6.src_addr)
        if message.msg.action == join:
            self.login_player(message.msg.player, message.ip6.src_addr)
        elif message.msg.action == check:
            message = self.check(player, message.msg.item_id)
        elif message.msg.action == move:
            message = self.move(player, message.direction)
        elif message.msg.action == take:
            message = self.take(player, message.item)
        elif message.msg.action == drop:
            message = self.drop(player, message.item)
        elif message.msg.action == inventory:
            message = self.inventory(player)
        elif message.msg.action == use:
            message = self.use(player, message.item)
        elif message.msg.action == speak:
            message = self.speak(player, message.message)
        elif message.msg.action == whisper:
            message = self.whisper(player, message.message)

        self.s.send(message, info)


    def init_rooms(self):
        r = Room("Calabouco")
        r.add_item(Item(1, "Cama com colchao", False, None))
        r.add_item(Item(2, "Jarro de agua", True, Item(3, "Chave sala 1", True, None)))
        r.add_item(Item(4, "Copo de plastico", True, None))
        self.rooms.append(copy.copy(r))

        r = Room("Sala de Tortura")
        r.add_item(Item(5, "Cadeira de ferro", False, None))
        r.add_item(Item(6, "Equipamento de choque", True, None))
        r.add_item(Item(7, "Saco de roupas sujas", True, None))
        r.add_item(Item(8, "Balde vazio", True, None))
        r.add_item(Item(9, "Garrafa quebrada", True, None))
        r.add_item(Item(10, "Caixa de fosforos", True, Item(11, "Chave sala 2", True, None)))
        r.add_item(Item(12, "Vela acesa", True, None))
        r.add_item(Item(13, "Martelo", True, None))
        self.rooms.append(copy.copy(r))

        r = Room("Sala de Jandar")
        r.add_item(Item(14, "Mesa com pratos quebrados", False, None))
        r.add_item(Item(15, "Lustre de velas", False, None))
        r.add_item(Item(16, "Parede cheia de quadros", False, None))
        r.add_item(Item(17, "Cristaleira com portas cadeadas", False, Item(18, "Chave sala 3", True, None)))
        r.add_item(Item(19, "Machado", False, None))
        self.rooms.append(copy.copy(r))

        r = Room("Cozinha")
        r.add_item(Item(20, "Fogao a lenha", False, None))
        r.add_item(Item(21, "Pilha de lenha no canto da sala", False, None))
        r.add_item(Item(22, "Facas espalhadas pelo chao", False, None))
        r.add_item(Item(23, "Garfos fincados em frutas em cima da mesa", False, None))
        r.add_item(Item(24, "Uma chaleira em cima do fogao a lenha", True, None))
        r.add_item(Item(25, "Uma gaveta entreaberta", False, Item(26, "Chave sala 4", True, None)))
        
        self.rooms.append(copy.copy(r))

        r = Room("Jardim dos Fundos do Castelo")
        r.add_item(Item(27, "Fonte com a estatua de anjos sem cabeca", False, Item(28, "Chave sala 5", True, None)))
        r.add_item(Item(29, "Uma caixa de ferramentas", True, None))
        r.add_item(Item(30, "Uma arvore sem folhas", False, None))
        r.add_item(Item(31, "Um limpador de piscina", False, None))
        self.rooms.append(copy.copy(r))

    def login_player(self, name, ip):
        if self.get_player(ip):
            return False
        
        self.players[ip] = Player(name, ip)
        return True

    def get_player(ip):
        if self.players.has_key(ip):
            return self.players[ip]
        return None

    def check(self, player, item_id):
        # TODO
        return "hello check"
        #if not player:
        #    return ""

        #room = self.rooms[player.room]

        #if item_id is None:
        #    return room.items

        #item = room.get_item(item_id)

        #if item.item:
        #    return item.item
        
        #return ""

    def move(self, player, direction):
        # TODO
        if not player:
            return ""
        
        return "hello move"

    def take(self, player, item):
        # TODO
        return "hello take"

    def drop(self, player, item):
        # TODO
        return "hello drop"

    def inventory(self, player):
        # TODO
        return "hello invetory"

    def use(self, player, item):
        # TODO
        return "hello item"

    def speak(self, player, message):
        # TODO
        return "hello speak"

    def whisper(self, player, message):
        # TODO
        return "hello whisper"

if __name__ == "__main__":
    serv = Server()
    
    #serv.login_player("Almir", "xalala")

    #serv.check("xalala", 2)
    try:
        serv.start()
    except:
        print sys.exc_info()[0]
        serv.exit()