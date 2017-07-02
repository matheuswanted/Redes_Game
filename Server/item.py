class Item:

    # name: nome do item
    # isCollectable: identifica se item e coletavel
    # item: item que esta escondido no item
    def __init__(self, id, name, isCollectable, item=None, out_door=None):
        self.id = id
        self.name = name
        self.isCollectable = isCollectable
        self.item = item
        self.out_door = out_door
    
    def to_string(self):
        return '(' + str(self.id) + ') - ' + str(self.name)

    def use_item(self, item):
        return 'Usou ' + item.to_string() + ' EM ' + self.to_string()