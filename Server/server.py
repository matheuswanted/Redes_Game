from player import *
from room import *
from item import *
import copy

class Server:

    def __init__(self):
        self.rooms = []
        self.players = dict()

        self.init_rooms()

        self.queue = Queue()
        self.s = Socket()

    def start(self):
        thread.start_new_thread(receiver,(self))
        while True:
            message = self.queue.get(True)
            self.queue.task_done()
            self.handle(message)

    def handle(self, message):
        message = ''
        if message.msg.action == 'join':
            self.login_player(message.msg.player, message.ip6.src_addr)
        elif message.msg.action == 'check':
            pass
        elif message.msg.action == 'move':
            pass
        elif message.msg.action == 'take':
            pass
        elif message.msg.action == 'drop':
            pass
        elif message.msg.action == 'inventory':
            pass
        elif message.msg.action == 'use':
            pass
        elif message.msg.action == 'speak':
            pass
        elif message.msg.action == 'whisper':
            pass

        self.s.send(message)
            

    def receiver(self):
        info = ConnectionInfo(to_mac_str('4c:eb:42:36:49:94'), to_mac_str('08:00:27:c0:8e:ad'), to_net_addr("fe80::1c10:334e:4ab2:af3d"), to_net_addr("fe80::42e6:72aa:2c16:5041"))
        filterObj = PacketFilter(info)
        s = Socket()
        while True:
            data = s.receive(filterObj)
            if data:
                self.queue.put_nowait(data)


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

        r = Room("Cozinha")check
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
        if ip in self.players:
            return False
        
        self.players[ip] = Player(name, ip)
        return True

    def check(self, ip, item_id):
        # TODO
        if ip not in self.players:
            return ""

        player = self.players[ip]

        room = self.rooms[player.room]

        if item_id is None:
            return room.items

        item = room.get_item(item_id)

        if item.item:
            return item.item
        
        return ""

    def move(self, direction):
        # TODO
        pass

    def take(self, item):
        # TODO
        pass

    def drop(self, item):
        # TODO
        pass

    def inventory(self):
        # TODO
        pass

    def use(self, item):
        # TODO
        pass

    def speak(self, message):
        # TODO
        pass

    def whisper(self, player, message):
        # TODO
        pass

if __name__ == "__main__":
    serv = Server()
    
    serv.login_player("Almir", "xalala")

    serv.check("xalala", 2)
    serv.start()