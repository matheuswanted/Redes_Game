class PacketFilter:
    def __init__(self, filterFn):
        self.filterFn = filterFn

    def filter(self, packet):
        return self.filterFn(packet)
