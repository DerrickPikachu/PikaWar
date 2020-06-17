from Game.moveException import MoveException
import random

class player:
    def __init__(self, name:str, position:list):
        # Player attribute
        self.name = name
        self.blood = 10
        self.power = 4
        self.defense = 2
        self.bull = 0

        # Player position and previous one
        self.previousPos = [0, 0]
        self.position = position

        # Player item
        self.items = set()

        # Player boolean
        self.usedCard = False
        self.ready = False
        self.alive = True

    def getName(self)->str:
        return self.name
    
    def getBlood(self)->int:
        return self.blood

    def getPower(self)->int:
        return self.power

    def getDefense(self)->int:
        return self.defense
    
    def getPosition(self)->list:
        return self.position

    def setBlood(self, level: int):
        self.blood = level

    def setPower(self, level: int):
        self.power = level

    def setDefense(self, level: int):
        self.defense= level

    def setDead(self):
        self.position = [-1, -1]
        self.previousPos = [-1, -1]
        self.alive = False

    def convertPostArr(self):
        mapList = [0, 0, 0, 0, 0, 0]
        if self.position[0] == 0:
            mapList[self.position[1]] = 'style=\"background-color: red;\"'
        else:
            mapList[self.position[1]+3] ='style=\"background-color: red;\"'
        return mapList

    def isSamePos(self, other):
        return self.position[0] == other.position[0] and self.position[1] == other.position[1]

    def move(self, action):
        # Save the previous position
        self.previousPos[0] = self.position[0]
        self.previousPos[1] = self.position[1]

        moveVector = [0, 0]
        if action == 'up':
            moveVector = [-1, 0]
        elif action == 'down':
            moveVector = [1, 0]
        elif action == 'right':
            moveVector = [0, 1]
        elif action == 'left':
            moveVector = [0, -1]

        temPos = [0, 0]
        temPos[0] = moveVector[0] + self.position[0]
        temPos[1] = moveVector[1] + self.position[1]
        self.position = temPos

    def detectMoveError(self, action):
        moveVector = [0, 0]
        if action == 'up':
            moveVector = [-1, 0]
        elif action == 'down':
            moveVector = [1, 0]
        elif action == 'right':
            moveVector = [0, 1]
        elif action == 'left':
            moveVector = [0, -1]

        temPos = [0, 0]
        temPos[0] = moveVector[0] + self.position[0]
        temPos[1] = moveVector[1] + self.position[1]

        if temPos[0] <= 1 and temPos[0] >= 0 and temPos[1] <= 2 and temPos[1] >= 0:
            pass
        else:
            print("raise MoveException")
            raise MoveException("move error!!")

    def moveBack(self):
        self.position[0] = self.previousPos[0]
        self.position[1] = self.previousPos[1]

    # Handle fighting, return loser
    def fightWith(self, other):
        other.blood -= self.power - other.defense
        self.blood -= other.power - self.defense

        # Return loser
        if self.blood < other.blood:
            return self
        elif self.blood > other.blood:
            return other
        else:
            # Randomly choose a user to be a loser
            choose = random.randint(1, 2)
            if choose == 1:
                return self
            else:
                return other


if __name__ == "__main__":
    playerTest = player("test")
    while True:
        string = input("action: ")
        playerTest.move(action=string)
        print(playerTest.position)
