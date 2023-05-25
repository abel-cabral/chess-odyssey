from copy import deepcopy
from PPlay.board import Board

from PPlay.piece import King

class IA:
    def __init__(self, cor, profundidade_max=2):
        self.cor = cor
        self.profundidade_max = profundidade_max
        self.ia_playing = False

    def avaliar_posicao(self, board):
        # Função de avaliação simples, que soma os valores das peças do tabuleiro.
        # No entanto, é possível implementar uma função mais sofisticada para 
        # melhorar o desempenho da IA.
        valor = 0
        for linha in board.tabuleiro:
            for peca in linha:
                if peca is not None:
                    if peca.color == self.cor:
                        valor += peca.value
                    else:
                        valor -= peca.value
        return valor

    def mover(self, board):
        _, jogada = self.alfa_beta(board, self.profundidade_max, float('-inf'), float('inf'), True)
        return jogada

    def alfa_beta(self, board, profundidade, alpha, beta, maximizando):
        if profundidade == 0:
            return self.avaliar_posicao(board), None

        melhor_jogada = None
        if maximizando:
            melhor_valor = float('-inf')
            for jogada in self.gerar_jogadas(board):
                novo_board = deepcopy(board)
                novo_board.origem = jogada[0]
                novo_board.destino = jogada[1]
                novo_board.mover_elemento(False)
                valor = self.alfa_beta(novo_board, profundidade - 1, alpha, beta, False)[0]
                if valor > melhor_valor:
                    melhor_valor = valor
                    melhor_jogada = jogada
                alpha = max(alpha, melhor_valor)
                if beta <= alpha:
                    break
            return melhor_valor, melhor_jogada
        else:
            melhor_valor = float('inf')
            for jogada in self.gerar_jogadas(board):
                novo_board = deepcopy(board)
                novo_board.origem = jogada[0]
                novo_board.destino = jogada[1]
                novo_board.mover_elemento(False)
                valor = self.alfa_beta(novo_board, profundidade - 1, alpha, beta, True)[0]
                if valor < melhor_valor:
                    melhor_valor = valor
                    melhor_jogada = jogada
                beta = min(beta, melhor_valor)
                if beta <= alpha:
                    break
            return melhor_valor, melhor_jogada

    def gerar_jogadas(self, board):
        jogadas = []
        for linha in range(len(board.tabuleiro)):
            for coluna in range(len(board.tabuleiro[linha])):
                peca = board.tabuleiro[linha][coluna]
                if peca is not None and peca.color == self.cor:
                    if isinstance(peca, King):
                        movimentos = peca.get_possible_moves(board)
                    else:
                        movimentos = peca.get_possible_moves(board.tabuleiro)
                        
                    # REMOVE JOGADAS QUE DEIXARIAM O REI EM CHECK
                    for movimento in movimentos:
                        board.origem = (linha, coluna)
                        board.destino = (movimento[0], movimento[1])
                        check = board.prever_check()
                        board.limpar_jogada()
                        
                        if not check:
                            jogadas.append(((linha, coluna), movimento))
        return jogadas
