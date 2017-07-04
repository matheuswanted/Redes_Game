import copy

class Room:

    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_item(self, id):
        for i in self.items:
            if i.id == id:
                return i

    def take_item(self, id):
        for i in range(len(self.items)):
            if self.items[i].id == id and self.items[i].isCollectable:
                item = copy.copy(self.items[i])
                del self.items[i]
                return item
