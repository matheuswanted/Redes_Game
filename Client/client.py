
class Client:

    def __init__(self):

        x = ""

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
    Client().help()

    