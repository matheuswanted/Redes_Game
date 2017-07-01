from Server.player import *
from Commom.ConnectionInfo import *
from Commom.Utils import *
from QueueListener import *
import threading


class Server(AsyncQueueListener):

    def __init__(self):
        AsyncQueueListener.__init__(self)
        self.players = dict()
        self.rooms = get_rooms()
        self.socket = Socket()

    def start(self):
        src_ip = to_net_addr(SRC_IP6)
        dst_ip = 0
        src_mac = to_mac_str(SRC_MAC)
        dst_mac = 0
        self.update_connection(src_mac, dst_mac, src_ip, dst_ip)

        threadRecv = threading.Thread(target=self.receiver, args=(self.socket,))
        threadRecv.start()

        print 'Server running'

        while True:
            self.handle_events()

    def handle(self, message, info):
        #print "handling"
        #Ja vem a conexao de saida, dst e o src que enviou a mensagem
        info.src_mac = self.connection.src_mac
        ip_key = to_str_addr(info.dst_ip)

        reply = GameMessage(message.action, 0)
        #print "reply done -- " + str(message.action)
        #print ip_key
        player = self.get_player(ip_key)
        #print 'hello'

        if message.action == join:
            #print message
            x = decode_json(message.message)
           # print 'decoded'
            reply.status = self.login_player(x.player, ip_key, info.src_mac.encode('hex'))
            reply.message = 'logged'
        elif message.action == check:
            d = decode_json(message.message)

            if d.target == 'sala':
                reply.message = self.check(player)
            else:
                reply.message = self.check(player, d.target)
            
        elif message.action == move:
            reply.message = self.move(player, message.direction)

        elif message.action == take:
            reply.message = self.take(player, message.item)

        elif message.action == drop:
            d = decode_json(message.message)

            reply.message = self.drop(player, d.target)

        elif message.action == inventory:
            reply.message = self.inventory(player)

        elif message.action == use:
            reply.message = self.use(player, message.item)

        elif message.action == speak:
            players = self.speak(player)

            d = decode_json(message.message)

            reply.message = str(player.name) + ' falou: ' + str(d.target)
            for p in players:
                self.socket.send(reply, ConnectionInfo(to_mac_str(SRC_MAC), to_mac_str(p.mac), to_net_addr(SRC_IP6), to_net_addr(p.ip) ))

            return None
        elif message.action == whisper:
            reply.message = self.whisper(player, message.message)
        
        self.socket.send(reply, info)

    def login_player(self, name, ip, mac):
        player = self.get_player(ip)
        if player and player.name != name:
            return FAIL

        self.players[ip] = Player(name, ip, mac)
        return SUCCESS

    def get_player(self, ip):
        if self.players.has_key(ip):
            return self.players[ip]
        return None

    def check(self, player, item_id=None):
        if not player:
           return ""

        room = self.rooms[player.room]

        if item_id is None:
            r = ''
            for i in room.items:
                r += i.to_string()
                r += '\n'
            return r

        item = room.get_item(int(item_id))

        # TODO: remover isso
        if item.id == 1:
            return 'mapa'

        if item is None:
            return "objeto n encontrado"

        if item.item:
            player.inventory.append(item.item)
            if 'Chave' in item.item.name:
                return 'Voce encontrou: ' + item.item.to_string() 
            else:
                return item.item

        return "nada encontrado"

    def move(self, player, direction):
        # TODO
        if not player:
            return ""

        return "hello move"

    def take(self, player, item):
        
        room = self.rooms[player.room]

        if item is None:
            return ''

        item = room.get_item(int(item))

        if item is None:
            return 'objeto n encontrado'

        if item.isCollectable:
            player.inventory.append(item)
            return 'voce pegou: ' + item.to_string()
        else:
            return 'item nao e coletavel'

        return 'nada encontrado'

    def drop(self, player, item):
        if item is None:
            return ''
        
        item = int(item)

        for i in range(len(player.inventory)):
            if player.inventory[i].id == item:
                del player.inventory[i]
                return 'Item removido'

        return 'voce nao tem o item ' + item

    def inventory(self, player):
        r = ''
        for item in player.inventory:
            r += item.to_string()
            r += '\n'
        return r

    def use(self, player, item):
        # TODO
        return "hello item"

    def speak(self, player):
        players = []

        for p in self.players:
            if self.players[p].room == player.room:
                players.append(self.players[p])

        return players

    def whisper(self, player, message):
        # TODO
        return "hello whisper"

if __name__ == "__main__":
    serv = Server()

    #serv.login_player("Almir", "xalala")

    #serv.check("xalala", 2)
    #try:
    serv.start()
    #except KeyboardInterrupt as k:
    #    pass
    #except Exception as e:
    #    raise e
    #finally:
    #    print '\nexiting'
    #    serv.exit()

