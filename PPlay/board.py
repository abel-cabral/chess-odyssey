from PPlay.chess_type import Peca
from PPlay.sprite import Sprite

class PiecePath:
    def __init__(self):
        self.pawnB = [Peca(Sprite("assets/blackPawn.png", cor=1), 6) for i in range(8)]
        self.pawnW = [Peca(Sprite("assets/whitePawn.png", cor=0), 6) for i in range(8)]
        self.rookB1 = Peca(Sprite("assets/blackRook.png", cor=1), 5)
        self.rookB2 = Peca(Sprite("assets/blackRook.png", cor=1), 5)
        self.rookW1 = Peca(Sprite("assets/whiteRook.png", cor=0), 5)
        self.rookW2 = Peca(Sprite("assets/whiteRook.png", cor=0), 5)
        self.knightB1 = Peca(Sprite("assets/blackKnight.png", cor=1), 4)
        self.knightB2 = Peca(Sprite("assets/blackKnight.png", cor=1), 4)
        self.knightW1 = Peca(Sprite("assets/whiteKnight.png", cor=0), 4)
        self.knightW2 = Peca(Sprite("assets/whiteKnight.png", cor=0), 4)
        self.bishopB1 = Peca(Sprite("assets/blackBishop.png", cor=1), 3)
        self.bishopB2 = Peca(Sprite("assets/blackBishop.png", cor=1), 3)
        self.bishopW1 = Peca(Sprite("assets/whiteBishop.png", cor=0), 3)
        self.bishopW2 = Peca(Sprite("assets/whiteBishop.png", cor=0), 3)
        self.kingB = Peca(Sprite("assets/blackKing.png", cor=1), 1)
        self.kingW = Peca(Sprite("assets/whiteKing.png", cor=0), 1)
        self.queenB = Peca(Sprite("assets/blackQueen.png", cor=1), 2)
        self.queenW = Peca(Sprite("assets/whiteQueen.png", cor=0), 2)

class Board:
    window_size = 600
    # Define o tamanho de cada quadrado do tabuleiro
    TAMANHO_QUADRADO = window_size / 8
    
    def __init__(self, pygame):
        self.pygame = pygame
        self.janela = pygame.display.set_mode((600, 600))
        self.tabuleiro = self.posicionar_pecas()
        self.origem = None
        self.destino = None
    
    # PREPARAR XADREZ PARA INICIO DO JOGO, GRAFICO + POSICOES DAS PEÇAS    
    def desenhar_tabuleiro(self):
        COR1 = (255, 244, 139) # Player 1
        COR2 = (117, 59, 39) # Player 2
        COR3 = (255, 0, 0) # Selecionado
        movimentos = self.rotas_movimento()
        
        # Calcula a posição do quadrado na tela
        for linha in range(8):
            for coluna in range(8):
                x = coluna * self.TAMANHO_QUADRADO
                y = linha * self.TAMANHO_QUADRADO
                
                if (linha, coluna) in movimentos:
                    cor = COR3
                else:
                    cor = COR1 if (linha + coluna) % 2 == 0 else COR2
                # Desenha o quadrado na tela
                self.pygame.draw.rect(self.janela, cor, (x, y, self.TAMANHO_QUADRADO, self.TAMANHO_QUADRADO))
                
    def posicionar_peças(self):
        for linha in range(8):
            for coluna in range(8):
                x = coluna * self.TAMANHO_QUADRADO
                y = linha * self.TAMANHO_QUADRADO
                # Desenha a peça na posição inicial correspondente na matriz
                if self.tabuleiro[linha] is not None and self.tabuleiro[linha][coluna] is not None:
                    peca_imagem = self.pygame.image.load(self.tabuleiro[linha][coluna].sprite.image_file)
                    # Obtém um objeto Rect que representa a imagem da peça e define sua posição central como o centro do quadrado
                    peca_rect = peca_imagem.get_rect()
                    peca_rect.center = (x + self.TAMANHO_QUADRADO // 2, y + self.TAMANHO_QUADRADO // 2)
                    # Desenha a imagem da peça na tela
                    self.janela.blit(peca_imagem, peca_rect)
    
    def posicionar_pecas(self):
        pieces = PiecePath()
        return [
            [pieces.rookB1, pieces.knightB1, pieces.bishopB1, pieces.queenB, pieces.kingB, pieces.bishopB2, pieces.knightB2, pieces.rookB2],
            pieces.pawnB,
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            pieces.pawnW,
            [pieces.rookW1, pieces.knightW1, pieces.bishopW1, pieces.queenW, pieces.kingW, pieces.bishopW2, pieces.knightW2, pieces.rookW2]
        ]
    
    def desenhar_pecas(self):
        for linha in range(8):
            for coluna in range(8):
                x = coluna * self.TAMANHO_QUADRADO
                y = linha * self.TAMANHO_QUADRADO
                # Desenha a peça na posição inicial correspondente na matriz
                if self.tabuleiro[linha] is not None and self.tabuleiro[linha][coluna] is not None:
                    peca_imagem = self.pygame.image.load(self.tabuleiro[linha][coluna].sprite.image_file)
                    # Obtém um objeto Rect que representa a imagem da peça e define sua posição central como o centro do quadrado
                    peca_rect = peca_imagem.get_rect()
                    peca_rect.center = (x + self.TAMANHO_QUADRADO // 2, y + self.TAMANHO_QUADRADO // 2)
                    # Desenha a imagem da peça na tela
                    self.janela.blit(peca_imagem, peca_rect)
    # FIM DA INICIALIZAÇÃO
    
    
    # MOVIMENTACAO
    def rotas_movimento(self):
        movimentos = []
        if self.origem is not None:
            linha = self.origem[0]
            coluna = self.origem[1]
            movimentos = self.tabuleiro[linha][coluna].movimento((linha, coluna), self.tabuleiro)
        return movimentos
    
    def mover_elemento(self):
        # Obter o valor do elemento na posição antiga
        valor = self.tabuleiro[self.origem[0]][self.origem[1]]

        # Definir o valor do elemento na posição antiga como None
        self.tabuleiro[self.origem[0]][self.origem[1]] = None

        # Definir o valor do elemento na nova posição como o valor da posição antiga
        self.tabuleiro[self.destino[0]][self.destino[1]] = valor
    # FIM MOVIMENTACAO
    
    def limpar_jogada(self):
        self.origem = None
        self.destino = None