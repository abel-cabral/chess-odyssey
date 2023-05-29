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
        #self.posicionar_peças()
    
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
    # Temos que pegar o board atualizado, se usarmos o do self, estaremos apontando para uma versao diferente
    def rotas_movimento(self):
        movimentos = []
        if self.origem is not None:
            linha, coluna = self.uci_para_matriz(self.origem)
            movimentos = self.tabuleiro_visual[linha][coluna].movimento(self)

        return movimentos

    def mover_elemento(self):
        # Movimenta no tabuleiro lib e atualiza no visual
        self.tabuleiro_lib.push_uci(self.origem + self.destino)
        self.tabuleiro_visual = self.board_to_matrix()
        self.limpar_jogada()
                
    # Preve se o proximo movimento pode gerar Check
    def prever_check(self, atualizar_pecas=True):
        # Obter o valor do elemento na posição antiga
        peca_original = self.tabuleiro_visual[self.origem[0]][self.origem[1]] # Peça Atual
        peca_misteriosa = self.tabuleiro_visual[self.destino[0]][self.destino[1]] # Pode estar com None ou uma Peça Inimiga
    
        # Primeiro move faz a movimentação
        self.tabuleiro_visual[self.origem[0]][self.origem[1]] = None
        self.tabuleiro_visual[self.destino[0]][self.destino[1]] = peca_original
        if atualizar_pecas: # Atualiza na peça sua localizacao
            self.tabuleiro_visual[self.destino[0]][self.destino[1]].update_position(self.destino[0], self.destino[1])
            
        # Segundo verifica se com essa movimentacao houve um check
        check = self.eh_check()
        
        # Terceiro desfaz a movimentacao
        self.tabuleiro_visual[self.origem[0]][self.origem[1]] = peca_original
        self.tabuleiro_visual[self.destino[0]][self.destino[1]] = peca_misteriosa
        if atualizar_pecas: # Atualiza na peça sua localizacao
            self.tabuleiro_visual[self.origem[0]][self.origem[1]].update_position(self.origem[0], self.origem[1])
            
        return check

    def eh_check(self):
        player = self.jogador_da_vez
        king_position = self.achar_posicao_rei()
        # Verifica se alguma peça do outro jogador pode atacar o rei
        for row in range(8):
            for col in range(8):
                piece = self.tabuleiro_visual[row][col]
                if piece is not None and piece.color != player:
                    if isinstance(piece, King):
                        possible_moves = piece.get_possible_moves(self)
                    else:
                        possible_moves = piece.get_possible_moves(self.tabuleiro_visual)
                    if king_position in possible_moves:
                        return True
        return False
    
    def eh_checkmate(self):
        if not self.eh_check():
            return False  # Se o rei não está em xeque, então não é checkmate

        # Salvar os valores salvos
        origem = self.origem
        destino = self.destino
        movimentos = self.movimentos
        
        # Acha o rei
        posicao_rei = self.achar_posicao_rei()
        rei = self.tabuleiro_visual[posicao_rei[0]][posicao_rei[1]]
        origem = self.origem
        jogadas = []
        
        # Remover jogadas que gerariam check
        for movimento in rei.get_possible_moves(self):
            self.origem = (posicao_rei[0], posicao_rei[1])
            self.destino = (movimento[0], movimento[1])
            check = self.prever_check()
            self.limpar_jogada()
            
            if not check:
                jogadas.append(movimento)
            
        # Restaurar valores
        self.origem = origem
        self.destino = destino
        self.movimentos = movimentos
        
        # Verifica se seu movimento é 0, se sim é checkmate
        if not jogadas:
            return True
        return False

    def eh_empate(self):
        # Conta quantas peças tem no jogo, se forem só duas é empate, são dois reis.
        contador = 0
        for linha in self.tabuleiro_visual:
            for elemento in linha:
                if elemento is not None:
                    contador += 1
        if contador == 2:
            return True
        return False

    def achar_posicao_rei(self):
        player = self.jogador_da_vez
        for pecas in self.tabuleiro_visual:
            for peca in pecas:
                if isinstance(peca, King) and peca.color == player:
                    return (peca.linha, peca.coluna)
        return None

    def inverter_jogador(self):
        self.jogador_da_vez = 'W' if self.tabuleiro_lib.turn else 'B'
    
    def limpar_jogada(self):
        self.origem = None
        self.destino = None
        self.movimentos = None
        
    # Mapeam o que acontece na tabela da lib Xadrez para o visual do nosso Xadrez

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


