import torch
import random
import numpy as np
from collections import deque
from snake_game_ia.src.game import Game
from model import Linear_QNet, QTrainer
from helper import plot
from time import sleep

MAX_MEMORY = 100_000
BATCH_SIZE = 1_000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, LR, self.gamma)


    def get_state(self, game):
        cabeca = [game.cobra.x, game.cobra.y]

        esquerda_cabeca = [cabeca[0] - 20, cabeca[1]]
        direita_cabeca = [cabeca[0] + 20, cabeca[1]]
        cima_cabeca = [cabeca[0], cabeca[1] - 20]
        baixo_cabeca = [cabeca[0], cabeca[1] + 20]

        esquerda_direcao = game.x_controle == -20
        direita_direcao = game.x_controle == 20
        cima_direcao = game.y_controle == -20
        baixo_direcao = game.y_controle == 20

        esquerda_comida = game.comida.x < cabeca[0]
        direita_comida = game.comida.x > cabeca[0]
        cima_comida = game.comida.y < cabeca[1]
        baixo_comida = game.comida.y > cabeca[1]

        esquerda_perigo = (
            (esquerda_direcao and game.handler_colisoes(baixo_cabeca)) or
            (direita_direcao and game.handler_colisoes(cima_cabeca)) or
            (cima_direcao and game.handler_colisoes(esquerda_cabeca)) or
            (baixo_direcao and game.handler_colisoes(direita_cabeca))
        )

        reto_perigo = (
            (esquerda_direcao and game.handler_colisoes(esquerda_cabeca)) or
            (direita_direcao and game.handler_colisoes(direita_cabeca)) or
            (cima_direcao and game.handler_colisoes(cima_cabeca)) or
            (baixo_direcao and game.handler_colisoes(baixo_cabeca))
        )

        direita_perigo = (
            (esquerda_direcao and game.handler_colisoes(cima_cabeca)) or
            (direita_direcao and game.handler_colisoes(baixo_cabeca)) or
            (cima_direcao and game.handler_colisoes(direita_cabeca)) or
            (baixo_direcao and game.handler_colisoes(esquerda_cabeca))
        )

        #perigo esquerda, perigo reto, perigo direita,
        #direcao_esquerda, direcao_direita, direcao_cima, direcao_baixo,
        #comida_esquerda, comida_direita, comida_cima, comida_baixo
        state = [
            esquerda_perigo, reto_perigo, direita_perigo,

            esquerda_direcao, direita_direcao, cima_direcao, baixo_direcao,

            esquerda_comida, direita_comida, cima_comida, baixo_comida
        ]
        return np.array(state, dtype=int)

    def remeber(self, state, acao, recompensa, next_state, game_over):
        self.memory.append((state, acao, recompensa, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states, acoes, recompensas, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, acoes, recompensas, next_states, game_overs)

    def train_short_memory(self, state, acao, recompensa, next_state, game_over):
        self.trainer.train_step(state, acao, recompensa, next_state, game_over)

    def get_action(self, state):
        self.epsilon = 200 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 600) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Game(480, 640)
    while True:
        state_old = agent.get_state(game)

        final_move = agent.get_action(state_old)

        recompensa, game_over, pontos = game.play_next_step(final_move)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, final_move, recompensa, state_new, game_over)

        agent.remeber(state_old, final_move, recompensa, state_new, game_over)

        if game_over:
            game.reload_game()
            agent.n_games += 1
            agent.train_long_memory()

            if pontos > record:
                record = pontos
                agent.model.save()


            print('Game', agent.n_games, 'Score', pontos, 'Record:', record)

            plot_scores.append(pontos)
            total_score += pontos
            mean_score = total_score/agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)



if __name__ == '__main__':
    train()