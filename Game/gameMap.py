from Game.item import items
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


if __name__ == '__main__':
    gameMap = GameMap()
    print(gameMap.blocks)