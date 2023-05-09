from PPlay.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook

class Board:
    window_size = 600
    # Define o tamanho de cada quadrado do tabuleiro
    TAMANHO_QUADRADO = window_size / 8
    
    def __init__(self, pygame):
        self.pygame = pygame
        self.janela = pygame.display.set_mode((600, 600))
        self.tabuleiro = [[None for j in range(8)] for i in range(8)]
        self.jogador_da_vez = "W"
        self.origem = None
        self.destino = None
        self.movimentos = None
        self.posicionar_peças()
    
    def set_origem(self, linha, coluna):
        self.origem = (linha, coluna)
        self.movimentos = self.rotas_movimento()

    
    # PREPARAR XADREZ PARA INICIO DO JOGO, GRAFICO + POSICOES DAS PEÇAS    
    def desenhar_tabuleiro(self):
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
                self.pygame.draw.rect(self.janela, cor, (x, y, self.TAMANHO_QUADRADO, self.TAMANHO_QUADRADO))
                
    def posicionar_peças(self):
        pieces = [
            [Pawn(1, i, Piece.Preta) for i in range(8)],
            [Pawn(6, i, Piece.Branca) for i in range(8)],
            Rook(0, 0, Piece.Preta, "ESQ"),
            Rook(0, 7, Piece.Preta, "DIR"),
            Rook(7, 0, Piece.Branca, "ESQ"),
            Rook(7, 7, Piece.Branca, "DIR"),
            Knight(0, 1, Piece.Preta),
            Knight(0, 6, Piece.Preta),
            Knight(7, 1, Piece.Branca),
            Knight(7, 6, Piece.Branca),
            Bishop(0, 2, Piece.Preta),
            Bishop(0, 5, Piece.Preta),
            Bishop(7, 2, Piece.Branca),
            Bishop(7, 5, Piece.Branca),
            King(7, 4, Piece.Branca),
            King(0, 4, Piece.Preta),
            Queen(7, 3, Piece.Branca),
            Queen(0, 3, Piece.Preta)
        ]

        for piece in pieces:
            if isinstance(piece, list):
                for pawn in piece:
                    if pawn is not None:
                        self.tabuleiro[pawn.linha][pawn.coluna] = pawn
            else:
                self.tabuleiro[piece.linha][piece.coluna] = piece
        self.tabuleiro

    def desenhar_pecas(self):
        for linha in range(8):
            for coluna in range(8):
                x = coluna * self.TAMANHO_QUADRADO
                y = linha * self.TAMANHO_QUADRADO
                # Desenha a peça na posição inicial correspondente na matriz
                if self.tabuleiro[linha] is not None and self.tabuleiro[linha][coluna] is not None:
                    peca_imagem = self.pygame.image.load(self.tabuleiro[linha][coluna].PATH)
                    # Obtém um objeto Rect que representa a imagem da peça e define sua posição central como o centro do quadrado
                    peca_rect = peca_imagem.get_rect()
                    peca_rect.center = (x + self.TAMANHO_QUADRADO // 2, y + self.TAMANHO_QUADRADO // 2)
                    # Desenha a imagem da peça na tela
                    self.janela.blit(peca_imagem, peca_rect)
    # FIM DA INICIALIZAÇÃO
    
    
    # MOVIMENTACAO
    # Temos que pegar o board atualizado, se usarmos o do self, estaremos apontando para uma versao diferente
    def rotas_movimento(self):
        movimentos = []
        if self.origem is not None:
            linha = self.origem[0]
            coluna = self.origem[1]
            movimentos = self.tabuleiro[linha][coluna].movimento(self)
        return movimentos
    
    def mover_elemento(self):
        torres = [(0,0), (0,7), (7,0), (7,7)]
        
        # Obter o valor do elemento na posição antiga
        valor = self.tabuleiro[self.origem[0]][self.origem[1]]
    
        # Definir o valor do elemento na posição antiga como None
        self.tabuleiro[self.origem[0]][self.origem[1]] = None
        
        # Tratamento para o caso de Rook (Roque)
        if isinstance(valor, King):
            try:
                offsets = [1, -2]  # Possíveis deslocamentos para encontrar a torre
                torre = None
                for offset in offsets:
                    try:
                        torre_index = torres.index((self.destino[0], self.destino[1] + offset))
                        linha, coluna = torres[torre_index]
                        torre = self.tabuleiro[linha][coluna]
                        if isinstance(torre, Rook):
                            break  # Encontramos a torre, então podemos sair do loop
                    except ValueError:
                        continue  # Se não encontrarmos a torre, tentamos o próximo deslocamento
                    
                if torre and torre.LADO == "DIR":  # Para a torre à direita
                    new_torre_coluna = self.destino[1] - 1
                else:  # Para a torre à esquerda
                    new_torre_coluna = self.destino[1] + 1
    
                # Move a Torre
                self.tabuleiro[linha][coluna] = None
                self.tabuleiro[self.destino[0]][new_torre_coluna] = torre
                torre.update_position(self.destino[0], new_torre_coluna)
    
            except:
                pass  # Ignoramos qualquer exceção no processo de roque e prosseguimos com o movimento normal
            
        # Definir o valor do elemento na nova posição como o valor da posição antiga
        self.tabuleiro[self.destino[0]][self.destino[1]] = valor
    
        # Atualiza na peça sua localizacao
        self.tabuleiro[self.destino[0]][self.destino[1]].update_position(self.destino[0], self.destino[1])


    def inverter_jogador(self):
        self.jogador_da_vez = "B" if self.jogador_da_vez == "W" else "W"
    
    def limpar_jogada(self):
        self.origem = None
        self.destino = None
        self.movimentos = None