from Game.gameMap import GameMap
from Game.player import player
from Game.event import MoveEvent, ItemEvent, SkillEvent, FightEvent, GetItemEvent
from Game.moveException import MoveException
import heapq


class Engine:
    MAX_PLAYER = 3

    def __init__(self):
        self.gameMap = GameMap()
        self.users = []
        self.eventList = []

    def addPlayer(self, user: player):
        self.users.append(user)

    def __choosePlayer(self, username: str):
        for user in self.users:
            if user.getName() == username:
                return user

    # Create move event
    def moveAction(self, username: str, action: str):
        tem = self.__choosePlayer(username=username)
        try:
            tem.detectMoveError(action)
            print("stop")
            event = MoveEvent(user=tem, action=action)
            heapq.heappush(self.eventList, event)
        except MoveException:
            print("action error")
            raise MoveException("move error 2!")

        

    # Create item event
    def chooseItem(self, username: str, item: str):
        tem = self.__choosePlayer(username=username)
        event = ItemEvent(tem, item)
        heapq.heappush(self.eventList, event)

    # Create skill event
    def useSkill(self, username: str):
        tem = self.__choosePlayer(username=username)
        event = SkillEvent(tem)
        heapq.heappush(self.eventList, event)

    # Create fight event
    def __generateFight(self, user1: player, user2: player, user3: player = None):
        if user3 is not None:
            event = FightEvent(user1, user2, user3)
            heapq.heappush(self.eventList, event)
        else:
            event = FightEvent(user1, user2)
            heapq.heappush(self.eventList, event)

    # Create get item event
    def __getItemOnMap(self, username: str):
        user = self.__choosePlayer(username)
        event = GetItemEvent(user)
        heapq.heappush(self.eventList, event)

    def run(self):
        # Is used to check whether the three player have moved
        moveCount = 0

        while len(self.eventList) != 0:
            event = heapq.heappop(self.eventList)
            if str(type(event)) == "<class 'Game.event.FightEvent'>":
                winner = event.eventHandle()
                print("winner " + winner)
                self.__getItemOnMap(winner)
            else:
                event.eventHandle()

            if str(type(event)) == "<class 'Game.event.MoveEvent'>":
                moveCount += 1

                # Generate fight event
                if moveCount == Engine.MAX_PLAYER:
                    moveCount = 0
                    # Check if three of them are at the same position
                    if self.users[0].isSamePos(self.users[1]) and self.users[0].isSamePos(self.users[2]):
                        self.__generateFight(self.users[0], self.users[1], self.users[2])
                    else:
                        # Here won't have the situation that we get three user in the same position
                        # We at most have two of them in the same position
                        for i in range(2):
                            for j in range(i + 1, 3):
                                if self.users[i].isSamePos(self.users[j]):
                                    self.__generateFight(self.users[i], self.users[j])



