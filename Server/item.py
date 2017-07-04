import copy

class Item:

    # name: nome do item
    # isCollectable: identifica se item e coletavel
    # item: item que esta escondido no item
    def __init__(self, id, name, isCollectable, item=None, out_door=None, unlocked=True):
        self.id = id
        self.name = name
        self.isCollectable = isCollectable
        self.item = item
        self.out_door = out_door
        self.unlocked = unlocked
    
    def to_string(self):
        return '(' + str(self.id) + ') ' + str(self.name)

    def use_item(self, item):
        if self.unlocked == True:
            return True

        if self.unlocked == item.id:
            self.unlocked = True
        
        return self.unlocked == True

    def check_item(self):
        if self.item and self.unlocked == True:
            return True
        return False

    def get_item(self):
        if self.item:
            i = copy.copy(self.item)
            self.item = None
            return i
        return None

