from paths import get_asset_path
import chess

class Piece():
    Branca = "W"
    Preta = "B"

    def __init__(self, square, color):
        self.color = color
        self.square = square
    
    def movimento(self, board):    
        # Obtém todos os movimentos legais
        legal_moves = list(board.tabuleiro_lib.legal_moves)

        # Filtra os movimentos para incluir apenas os da peça no quadrado selecionado
        piece_moves = [move for move in legal_moves if move.from_square == self.square]

        # index 0 é do tabuleiro_lib e o outro é da matriz 8x8
        movimentos = []
        
        for move in piece_moves:
            # movimentos[0].append(move.uci())
            uci = chess.square_name(move.to_square)
            movimentos.append(board.uci_para_matriz(uci))
            
        return movimentos

    def update_position(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self.first_move = False

class Rook(Piece):
    def __init__(self, posicao, color):
        self.PATH = get_asset_path('whiteRook.png' if color == 'W' else 'blackRook.png')
        super(Rook, self).__init__(posicao, color)
    

class Knight(Piece):
   def __init__(self, posicao, color):
        self.PATH = get_asset_path('whiteKnight.png' if color == 'W' else 'blackKnight.png')
        super(Knight, self).__init__(posicao, color)

class Bishop(Piece):
    def __init__(self, posicao, color):
        self.PATH = get_asset_path('whiteBishop.png' if color == 'W' else 'blackBishop.png')
        super(Bishop, self).__init__(posicao, color)

class Queen(Piece):
    def __init__(self, posicao, color):
        self.PATH = get_asset_path('whiteQueen.png' if color == 'W' else 'blackQueen.png')
        super(Queen, self).__init__(posicao, color)

class King(Piece):
    def __init__(self, posicao, color):
        self.PATH = get_asset_path('whiteKing.png' if color == 'W' else 'blackKing.png')
        super(King, self).__init__(posicao, color)

class Pawn(Piece):
    def __init__(self, posicao, color):
        self.PATH = get_asset_path('whitePawn.png' if color == 'W' else 'blackPawn.png')
        super(Pawn, self).__init__(posicao, color)
          
    def promocao_peao(self):
        if self.color == self.Branca and self.linha == 0:
            return True
        elif self.color == self.Preta and self.linha == 7:
            return True
        return False
