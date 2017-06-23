# SocketGame

## Regras do Jogo:
 
### Objetivo: 
    Sair do castelo. 
 
### Contexto: 
    Cada jogador que se conectar ao servidor acordará no calabouço do castelo (sala 1). 
    Seu objetivo será se libertar e, para isso, deverá passar por 
    5 salas dentro do castelo.
    
### Regras: 
    Cada sala do castelo possui uma porta de entrada e outra de saída. 
    Quando o jogador entrar na sala a porta de saída sempre estará fechada. 
    Para abrir a porta o jogador deverá coletar a chave específica que abre a 
    porta de saída. Essa chave estará sempre escondida  em algum lugar da sala,
    seja em uma caixa, cofre, armário etc. Somente quando estiver com esse ítem em mãos a porta 
    poderá ser aberta. Cada pessoa precisa da chave correta para sair da sala, 
    independentemente de outra pessoa ter encontrado a chave antes. 
    
### Calabouço  - Sala 1 
    Objetos: Uma cama com colchão e sem lençol;
             Um jarro de cheio de água
             Um copo de plástico
             Uma chave que abre a porta de saída da sala 1 (1S)
             Uma porta de ferro de saída
             
    * Onde está a chave: Dentro do jarro de água
    * Como pegar a chave: PEGAR o jarro;
                          USAR [jarro] {copo} 
    
### Sala de Tortura - Sala 2 
    Objetos: Uma cadeira de ferro;
             Um equipamento de choque;
             Um saco de roupas sujas;
             Um balde vazio;
             Uma garrafa quebrada;
             Uma caixa de fósforos;
             Uma vela acesa;
             Um martelo;
             Uma chave que abre a porta de saída da sala 2 (2S)
             Uma porta de ferro de saída

             
    * Onde está a chave: Dentro da caixa de fósforos
    * Como pegar a chave: PEGAR caixa de fósforos;
                          Usar [caixa de fósforos] (abrir caixa de fósforos)

### Sala de Jandar - Sala 3 
    Objetos: Uma mesa com pratos quebrados;
             Um lustre de velas;
             Um parede cheia de quadros;
             Um cristaleira com portas cadeadas;
             Um machado no chão;
             Uma chave que abre a porta de saída da sala 3 (3S)
             Uma porta de madeira de saída

             
    * Onde está a chave: Dentro da cristaleira 
    * Como pegar a chave: PEGAR machado
                          USAR [machado] {cristaleira}
                          
### Cozinha - Sala 4 
    Objetos: Um fogão a lenha;
             Uma pilha de lenha no canto da sala
             Facas espalhadas pelo chão;
             Garfos fincados em frutas em cima da mesa;
             Uma chave que abre a porta de saída da sala 4 (4S)
             Uma chaleira em cima do fogão a lenha
             Uma gaveta entreaberta
             Uma porta de saída

             
    * Onde está a chave: Dentro da gaveta
    * Como pegar a chave: USAR [gaveta]  
                                                    

### Jardim dos Fundos do Castelo - Sala 5 
    Objetos: Uma fonte com a estátua de anjos sem cabeça;
             Uma caixa de ferramentas;
             Um portão de ferro (saída);
             Uma árvore sem folhas;
             Um limpador de piscina;
             Uma chave que abre o portão de saída do castelo (5S)

             
    * Onde está a chave: Dentro da fonte
    * Como pegar a chave: PEGAR limpador de piscina
                          USAR [limpador de psicina] {fonte}
                          
#VSCode como root
sudo code --user-data-dir="~/.vscode-root"
