class Item:

    # name: nome do item
    # isCollectable: identifica se item e coletavel
    # item: item que esta escondido no item
    def __init__(self, id, name, isCollectable, item=None):
        self.id = id
        self.name = name
        self.isCollectable = isCollectable
        self.item = item
    
    def to_string(self):
        return '(' + str(self.id) + ') - ' + str(self.name)