import copy

class Player:

    def __init__(self, name, ip, mac):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.room = 0
        self.inventory = []
    
    def get_item(self, id):
        for i in self.inventory:
            if i.id == id:
                return i
    
    def remove_item(self, id):
        for i in range(len(self.inventory)):
            if self.inventory[i].id == id:
                item = copy.copy(self.inventory[i])
                del self.inventory[i]
                return item
        return False
    
    def move(self, rooms_items, direction):
        response = -1

        for item in rooms_items:
            if 'Porta ' + str(direction) in item.name:
                response = 0
                if item.unlocked == True:
                    response = 1
                    self.room = item.out_door
                    break

        return response
