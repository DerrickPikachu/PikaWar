class player:
    def __init__(self, name:str):
        self.name = name
        self.blood = 10
        self.power = 10
        self.defense = 10
        self.position = [0, 0]

    def getName(self)->str:
        return self.name
    
    def getBlood(self)->int:
        return self.blood

    def getPower(self)->int:
        return self.power

    def getDefense(self)->int:
        return self.defense

    def convertPostoArr(self):
        mapList = [0,0,0,0,0,0]
        if self.position[0] == 0:
            mapList[self.position[1]] = 'style=\"background-color: red;\"'
        else:
            mapList[self.position[1]+3] ='style=\"background-color: red;\"'
        return mapList

    def move(self, action):
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
            self.position = temPos
        else:
            # TODO: Raise an exception
            print("move error!!")


if __name__ == "__main__":
    playerTest = player("test")
    while True:
        string = input("action: ")
        playerTest.move(action=string)
        print(playerTest.position)
