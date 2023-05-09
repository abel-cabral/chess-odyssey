
import sys
from PPlay.game import Game
from PPlay.sound import Sound
from PPlay.board import Board


def main():
    game = Game('Xadrez (1.0.0)', 'assets/blackQueen.png')
    pygame = game.pygame
    # Cria o tabuleiro do jogo
    BOARD = game.start()
    update_screen = False

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
                        
        game.desenha_tela(BOARD)
        if update_screen:
            pygame.display.update()
            update_screen = False
            check = BOARD.is_check()
            check_matte = BOARD.is_checkmate()
            if check and check_matte:
                game.end_game()
        #print(f'Tempo de jogo: {tempo_de_jogo} segundos')

if __name__ == '__main__':
    main()
