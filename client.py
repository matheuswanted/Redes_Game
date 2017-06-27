import thread
from Commom.Utils import *
from Commom.Socket import *
from Commom.Packet import *
from Queue import *
import thread
import threading


class Client:

    def __init__(self):
        self.x = ""
        self.s = Socket()
        self.queue = Queue()
        self.exiting = False
        self.lock = threading.Lock()

    def game(self):
        #src_ip = raw_input('Insira o IP do servidor destino:\n')
        src_ip = to_net_addr(SRC_IP6)
        src_mac = to_mac_str(SRC_MAC)

        #username = raw_input('Insira o nome de jogador:\n')
        username = 'm'
        c = ConnectionInfo(src_mac, src_mac, src_ip, src_ip)
        #nfo = ConnectionInfo(to_mac_str('4c:eb:42:36:49:94'), to_mac_str('08:00:27:c0:8e:ad'), to_net_addr("fe80::1c10:334e:4ab2:af3d"), to_net_addr("fe80::42e6:72aa:2c16:5041"))

        self.s.send(GameMessage(join, 'hello'), c)

    def start(self):
        thread.start_new_thread(self.receiver, ())
        self.help()
        self.game()
        wait = False
        while True:
            self.handle_events(wait)
            action = raw_input('>>')
            wait = self.do_action(action)

    def do_action(self,action):
        return False

    def handle_events(self, wait):
        if not wait and self.queue.qsize() < 1:
            return
        message, info = self.queue.get(True)
        self.queue.task_done()
        self.handle(message, info)

    def handle(self, message, info):
        pass

    def exit(self):
        self.lock.acquire()
        self.exiting = True
        self.lock.release()

    def is_exiting(self):
        self.lock.acquire()
        ex = self.exiting
        self.lock.release()
        return ex

    def receiver(self):
        s = Socket()
        info = ConnectionInfo(to_mac_str(SRC_MAC), 0, to_net_addr(SRC_IP6), 0)
        filterObj = PacketFilter(info)
        while True:
            if self.is_exiting():
                thread.exit()

            data = s.receive(filterObj)
            if data:
                print "recebido GameMessage"
                print data[0].message
                self.queue.put_nowait(data)

    def help(self):
        # TODO: listar todos os comandos
        print "Lista de comandos diponiveis no jogo: \n "
        print " > Examinar [sala/objeto] "
        print "     o Retorna a descricao da sala atual (sala) ou objeto mencionado. "
        print " > Mover [N/S/L/O] "
        print "     o A descricao da sala tambem deve listar as salas adjacentes e suas respectivas direcoes, objetos e demais jogadores presentes no local."
        print " > Mover [N/S/L/O] "
        print "     o O jogador deve mover-se para a direcao indicada (norte, sul, leste ou oeste)."
        print "     o Ao entrar numa nova sala, o jogo deve executar automaticamente o comando 'examinar sala', que descreve o novo ambiente ao jogador."
        print " > Pegar [objeto] "
        print "     o O jogador coleta um objeto que esta na sala atual."
        print "     o Alguns objetos nao podem ser coletados, como no caso de 'porta'. "
        print " > Largar [objeto] "
        print "     o O jogador larga um objeto que esta no seu inventorio, na sala atual."
        print " > Inventorio "
        print "     o O jogo lista todos os objetos carregados atualmente pelo jogador. "
        print " > Usar [objeto] {alvo} "
        print "     o O jogador usa o objeto mencionado; "
        print "     o Em alguns casos especificos, o objeto indicado necessitara de outro (alvo) para ser ativado (ex: usar chave porta)."
        print " > Falar [texto] "
        print "     o O jogador envia um texto que sera retransmitido para todos os jogadores presentes na sala atual. "
        print " > Cochichar [texto] [jogador] "
        print "     o O jogador envia uma mensagem de texto apenas para o jogador especificado, se ambos estiverem na mesma sala."
        print " > Ajuda "
        print "     o Lista todos os comandos possiveis do jogo."


if __name__ == "__main__":
    c = Client()
    try:
        c.start()
    except:
        print sys.exc_info()[0]
        c.exit()
