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
        item = ""

        if self.blocks[position[0]][position[1]] != "":
            itemsMap = {items[0]: 0, items[1]:1, items[2]:2, items[3]:3}
            user.items.add(itemsMap[self.blocks[position[0]][position[1]]])
            item = self.blocks[position[0]][position[1]]
            self.blocks[position[0]][position[1]] = ""

        return item

if __name__ == '__main__':
    gameMap = GameMap()
    print(gameMap.blocks)