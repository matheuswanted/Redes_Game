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

    def handle_events(self):
        while True:
            if self.is_exiting():
                thread.exit()

            if self.queue.qsize() < 1:
                time.sleep(0.5)
                continue
            message, info = self.queue.get(True)
            self.queue.task_done()
            self.handle(message, info)

    def handle(self, message, info):
        pass

    def receiver(self, socket, connection):
        filterObj = PacketFilter(connection)

        while True:
            if self.is_exiting():
                thread.exit()

            data = socket.receive(filterObj)
            if data:
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
