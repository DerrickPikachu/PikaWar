from Game.gameMap import GameMap
from Game.player import player


class Engine:
    def __init__(self, user1: player, user2: player, user3: player):
        self.gameMap = GameMap()
        self.p1 = user1
        self.p2 = user2
        self.p3 = user3