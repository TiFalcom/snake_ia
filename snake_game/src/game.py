import pygame
from pygame.locals import *
from sys import exit
from snake import Cobra
from food import Comida

class Game:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.pontos = 0
        self.velocidade = 10
        self.x_controle = 0
        self.y_controle = self.velocidade
        self.cor_tela = (255, 255, 255)

        pygame.init()
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        self.fonte = pygame.font.SysFont('arial', 40, True, True)
        self.relogio = pygame.time.Clock()
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption('Snake')

        self.cobra = Cobra(640, 480)
        self.comida = Comida((0, 600), (0, 440))
        

    def __handler_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_a:
                    if self.x_controle == self.velocidade:
                        pass
                    else:
                        self.x_controle = -self.velocidade
                        self.y_controle = 0
                if event.key == K_d:
                    if self.x_controle == -self.velocidade:
                        pass
                    else:
                        self.x_controle = self.velocidade
                        self.y_controle = 0
                if event.key == K_w:
                    if self.y_controle == self.velocidade:
                        pass
                    else:
                        self.x_controle = 0
                        self.y_controle = -self.velocidade
                if event.key == K_s:
                    if self.y_controle == -self.velocidade:
                        pass
                    else:
                        self.x_controle = 0
                        self.y_controle = self.velocidade

    def __handler_limite_tela(self):
        if self.cobra.y >= self.altura:
                self.cobra.y = 0
        elif self.cobra.y < 0:
            self.cobra.y = self.altura

        if self.cobra.x >= self.largura:
            self.cobra.x = 0
        elif self.cobra.x < 0:
            self.cobra.x = self.largura

    def __handler_colisao_cobra_comida(self):
        if self.cobra.cobra.colliderect(self.comida.comida):
            self.comida.colisao_com_cobra()
            self.pontos += 1
            self.cobra.tamanho += 1

    def __reload_game(self):
        self.pontos = 0
        self.cobra = Cobra(self.largura, self.altura)
        self.comida = Comida((0, 600), (0, 440))
        morreu = False
        return morreu

    def __game_over(self):
        self.tela.fill(self.cor_tela)
        fonte2 = pygame.font.SysFont('arial', 20, True, True)
        mensagem2 = f'Você perdeu! Para reiniciar o jogo pressione a tecla R'
        texto_formatado2 = fonte2.render(mensagem2, True, (0, 0, 0))
        ret_texto = texto_formatado2.get_rect()

        morreu = True
        while morreu:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                if event.type == KEYDOWN:
                    if event.key == K_r:
                        morreu = self.__reload_game()

            ret_texto.center = ((self.largura//2), (self.altura//2))
            self.tela.blit(texto_formatado2, ret_texto)
            pygame.display.update()

    def run(self):
        while True:
            self.relogio.tick(30)
            self.tela.fill(self.cor_tela)

            mensagem = f'Pontos: {self.pontos}'
            texto_formatado = self.fonte.render(mensagem, True, (0, 0, 0))

            self.__handler_events()

            self.cobra.x += self.x_controle
            self.cobra.y += self.y_controle

            self.__handler_limite_tela()
            
            self.cobra.desenhar(self.tela)
            self.comida.desenhar(self.tela)

            self.__handler_colisao_cobra_comida()

            #Isso aqui deveria ser um método de cobra
            self.cobra.lista_cabeca = [self.cobra.x, self.cobra.y]
            self.cobra.lista_cobra.append(self.cobra.lista_cabeca)

            if self.cobra.colisao_interna():
                self.__game_over()

            self.cobra.crescer(self.tela)
            
            self.tela.blit(texto_formatado, (400, 40))

            pygame.display.update()