from PPlay.chess_type import Peca
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.gameimage import *

window_size = 600


def piece_path():
    class PiecePath:
        def __init__(self):
            self.pawnB = [Peca(Sprite("assets/blackPawn.png", cor=1), 6) for i in range(8)]
            self.pawnW = [Peca(Sprite("assets/whitePawn.png"), 6) for i in range(8)]

            self.rookB1 = Peca(Sprite("assets/blackRook.png", cor=1), 5)
            self.rookB2 = Peca(Sprite("assets/blackRook.png", cor=1), 5)

            self.rookW1 = Peca(Sprite("assets/whiteRook.png"), 5)
            self.rookW2 = Peca(Sprite("assets/whiteRook.png"), 5)

            self.knightB1 = Peca(Sprite("assets/blackKnight.png", cor=1), 4)
            self.knightB2 = Peca(Sprite("assets/blackKnight.png", cor=1), 4)

            self.knightW1 = Peca(Sprite("assets/whiteKnight.png"), 4)
            self.knightW2 = Peca(Sprite("assets/whiteKnight.png"), 4)

            self.bishopB1 = Peca(Sprite("assets/blackBishop.png", cor=1), 3)
            self.bishopB2 = Peca(Sprite("assets/blackBishop.png", cor=1), 3)

            self.bishopW1 = Peca(Sprite("assets/whiteBishop.png"), 3)
            self.bishopW2 = Peca(Sprite("assets/whiteBishop.png"), 3)

            self.kingB = Peca(Sprite("assets/blackKing.png", cor=1), 1)
            self.kingW = Peca(Sprite("assets/whiteKing.png"), 1)

            self.queenB = Peca(Sprite("assets/blackQueen.png", cor=1), 2)
            self.queenW = Peca(Sprite("assets/whiteQueen.png"), 2)
    return PiecePath()



def draw_landscape(pieces):
    for x in range(len(pieces)):
        pieces[x].draw()


