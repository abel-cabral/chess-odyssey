from PPlay.window import *
from PPlay.gameimage import *
def main():
    janela = Window(400, 400)
    janela.set_title("Jogo")
    fundo = GameImage("assets/Board1.png")
    while(True):
        fundo.draw()
        janela.update()

if __name__ == '__main__':
    main()

