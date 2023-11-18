from snake_game_human.src.game import Game
import yaml
import os

config = yaml.safe_load(open(os.path.join('snake_game_human', 'config', 'config.yaml'), 'r'))

game = Game(config['altura'], config['largura'])

game.run()