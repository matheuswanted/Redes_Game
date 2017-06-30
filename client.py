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
        #dst_ip = raw_input('\n\nInsira o IP do servidor destino:\n')

        dst_ip = 'fe80::42e6:72aa:2c16:5041'# 'fe80::1c10:334e:4ab2:af3d'

        dst_mac = '08:00:27:c0:8e:ad'# '4c:eb:42:36:49:94'

        #dst_mac = raw_input('\n\nInsira o MAC do servidor destino:\n')

        #username = raw_input('Insira o nome de jogador:\n')
        username = 'testandooo'

        dst_ip = to_net_addr(dst_ip)
        dst_mac = to_mac_str(dst_mac)

        src_ip = to_net_addr(SRC_IP6)
        src_mac = to_mac_str(SRC_MAC)
        
        self.update_connection(src_mac, dst_mac, src_ip, dst_ip, True)
        
        g = GameMessage(join, REQUEST, encode_json({ 'player' : username}))
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

        args = action.split(' ')
        act = int(args[0])

        if act == check:
            g = GameMessage(act, REQUEST, encode_json({'target' : args[1]}))
            self.s.send(g, self.connection)
            return True

        elif act == help:
            self.help()
            return False

        return False

    def handle(self, message, info):
        if message.action == join:
            if message.status == SUCCESS:
                print 'joined'
                self.joined = True
            else:
                raise Exception('Cannot connect to server!')
        elif message.action == check:
            print 'retorno do check recebido'
            self.wait = False
            pass

    def help(self):
        # TODO: listar todos os comandos
        print "Lista de comandos diponiveis no jogo: \n "
        print " > (2) Examinar [sala/objeto] "
        print "     o Retorna a descricao da sala atual (sala) ou objeto mencionado. "
        print "     o A descricao da sala tambem deve listar as salas adjacentes e suas respectivas direcoes, objetos e demais jogadores presentes no local."
        print " > (3) Mover [N/S/L/O] "
        print "     o O jogador deve mover-se para a direcao indicada (norte, sul, leste ou oeste)."
        print "     o Ao entrar numa nova sala, o jogo deve executar automaticamente o comando 'examinar sala', que descreve o novo ambiente ao jogador."
        print " > (4) Pegar [objeto] "
        print "     o O jogador coleta um objeto que esta na sala atual."
        print "     o Alguns objetos nao podem ser coletados, como no caso de 'porta'. "
        print " > (5) Largar [objeto] "
        print "     o O jogador larga um objeto que esta no seu inventorio, na sala atual."
        print " > (6) Inventario "
        print "     o O jogo lista todos os objetos carregados atualmente pelo jogador. "
        print " > (7) Usar [objeto] {alvo} "
        print "     o O jogador usa o objeto mencionado; "
        print "     o Em alguns casos especificos, o objeto indicado necessitara de outro (alvo) para ser ativado (ex: usar chave porta)."
        print " > (8) Falar [texto] "
        print "     o O jogador envia um texto que sera retransmitido para todos os jogadores presentes na sala atual. "
        print " > (9) Cochichar [texto] [jogador] "
        print "     o O jogador envia uma mensagem de texto apenas para o jogador especificado, se ambos estiverem na mesma sala."
        print " > (10) Ajuda "
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
