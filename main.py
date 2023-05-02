import pygame.event
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.gameimage import *
from pygame.locals import *

window_size = 600


def piece_path():
    class PiecePath:
        def __init__(self):
            self.pawnB = [Sprite("assets/blackPawn.png") for i in range(8)]
            self.pawnW = [Sprite("assets/whitePawn.png") for i in range(8)]

            self.rookB1 = Sprite("assets/blackRook.png")
            self.rookB2 = Sprite("assets/blackRook.png")

            self.rookW1 = Sprite("assets/whiteRook.png")
            self.rookW2 = Sprite("assets/whiteRook.png")

            self.knightB1 = Sprite("assets/blackKnight.png")
            self.knightB2 = Sprite("assets/blackKnight.png")

            self.knightW1 = Sprite("assets/whiteKnight.png")
            self.knightW2 = Sprite("assets/whiteKnight.png")

            self.bishopB1 = Sprite("assets/blackBishop.png")
            self.bishopB2 = Sprite("assets/blackBishop.png")

            self.bishopW1 = Sprite("assets/whiteBishop.png")
            self.bishopW2 = Sprite("assets/whiteBishop.png")

            self.kingB = Sprite("assets/blackKing.png")
            self.kingW = Sprite("assets/whiteKing.png")

            self.queenB = Sprite("assets/blackQueen.png")
            self.queenW = Sprite("assets/whiteQueen.png")
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
    BRANCO = (255, 255, 255)
    PRETO = (110, 58, 41)
    
    # Movimentacao
    ORIGEM = None
    DESTINO = None

    # Define o tamanho de cada quadrado do tabuleiro
    TAMANHO_QUADRADO = window_size / 8

    # Carrega a imagem da peça

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
        # Desenha os quadrados na tela e as peças nas posições iniciais
        for linha in range(8):
            for coluna in range(8):
                # Calcula a posição do quadrado na tela
                x = coluna * TAMANHO_QUADRADO
                y = linha * TAMANHO_QUADRADO

                # Desenha o quadrado na tela
                cor = BRANCO if (linha + coluna) % 2 == 0 else PRETO
                pygame.draw.rect(janela, cor, (x, y, TAMANHO_QUADRADO, TAMANHO_QUADRADO))

                # Desenha a peça na posição inicial correspondente na matriz
                if tabuleiro[linha] is not None and tabuleiro[linha][coluna] is not None:
                    peca_imagem = pygame.image.load(tabuleiro[linha][coluna].image_file)
                    # Obtém um objeto Rect que representa a imagem da peça e define sua posição central como o centro do quadrado
                    peca_rect = peca_imagem.get_rect()
                    peca_rect.center = (x + TAMANHO_QUADRADO // 2, y + TAMANHO_QUADRADO // 2)

                    # Desenha a imagem da peça na tela
                    janela.blit(peca_imagem, peca_rect)
                    
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

                if tabuleiro[row][col] is not None:
                    ORIGEM = (row, col)
                else:
                    DESTINO = (row, col)      

                if ORIGEM is not None and DESTINO is not None:
                    tabuleiro = mover_elemento(tabuleiro, ORIGEM, DESTINO)
                    # Zera movimentacao
                    ORIGEM = None
                    DESTINO = None
                    
        # Atualiza a tela
        pygame.display.update()

        # Limita a taxa de quadros do jogo
        clock.tick(60)


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