def main():
    
    pygame.init()

    # Cria a janela do jogo
    janela = pygame.display.set_mode((window_size, window_size))
    #janela.set_title("Xadrez (0.1.1)")

    # Define as cores que serão usadas no jogo
    
    # Movimentacao
    ORIGEM = None
    DESTINO = None
    PLAYER = 1

    # Define o tamanho de cada quadrado do tabuleiro
    TAMANHO_QUADRADO = window_size / 8
    
    # Armazena a posição do quadrado selecionado
    quadrado_selecionado = None

    # Carrega a imagem da peça
    update_screen = True
    has_board = False
    
    # Cria o tabuleiro do jogo
    pieces = piece_path()
    tabuleiro = [
        [pieces.rookW1, pieces.knightW1, pieces.bishopW1, pieces.queenW, pieces.kingW, pieces.bishopW2, pieces.knightW2, pieces.rookW2],
        pieces.pawnW,
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        pieces.pawnB,
        [pieces.rookB1, pieces.knightB1, pieces.bishopB1, pieces.queenB, pieces.kingB, pieces.bishopB2, pieces.knightB2, pieces.rookB2]
    ]

    # Cria um objeto Clock para limitar a taxa de quadros do jogo
    clock = pygame.time.Clock()

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse
                mouse_pos = pygame.mouse.get_pos()

                # Calculate the row and column of the clicked square
                col = int(mouse_pos[0] // TAMANHO_QUADRADO)
                row = int(mouse_pos[1] // TAMANHO_QUADRADO)

                
                if ORIGEM is None:
                    # Se nenhum quadrado tiver sido selecionado anteriormente, atualiza a posição da origem, so pode ser uma das suas peças
                    if tabuleiro[row][col] is not None and tabuleiro[row][col].sprite.cor == PLAYER:
                        ORIGEM = (row, col)
                        quadrado_selecionado = ORIGEM
                elif DESTINO is None:
                    # Se nenhum quadrado tiver sido selecionado anteriormente, atualiza a posição da origem
                    DESTINO = (row, col)
                    
                if ORIGEM is not None and DESTINO is not None:
                    # Se nenhum quadrado tiver sido selecionado anteriormente, atualiza a posição da origem
                    DESTINO = (row, col)
                    if tabuleiro[DESTINO[0]][DESTINO[1]] is None or tabuleiro[ORIGEM[0]][ORIGEM[1]].sprite.cor != tabuleiro[DESTINO[0]][DESTINO[1]].sprite.cor:
                        tabuleiro = mover_elemento(tabuleiro, ORIGEM, DESTINO)
                        update_screen = True
                        # Zera movimentacao
                        ORIGEM = None
                        DESTINO = None
                        quadrado_selecionado = None
        
        # Desenha os quadrados na tela e as peças nas posições iniciais
        for linha in range(8):
            for coluna in range(8):
                desenhar_tabuleiro(janela, linha, coluna, TAMANHO_QUADRADO)
                desenhar_pecas(tabuleiro, linha, coluna, janela, TAMANHO_QUADRADO)
                desenhar_selecao(janela, tabuleiro, linha, coluna, quadrado_selecionado, TAMANHO_QUADRADO)   
                
                    
        if update_screen:        
            pygame.display.update()
            update_screen = False
        
        # Limita a taxa de quadros do jogo
        clock.tick(10)

def desenhar_selecao(janela, tabuleiro, linha, coluna, quadrado_selecionado, TAMANHO_QUADRADO):
    COR = (255, 0, 0, 128)
    # Verifica se o quadrado atual está selecionado e desenha um quadrado vermelho sobre ele
    if tabuleiro[linha][coluna] is not None and (linha, coluna) == quadrado_selecionado:
        movimentos = tabuleiro[linha][coluna].movimento((linha, coluna), tabuleiro)
        for tupla in movimentos:
            pygame.draw.rect(janela, COR, (tupla[1] * TAMANHO_QUADRADO, tupla[0] * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO))     
        pygame.display.update()
                
def desenhar_tabuleiro(janela, linha, coluna, TAMANHO_QUADRADO):
    BRANCO = (255, 255, 255)
    PRETO = (110, 58, 41)
    # Calcula a posição do quadrado na tela
    x = coluna * TAMANHO_QUADRADO
    y = linha * TAMANHO_QUADRADO
    # Desenha o quadrado na tela
    cor = BRANCO if (linha + coluna) % 2 == 0 else PRETO
    pygame.draw.rect(janela, cor, (x, y, TAMANHO_QUADRADO, TAMANHO_QUADRADO))

def desenhar_pecas(tabuleiro, linha, coluna, janela, TAMANHO_QUADRADO):
    x = coluna * TAMANHO_QUADRADO
    y = linha * TAMANHO_QUADRADO
    # Desenha a peça na posição inicial correspondente na matriz
    if tabuleiro[linha] is not None and tabuleiro[linha][coluna] is not None:
        peca_imagem = pygame.image.load(tabuleiro[linha][coluna].sprite.image_file)
        # Obtém um objeto Rect que representa a imagem da peça e define sua posição central como o centro do quadrado
        peca_rect = peca_imagem.get_rect()
        peca_rect.center = (x + TAMANHO_QUADRADO // 2, y + TAMANHO_QUADRADO // 2)
        # Desenha a imagem da peça na tela
        janela.blit(peca_imagem, peca_rect)

def mover_elemento(matriz, pos_antiga, pos_nova):
    # Obter o valor do elemento na posição antiga
    valor = matriz[pos_antiga[0]][pos_antiga[1]]

    # Definir o valor do elemento na posição antiga como None
    matriz[pos_antiga[0]][pos_antiga[1]] = None

    # Definir o valor do elemento na nova posição como o valor da posição antiga
    matriz[pos_nova[0]][pos_nova[1]] = valor

    return matriz


if __name__ == '__main__':
    main()
