import thread
from Commom.Utils import *
from QueueListener import *


class Client(AsyncQueueListener):

    def __init__(self):
        AsyncQueueListener.__init__(self)
        self.x = ""
        self.joined = False
        self.wait = False

    def game(self):
        self.help()
        dst_ip = raw_input('\n\nInsira o IP do servidor destino:\n')

        username = raw_input('Insira o nome de jogador:\n')
        #username = 'm'
        dst_ip = to_net_addr(dst_ip)
        src_ip = to_net_addr(SRC_IP6)
        src_mac = to_mac_str(SRC_MAC)
        dst_mac = to_mac_str(STANDART_MULTICAST_MAC)
        self.update_connection(src_mac, dst_mac, src_ip, dst_ip, True)
        #print 'send now!'
        #print '{player:\''+username+'\'}'
        g = GameMessage(join, REQUEST, '{"player": "'+username+'"}')
        self.s.send(g, self.connection)
        self.start()

    def start(self):
        thread.start_new_thread(self.receiver, ())
        wait = True
        while True:
            self.handle_events()
            if not self.wait_server():
                action = raw_input('>>')
                wait = self.do_action(action)

    def wait_server(self):
        return not self.joined or self.wait

    def do_action(self, action):
        return False

    def handle(self, message, info):
        if message.action == join:
            if message.status == SUCCESS:
                print 'joined'
                self.joined = True
            else:
                raise Exception('Cannot connect to server!')

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
        c.game()
    except KeyboardInterrupt as k:
        pass
    except Exception as e:
        raise e
    finally:
        print '\nexiting'
        c.exit()
