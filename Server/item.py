class Item:

    # name: nome do item
    # isCollectable: identifica se item e coletavel
    # item: item que esta escondido no item
    def __init__(self, name, isCollectable, item):
        self.name = name
        self.isCollectable = isCollectable
        self.item = item