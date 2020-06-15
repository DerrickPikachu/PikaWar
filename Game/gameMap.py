from Game.item import items
from Game.player import player
import random


class GameMap:
    def __init__(self):
        self.blocks = [["", "", ""], ["", "", ""]]
        pos = [0, 1, 2, 3, 4, 5]
        random.shuffle(pos)

        for i in range(4):
            row = pos[i] // 3
            col = pos[i] % 3
            self.blocks[row][col] = items[i]

    def moveOn(self, position: list, user: player):
        if self.blocks[position[0]][position[1]] != "":
            pass
            # Give the player item


if __name__ == '__main__':
    gameMap = GameMap()
    print(gameMap.blocks)