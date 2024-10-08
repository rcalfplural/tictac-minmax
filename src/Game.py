import pygame
from Velha import Velha
from Velha import Jogadores
from Spritesheet import Spritesheet

MULTIPLAYER: bool = False # Se for verdadeira então ambos os jogadores serão controlados manualmente por jogadores. Caso contrario a IA irá tomar conta de um

# Botões
class Button:
    rect: pygame.Rect
    pos: tuple
    used: bool

    def __init__(self, pos: tuple, dimensions: tuple) -> None:
        self.used = False
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], dimensions[0], dimensions[1])

#==========
#   Classe onde é definida as propriedades do jogo
#   o "frontend" da aplicação onde será processada os Input dos jogadores
#   e apresentação ao usuário por meio da biblioteca PyGame
class Game:
    # Pygame - Componentes PyGame
    screen: pygame.Surface
    clock: pygame.time.Clock
    running: bool
    font: pygame.font.Font

    # Jogo da velha
    velha: Velha

    tabuleiro = [[0 for _ in range(3)] for _ in range(3)]   # Representação tabuleiro em botões
    spritesheet: Spritesheet

    def __init__(self, titulo: str, width: int, height: int) -> None:

        # Inicializa pygame e seus componentes
        pygame.init()
        pygame.display.set_caption(titulo)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True

        # Jogo da velha e seus componentes
        self.velha = Velha()

        # Start
        self.Start()
        return

    # Método que da início a partida
    def Start(self):
        self.velha.Inicio()

        # Botões do tabuleiro
        for r in range(3):
            for c in range(3):
                self.tabuleiro[r][c] = Button((c*128, r*128), (128, 128))

        # Carrega recursos
        self.spritesheet = Spritesheet("assets/velha_128.png")
        self.font = pygame.font.Font("assets/csans.ttf", 24)
        self.__Draw()

    # Onde a lógica do jogo será processada
    def Update(self):

        # Loop principal
        while self.running:
            mouse_b: bool = False
            keys_pressed: pygame.key.ScancodeWrapper = []
            # Capturar eventos de input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    mouse_b = pygame.mouse.get_pressed()[0]
                
                if(event.type == pygame.KEYDOWN):
                    keys_pressed = pygame.key.get_pressed()


            # Captura o input e processa as jogadas se o jogo ainda não tem um fim
            if(not self.velha.fim_jogo):
                if(MULTIPLAYER):        # Partida multiplayer com dois jogadores
                    if(mouse_b):
                        jogada: tuple = self.__GetPlayerInput()
                        if(jogada == None): continue
                        self.velha.Jogada(jogada)
                        self.__Draw()
                else:
                    # Calcula aqui a ia
                    if(self.velha.vez == Jogadores.P1): # Partida com a IA alterna vez entre o jogador e a IA
                        if(mouse_b):
                            jogada: tuple = self.__GetPlayerInput()
                            if(jogada == None): continue
                            self.velha.Jogada(jogada)
                            self.__Draw()
                    else:
                        jogada: tuple = self.velha.Cpu()
                        self.velha.Jogada(jogada)
                        self.__Draw()
            else:
                if(len(keys_pressed) > 0 and keys_pressed[pygame.K_r]): # Reinicio da partida
                    self.Start()

        # Finaliza o pygame quando sair do loop
        pygame.quit()
        return
    
    # Loop de renderização
    def __Draw(self):
        self.screen.fill((128, 128, 128))

        self.__DrawTabuleiro()

        self.__DrawText("Jogador 1: O", (400, 8))
        self.__DrawText("Jogador 2: X", (400, 32))
        self.__DrawText("Vez de: "+self.velha.vez.to_str(), (16, 384))
        
        if(not MULTIPLAYER):
            self.__DrawText("Jogando com a CPU", (400, 56))
        else:
            self.__DrawText("Jogando com Alguem", (400, 56))


        # Fim de Jogo
        if(self.velha.fim_jogo):
            vencedor_str: str = self.velha.vencedor.to_str() if(self.velha.vencedor != None) else "Deu Velha!"
            self.__DrawText("Fim de jogo. Vencedor: "+vencedor_str, (16, 414), "red")
            self.__DrawText("Pressione 'R' para jogar novamente", (16, 444), "yellow")

        pygame.display.flip()
        self.clock.tick()
        return
    
    # Método para renderizar o tabuleiro
    def __DrawTabuleiro(self):          # Desenha as casas do tabuleiro
        t = self.tabuleiro
        for r in range(3):
            for c in range(3):
                p = self.velha.tabuleiro[r][c].value
                b: Button = t[r][c]
                self.screen.blit(self.spritesheet.image_at((p*128, 0, 128, 128)), b.pos)
        return
    
    # Método para renderizar textos
    def __DrawText(self, texto: str, pos: tuple, color: pygame.Color = "white"):
        img = self.font.render(texto, True, color)
        self.screen.blit(img, pos)


    # Verifica se algum botão foi pressionado
    def __CheckButtonPressed(self)->Button:
        for r in range(3):
            for c in range(3):
                mouse_pos = pygame.mouse.get_pos()
                b: Button = self.tabuleiro[r][c]

                if(b.rect.collidepoint(mouse_pos)):
                    return b
        
        return None
    
    # Captura qual movimento o jogador escolheu. Ou seja qual posição no tabuleiro ele irá jogar
    def __GetPlayerInput(self)->tuple:
        b = self.__CheckButtonPressed()
        if(b != None):
            jogada: tuple = ( int(b.pos[1]/128), int(b.pos[0]/128) )
            self.velha.Jogada(jogada)
            self.__Draw()
            return jogada
        return None
                
                