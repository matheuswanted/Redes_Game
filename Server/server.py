from player import *
from room import *
from item import *
import copy

class Server:

    def __init__(self):
        self.rooms = []
        self.players = dict()

        self.init_rooms()

    def init_rooms(self):
        r = Room("Calabouco")
        r.add_item(Item("Cama com colchão", False, None))
        r.add_item(Item("Jarro de água", True, Item("Chave sala1", True, None)))
        r.add_item(Item("Copo de plástico", True, None))
        self.rooms.append(copy.copy(r))

        r = Room("Sala de Tortura")
        r.add_item(Item("Cadeira de ferro", False, None))
        r.add_item(Item("Equipamento de choque", True, None))
        r.add_item(Item("Saco de roupas sujas", True, None))
        r.add_item(Item("Balde vazio", True, None))
        r.add_item(Item("Garrafa quebrada", True, None))
        r.add_item(Item("Caixa de fósforos", True, Item("Chave sala2", True, None)))
        r.add_item(Item("Vela acesa", True, None))
        r.add_item(Item("Martelo", True, None))
        self.rooms.append(copy.copy(r))

        r = Room("Sala de Jandar")
        r.add_item(Item("Mesa com pratos quebrados", False, None))
        r.add_item(Item("Lustre de velas", False, None))
        r.add_item(Item("Parede cheia de quadros", False, None))
        r.add_item(Item("Cristaleira com portas cadeadas", False, Item("Chave sala3", True, None)))
        r.add_item(Item("Machado", False, None))
        self.rooms.append(copy.copy(r))

        r = Room("Cozinha")
        r.add_item(Item("Fogão a lenha", False, None))
        r.add_item(Item("Pilha de lenha no canto da sala", False, None))
        r.add_item(Item("Facas espalhadas pelo chão", False, None))
        r.add_item(Item("Garfos fincados em frutas em cima da mesa", False, None))
        self.rooms.append(copy.copy(r))

        r = Room("Jardim dos Fundos do Castelo")
        r.add_item(Item("Fonte com a estátua de anjos sem cabeça", False, None))
        r.add_item(Item("Uma caixa de ferramentas", False, None))
        r.add_item(Item("Um portão de ferro (saída)", False, None))
        r.add_item(Item("Uma árvore sem folhas", False, None))
        self.rooms.append(copy.copy(r))

    def login_player(self, name, ip):
        if ip in self.players:
            return False
        
        self.players[ip] = {"name" : name, "ip" : ip, "room" : 0 }
        return True

    def check(self, ip, item):
        # TODO
        pass

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

    def speek(self, message):
        # TODO
        pass

    def whisper(self, player, message):
        # TODO
        pass

if __name__ == "__main__":
    serv = Server()
    
    serv.login_player("Almir", "xalala")