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
        src_ip6, src_mac = self.socket.get_ip_mac()

        #dst_ip = 'fe80::1c10:334e:4ab2:af3d' #'fe80::42e6:72aa:2c16:5041'

        #dst_mac = '4c:eb:42:36:49:94' #'08:00:27:c0:8e:ad'

        #self.username = 'testando' + str( random.randint(0, 100))

        dst_ip = raw_input('\n\nInsira o IP do servidor destino:\n')

        dst_mac = raw_input('\n\nInsira o MAC do servidor destino:\n')

        self.username = raw_input('\n\nInsira o nome de jogador:\n')

        self.username = self.username.replace(' ','_')

        print '\n\n'

        cprint(figlet_format('Castle Escape!'), 'yellow', 'on_blue', attrs=['bold'])

        print 'conectando...'

        dst_ip = to_net_addr(dst_ip)
        dst_mac = to_mac_str(dst_mac)
        
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
            if len(args) < 2 or len(args) > 3:
                print 'Essa acao nao existe ex.: usar 2 ou usar 2 4'
                return False

            baseData['target'] = args[1]
            if len(args) > 2:
                baseData['target2'] = args[2]

            g = GameMessage(act, REQUEST, encode_json(baseData))
            self.socket.send(g, self.connection)
            return True

        elif act == speak:
            if len(args) < 2:
                print 'Essa acao nao existe ex.: falar lorem ipsum...'
                return False

            del args[0]

            texto = ' '.join(str(x) for x in args)[:150]

            baseData['target'] = texto
                        
            g = GameMessage(act, REQUEST, encode_json(baseData))
            self.socket.send(g, self.connection)

            return False

        elif act == whisper:
            if len(args) < 3:
                print 'Essa acao nao existe ex.: cochichar lorem ipsum... jogador'
                return False
            
            del args[0]
            baseData['target2'] = args[len(args)-1]
            del args[len(args)-1]
            
            baseData['target'] = ' '.join(str(x) for x in args)[:150]
            
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
                print 'Jogo iniciado \n'

                self.do_action('examinar sala')
            else:
                raise Exception('Cannot connect to server!')
        elif message.action == check:
                self.joined = True
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
                self.do_action('examinar sala')
                return False

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
        print " >> Exemplos : \n examinar sala (esse comando lista todos os objetos dentro da sala"
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
