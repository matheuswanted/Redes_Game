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

        dst_ip = 'fe80::42e6:72aa:2c16:5041'

        dst_mac = '08:00:27:c0:8e:ad'

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
            act = get_command(args[0].upper())

            if act == -1:
                print "Essa acao nao existe e voce segue preso na sala, tente de novo."
                return False            
        except:
            print "Essa acao nao existe e voce segue preso na sala, tente de novo."            
            return False

        baseData = { 'player' : self.username }

        if act == check:
            if len(args) != 2:
                print 'Essa acao nao existe ex.: examinar sala ou examinar 2'
                return False

            baseData['target'] = args[1]
            
            g = GameMessage(act, REQUEST, encode_json(baseData))
            self.socket.send(g, self.connection)
            return True

        elif act == move:
            if len(args) != 2:
                print 'Essa acao nao existe ex.: mover n'
                return False

            baseData['target'] = args[1].upper()
            g = GameMessage(act, REQUEST, encode_json(baseData))
            self.socket.send(g, self.connection)
            return True
        
        elif act == take:
            if len(args) != 2:
                print 'Essa acao nao existe ex.: pegar 2'
                return False

            baseData['target'] = args[1]
            g = GameMessage(act, REQUEST, encode_json(baseData))
            self.socket.send(g, self.connection)
            return True
        
        elif act == drop:
            if len(args) != 2:
                print 'Essa acao nao existe ex.: largar 2'
                return False

            baseData['target'] = args[1]
            g = GameMessage(act, REQUEST, encode_json(baseData))
            self.socket.send(g, self.connection)
            return True   

        elif act == inventory:
            g = GameMessage(act, REQUEST, encode_json(baseData))
            self.socket.send(g, self.connection)
            return True        

        elif act == use:
            if len(args) != 3:
                print 'Essa acao nao existe ex.: usar 2 4'
                return False

            baseData['target'] = args[1]
            if len(args) > 2:
                baseData['target2'] = args[2]

            g = GameMessage(act, REQUEST, encode_json(baseData))
            self.socket.send(g, self.connection)
            return True

        elif act == speak:
            texto = None

            try:            
                texto = raw_input('Envie uma mensagem de 140 caracteres(enter para enviar):\n')[:140]
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
            try:
                baseData['target2'] = raw_input('Digite o nome do jogador que voce quer conversar:\n')
                #[:30]  
                # print "Voce precisa digitar o nome do jogador que quer conversar, tente de novo..."
                baseData['target'] = raw_input('Envie uma mensagem de 140 caracteres para um jogador especifico:\n')
                #[:140]
            except:
                print 'Informacoes invalidas, tente de novo...'
                return False
            
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
        print "Lista de comandos diponiveis no jogo: \n "
        print " > EXAMINAR [sala/objeto] "
        print " > MOVER [N/S/L/O] "
        print " > PEGAR [objeto] "
        print " > LARGAR [objeto] "
        print " > INVENTARIO "
        print " > USAR [objeto] {alvo} "
        print " > FALAR [texto] "
        print " > COCHICHAR [texto] [jogador] "
        print " > AJUDA "
        print " >> Exemplos : \n examinar sala (esse comando lista todos os objetos dentro da sala \n"
        print " examinar 1 (esse comando examina o objeto de id 1)."

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
