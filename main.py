import pygame.event
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.gameimage import *
from pygame.locals import *

window_size = 600


def piece_path():
    pawnB = []
    for x in range(8):
        pawnB.append(Sprite("assets/blackPawn.png"))
        pawnB[x].set_position(x * (window_size) / 8, window_size / 8)
        pawnB[x].draw()

    pawnW = []
    for x in range(8):
        pawnW.append(Sprite("assets/whitePawn.png"))
        pawnW[x].set_position(x * window_size / 8, 6 * window_size / 8 - 10)
        pawnW[x].draw()

    rookB1 = Sprite("assets/blackRook.png")
    rookB2 = Sprite("assets/blackRook.png")
    rookB1.set_position(10, 5)
    rookB2.set_position(window_size - window_size / 8 - 10, 5)
    rookB2.draw()
    rookB1.draw()

    rookW1 = Sprite("assets/whiteRook.png")
    rookW2 = Sprite("assets/whiteRook.png")
    rookW1.set_position(7, 7 * window_size / 8 - 10)
    rookW2.set_position(7 * window_size / 8 - 10, 7 * window_size / 8 - 10)
    rookW2.draw()
    rookW1.draw()

    knightB1 = Sprite("assets/blackKnight.png")
    knightB2 = Sprite("assets/blackKnight.png")
    knightB1.set_position(5 + window_size / 8, 5)
    knightB2.set_position(window_size - 2 * window_size / 8 - 10, 5)
    knightB1.draw()
    knightB2.draw()

    knightW1 = Sprite("assets/whiteKnight.png")
    knightW2 = Sprite("assets/whiteKnight.png")
    knightW1.set_position(5 + window_size / 8, 7 * window_size / 8 - 10)
    knightW2.set_position(window_size - 2 * window_size / 8 - 10, 7 * window_size / 8 - 10)
    knightW1.draw()
    knightW2.draw()

    bishopB1 = Sprite("assets/blackBishop.png")
    bishopB2 = Sprite("assets/blackBishop.png")
    bishopB1.set_position(3 + 2 * window_size / 8, 5)
    bishopB2.set_position(window_size - 3 * window_size / 8 - 5, 5)
    bishopB1.draw()
    bishopB2.draw()

    bishopW1 = Sprite("assets/whiteBishop.png")
    bishopW2 = Sprite("assets/whiteBishop.png")
    bishopW1.set_position(3 + 2 * window_size / 8, 7 * window_size / 8 - 10)
    bishopW2.set_position(window_size - 3 * window_size / 8 - 5, 7 * window_size / 8 - 10)
    bishopW1.draw()
    bishopW2.draw()

    kingB = Sprite("assets/blackKing.png")
    kingW = Sprite("assets/whiteKing.png")
    kingB.set_position(4 * window_size / 8 - 2, 5)
    kingW.set_position(4 * window_size / 8 - 2, 7 * window_size / 8 - 10)
    kingW.draw()
    kingB.draw()

    queenB = Sprite("assets/blackQueen.png")
    queenW = Sprite("assets/whiteQueen.png")
    queenB.set_position(3 * window_size / 8, 5)
    queenW.set_position(3 * window_size / 8, 7 * window_size / 8 - 10)
    queenB.draw()
    queenW.draw()

    return [pawnB[0], pawnB[1], pawnB[2], pawnB[3], pawnB[4], pawnB[5], pawnB[6], pawnB[7], pawnW[0], pawnW[1],
            pawnW[2], pawnW[3], pawnW[4], pawnW[5], pawnW[6], pawnW[7], kingW, kingB, queenW, queenB, bishopW1,
            bishopW2, bishopB2, bishopB1, knightW1, knightW2, knightB2, knightB1, rookW1, rookW2, rookB1, rookB2]


def draw_landscape(pieces):
    for x in range(len(pieces)):
        pieces[x].draw()


def main():
    janela = Window(window_size, window_size)
    janela.set_title("Xadrez (0.1.1)")
    window = pygame.display.set_mode((window_size, window_size))
    fundo = GameImage("assets/Board1.png")
    fundo.draw()

    pieces = piece_path()

    player_mouse = Window.get_mouse()

    while True:
        fundo.draw()
        draw_landscape(pieces)
        janela.update()
        for x in range(len(pieces)):
            while player_mouse.is_over_object(pieces[x]) and player_mouse.is_button_pressed(1):
                coord = player_mouse.get_position()
                pieces[x].set_position(coord[0] - window_size / 16, coord[1] - window_size / 16)
                janela.update()
                fundo.draw()
                draw_landscape(pieces)
                pieces[x].draw()


if __name__ == '__main__':
    main()
