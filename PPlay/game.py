from PPlay.board import Board
from PPlay.sound import Sound
import pygame as pygame

class Game:
    SOUND = None
    
    def __init__(self, app_name, icon_path):
        pygame.init()
        pygame.display.set_caption(app_name)
        pygame.display.set_icon(pygame.image.load(icon_path))
        self.janela = pygame.display.set_mode((800, 800))
        self.pygame = pygame
    
    def start(self):
        # Musica de fundo
        sound = Sound('assets/music/theme.mp3')
        sound.loop = True
        sound.play()
        self.SOUND = sound
        
        # Tela e peças
        BOARD = Board()
        
        self.desenha_tela(BOARD)
        
        self.pygame.display.update()
        return BOARD
    
    def end_game(self):
        self.SOUND.stop()

        # Configura a janela
        screen = self.pygame.display.get_surface()  # Obtém a superfície atual

        # Configura a fonte
        font = self.pygame.font.Font(None, 48)  # Escolha o tamanho da fonte que achar melhor

        # Configura a mensagem
        text = font.render('Fim de Jogo! {} venceu!\n'.format("Jogador Preto"), True, (255, 0, 0))  # Texto, antialiasing e cor (RGB)

        # Configura onde o texto será desenhado
        textRect = text.get_rect()
        textRect.center = (screen.get_width() // 2, screen.get_height() // 2)  # Posiciona o texto no centro da tela

        # Desenha o texto
        screen.blit(text, textRect)

        # Atualiza a tela
        self.pygame.display.flip()
        
    def desenha_tela(self, BOARD):
        BOARD.desenhar_tabuleiro(self.pygame, self.janela)
        BOARD.desenhar_pecas(self.pygame, self.janela)