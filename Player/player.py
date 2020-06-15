class player:
    def __init__(self, name:str):
        self.name = name
        self.blood = 10
        self.power = 10
        self.defense  = 10
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


