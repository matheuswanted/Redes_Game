class ConnectionInfo:
    def __init__(self, src_mac, dst_mac, src_ip, dst_ip, ignore_loop_back=False, username=None):
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.ignore_loop_back = ignore_loop_back
        self.username = username
