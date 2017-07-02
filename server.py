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
        # self.update_connection(src_mac, dst_mac, src_ip, dst_ip)
        self.connection = ConnectionInfo(src_mac, dst_mac, src_ip, dst_ip)

        threadRecv = threading.Thread(target=self.receiver, args=(self.socket, self.connection,))
        threadRecv.start()

        print 'Server running'

        while True:
            self.handle_events()

    def handle(self, message, info):
        info.src_mac = self.connection.src_mac

        reply = GameMessage(message.action, RESPONSE)

        data = message.message

        responseData = {}

        player = None

        if hasattr(data, 'player'):
            player = self.get_player(data.player)

        if player:
            responseData = { 'player' : player.name }

        if message.action == join:
            ip_key = to_str_addr(info.dst_ip)
            reply.status = self.login_player(data.player, ip_key, info.src_mac.encode('hex'))
            responseData['player'] = data.player
            responseData['message'] = 'logged'

        elif message.action == check:
            if data.target == 'sala':
                responseData['message'] = self.check(player)
            else:
                responseData['message'] = self.check(player, data.target)
            
        elif message.action == move:
            responseData['message'] = self.move(player, data.target)

        elif message.action == take:

            responseData['message'] = self.take(player, data.target)

        elif message.action == drop:

            responseData['message'] = self.drop(player, data.target)

        elif message.action == inventory:
            responseData['message'] = self.inventory(player)

        elif message.action == use:

            responseData['message'] = self.use(player, data)

        elif message.action == speak:
            reply.status = SUCCESS

            players = self.speak(player)

            responseData['message'] = str(player.name) + ' falou: ' + str(data.target)

            responseData['player'] = players

            reply.message = encode_json(responseData)

            # multicast send
            info.dst_mac = to_mac_str(MULTICAST_MAC)
            info.dst_ip = to_net_addr(MULTICAST_IPV6)
            
        elif message.action == whisper:
            reply.status = SUCCESS

            responseData['message'] = str(player.name) + ' falou: ' + str(data.target)

            p = self.whisper(player, data.target2)

            if p:
                responseData['player'] = p.name

                info.dst_mac = to_mac_str(p.mac)
                info.dst_ip = to_net_addr(p.ip)
            else:
                responseData['message'] = 'Jogador nao esta na sala'


        reply.message = encode_json(responseData)

        #TODO: enviar em multicast feedback do comandos
        self.socket.send(reply, info)

    def login_player(self, name, ip, mac):
        player = self.get_player(name)

        if player and player.ip != ip:
            return FAIL

        self.players[name] = Player(name, ip, mac)
        return SUCCESS

    def get_player(self, name):
        if self.players.has_key(name):
            return self.players[name]
        return None

    def check(self, player, item_id=None):
        if not player:
           return ""

        room = self.rooms[player.room]

        # check room items and players
        if item_id is None:
            r = ''
            for i in room.items:
                r += i.to_string()
                r += '\n'

            r += 'Jogadores: ' + self.speak(player)

            return r
        
        item = room.get_item(int(item_id))

        if item is None:
            return "nada encontrado"

        if item.item:
            player.inventory.append(item.item)
            if 'Chave' in item.item.name:
                return 'Voce encontrou: ' + item.item.to_string() 
            else:
                return item.item

        return "nada encontrado"

    def move(self, player, direction):        
        room = self.rooms[player.room]

        response = player.move(room.items, direction)
    
        if response == 1:
            if player.room == 5:
                del self.players[player.name]
                return 'END_GAME'

            return 'Voce esta na sala: ' + str(self.rooms[player.room].name)
        elif response == 0:
            return 'Porta trancada'
        else:
            return 'Nao existe porta nesta direcao'

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

        if player.remove_item(item):
            return 'Item removido'

        return 'voce nao tem o item ' + item

    def inventory(self, player):
        r = ''
        for item in player.inventory:
            r += item.to_string()
            r += '\n'
        return r

    def use(self, player, args):
        target = args.target
        itemTarget = False

        room = self.rooms[player.room]

        item = player.get_item(int(target))

        if  hasattr(args, 'target2'):
            itemTarget = room.get_item(int(args.target2))        

        if item is None:
            return "nada encontrado"

        if item.name == 'Mapa':
            return 'mapa-' + str(player.room)

        if itemTarget:
            if 'Porta' in itemTarget.name and 'Chave' in item.name:
                if str(player.room+1) in item.name:
                    player.openDoors[itemTarget.id] = item
                    return 'Voce abriu: ' + itemTarget.to_string()
                else:
                    return 'Chave incorreta'

            return itemTarget.use_item(item)

        return "nao e possivel usar"

    def speak(self, player):
        players = ''

        for p in self.players:
            if self.players[p].room == player.room:
                players += p + ' - '

        return players

    def whisper(self, player, targetPlayer):

        for p in self.players:
            if self.players[p].room == player.room and self.players[p].name == targetPlayer:
                return self.players[p]

        return None

if __name__ == "__main__":
    serv = Server()
    
    try:
        serv.start()
    except KeyboardInterrupt as k:
        pass
    except Exception as e:
        raise e
    finally:
        print '\nexiting'
        serv.exit()
