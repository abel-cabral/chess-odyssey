
import sys
import pygame as pygame
from PPlay.sprite import *
from PPlay.board import Board


def main():
    pygame.init()
    pygame.display.set_caption('Xadrez (0.1.3)')
    icon = pygame.image.load("assets/blackQueen.png")
    pygame.display.set_icon(icon)

    # Carrega a imagem da peça
    update_screen = True
    
    # Cria o tabuleiro do jogo
    BOARD = Board(pygame)

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
                col = int(mouse_pos[0] // BOARD.TAMANHO_QUADRADO)
                row = int(mouse_pos[1] // BOARD.TAMANHO_QUADRADO)

                if BOARD.origem is None:
                    # Se nenhum quadrado tiver sido selecionado anteriormente, atualiza a posição da origem, so pode ser uma das suas peças
                    if BOARD.tabuleiro[row][col] is not None and BOARD.tabuleiro[row][col].sprite.cor == 0:
                        # A peça tem movimentação?
                        BOARD.origem = (row, col)
                        update_screen = True
                            
                elif BOARD.destino is None:
                    # Se nenhum quadrado tiver sido selecionado anteriormente, atualiza a posição da origem
                    #movimentos = BOARD.tabuleiro[ORIGEM[0]][ORIGEM[1]].movimento((ORIGEM[0], ORIGEM[1]), BOARD.tabuleiro)
                    if (row, col) in BOARD.rotas_movimento():
                        BOARD.destino = (row, col)
                    else:
                        BOARD.limpar_jogada()
                        update_screen = True

                if BOARD.origem is not None and BOARD.destino is not None:
                    # Se nenhum quadrado tiver sido selecionado anteriormente, atualiza a posição da origem
                    BOARD.mover_elemento()
                    BOARD.limpar_jogada()
                    update_screen = True
                        

        # Desenha os quadrados na tela e as peças nas posições iniciais
        BOARD.desenhar_tabuleiro()
        BOARD.desenhar_pecas()
        
                #desenhar_pecas(tabuleiro, linha, coluna, janela, TAMANHO_QUADRADO)
                # desenhar_selecao(janela, tabuleiro, linha, coluna, quadrado_selecionado, TAMANHO_QUADRADO)

        if update_screen:
            pygame.display.update()
            update_screen = False

        # Limita a taxa de quadros do jogo
        clock.tick(60)

if __name__ == '__main__':
    main()
