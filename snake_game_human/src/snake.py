import pygame

class Cobra:
    def __init__(self, largura_tela, altura_tela):
        self.altura = 20
        self.largura = 20
        self.x = int(largura_tela/2)
        self.y = int(altura_tela/2)
        self.cor = (0, 255, 0)
        self.lista_cabeca = []
        self.lista_cobra = []
        self.tamanho = 5


    def desenhar(self, tela):
        self.cobra = pygame.draw.rect(tela, self.cor, (self.x, self.y, self.largura, self.altura))


    def crescer(self, tela):
        if len(self.lista_cobra) > self.tamanho:
                del self.lista_cobra[0]

        for x, y in self.lista_cobra:
            pygame.draw.rect(tela, (0, 255, 0), (x, y, self.largura, self.altura))


    def colisao_interna(self):
        if self.lista_cobra.count(self.lista_cabeca) > 1:
            return True
        return False
            
    