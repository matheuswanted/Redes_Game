import thread
import sys
from Commom.Utils import *
from QueueListener import *


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

    def game(self):
        self.help()
        #dst_ip = raw_input('\n\nInsira o IP do servidor destino:\n')

        dst_ip = 'fe80::bcb6:cdb1:6bcb:84b7'# 'fe80::1c10:334e:4ab2:af3d'

        dst_mac = '84:8f:69:bf:bd:eb'# '4c:eb:42:36:49:94'

        cprint(figlet_format('Castle Escape!'),
       'yellow', 'on_blue', attrs=['bold'])

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
    
    def drawMap(self):
        cprint("______________                 _____________________",'yellow', 'on_blue', attrs=['bold']) 
        cprint("|             |                |                    |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|   Cozinha   |                |     Jardim do      |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|   Room 4    |                |     Fundos do      |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|             |________________|     Castelo        |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|              ________________                     |",'yellow', 'on_blue', attrs=['bold'])     
        cprint("|             |                |                    |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|             |                |       Room 5       |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|             |                |_________xxx________|",'yellow', 'on_blue', attrs=['bold'])
        cprint("______||______|_____________",'yellow', 'on_blue', attrs=['bold']) 
        cprint("|     ||      |             |           FIM!        ",'yellow', 'on_blue', attrs=['bold'])
        cprint("|             |   Sala de   |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|  Room 3     |   Tortura   |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|             |             |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|           (   )  Room 2   |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|             |             |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|  Sala de    |             |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|   Jantar    |             |",'yellow', 'on_blue', attrs=['bold'])
        cprint("|_____________|______||_____|",'yellow', 'on_blue', attrs=['bold']) 
        cprint("              |      ||     |",'yellow', 'on_blue', attrs=['bold'])
        cprint("              |             |",'yellow', 'on_blue', attrs=['bold'])
        cprint("              |             |",'yellow', 'on_blue', attrs=['bold'])
        cprint("              |  Calabouco  |",'yellow', 'on_blue', attrs=['bold'])
        cprint("              |    Room 1   |",'yellow', 'on_blue', attrs=['bold'])
        cprint("              |             |",'yellow', 'on_blue', attrs=['bold'])
        cprint("              |             |",'yellow', 'on_blue', attrs=['bold'])
        cprint("              |_____________|",'yellow', 'on_blue', attrs=['bold'])

        return True
        

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
        act = None        
        try:
            act = int(args[0])
            if act > 10:
                print "Essa acao nao existe e voce segue preso na sala, tente de novo."
                return False            
        except:
            print "Essa acao nao existe e voce segue preso na sala, tente de novo. Digite o numero correspondente a acao"            
            return False            

        if act == check:
            g = GameMessage(act, REQUEST, encode_json({'target' : args[1]}))
            self.s.send(g, self.connection)
            return True

        elif act == move:
            g = GameMessage(act, REQUEST, encode_json({'target' : args[1]}))
            self.s.send(g, self.connection)
            return True
        
        elif act == take:
            g = GameMessage(act, REQUEST, encode_json({'target' : args[1]}))
            self.s.send(g, self.connection)
            return True
        
        elif act == drop:
            g = GameMessage(act, REQUEST, encode_json({'target' : args[1]}))
            self.s.send(g, self.connection)
            return True   

        elif act == inventory:
            g = GameMessage(act, REQUEST)
            self.s.send(g, self.connection)
            return True        

        elif act == use:
            g = GameMessage(act, REQUEST, encode_json({'target' : args[1] , 'target2' : args[2]}))
            self.s.send(g, self.connection)
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
                        
            g = GameMessage(act, REQUEST, encode_json({'target' : texto}))
            self.s.send(g, self.connection)
            return True

        elif act == whisper:
            player2 = raw_input('Digite o nome do jogador que voce quer conversar:\n')[:30]
            
            try:            
                if not player2:
                    print "Voce precisa digitar o nome do jogador que quer conversar, tente de novo..."
                    return False
            except:
                    print "Voce precisa digitar o nome do jogador que quer conversar, tente de novo..."
                    return False
            
            texto = raw_input('Envie uma mensagem de 140 para um jogador especifico:\n')[:140]
            g = GameMessage(act, REQUEST, encode_json({'target' : texto , 'target2' : player2}))
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
            print 'actiom'
            print message.action                     
            print 'message.mwaaFW'         
            print message.message                
            if message.message == "mapa":
                self.drawMap()
            self.wait = False
            pass
        
        
    def help(self):
        # TODO: listar todos os comandos
        print "Lista de comandos diponiveis no jogo: \n "
        print " > (2) EXAMINAR [sala/objeto] "
        print "     o Retorna a descricao da sala atual (sala) ou objeto mencionado. "
        print "     o A descricao da sala tambem deve listar as salas adjacentes e suas respectivas direcoes, objetos e demais jogadores presentes no local."
        print " > (3) MOVER [N/S/L/O] "
        print "     o O jogador deve mover-se para a direcao indicada (norte, sul, leste ou oeste)."
        print "     o Ao entrar numa nova sala, o jogo deve executar automaticamente o comando 'examinar sala', que descreve o novo ambiente ao jogador."
        print " > (4) PEGAR [objeto] "
        print "     o O jogador coleta um objeto que esta na sala atual."
        print "     o Alguns objetos nao podem ser coletados, como no caso de 'porta'. "
        print " > (5) LARGAR [objeto] "
        print "     o O jogador larga um objeto que esta no seu inventorio, na sala atual."
        print " > (6) INVENTARIO "
        print "     o O jogo lista todos os objetos carregados atualmente pelo jogador. "
        print " > (7) USAR [objeto] {alvo} "
        print "     o O jogador usa o objeto mencionado; "
        print "     o Em alguns casos especificos, o objeto indicado necessitara de outro (alvo) para ser ativado (ex: usar chave porta)."
        print " > (8) FALAR [texto] "
        print "     o O jogador envia um texto que sera retransmitido para todos os jogadores presentes na sala atual. "
        print " > (9) COCHICHAR [texto] [jogador] "
        print "     o O jogador envia uma mensagem de texto apenas para o jogador especificado, se ambos estiverem na mesma sala."
        print " > (10) AJUDA "
        print "     o Lista todos os comandos possiveis do jogo."
        print " > Baseado na lista de comandos acima voce deve executar os comandos utilizandos os seus ids. \n"
        print " >> Exemplos : \n 2 sala (esse comando lista todos os objetos dentro da sala \n"
        print " 2 1 (esse comando examina o objeto de id 1)."        
        print " 2 1 (esse comando examina o objeto de id 1)."

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
