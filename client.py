import thread
import threading
import sys
from Commom.Utils import *
from QueueListener import *
import random


from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format


'''
Libs Necessarias para rodar art asc
pip install setuptools
pip install pyfiglet
pip install termcolor
pip install colorama


'''

class Client(AsyncQueueListener):

    def __init__(self):
        AsyncQueueListener.__init__(self)
        self.x = ""
        self.joined = False
        self.wait = False
        self.lock = threading.Lock()
        self.socket = Socket()
        self.username = None

    def game(self):
        self.help()
        
        src_ip6, src_mac = self.socket.get_ip_mac()

        #dst_ip = raw_input('\n\nInsira o IP do servidor destino:\n')

        dst_ip = 'fe80::1c10:334e:4ab2:af3d' #'fe80::42e6:72aa:2c16:5041'

        dst_mac = '4c:eb:42:36:49:94' #'08:00:27:c0:8e:ad'

        cprint(figlet_format('Castle Escape!'), 'yellow', 'on_blue', attrs=['bold'])

        #dst_mac = raw_input('\n\nInsira o MAC do servidor destino:\n')

        #username = raw_input('Insira o nome de jogador:\n')
        self.username = 'testando' + str( random.randint(0, 100))

        dst_ip = to_net_addr(dst_ip)
        dst_mac = to_mac_str(dst_mac)
        
        # self.update_connection(src_mac, dst_mac, src_ip, dst_ip, True)
        self.connection = ConnectionInfo(to_mac_str(src_mac), dst_mac, to_net_addr(src_ip6), dst_ip, False, self.username)

        threadRecv = threading.Thread(target = self.receiver, args=(self.socket, self.connection,))
        threadRecv.start()
        
        g = GameMessage(join, REQUEST, encode_json({ 'player' : self.username}))

        self.socket.send(g, self.connection)

        self.start()

    def start(self):
        
        threadHandle = threading.Thread(target = self.handle_events, args=())
        threadHandle.start()

        while True:
            if not self.wait_server():
                action = raw_input('>>')
                self.lock.acquire()
                self.wait = self.do_action(action)
                self.lock.release()
            else:
                time.sleep(0.5)

            if self.is_exiting():
                return

    def wait_server(self):
        self.lock.acquire()
        value = not self.joined or self.wait
        self.lock.release()
        return value

    def do_action(self, action):

        args = action.split(' ')
        act = None        
        try:
            act = int(args[0])
            if act > 10:
                print "Essa acao nao existe e voce segue preso na sala, tente de novo."
                return False            
        except:
            print "Essa acao nao existe e voce segue preso na sala, tente de novo. Digite o numero correspondente a acao"            
            return False

        baseData = { 'player' : self.username }

        if act == check:
            baseData['target'] = args[1]
            
            g = GameMessage(act, REQUEST, encode_json(baseData))
            self.socket.send(g, self.connection)
            return True

        elif act == move:
            baseData['target'] = args[1].upper()
            g = GameMessage(act, REQUEST, encode_json(baseData))
            self.socket.send(g, self.connection)
            return True
        
        elif act == take:
            baseData['target'] = args[1]
            g = GameMessage(act, REQUEST, encode_json(baseData))
            self.socket.send(g, self.connection)
            return True
        
        elif act == drop:
            baseData['target'] = args[1]
            g = GameMessage(act, REQUEST, encode_json(baseData))
            self.socket.send(g, self.connection)
            return True   

        elif act == inventory:
            g = GameMessage(act, REQUEST, encode_json(baseData))
            self.socket.send(g, self.connection)
            return True        

        elif act == use:

            baseData['target'] = args[1]
            if len(args) > 2:
                baseData['target2'] = args[2]

            g = GameMessage(act, REQUEST, encode_json(baseData))
            self.socket.send(g, self.connection)
            return True

        elif act == speak:
            texto = raw_input('Envie uma mensagem de 140 caracteres para ser retransmitida para todos os jogadores e aperte enter para finalizar:\n')[:140]
            try:            
                if not texto:
                    print "Voce precisa digitar alguma coisa, tente de novo..."
                    return False
            except:
                    print "Voce precisa digitar alguma coisa, tente de novo..."
                    return False

            baseData['target'] = texto
                        
            g = GameMessage(act, REQUEST, encode_json(baseData))
            self.socket.send(g, self.connection)

            return False

        elif act == whisper:
            
            baseData['target2'] = raw_input('Digite o nome do jogador que voce quer conversar:\n')
            #[:30]  
            # print "Voce precisa digitar o nome do jogador que quer conversar, tente de novo..."

            baseData['target'] = raw_input('Envie uma mensagem de 140 caracteres para um jogador especifico:\n')
            #[:140]

            
            g = GameMessage(act, REQUEST, encode_json(baseData))

            self.socket.send(g, self.connection)
            
            return False

        elif act == help:
            self.help()
            return False

        return False

    def handle(self, message, info):

        data = {}

        if hasattr(message.message, 'player'):
            data = message.message

        if message.action == join:
            if message.status == SUCCESS:
                print 'joined'
                self.joined = True
            else:
                raise Exception('Cannot connect to server!')
        elif message.action == check:
                print data.message
        elif message.action == use:
            if 'mapa' in data.message:
                pos = int(data.message.split('-')[1])
                self.drawMap(pos)
            else:
                print data.message
        elif message.action == move:
            if data.message == 'END_GAME':
                print 'VOCE ESCAPOU'
                self.exit()
                return
            else:
                print data.message

        elif message.action == feedback:
            print 'FEEDBACK: ' + data.message

        elif data.message:
            print data.message

        self.lock.acquire()
        self.wait = False
        self.lock.release()
        
        
    def help(self):
        # TODO: listar todos os comandos
        print "Lista de comandos diponiveis no jogo: \n "
        print " > (2) EXAMINAR [sala/objeto] "
        # print "     o Retorna a descricao da sala atual (sala) ou objeto mencionado. "
        # print "     o A descricao da sala tambem deve listar as salas adjacentes e suas respectivas direcoes, objetos e demais jogadores presentes no local."
        print " > (3) MOVER [N/S/L/O] "
        # print "     o O jogador deve mover-se para a direcao indicada (norte, sul, leste ou oeste)."
        # print "     o Ao entrar numa nova sala, o jogo deve executar automaticamente o comando 'examinar sala', que descreve o novo ambiente ao jogador."
        print " > (4) PEGAR [objeto] "
        # print "     o O jogador coleta um objeto que esta na sala atual."
        # print "     o Alguns objetos nao podem ser coletados, como no caso de 'porta'. "
        print " > (5) LARGAR [objeto] "
        # print "     o O jogador larga um objeto que esta no seu inventorio, na sala atual."
        print " > (6) INVENTARIO "
        # print "     o O jogo lista todos os objetos carregados atualmente pelo jogador. "
        print " > (7) USAR [objeto] {alvo} "
        # print "     o O jogador usa o objeto mencionado; "
        # print "     o Em alguns casos especificos, o objeto indicado necessitara de outro (alvo) para ser ativado (ex: usar chave porta)."
        print " > (8) FALAR [texto] "
        # print "     o O jogador envia um texto que sera retransmitido para todos os jogadores presentes na sala atual. "
        print " > (9) COCHICHAR [texto] [jogador] "
        # print "     o O jogador envia uma mensagem de texto apenas para o jogador especificado, se ambos estiverem na mesma sala."
        print " > (10) AJUDA "
        # print "     o Lista todos os comandos possiveis do jogo."
        print " > Baseado na lista de comandos acima voce deve executar os comandos utilizandos os seus ids. \n"
        print " >> Exemplos : \n 2 sala (esse comando lista todos os objetos dentro da sala \n"
        print " 2 1 (esse comando examina o objeto de id 1)."        
        print " 2 1 (esse comando examina o objeto de id 1)."

    def drawMap(self, player_pos):
        arr = [' ',' ',' ',' ',' ']
        arr[player_pos] = 'X'


        cprint("______________                 _____________________",'yellow', 'on_blue', attrs=['bold']) 
        cprint("|             |                |                    |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|   Cozinha   |                |     Jardim do      |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|   Room 4    |                |     Fundos do      |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|             |________________|     Castelo        |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|              ________________                     |",'yellow', 'on_blue', attrs=['bold'])     
        cprint("|     " + arr[3] + "       |                |        " + arr[4] + "           |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|             |                |       Room 5       |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|             |                |_________xxx________|",'yellow', 'on_blue', attrs=['bold'])
        cprint("|_____||______|_____________",'yellow', 'on_blue', attrs=['bold']) 
        cprint("|     ||      |             |           FIM!        ",'yellow', 'on_blue', attrs=['bold'])
        cprint("|             |   Sala de   |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|  Room 3     |   Tortura   |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|             |             |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|    " + arr[2] + "             Room 2   |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|             |             |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|  Sala de    |      " + arr[1] + "      |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|   Jantar    |             |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|_____________|______||_____|",'yellow', 'on_blue', attrs=['bold']) 
        cprint("              |      ||     |",'yellow', 'on_blue', attrs=['bold'])
        cprint("              |             |",'yellow', 'on_blue', attrs=['bold'])
        cprint("              |             |",'yellow', 'on_blue', attrs=['bold'])
        cprint("              |  Calabouco  |",'yellow', 'on_blue', attrs=['bold'])
        cprint("              |    Room 1   |",'yellow', 'on_blue', attrs=['bold'])
        cprint("              |             |",'yellow', 'on_blue', attrs=['bold'])
        cprint("              |      " + arr[0] + "      |",'yellow', 'on_blue', attrs=['bold'])
        cprint("              |_____________|",'yellow', 'on_blue', attrs=['bold'])

        return True

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
