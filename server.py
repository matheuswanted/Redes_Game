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
        src_ip6, src_mac = self.socket.get_ip_mac()

        dst_ip = 0
        dst_mac = 0
        
        self.connection = ConnectionInfo(to_mac_str(src_mac), dst_mac, to_net_addr(src_ip6), dst_ip)

        threadRecv = threading.Thread(target=self.receiver, args=(self.socket, self.connection,))
        threadRecv.start()

        print 'Server running'

        while True:
            self.handle_events()

    def handle(self, message, info):
        #Ja vem a conexao de saida, dst e o src que enviou a mensagem

        info.src_mac = self.connection.src_mac

        # infos para enviar feedback por multicast
        infoMulticast = copy.copy(info)
        infoMulticast.dst_ip = to_net_addr(MULTICAST_IPV6)
        infoMulticast.dst_mac = to_mac_str(MULTICAST_MAC)
        replyMulticast = GameMessage(feedback, RESPONSE)
        multicastMsg = None

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
            reply.status, multicastMsg = self.login_player(data.player, ip_key, info.dst_mac.encode('hex'))
            responseData['player'] = data.player
            responseData['message'] = 'logged'

        elif message.action == check:
            if data.target == 'sala':
                responseData['message'], multicastMsg = self.check(player)
            else:
                responseData['message'], multicastMsg = self.check(player, data.target)
            
        elif message.action == move:
            responseData['message'], multicastMsg = self.move(player, data.target)

        elif message.action == take:

            responseData['message'], multicastMsg = self.take(player, data.target)

        elif message.action == drop:

            responseData['message'], multicastMsg = self.drop(player, data.target)

        elif message.action == inventory:
            responseData['message'] = self.inventory(player)

        elif message.action == use:

            responseData['message'], multicastMsg = self.use(player, data)

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

            responseData['message'] = str(player.name) + ' cochichou: ' + str(data.target)

            p = self.whisper(player, data.target2)

            if p:
                responseData['player'] = p.name

                info.dst_mac = to_mac_str(p.mac)
                info.dst_ip = to_net_addr(p.ip)
            else:
                responseData['message'] = 'Jogador nao esta na sala'

        # envio da resposata para solicitante
        reply.message = encode_json(responseData)
        self.socket.send(reply, info)

        # feedback do comandos para players na sala
        roomPlayers = self.get_players_room(self.get_player(data.player))
        if multicastMsg is not None and len(roomPlayers) > 0:
            responseMulticast = { 'message' : multicastMsg }
            responseMulticast['player'] = roomPlayers
            replyMulticast.message = encode_json(responseMulticast)
            self.socket.send(replyMulticast, infoMulticast)

    def login_player(self, name, ip, mac):
        player = self.get_player(name)

        if player and player.ip != ip:
            return FAIL, None

        self.players[name] = Player(name, ip, mac)
        return SUCCESS, str(name) + ' entrou no jogo' 

    def get_player(self, name):
        if self.players.has_key(name):
            return self.players[name]
        return None

    def check(self, player, item_id=None):
        if not player:
           return "", None

        room = self.rooms[player.room]

        # check room items and players
        if item_id is None:
            r = ''
            for i in room.items:
                r += i.to_string()
                r += '\n'

            r += 'Jogadores: ' + self.speak(player)

            return r, None
        
        item = room.get_item(int(item_id))

        if item is None:
            return "Nada encontrado", None

        if item.item:
            player.inventory.append(item.item)
            if 'Chave' in item.item.name:
                return 'Voce encontrou: ' + item.item.to_string(), str(player.name) + ' encontrou: ' + item.item.to_string()
            else:
                return item.item, None

        return "Nada encontrado", None

    def move(self, player, direction):        
        room = self.rooms[player.room]

        response = player.move(room.items, direction)
    
        if response == 1:
            if player.room == 5:
                del self.players[player.name]
                return 'END_GAME', str(player.name) + ' encontrou a saida'

            return 'Voce esta na sala: ' + str(self.rooms[player.room].name), str(player.name) + ' entrou na sala'
        elif response == 0:
            return 'Porta trancada', None
        else:
            return 'Nao existe porta nesta direcao', None

    def take(self, player, item):
        
        room = self.rooms[player.room]

        if item is None:
            return '', None

        item = room.get_item(int(item))

        if item is None:
            return 'Objeto nao encontrado', None

        if item.isCollectable:
            player.inventory.append(item)
            return 'Voce pegou: ' + item.to_string(), str(player.name) + ' pegou ' + item.to_string()
        else:
            return 'Item nao e coletavel', None

        return 'Nada encontrado', None

    def drop(self, player, item):
        if item is None:
            return '', None
        
        item = int(item)

        if player.remove_item(item):
            return 'Item removido', str(player.name) + ' soltou ' + item.to_string()

        return 'voce nao tem o item ' + item, None

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
            return "Nada encontrado", None

        if item.name == 'Mapa':
            return 'mapa-' + str(player.room), None

        if itemTarget:
            if 'Porta' in itemTarget.name and 'Chave' in item.name:
                if str(player.room+1) in item.name:
                    player.openDoors[itemTarget.id] = item
                    return 'Voce abriu: ' + itemTarget.to_string(), str(player.name) + ' abriu ' + itemTarget.to_string()
                else:
                    return 'Chave incorreta', None

            return itemTarget.use_item(item), str(player.name) + ' ' + itemTarget.use_item(item)

        return "Nao e possivel usar", None

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

    def get_players_room(self, player):
        players = ''
        for p in self.players:
            if self.players[p].room == player.room and self.players[p].name != player.name:
                players += p + ' - '
        return players

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
