import pygame
from pygame.locals import *
from sys import exit
from snake_game_ia.src.snake import Cobra
from snake_game_ia.src.food import Comida
import numpy as np


class Game:
    def __init__(self, altura_tela, largura_tela):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.pontos = 0
        self.velocidade = 20
        self.x_controle = 0
        self.y_controle = self.velocidade
        self.cor_tela = (255, 255, 255)
        self.iteracao = 0

        pygame.init()
        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        self.fonte = pygame.font.SysFont('yugothicmedium', 40, True, False)
        self.relogio = pygame.time.Clock()
        self.tela = pygame.display.set_mode((largura_tela, altura_tela))
        pygame.display.set_caption('Snake')

        self.reload_game()
        
        
    def _handler_events(self, acao):
        #esquerda, reto, direita
        if np.array_equal(acao, [0, 1, 0]):
            pass
        if np.array_equal(acao, [1, 0, 0]):
            if self.x_controle == self.velocidade:
                self.x_controle = 0
                self.y_controle = -self.velocidade
            elif self.x_controle == - self.velocidade:
                self.x_controle = 0
                self.y_controle = self.velocidade
            elif self.y_controle == self.velocidade:
                self.y_controle = 0
                self.x_controle = self.velocidade
            elif self.y_controle == -self.velocidade:
                self.y_controle = 0
                self.x_controle = -self.velocidade
        if np.array_equal(acao, [0, 0, 1]):
            if self.x_controle == self.velocidade:
                self.x_controle = 0
                self.y_controle = self.velocidade
            elif self.x_controle == -self.velocidade:
                self.x_controle = 0
                self.y_controle = -self.velocidade
            elif self.y_controle == self.velocidade:
                self.y_controle = 0
                self.x_controle = -self.velocidade
            elif self.y_controle == -self.velocidade:
                self.y_controle = 0
                self.x_controle = self.velocidade
        
        self.cobra.x += self.x_controle
        self.cobra.y += self.y_controle
        
    def handler_colisoes(self, pixel=None):
        if pixel == None:
            pixel_x = self.cobra.x
            pixel_y = self.cobra.y
        else:
            pixel_x = pixel[0]
            pixel_y = pixel[1]

        if pixel_y not in range(0, self.altura_tela):
            return True

        if pixel_x not in range(0, self.largura_tela):
            return True
        
        if self.cobra.lista_cobra.count([pixel_x, pixel_y]) > 1:
            return True
        
        return False


    def _handler_colisao_cobra_comida(self):
        if self.cobra.cobra.colliderect(self.comida.comida):
            self.comida.colisao_com_cobra(self.tela)
            self.pontos += 1
            self.cobra.tamanho += 1
            return 10
        return 0

    def reload_game(self):
        self.cobra = Cobra(self.largura_tela, self.altura_tela)
        self.comida = Comida((0, self.largura_tela), (0, self.altura_tela))

        self.cobra.desenhar(self.tela)
        self.comida.desenhar(self.tela)

        self.pontos = 0
        self.iteracao = 0

    def _atualiza_interface(self):
        self.tela.fill(self.cor_tela)
        mensagem = f'Pontos: {self.pontos}'
        texto_formatado = self.fonte.render(mensagem, True, (0, 0, 0))

        self.comida.desenhar(self.tela)

        self.cobra.crescer(self.tela)

        self.tela.blit(texto_formatado, (400, 40))

        pygame.display.flip()


    def play_next_step(self, acao):
        self.iteracao += 1
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        self._handler_events(acao)

        #Isso aqui deveria ser um método de cobra
        lista_cabeca = [self.cobra.x, self.cobra.y]
        self.cobra.lista_cobra.append(lista_cabeca)

        #ponto de parada, pra evitar que fique rodando sem comer
        recompensa = 0
        game_over = False
        if self.handler_colisoes() or self.iteracao > 100*self.cobra.tamanho:
            recompensa = -10
            game_over = True
            return recompensa, game_over, self.pontos

        recompensa = self._handler_colisao_cobra_comida()

        self._atualiza_interface()
        self.relogio.tick(self.velocidade)

        return recompensa, game_over, self.pontos
        