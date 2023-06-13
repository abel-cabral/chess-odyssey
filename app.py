import os
from PPlay.game import Game
from PPlay.sound import Sound
from paths import get_asset_path
import chess
import chess.engine
import platform
import shutil

def definir_stockfish():
    sistema_operacional = platform.system()
    destino_arquivo = get_asset_path('stockfish')

    if os.path.exists(destino_arquivo):
        # O arquivo 'stockfish' já existe, não é necessário fazer nada
        return

    if sistema_operacional == 'Windows':
        caminho_arquivo = get_asset_path('win.exe')
        destino_arquivo += '.exe'  # Adiciona a extensão '.exe' no sistema Windows
    elif sistema_operacional == 'Linux':
        caminho_arquivo = get_asset_path('linux')
    else:
        caminho_arquivo = get_asset_path('mac')

    shutil.copy(caminho_arquivo, destino_arquivo)

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
    pause_render_tabuleiro = False
    fim_partida = False
    drag = False
    selected_piece = None
    selected_piece_clone = None
    original_position = None
    peca_imagem = None
    
    while running:
        dt = clock.tick(60)  # Limita o loop a no máximo 60 frames por segundo
        tempo_de_jogo += dt / 1000.0
        if BOARD.tabuleiro_lib.is_checkmate():
            fim_partida = True
            
        if BOARD.PROMOVER[0] and not pause_render_tabuleiro:
                pause_render_tabuleiro = True
                game.desenhar_botoes_de_pecas('W')
                            
        if not fim_partida:
            if BOARD.jogador_da_vez == 'W':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        os._exit(0)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # ... o código anterior ...
                        if not BOARD.PROMOVER[0] and not fim_partida:
                            # Jogadas
                            mouse_pos = pygame.mouse.get_pos()
                            row = int(mouse_pos[1] // BOARD.TAMANHO_QUADRADO)
                            col = int(mouse_pos[0] // BOARD.TAMANHO_QUADRADO)

                            if BOARD.tabuleiro_visual[row][col] is not None and BOARD.tabuleiro_visual[row][col].color == BOARD.jogador_da_vez:
                                BOARD.set_origem(row, col)
                                drag = True
                                selected_piece = BOARD.tabuleiro_visual[row][col]
                                # Supondo que sua peça tem um método clone
                                selected_piece_clone = selected_piece.clone()
                                # Salve a posição original da peça
                                original_position = (row, col)
                                # Faça a peça original invisível
                                selected_piece.VISIBLE = False
                                peca_imagem = pygame.image.load(BOARD.tabuleiro_visual[row][col].PATH)
                    elif event.type == pygame.MOUSEMOTION:
                        # Se uma peça estiver selecionada, mova a cópia com o mouse
                        if drag and selected_piece_clone:
                            # Controle da tela, ela precisa atualizar antes da peça
                            pause_render_tabuleiro = True
                            game.desenha_tela(BOARD)
        
                            # Obtém um objeto Rect que representa a imagem da peça e define sua posição central como o centro do quadrado                    
                            peca_rect = peca_imagem.get_rect()
                            peca_rect.center = (event.pos[0], event.pos[1])
                            game.janela.blit(peca_imagem, peca_rect)
                            pygame.display.update()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        row = int(event.pos[1] // BOARD.TAMANHO_QUADRADO)
                        col = int(event.pos[0] // BOARD.TAMANHO_QUADRADO)
                        movimentos = BOARD.movimentos
                        pause_render_tabuleiro = False
                        
                        # Ao soltar o botão do mouse, pare de arrastar a peça
                        drag = False
                        
                        # Verificar se a peça pode ser movida para a posição de soltura e realizar o movimento
                        if movimentos is not None and (row, col) in movimentos:
                            BOARD.destino = BOARD.matriz_para_uci(row, col)
                        else:
                            BOARD.limpar_jogada()
                            # Restaure a peça original à sua posição original se a peça foi solta em um local inválido
                            selected_piece.x, selected_piece.y = original_position
                            selected_piece.VISIBLE = True

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
            if not pause_render_tabuleiro:
                game.end_game()
                game.desenhar_botoes_de_fim()
                pause_render_tabuleiro = True
                
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
                            pause_render_tabuleiro = False
                            fim_partida = False
        
        if not pause_render_tabuleiro:
            game.desenha_tela(BOARD)

if __name__ == '__main__':
    definir_stockfish()
    main()
