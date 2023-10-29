from random import randint
import pygame

class Comida:
    def __init__(self, limites_x, limites_y):
        self.altura = 20
        self.largura = 20
        self.limites_x = limites_x
        self.limites_y = limites_y
        self.cor = (255, 0, 0)
        self.x = randint(self.limites_x[0], self.limites_x[1])
        self.y = randint(self.limites_y[0], self.limites_y[1])

    def desenhar(self, tela):
        self.comida = pygame.draw.rect(tela, self.cor, (self.x, self.y, self.largura, self.altura))

    def colisao_com_cobra(self):
        self.x = randint(self.limites_x[0], self.limites_x[1])
        self.y = randint(self.limites_y[0], self.limites_y[1])


    