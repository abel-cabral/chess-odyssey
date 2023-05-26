import sys
from PPlay.board import Board
from PPlay.game import Game
from PPlay.ia import IA
from PPlay.sound import Sound
import concurrent.futures
from PPlay.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook

def handle_ai_move(ia, board):
    return ia.mover(board)

def main():
    game = Game('Xadrez (1.0.0)', 'assets/blackQueen.png')
    pygame = game.pygame
    ia = IA(cor='B')
    
    # Cria o tabuleiro do jogo
    BOARD = game.start()

    # Cria um objeto Clock para limitar a taxa de quadros do jogo
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    clock = pygame.time.Clock()
    tempo_de_jogo = 0
    running = True
    
    botoes_visiveis = False
    game.desenha_tela(BOARD)
    
    while True:
        dt = clock.tick(60)  # Limita o loop a no máximo 60 frames por segundo
        tempo_de_jogo += dt / 1000.0
        checkmate = BOARD.eh_checkmate()
        empate = BOARD.eh_empate()
            
        if BOARD.PROMOVER[0] and not botoes_visiveis:
            botoes_visiveis = True
            game.desenhar_botoes('W')
            
        if not checkmate and not empate:
            if BOARD.jogador_da_vez == 'W':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Botão Pressionado
                        if (BOARD.PROMOVER[0]):
                            nomePeca = game.botao_clicado(event.pos)
                            if nomePeca is not None:
                                nova_peca = eval (nomePeca) (0, 0, BOARD.jogador_da_vez)
                                BOARD.tabuleiro[BOARD.PROMOVER[1]][BOARD.PROMOVER[2]] = nova_peca
                                BOARD.PROMOVER[0] = False
                                BOARD.inverter_jogador()
                                BOARD.limpar_jogada()
                        else:
                            # Jogadas
                            mouse_pos = pygame.mouse.get_pos()
                            row = int(mouse_pos[1] // BOARD.TAMANHO_QUADRADO)
                            col = int(mouse_pos[0] // BOARD.TAMANHO_QUADRADO)

                            if BOARD.origem is None:
                                if BOARD.tabuleiro[row][col] is not None and BOARD.tabuleiro[row][col].color == BOARD.jogador_da_vez:
                                    BOARD.set_origem(row, col)

                            elif BOARD.destino is None:
                                movimentos = BOARD.movimentos

                                if (row, col) in movimentos:
                                    BOARD.destino = (row, col)
                                else:
                                    BOARD.limpar_jogada()

                            if BOARD.origem is not None and BOARD.destino is not None:
                                BOARD.mover_elemento()
                                Sound("assets/music/move.mp3").play()
                                if not BOARD.PROMOVER[0]:
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
                    except Exception as e:
                        print("A thread levantou uma exceção:", e)
        else:
            game.end_game(BOARD.jogador_da_vez)
        
        game.desenha_tela(BOARD)
        

if __name__ == '__main__':
    main()
