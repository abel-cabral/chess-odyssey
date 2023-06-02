import os
from PPlay.game import Game
from PPlay.sound import Sound
from paths import get_asset_path
import chess
import chess.engine

def main():
    game = Game('Xadrez 2.0.0', get_asset_path('chess.ico'))
    engine = chess.engine.SimpleEngine.popen_uci(get_asset_path('stockfish'))
    pygame = game.pygame
    
    # Cria o tabuleiro_visual do jogo
    BOARD = game.start()
    BOARD.tabuleiro_visual = BOARD.board_to_matrix()
    move_sound = Sound(get_asset_path('music/move.ogg'), pygame)
    game.desenha_tela(BOARD)
    
    clock = pygame.time.Clock()
    tempo_de_jogo = 0
    running = True
    botoes_visiveis = False
    fim_partida = False
    
    while running:
        dt = clock.tick(60)  # Limita o loop a no máximo 60 frames por segundo
        tempo_de_jogo += dt / 1000.0
        if BOARD.tabuleiro_lib.is_checkmate():
            fim_partida = True
            
        if BOARD.PROMOVER[0] and not botoes_visiveis:
                botoes_visiveis = True
                game.desenhar_botoes_de_pecas('W')
                    
        if not fim_partida:
            if BOARD.jogador_da_vez == 'W':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        os._exit(0)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Botão Pressionado
                        if (BOARD.PROMOVER[0]):
                            btn = game.peca_selecionada(event.pos)
                            nome_peca = btn['piece']
                            if nome_peca is not None:
                                piece_mapping = {'QUEEN': chess.QUEEN, 'ROOK': chess.ROOK, 'BISHOP': chess.BISHOP, 'KNIGHT': chess.KNIGHT}
                                botoes_visiveis = False
                                
                                move = BOARD.PROMOVER[1]
                                cor = chess.WHITE if BOARD.jogador_da_vez == 'W' else chess.BLACK
                                BOARD.tabuleiro_lib.set_piece_at(move.to_square, chess.Piece(piece_mapping[nome_peca], cor))                                
                                BOARD.tabuleiro_visual = BOARD.board_to_matrix()

                                BOARD.PROMOVER[0] = False
                                BOARD.inverter_jogador()
                                BOARD.limpar_jogada()
                        else:
                            # Jogadas
                            mouse_pos = pygame.mouse.get_pos()
                            row = int(mouse_pos[1] // BOARD.TAMANHO_QUADRADO)
                            col = int(mouse_pos[0] // BOARD.TAMANHO_QUADRADO)

                            if BOARD.origem is None:
                                if BOARD.tabuleiro_visual[row][col] is not None and BOARD.tabuleiro_visual[row][col].color == BOARD.jogador_da_vez:
                                    BOARD.set_origem(row, col)

                            elif BOARD.destino is None:
                                movimentos = BOARD.movimentos

                                if (row, col) in movimentos:
                                    BOARD.destino = BOARD.matriz_para_uci(row, col)
                                else:
                                    BOARD.limpar_jogada()

                            if BOARD.origem is not None and BOARD.destino is not None:
                                BOARD.mover_elemento()
                                move_sound.play_som()
                                if not BOARD.PROMOVER[0]:
                                    BOARD.inverter_jogador()     
            else:
                # SISTEMAS MAC
                #fim_partida = True
                result = engine.play(BOARD.tabuleiro_lib, chess.engine.Limit(time=2.0))
                best_move = result.move
                BOARD.mover_elemento_ia(best_move)
                move_sound.play_som()
        else:
            if not botoes_visiveis:
                game.end_game()
                game.desenhar_botoes_de_fim()
                botoes_visiveis = True
                
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        os._exit(0)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        btn = game.peca_selecionada(event.pos)
                        if btn is not None and btn['text'] == 'Sair':
                            pygame.quit()
                            os._exit(0)
                        elif btn is not None and btn['text'] == 'Reiniciar':
                            BOARD = game.start()
                            botoes_visiveis = False
                            fim_partida = False
        
        if not botoes_visiveis:
            game.desenha_tela(BOARD)
        

if __name__ == '__main__':
    main()
