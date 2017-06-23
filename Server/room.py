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

