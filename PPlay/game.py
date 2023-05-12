from PPlay.board import Board
from PPlay.sound import Sound
import pygame as pygame

from paths import get_asset_path

class Game:
    SOUND = None
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT =800
    
    def __init__(self, app_name, icon_path):
        pygame.init()
        pygame.display.set_caption(app_name)
        pygame.display.set_icon(pygame.image.load(icon_path))
        self.janela = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
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
        
    def desenhar_botoes(self, color):
        BUTTON_WIDTH = BUTTON_HEIGHT = 128
        BUTTON_PADDING = 20
        bishop_image = pygame.image.load(get_asset_path('whiteBishop.png' if color == 'W' else 'blackBishop.png'))
        knight_image = pygame.image.load(get_asset_path('whiteKnight.png' if color == 'W' else 'blackKnight.png'))
        queen_image = pygame.image.load(get_asset_path('whiteQueen.png' if color == 'W' else 'blackQueen.png'))
        rook_image = pygame.image.load(get_asset_path('whiteRook.png' if color == 'W' else 'blackRook.png'))

        # Redimensionar imagens
        image_size = (BUTTON_WIDTH // 2, BUTTON_HEIGHT // 2)  # Ajuste o tamanho de acordo com suas necessidades
        bishop_image = pygame.transform.scale(bishop_image, image_size)
        knight_image = pygame.transform.scale(knight_image, image_size)
        queen_image = pygame.transform.scale(queen_image, image_size)
        rook_image = pygame.transform.scale(rook_image, image_size)

        promotion_buttons = [
            {'rect': pygame.Rect(self.SCREEN_WIDTH // 2 - 2 * (BUTTON_WIDTH + BUTTON_PADDING), self.SCREEN_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT), 'image': bishop_image, 'piece': 'Bishop'},
            {'rect': pygame.Rect(self.SCREEN_WIDTH // 2 - (BUTTON_WIDTH + BUTTON_PADDING), self.SCREEN_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT), 'image': knight_image, 'piece': 'Knight'},
            {'rect': pygame.Rect(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT), 'image': queen_image, 'piece': 'Queen'},
            {'rect': pygame.Rect(self.SCREEN_WIDTH // 2 + (BUTTON_WIDTH + BUTTON_PADDING), self.SCREEN_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT), 'image': rook_image, 'piece': 'Rook'},
        ]

        for button in promotion_buttons:
            pygame.draw.circle(self.janela, (255, 255, 255), button['rect'].center, button['rect'].width // 2)
            image_pos = button['rect'].centerx - image_size[0] // 2, button['rect'].centery - image_size[1] // 2
            self.janela.blit(button['image'], image_pos)