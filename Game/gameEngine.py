from Game.gameMap import GameMap
from Game.player import player
from Game.event import MoveEvent, ItemEvent, SkillEvent, FightEvent, GetItemEvent
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
        event = MoveEvent(user=tem, action=action)
        heapq.heappush(self.eventList, event)

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
    def __generateFight(self, username1: str, username2: str):
        user1 = self.__choosePlayer(username1)
        user2 = self.__choosePlayer(username2)
        event = FightEvent(user1, user2)
        heapq.heappush(self.eventList, event)

    # Create get item event
    def __getItemOnMap(self, username: str, pos: list):
        user = self.__choosePlayer(username)
        event = GetItemEvent(user, pos)
        heapq.heappush(self.eventList, event)

    def run(self):
        while len(self.eventList) != 0:
            heapq.heappop(self.eventList).eventHandle()
