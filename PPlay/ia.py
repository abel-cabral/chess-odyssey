import time
from copy import deepcopy
from PPlay.piece import King
from PPlay.piece import Queen
from PPlay.piece import Knight
from PPlay.piece import Pawn
from PPlay.piece import Bishop
from PPlay.piece import Rook

PAWN_POSITION_VALUE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

KNIGHT_POSITION_VALUE = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20,   0,   0,   0,   0, -20, -40],
    [-30,   0,  10,  15,  15,  10,   0, -30],
    [-30,   5,  15,  20,  20,  15,   5, -30],
    [-30,   0,  15,  20,  20,  15,   0, -30],
    [-30,   5,  10,  15,  15,  10,   5, -30],
    [-40, -20,   0,   5,   5,   0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

BISHOP_POSITION_VALUE = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10,   0,   0,   0,   0,   0,   0, -10],
    [-10,   0,   5,  10,  10,   5,   0, -10],
    [-10,   5,   5,  10,  10,   5,   5, -10],
    [-10,   0,  10,  10,  10,  10,   0, -10],
    [-10,  10,  10,  10,  10,  10,  10, -10],
    [-10,   5,   0,   0,   0,   0,   5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]

ROOK_POSITION_VALUE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,  0,  0,  5,  5,  0,  0,  0]
]

QUEEN_POSITION_VALUE = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10,   0,   0,  0,  0,   0,   0, -10],
    [-10,   0,   5,  5,  5,   5,   0, -10],
    [-5,   0,   5,  5,  5,   5,   0, -5],
    [0,   0,   5,  5,  5,   5,   0, -5],
    [-10,   5,   5,  5,  5,   5,   0, -10],
    [-10,   0,   5,  0,  0,   0,   0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
]

class IA:
    def __init__(self, cor, profundidade_max=2):
        self.cor = cor
        self.profundidade_max = profundidade_max
        self.ia_playing = False
        self.movimentos_possiveis = {}

    def avaliar_posicao(self, board):
        valor = 0
        for linha in range(len(board.tabuleiro)):
            for coluna in range(len(board.tabuleiro[linha])):
                peca = board.tabuleiro[linha][coluna]    
                if peca is not None:
                    if isinstance(peca, King):
                        valor_posicional = 0
                    elif isinstance(peca, Queen):
                        valor_posicional = QUEEN_POSITION_VALUE[linha][coluna] if isinstance(peca, Queen) else 0
                    elif isinstance(peca, Rook):
                        valor_posicional = ROOK_POSITION_VALUE[linha][coluna] if isinstance(peca, Rook) else 0
                    elif isinstance(peca, Bishop):
                        valor_posicional = BISHOP_POSITION_VALUE[linha][coluna] if isinstance(peca, Bishop) else 0
                    elif isinstance(peca, Knight):
                        valor_posicional = KNIGHT_POSITION_VALUE[linha][coluna] if isinstance(peca, Knight) else 0
                    elif isinstance(peca, Pawn):
                        valor_posicional = PAWN_POSITION_VALUE[linha][coluna] if isinstance(peca, Pawn) else 0
                    if peca.color == self.cor:
                        valor += peca.value + valor_posicional
                    else:
                        valor -= peca.value + valor_posicional
        return valor

    def mover(self, board):
        self.movimentos_possiveis = self.gerar_jogadas(board)  # Pré-calcular todos os movimentos possíveis
        melhor_jogada = None
        profundidade = 1
        tempo_inicial = time.time()
        tempo_maximo = 3
        while True:  # Você precisará adicionar alguma condição de parada aqui, como um limite de tempo
            try:
                _, jogada = self.alfa_beta(board, profundidade, float('-inf'), float('inf'), True)
                melhor_jogada = jogada
                profundidade += 1
                tempo_atual = time.time()
                if tempo_atual - tempo_inicial >= tempo_maximo:
                    break
            except Exception as e:
                break
        return melhor_jogada

    def alfa_beta(self, board, profundidade, alpha, beta, maximizando):
        if profundidade == 0 or not self.movimentos_possiveis:
            return self.avaliar_posicao(board), None

        melhor_jogada = None
        if maximizando:
            melhor_valor = float('-inf')
            for jogada in self.movimentos_possiveis:
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
            for jogada in self.movimentos_possiveis:
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
