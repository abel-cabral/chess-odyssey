# coding= utf-8

# Modules
"""Sprite é uma animação que pode ser movida por input, é o "ator" do jogo"""
class Sprite():
    def __init__(self, image_file, cor):
        self.image_file = image_file
        self.cor = cor
