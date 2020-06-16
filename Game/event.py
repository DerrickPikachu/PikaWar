from Game.player import player
import heapq


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
        # self.user.move(self.action)
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
    def __init__(self, user1: player, user2: player):
        super().__init__(user1)
        self.user2 = user2
        self.priority = 4

    def eventHandle(self):
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
