from PPlay.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook
import chess

class Board:
    window_size = 800
    # Define o tamanho de cada quadrado do tabuleiro_visual
    TAMANHO_QUADRADO = window_size / 8
    PROMOVER = [False]
    
    def __init__(self):
        self.tabuleiro_lib = chess.Board()
        self.tabuleiro_visual = self.board_to_matrix()
        self.jogador_da_vez = 'W'
        self.origem = None
        self.destino = None
        self.movimentos = None
    
    def set_origem(self, linha, coluna):
        self.origem = self.matriz_para_uci(linha, coluna)
        self.movimentos = self.rotas_movimento()

    
    # PREPARAR XADREZ PARA INICIO DO JOGO, GRAFICO + POSICOES DAS PEÇAS    
    def desenhar_tabuleiro(self, pygame, janela):
        COR1 = (255, 244, 139) # Player 1
        COR2 = (117, 59, 39) # Player 2
        COR3 = (255, 0, 0) # Selecionado
        
        # Calcula a posição do quadrado na tela
        for linha in range(8):
            for coluna in range(8):
                x = coluna * self.TAMANHO_QUADRADO
                y = linha * self.TAMANHO_QUADRADO
                
                if self.movimentos is not None and (linha, coluna) in self.movimentos:
                    cor = COR3
                else:
                    cor = COR1 if (linha + coluna) % 2 == 0 else COR2
                # Desenha o quadrado na tela
                pygame.draw.rect(janela, cor, (x, y, self.TAMANHO_QUADRADO, self.TAMANHO_QUADRADO))

    def desenhar_pecas(self, pygame, janela):
        for linha in range(8):
            for coluna in range(8):
                x = coluna * self.TAMANHO_QUADRADO
                y = linha * self.TAMANHO_QUADRADO
                # Desenha a peça na posição inicial correspondente na matriz
                if self.tabuleiro_visual[linha] is not None and self.tabuleiro_visual[linha][coluna] is not None:
                    peca_imagem = pygame.image.load(self.tabuleiro_visual[linha][coluna].PATH)
                    # Obtém um objeto Rect que representa a imagem da peça e define sua posição central como o centro do quadrado
                    peca_rect = peca_imagem.get_rect()
                    peca_rect.center = (x + self.TAMANHO_QUADRADO // 2, y + self.TAMANHO_QUADRADO // 2)
                    # Desenha a imagem da peça na tela
                    janela.blit(peca_imagem, peca_rect)
    # FIM DA INICIALIZAÇÃO
    
    # MOVIMENTACAO
    def rotas_movimento(self):
        movimentos = []
        if self.origem is not None:
            linha, coluna = self.uci_para_matriz(self.origem)
            movimentos = self.tabuleiro_visual[linha][coluna].movimento(self)

        return movimentos

    def mover_elemento(self):
        move = chess.Move.from_uci(self.origem + self.destino)
        self.tabuleiro_lib.push(move)
        # Verificar se houve promoção de peça
        if move.to_square // 8 == 0 or move.to_square // 8 == 7:
            self.PROMOVER[0] = True
            self.PROMOVER.append(move)
        else:
            self.tabuleiro_visual = self.board_to_matrix()
        self.limpar_jogada()
        
    def mover_elemento_ia(self, best_move):
        # Movimenta no tabuleiro lib e atualiza no visual
        self.tabuleiro_lib.push(best_move)
        self.tabuleiro_visual = self.board_to_matrix()
        self.inverter_jogador()
        self.limpar_jogada()

    def inverter_jogador(self):
        self.jogador_da_vez = 'W' if self.tabuleiro_lib.turn else 'B'
    
    def limpar_jogada(self):
        self.origem = None
        self.destino = None
        self.movimentos = None
        
    # Mapeam o que acontece na tabela da lib Xadrez para o visual do nosso Xadrez
    def promocao_peao(self):
        pass
    
    def piece_to_fullname(self, piece):
        # Cria um dicionário para mapear os tipos de peças para seus nomes completos
        PIECE_NAME = {
            chess.PAWN: 'Pawn',
            chess.KNIGHT: 'Knight',
            chess.BISHOP: 'Bishop',
            chess.ROOK: 'Rook',
            chess.QUEEN: 'Queen',
            chess.KING: 'King'
        }
        return PIECE_NAME.get(piece.piece_type) if piece else None

    def board_to_matrix(self):
        matrix_visual = [[None for _ in range(8)] for _ in range(8)]
        for rank in range(8):
            for file in range(8):
                square = chess.square(file, rank)
                piece = self.tabuleiro_lib.piece_at(square)
                if piece:
                    color = 'W' if piece.color == chess.WHITE else 'B'
                    # Note a inversão da linha aqui
                    matrix_visual[7 - rank][file] = eval(self.piece_to_fullname(piece))(square, color)
        return matrix_visual

    def matriz_para_uci(self, linha, coluna):
        return chess.square_name(chess.square(coluna, 7 - linha))

    def uci_para_matriz(self, uci):
        square = chess.parse_square(uci)
        linha = 7 - chess.square_rank(square)
        coluna = chess.square_file(square)
        return linha, coluna


