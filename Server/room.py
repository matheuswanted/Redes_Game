class Room:

    def __init__(self, name, doors):
        self.name = name
        self.items = []
        self.doors = doors #[N/S/L/O]

    def add_item(self, item):
        self.items.append(item)

    def get_item(self, id):
        for i in self.items:
            if i.id == id:
                return i

    def open_door(self, direction, key):
        d = -1
        if direction == 'N':
            d = 0
        elif direction == 'S':
            d = 1
        elif direction == 'L':
            d = 2
        elif direction == 'O':
            d = 3

        if d == -1:
            return False

        # nae existe porta
        if self.doors[d] == 0:
            return 0
        
        # precisa de chave
        if not key:
            return -1

        return self.doors[d]
