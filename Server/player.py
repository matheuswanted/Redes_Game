
class Player:

    def __init__(self, name, ip, mac):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.room = 0
        self.inventory = []
        self.currentePos = 1 #1 left, 2 top, 3 right, 4 down
