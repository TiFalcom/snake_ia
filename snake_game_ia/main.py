from snake_game_ia.src.game import Game
import yaml
import os
from time import sleep

config = yaml.safe_load(open(os.path.join('snake_game_human', 'config', 'config.yaml'), 'r'))

game = Game(config['altura'], config['largura'])

for i in [[1, 0, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 0, 1]]:
    sleep(1.5)
    game.play_next_step(i)