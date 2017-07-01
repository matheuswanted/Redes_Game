from Queue import *
from Commom.Socket import *
from Commom.Packet import *
import thread
import threading
import time

class AsyncQueueListener:

    def __init__(self):
        self.queue = Queue()
        self.exiting = False
        self.upd_conn = False
        self.lock = threading.Lock()
        self.lock_conn = threading.Lock()
        self.connection = ConnectionInfo(0, 0, 0, 0)
        self.s = Socket()

    def update_connection(self, src_mac, dst_mac, src_ip, dst_ip, ignore_loop_back=False):
        self.lock_conn.acquire()
        self.upd_conn = True
        if src_mac != None:
            self.connection.src_mac = src_mac
        if dst_mac != None:
            self.connection.dst_mac = dst_mac
        if src_ip != None:
            self.connection.src_ip = src_ip
        if dst_ip != None:
            self.connection.dst_ip = dst_ip
        self.connection.ignore_loop_back = ignore_loop_back
        self.lock_conn.release()

    def get_connection(self):
        #print 'get_connection'
        self.lock_conn.acquire()
        conn = self.connection
        self.lock_conn.release()
        return conn

    def connection_updated(self):
        #print 'connection_updated'
        self.lock_conn.acquire()
        upd_conn = self.upd_conn
        self.upd_conn = False
        self.lock_conn.release()
        return upd_conn

    def handle_events(self):
        if self.queue.qsize() < 1:
            #print 'sleeping'
            time.sleep(0.5)
            return
        message, info = self.queue.get(True)
        self.queue.task_done()
        self.handle(message, info)

    def handle(self, message, info):
        pass

    def create_filter(self):
        #print 'create_filter'
        info = self.get_connection()
        return PacketFilter(info)

    def receiver(self):
        s = Socket()
        filterObj = self.create_filter()
        while True:
            if self.is_exiting():
                thread.exit()

            if self.connection_updated():
                #print 'updated'
                filterObj = self.create_filter()

            data = s.receive(filterObj)
            if data:
                # print "recebido GameMessage"
                # print data[0].message
                self.queue.put_nowait(data)

    def exit(self):
        self.lock.acquire()
        self.exiting = True
        self.lock.release()

    def is_exiting(self):
        self.lock.acquire()
        ex = self.exiting
        self.lock.release()
        return ex
