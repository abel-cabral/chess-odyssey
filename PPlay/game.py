from PPlay.board import Board
from PPlay.sound import Sound
import pygame as pygame

from PPlay.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from paths import get_asset_path

class Game:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    BOTOES = None
    
    def __init__(self, app_name, icon_path):
        pygame.init()
        pygame.display.set_caption(app_name)
        pygame.display.set_icon(pygame.image.load(icon_path))
        self.janela = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.pygame = pygame
    
    def start(self):
        # Musica de fundo
        self.sound = Sound('assets/music/theme.mp3')
        self.sound.loop = True
        self.sound.play()
        
        # Tela e peças
        board = Board()
        
        self.desenha_tela(board)
        return board
    
    def end_game(self, jogador):
        # Encerra a música de fundo
        self.sound.stop()
        
        # Configura a janela
        screen = self.pygame.display.get_surface()  # Obtém a superfície atual

        # Configura a fonte
        font = self.pygame.font.Font(None, 45)  # Escolha o tamanho da fonte que achar melhor

        # Configura a mensagem
        text = font.render('Fim de Jogo! Você {} :{}'.format('venceu' if jogador == 'W' else 'perdeu', jogador), True, (255, 0, 0))  # Texto, antialiasing e cor (RGB)

        # Configura onde o texto será desenhado
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))  # Posiciona o texto no centro da tela

        # Desenha o texto
        screen.blit(text, text_rect)

        # Atualiza a tela
        self.pygame.display.update()
        
    def desenha_tela(self, board):
        if not board.PROMOVER[0]:
            board.desenhar_tabuleiro(self.pygame, self.janela)
            board.desenhar_pecas(self.pygame, self.janela)
            self.pygame.display.update()
            
        
    def desenhar_botoes_de_pecas(self, color):
        BUTTON_WIDTH = BUTTON_HEIGHT = 96
        BUTTON_PADDING = 24
        
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
            
        self.BOTOES = promotion_buttons
        self.pygame.display.update()
        
    def desenhar_botoes_de_fim(self):
        BUTTON_WIDTH = BUTTON_HEIGHT = 96
        BUTTON_PADDING = 24
        

        # Calcula a posição horizontal central dos botões
        total_width = 2 * (BUTTON_WIDTH + BUTTON_PADDING)
        start_x = self.SCREEN_WIDTH // 2 - total_width // 2

        # Calcula a posição vertical central dos botões com base no tamanho do tabuleiro
        board_size = self.SCREEN_WIDTH if self.SCREEN_WIDTH < self.SCREEN_HEIGHT else self.SCREEN_HEIGHT
        start_y = board_size // 2 - BUTTON_HEIGHT // 2
        button_exit = board_size // 2
        button_restart = board_size // 2

        end_buttons = [
            {'rect': pygame.Rect(start_y, start_y, BUTTON_WIDTH, BUTTON_HEIGHT), 'text': 'Reiniciar'},
            {'rect': pygame.Rect(button_exit + BUTTON_WIDTH, button_exit, BUTTON_WIDTH, BUTTON_HEIGHT), 'text': 'Sair'}
        ]
        
        for button in end_buttons:
            pygame.draw.circle(self.janela, (255, 255, 255), button['rect'].center, button['rect'].width // 2)
            font = pygame.font.Font(None, 24)  # Escolha o tamanho e a fonte do texto
            text = font.render(button['text'], True, (0, 0, 0))  # Crie uma superfície de texto com o texto desejado e a cor preta
            text_rect = text.get_rect(center=button['rect'].center)  # Posicione o texto no centro do botão
            self.janela.blit(text, text_rect)
        
        self.BOTOES = end_buttons
        self.pygame.display.update()
    
    # Descobre qual botão foi clicado e retorna o nome da peça
    def peca_selecionada(self, pos):
        if self.BOTOES:
            for botao in self.BOTOES:
                if botao['rect'].collidepoint(pos[0], pos[1]):
                    return botao
