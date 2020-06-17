from Game.player import player
from Game.moveException import MoveException
import heapq
import random


class Event:
    def __init__(self, user: player):
        self.user = user
        self.priority = 0

    def eventHandle(self):
        pass

    def __lt__(self, other):
        return self.priority < other.priority


class MoveEvent(Event):
    def __init__(self, user: player, action: str):
        super().__init__(user)
        self.action = action
        self.priority = 2

    def eventHandle(self):
        self.user.move(self.action)
        print(self.user.getName() + " moving")


class SkillEvent(Event):
    def __init__(self, user: player):
        super().__init__(user)
        self.priority = 1

    def eventHandle(self):
        print(self.user.getName() + " use skill!!")


class ItemEvent(Event):
    def __init__(self, user: player, item: str):
        super().__init__(user)
        self.item = item
        self.priority = 3

    def eventHandle(self):
        print(self.user.getName() + " use item!!!")


class FightEvent(Event):
    def __init__(self, user1: player, user2: player, user3: player = None):
        super().__init__(user1)
        self.user2 = user2
        self.user3 = user3
        self.priority = 4

    def eventHandle(self):
        if self.user3 is not None:
            # Let everyone get a fight
            self.user.fightWith(self.user2)
            self.user.fightWith(self.user3)
            self.user2.fightWith(self.user3)

            # If there is a problem in the future, first consider here
            if self.user.blood == self.user2.blood and self.user.blood == self.user3.blood:
                choose = random.randint(1, 3)
                if choose == 1:
                    self.user2.moveBack()
                    self.user3.moveBack()
                elif choose == 2:
                    self.user.moveBack()
                    self.user3.moveBack()
                elif choose == 3:
                    self.user.moveBack()
                    self.user2.moveBack()
            elif self.user.blood >= self.user2.blood and self.user.blood >= self.user3.blood:
                self.user2.moveBack()
                self.user3.moveBack()
            elif self.user2.blood >= self.user.blood and self.user2.blood >= self.user3.blood:
                self.user.moveBack()
                self.user3.moveBack()
            elif self.user3.blood >= self.user.blood and self.user3.blood >= self.user2.blood:
                self.user.moveBack()
                self.user2.moveBack()

            print(self.user.getName() + " fight with " + self.user2.getName() + " and " + self.user3.getName())
        else:
            loser = self.user.fightWith(self.user2)
            loser.moveBack()
            print(self.user.getName() + " fight with " + self.user2.getName())


class GetItemEvent(Event):
    def __init__(self, user: player, pos: list):
        super().__init__(user)
        self.priority = 5

    def eventHandle(self):
        print(self.user.getName() + "get item")


if __name__ == '__main__':
    user1 = player("p1")
    user2 = player("p2")
    eventList = []

    heapq.heappush(eventList, FightEvent(user1, user2))
    heapq.heappush(eventList, MoveEvent(user1, "up"))
    heapq.heappush(eventList, ItemEvent(user2, "狙擊槍"))
    heapq.heappush(eventList, SkillEvent(user2))

    # eventList.append(FightEvent(user1, user2))
    # eventList.append(MoveEvent(user1, "up"))
    # eventList.append(ItemEvent(user2, "狙擊槍"))
    # eventList.append(SkillEvent(user2))

    # for obj in eventList:
    #     obj.eventHandle()
    while len(eventList) != 0:
        heapq.heappop(eventList).eventHandle()
