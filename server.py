from Server.player import *
from Server.room import *
from Server.item import *
from Commom.ConnectionInfo import *
from Commom.Utils import *
from QueueListener import *
import copy


class Server(AsyncQueueListener):

    def __init__(self):
        AsyncQueueListener.__init__(self)
        self.rooms = []
        self.players = dict()

        self.init_rooms()

    def start(self):
        src_ip = to_net_addr(SERVER_IP6)
        dst_ip = 0
        src_mac = to_mac_str(SRC_MAC)
        dst_mac = 0
        self.update_connection(src_mac, dst_mac, src_ip, dst_ip)
        thread.start_new_thread(self.receiver, ())
        while True:
            self.handle_events()

    def handle(self, message, info):
        #print "handling"
        #Ja vem a conexao de saida, dst e o src que enviou a mensagem
        info.src_mac = self.connection.src_mac
        ip_key = to_str_addr(info.dst_ip)

        reply = GameMessage(message.action,0)
        #print "reply done -- " + str(message.action)
        #print ip_key
        player = self.get_player(ip_key)
        #print 'hello'

        if message.action == join:
            #print message
            x = decode_json(message.message)
           # print 'decoded'
            reply.status = self.login_player(x.player, ip_key)
            reply.message = 'logged'
        elif message.action == check:
            reply.message = self.check(player, message.item_id)

        elif message.action == move:
            reply.message = self.move(player, message.direction)

        elif message.action == take:
            reply.message = self.take(player, message.item)

        elif message.action == drop:
            reply.message = self.drop(player, message.item)

        elif message.action == inventory:
            reply.message = self.inventory(player)

        elif message.action == use:
            reply.message = self.use(player, message.item)

        elif message.action == speak:
            reply.message = self.speak(player, message.message)

        elif message.action == whisper:
            reply.message = self.whisper(player, message.message)
        
        self.s.send(reply, info)

    def init_rooms(self):
        r = Room("Calabouco")
        r.add_item(Item(1, "Cama com colchao", False, None))
        r.add_item(Item(2, "Jarro de agua", True,
                        Item(3, "Chave sala 1", True, None)))
        r.add_item(Item(4, "Copo de plastico", True, None))
        self.rooms.append(copy.copy(r))

        r = Room("Sala de Tortura")
        r.add_item(Item(5, "Cadeira de ferro", False, None))
        r.add_item(Item(6, "Equipamento de choque", True, None))
        r.add_item(Item(7, "Saco de roupas sujas", True, None))
        r.add_item(Item(8, "Balde vazio", True, None))
        r.add_item(Item(9, "Garrafa quebrada", True, None))
        r.add_item(Item(10, "Caixa de fosforos", True,
                        Item(11, "Chave sala 2", True, None)))
        r.add_item(Item(12, "Vela acesa", True, None))
        r.add_item(Item(13, "Martelo", True, None))
        self.rooms.append(copy.copy(r))

        r = Room("Sala de Jandar")
        r.add_item(Item(14, "Mesa com pratos quebrados", False, None))
        r.add_item(Item(15, "Lustre de velas", False, None))
        r.add_item(Item(16, "Parede cheia de quadros", False, None))
        r.add_item(Item(17, "Cristaleira com portas cadeadas",
                        False, Item(18, "Chave sala 3", True, None)))
        r.add_item(Item(19, "Machado", False, None))
        self.rooms.append(copy.copy(r))

        r = Room("Cozinha")
        r.add_item(Item(20, "Fogao a lenha", False, None))
        r.add_item(Item(21, "Pilha de lenha no canto da sala", False, None))
        r.add_item(Item(22, "Facas espalhadas pelo chao", False, None))
        r.add_item(
            Item(23, "Garfos fincados em frutas em cima da mesa", False, None))
        r.add_item(Item(24, "Uma chaleira em cima do fogao a lenha", True, None))
        r.add_item(Item(25, "Uma gaveta entreaberta", False,
                        Item(26, "Chave sala 4", True, None)))

        self.rooms.append(copy.copy(r))

        r = Room("Jardim dos Fundos do Castelo")
        r.add_item(Item(27, "Fonte com a estatua de anjos sem cabeca",
                        False, Item(28, "Chave sala 5", True, None)))
        r.add_item(Item(29, "Uma caixa de ferramentas", True, None))
        r.add_item(Item(30, "Uma arvore sem folhas", False, None))
        r.add_item(Item(31, "Um limpador de piscina", False, None))
        self.rooms.append(copy.copy(r))

    def login_player(self, name, ip):
        if self.get_player(ip):
            return FAIL

        self.players[ip] = Player(name, ip)
        return SUCCESS

    def get_player(self, ip):
        if self.players.has_key(ip):
            return self.players[ip]
        return None

    def check(self, player, item_id):
        # TODO
        return "hello check"
        # if not player:
        #    return ""

        #room = self.rooms[player.room]

        # if item_id is None:
        #    return room.items

        #item = room.get_item(item_id)

        # if item.item:
        #    return item.item

        # return ""

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
    except KeyboardInterrupt as k:
        pass
    except Exception as e:
        raise e
    finally:
        print '\nexiting'
        serv.exit()

