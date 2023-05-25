import sys
from PPlay.game import Game
from PPlay.ia import IA
from PPlay.sound import Sound
import concurrent.futures

def handle_ai_move(ia, board):
    return ia.mover(board)

def main():
    game = Game('Xadrez (1.0.0)', 'assets/blackQueen.png')
    pygame = game.pygame
    ia = IA(cor='B', profundidade_max=3)
    
    # Cria o tabuleiro do jogo
    BOARD = game.start()
    update_screen = False

    # Cria um objeto Clock para limitar a taxa de quadros do jogo
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    clock = pygame.time.Clock()
    tempo_de_jogo = 0
    
    # Configuração
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
    BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50
    BUTTON_PADDING = 20
    
    # A flag de promoção inicia como False
    promotion = False
    running = True
    
    while True:
        dt = clock.tick(60)  # Limita o loop a no máximo 60 frames por segundo
        tempo_de_jogo += dt / 1000.0
                      
        if (running):
            game.desenha_tela(BOARD)
        
        if update_screen:
            update_screen = False
            pygame.display.update()
            check_matte = BOARD.is_checkmate()
            if check_matte:
                running = False
            
        if (running):
            if BOARD.jogador_da_vez == 'W':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        row = int(mouse_pos[1] // BOARD.TAMANHO_QUADRADO)
                        col = int(mouse_pos[0] // BOARD.TAMANHO_QUADRADO)

                        if BOARD.origem is None:
                            if BOARD.tabuleiro[row][col] is not None and BOARD.tabuleiro[row][col].color == BOARD.jogador_da_vez:
                                BOARD.set_origem(row, col)
                                update_screen = True

                        elif BOARD.destino is None:
                            movimentos = BOARD.movimentos

                            if (row, col) in movimentos:
                                BOARD.destino = (row, col)
                            else:
                                BOARD.limpar_jogada()
                                update_screen = True

                        if BOARD.origem is not None and BOARD.destino is not None:
                            update_screen = True
                            BOARD.mover_elemento()
                            Sound("assets/music/move.mp3").play()
                            BOARD.inverter_jogador()
                            BOARD.limpar_jogada()
            else:
                # Inicia o thread da IA.
                if not ia.ia_playing:
                    ia, BOARD
                    future = executor.submit(handle_ai_move, ia, BOARD)
                    ia.ia_playing = True

                # Verifique se a tarefa da IA terminou
                if future.done():
                    try:
                        # Movimentacao da IA
                        source, destination = future.result()
                        BOARD.origem = source
                        BOARD.destino = destination
                        BOARD.mover_elemento()
                        Sound("assets/music/move.mp3").play()
                        BOARD.inverter_jogador()
                        BOARD.limpar_jogada()
                        ia.ia_playing = False
                        # Inicie uma nova tarefa, se necessário
                        future = executor.submit(handle_ai_move, ia, BOARD)
                        update_screen = True
                    except Exception as e:
                        print("A thread levantou uma exceção:", e)

            # Se a promoção está ativa, desenhe os botões de promoção
            if False:
                mouse_pos = pygame.mouse.get_pos()
                game.desenhar_botoes(BOARD.jogador_da_vez)
                update_screen = True
        else:
            game.end_game()

if __name__ == '__main__':
    main()
