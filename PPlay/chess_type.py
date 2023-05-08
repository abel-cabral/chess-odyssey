'''
TIPOS:
    1 - Rei
    2 - Rainha
    3 - Bispo
    4 - Cavalo
    5 - Torre
    6 - Peao
'''

class Peca():
    def __init__(self, sprite, tipo):
        self.sprite = sprite
        self.tipo = tipo
        self.primeiro_movimento = True
    
    def movimento(self, posicao, tabuleiro):
        match self.tipo:
            case 1:
                return self.movimento_rei(posicao, tabuleiro)
            case 2:
                return self.movimento_rainha(posicao, tabuleiro)
            case 3:
                return self.movimento_bispo(posicao, tabuleiro)
            case 4:
                return self.movimento_cavalo(posicao, tabuleiro)
            case 5:
                return self.movimento_torre(posicao, tabuleiro)
            case 6:
                return self.movimento_peao(posicao, tabuleiro)
    
    def mover_elemento(matriz, pos_antiga, pos_nova):
        # Obter o valor do elemento na posição antiga
        valor = matriz[pos_antiga[0]][pos_antiga[1]]

        # Definir o valor do elemento na posição antiga como None
        matriz[pos_antiga[0]][pos_antiga[1]] = None

        # Definir o valor do elemento na nova posição como o valor da posição antiga
        matriz[pos_nova[0]][pos_nova[1]] = valor

        return matriz
    
    def movimento_torre(self, posicao_torre, tabuleiro):
        posicoes_possiveis = []

        # Verifica as posições possíveis na horizontal (mesma linha)
        for coluna in range(posicao_torre[1] - 1, -1, -1):
            if tabuleiro[posicao_torre[0]][coluna] is None:
                posicoes_possiveis.append((posicao_torre[0], coluna))
            elif tabuleiro[posicao_torre[0]][coluna].sprite.cor != self.sprite.cor:
                posicoes_possiveis.append((posicao_torre[0], coluna))
                break
            else:
                break

        for coluna in range(posicao_torre[1] + 1, len(tabuleiro[0])):
            if tabuleiro[posicao_torre[0]][coluna] is None:
                posicoes_possiveis.append((posicao_torre[0], coluna))
            elif tabuleiro[posicao_torre[0]][coluna].sprite.cor != self.sprite.cor:
                posicoes_possiveis.append((posicao_torre[0], coluna))
                break
            else:
                break

        # Verifica as posições possíveis na vertical (mesma coluna)
        for linha in range(posicao_torre[0] - 1, -1, -1):
            if tabuleiro[linha][posicao_torre[1]] is None:
                posicoes_possiveis.append((linha, posicao_torre[1]))
            elif tabuleiro[linha][posicao_torre[1]].sprite.cor != self.sprite.cor:
                posicoes_possiveis.append((linha, posicao_torre[1]))
                break
            else:
                break

        for linha in range(posicao_torre[0] + 1, len(tabuleiro)):
            if tabuleiro[linha][posicao_torre[1]] is None:
                posicoes_possiveis.append((linha, posicao_torre[1]))
            elif tabuleiro[linha][posicao_torre[1]].sprite.cor != self.sprite.cor:
                posicoes_possiveis.append((linha, posicao_torre[1]))
                break
            else:
                break

        return posicoes_possiveis

    def movimento_cavalo(self, posicao_cavalo, tabuleiro):
        posicoes_possiveis = []

        # Movimentos possíveis para o cavalo (em relação à sua posição)
        movimentos = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        # Verifica as posições possíveis para cada um dos movimentos
        for movimento in movimentos:
            nova_coluna = posicao_cavalo[1] + movimento[0]
            nova_linha = posicao_cavalo[0] + movimento[1]

            # Verifica se a posição é válida e se não há uma peça da mesma cor na posição
            if (0 <= nova_linha < 8 and 0 <= nova_coluna < 8 and
                    (tabuleiro[nova_linha][nova_coluna] is None or
                     tabuleiro[nova_linha][nova_coluna].sprite.cor != self.sprite.cor)):
                posicoes_possiveis.append((nova_linha, nova_coluna))

        return posicoes_possiveis

    def movimento_peao(self, posicao_peao, tabuleiro):
        posicoes_possiveis = []

        # Define o sentido do movimento do peão (de acordo com a sua cor)
        sentido = 1 if self.sprite.cor == "branca" else -1

        # Verifica o movimento de avanço
        nova_linha = posicao_peao[0] + sentido
        if nova_linha >= 0 and nova_linha < 8 and tabuleiro[nova_linha][posicao_peao[1]] is None:
            posicoes_possiveis.append((nova_linha, posicao_peao[1]))

            # Verifica o movimento de avanço duplo (apenas se o peão ainda não se moveu)
            if (self.sprite.cor == "branca" and posicao_peao[0] == 6) or (self.sprite.cor == "preta" and posicao_peao[0] == 1):
                nova_linha = posicao_peao[0] + sentido * 2
                if tabuleiro[nova_linha][posicao_peao[1]] is None:
                    posicoes_possiveis.append((nova_linha, posicao_peao[1]))

        # Verifica os movimentos de captura diagonal
        for coluna in range(posicao_peao[1] - 1, posicao_peao[1] + 2):
            if coluna < 0 or coluna >= 8 or coluna == posicao_peao[1]:
                continue

            nova_linha = posicao_peao[0] + sentido
            if nova_linha >= 0 and nova_linha < 8:
                peca = tabuleiro[nova_linha][coluna]
                if peca is not None and peca.sprite.cor != self.sprite.cor:
                    posicoes_possiveis.append((nova_linha, coluna))

        return posicoes_possiveis
    
    def movimento_bispo(self, posicao_bispo, tabuleiro):
        posicoes_possiveis = []

        # Verifica as posições possíveis na diagonal superior direita
        for i in range(1, 8):
            linha = posicao_bispo[0] - i
            coluna = posicao_bispo[1] + i
            if linha < 0 or coluna > 7:
                break
            if tabuleiro[linha][coluna] is None:
                posicoes_possiveis.append((linha, coluna))
            elif tabuleiro[linha][coluna].sprite.cor != self.sprite.cor:
                posicoes_possiveis.append((linha, coluna))
                break
            else:
                break

        # Verifica as posições possíveis na diagonal inferior direita
        for i in range(1, 8):
            linha = posicao_bispo[0] + i
            coluna = posicao_bispo[1] + i
            if linha > 7 or coluna > 7:
                break
            if tabuleiro[linha][coluna] is None:
                posicoes_possiveis.append((linha, coluna))
            elif tabuleiro[linha][coluna].sprite.cor != self.sprite.cor:
                posicoes_possiveis.append((linha, coluna))
                break
            else:
                break

        # Verifica as posições possíveis na diagonal inferior esquerda
        for i in range(1, 8):
            linha = posicao_bispo[0] + i
            coluna = posicao_bispo[1] - i
            if linha > 7 or coluna < 0:
                break
            if tabuleiro[linha][coluna] is None:
                posicoes_possiveis.append((linha, coluna))
            elif tabuleiro[linha][coluna].sprite.cor != self.sprite.cor:
                posicoes_possiveis.append((linha, coluna))
                break
            else:
                break

        # Verifica as posições possíveis na diagonal superior esquerda
        for i in range(1, 8):
            linha = posicao_bispo[0] - i
            coluna = posicao_bispo[1] - i
            if linha < 0 or coluna < 0:
                break
            if tabuleiro[linha][coluna] is None:
                posicoes_possiveis.append((linha, coluna))
            elif tabuleiro[linha][coluna].sprite.cor != self.sprite.cor:
                posicoes_possiveis.append((linha, coluna))
                break
            else:
                break

        return posicoes_possiveis

    def movimento_rainha(self, tabuleiro):
        posicoes_possiveis = []

        # Verifica as posições possíveis na horizontal (mesma linha)
        for coluna in range(8):
            if coluna != self.coluna:
                if tabuleiro[self.linha][coluna] is None:
                    posicoes_possiveis.append((self.linha, coluna))
                elif tabuleiro[self.linha][coluna].sprite.cor != self.sprite.cor:
                    posicoes_possiveis.append((self.linha, coluna))
                    break
                else:
                    break

        # Verifica as posições possíveis na vertical (mesma coluna)
        for linha in range(8):
            if linha != self.linha:
                if tabuleiro[linha][self.coluna] is None:
                    posicoes_possiveis.append((linha, self.coluna))
                elif tabuleiro[linha][self.coluna].sprite.cor != self.sprite.cor:
                    posicoes_possiveis.append((linha, self.coluna))
                    break
                else:
                    break

        # Verifica as posições possíveis na diagonal
        for i, j in zip(range(self.linha-1, -1, -1), range(self.coluna-1, -1, -1)):
            if i < 0 or j < 0:
                break
            
            if tabuleiro[i][j] is None:
                posicoes_possiveis.append((i, j))
            elif tabuleiro[i][j].sprite.cor != self.sprite.cor:
                posicoes_possiveis.append((i, j))
                break
            else:
                break
            
        for i, j in zip(range(self.linha+1, 8), range(self.coluna+1, 8)):
            if i > 7 or j > 7:
                break
            
            if tabuleiro[i][j] is None:
                posicoes_possiveis.append((i, j))
            elif tabuleiro[i][j].sprite.cor != self.sprite.cor:
                posicoes_possiveis.append((i, j))
                break
            else:
                break
            
        for i, j in zip(range(self.linha+1, 8), range(self.coluna-1, -1, -1)):
            if i > 7 or j < 0:
                break
            
            if tabuleiro[i][j] is None:
                posicoes_possiveis.append((i, j))
            elif tabuleiro[i][j].sprite.cor != self.sprite.cor:
                posicoes_possiveis.append((i, j))
                break
            else:
                break
            
        for i, j in zip(range(self.linha-1, -1, -1), range(self.coluna+1, 8)):
            if i < 0 or j > 7:
                break
            
            if tabuleiro[i][j] is None:
                posicoes_possiveis.append((i, j))
            elif tabuleiro[i][j].sprite.cor != self.sprite.cor:
                posicoes_possiveis.append((i, j))
                break
            else:
                break
            
        return posicoes_possiveis

    def movimento_rei(self, posicao_rei, tabuleiro):
        posicoes_possiveis = []

        # Movimentos possíveis do rei (8 posições ao redor)
        movimentos = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for movimento in movimentos:
            linha = posicao_rei[0] + movimento[0]
            coluna = posicao_rei[1] + movimento[1]

            # Verifica se a posição está dentro do tabuleiro
            if 0 <= linha < 8 and 0 <= coluna < 8:
                # Verifica se a posição está vazia ou ocupada por uma peça inimiga
                if tabuleiro[linha][coluna] is None or tabuleiro[linha][coluna].sprite.cor != self.sprite.cor:
                    posicoes_possiveis.append((linha, coluna))
        return posicoes_possiveis
