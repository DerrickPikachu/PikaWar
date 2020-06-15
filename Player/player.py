class player:
    def __init__(self, name:str):
        self.name = name
        self.blood = 10
        self.power = 10
        self.defense  = 10
    def getName(self)->str:
        return self.name
    
    def getBlood(self)->int:
        return self.blood

    def getPower(self)->int:
        return self.power

    def getDefense(self)->int:
        return self.defense

