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
    # Give the player item
    def moveOn(self, user: player):
        position = user.getPosition()
        if self.blocks[position[0]][position[1]] != "":
            itemsMap = {"狙擊槍": 0, "醫療箱":1, "步槍":2, "防彈衣":3}
            user.items.add(itemsMap[self.blocks[position[0]][position[1]]])
            self.blocks[position[0]][position[1]] = ""

if __name__ == '__main__':
    gameMap = GameMap()
    print(gameMap.blocks)