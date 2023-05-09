
import sys
from PPlay.sound import Sound
import pygame as pygame
from PPlay.sprite import *
from PPlay.board import Board


def main():
    pygame.init()
    pygame.display.set_caption('Xadrez (1.0.0)')
    icon = pygame.image.load("assets/music/blackQueen.png")
    pygame.display.set_icon(icon)

    # Carrega a imagem da peça
    update_screen = True
    
    # Musica de fundo
    sound = Sound('assets/theme.mp3')
    sound.loop = True
    sound.play()
    
    # Cria o tabuleiro do jogo
    BOARD = Board(pygame)

    # Cria um objeto Clock para limitar a taxa de quadros do jogo
    clock = pygame.time.Clock()
    tempo_de_jogo = 0

    while True:
        # Calcula o tempo decorrido desde a última chamada (em milissegundos)
        dt = clock.tick(60)  # Limita o loop a no máximo 60 frames por segundo

        # Converte para segundos e adiciona ao tempo de jogo total
        tempo_de_jogo += dt / 1000.0
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse
                mouse_pos = pygame.mouse.get_pos()

                # Calculate the row and column of the clicked square
                row = int(mouse_pos[1] // BOARD.TAMANHO_QUADRADO)
                col = int(mouse_pos[0] // BOARD.TAMANHO_QUADRADO)

                if BOARD.origem is None:
                    # Se nenhum quadrado tiver sido selecionado anteriormente, atualiza a posição da origem, so pode ser uma das suas peças
                    if BOARD.tabuleiro[row][col] is not None and BOARD.tabuleiro[row][col].color == BOARD.jogador_da_vez:
                        # A peça tem movimentação?
                        BOARD.set_origem(row, col)
                        update_screen = True
                            
                elif BOARD.destino is None:
                    # Se nenhum quadrado tiver sido selecionado anteriormente, atualiza a posição da origem
                    movimentos = BOARD.movimentos
                    
                    if (row, col) in movimentos:
                        BOARD.destino = (row, col)
                    else:
                        BOARD.limpar_jogada()
                        update_screen = True

                if BOARD.origem is not None and BOARD.destino is not None:
                    # Se nenhum quadrado tiver sido selecionado anteriormente, atualiza a posição da origem
                    BOARD.mover_elemento()
                    Sound("assets/music/move.mp3").play()
                    BOARD.inverter_jogador()
                    
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
        print(f'Tempo de jogo: {tempo_de_jogo} segundos')

if __name__ == '__main__':
    main()
