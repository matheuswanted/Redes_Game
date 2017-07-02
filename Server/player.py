
class Player:

    def __init__(self, name, ip, mac):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.room = 0
        self.inventory = []
        self.openDoors = dict()
    
    def get_item(self, id):
        for i in self.inventory:
            if i.id == id:
                return i
    
    def remove_item(self, id):
        for i in range(len(self.inventory)):
            if self.inventory[i].id == item:
                del self.inventory[i]
                return True
    
    def move(self, rooms_items, direction):
        response = -1

        for r in rooms_items:
            if 'Porta ' + str(direction) in r.name:
                response = 0
                if self.openDoors.has_key(r.id):
                    response = 1
                    self.room = r.out_door
                    break

        return response
