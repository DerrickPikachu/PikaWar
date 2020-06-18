import threading

from Controller.LEDController import LEDController
from Game.player import player
from Game.moveException import MoveException
from Game.gameMap import GameMap
from Game.item import items, sniperRifle, medical, rifle, armor, skillCard, fireEveryone, entireHeal
from Controller.LCDController import LCDController
from time import sleep
import heapq
import random


class Event:
    def __init__(self, user: player):
        self.user = user
        self.priority = 0

    def eventHandle(self, lcd):
        pass

    def __lt__(self, other):
        return self.priority < other.priority


class MoveEvent(Event):
    def __init__(self, user: player, action: str):
        super().__init__(user)
        self.action = action
        self.priority = 2

    def eventHandle(self, lcd):
        self.user.move(self.action)
        print(self.user.getName() + " moving")
        lcd.writeLcd(self.user.getName() + " moving")
        sleep(3)


class SkillEvent(Event):
    def __init__(self, ledController: LEDController, user: player, id: str, users: list = None):
        super().__init__(user)
        self.priority = 1
        self.users = users
        self.led = ledController
        self.id = id

    def eventHandle(self, lcd):
        print(self.user.getName() + " use skill!!")
        lcd.writeLcd(self.user.getName() + " use skill!!")
        if self.id == skillCard[0]:
            fireEveryone(self.user, self.users, self.led)
        elif self.id == skillCard[1]:
            entireHeal(self.user)
        elif self.id == skillCard[2]:
            pass
        sleep(3)

class ItemEvent(Event):
    def __init__(self, ledController: LEDController, user: player, item: str, users: list = None, pos: list = None):
        super().__init__(user)
        self.users = users
        self.pos = pos
        self.item = item
        self.priority = 3
        self.led = ledController

    def eventHandle(self, lcd):
        print(self.user.getName() + " use item!!!")
        if self.item == items[0]:
            self.led.hintLed(self.pos[0], self.pos[1])
            lcd.writeLcd(self.user.getName() + " use sniperRifle", "Location: "+ self.pos)
            sleep(3)
            sniperRifle(self.user, self.users[0], self.users[1], self.users[2], self.pos)
        elif self.item == items[1]:
            lcd.writeLcd(self.user.getName() + " use medical")
            sleep(3)
            medical(self.user)


class FightEvent(Event):
    def __init__(self, ledController: LEDController, user1: player, user2: player, user3: player = None):
        super().__init__(user1)
        self.user2 = user2
        self.user3 = user3
        self.priority = 4
        self.led = ledController

    def eventHandle(self, lcd):
        # Ping led
        # th = threading.Thread(target=self.led.hintLed,
        #                       args=(self.user.position[0], self.user.position[1],))
        # th.start()
        self.led.hintLed(self.user.position[0], self.user.position[1])

        if self.user3 is not None:
            print(self.user.getName() + " fight with " + self.user2.getName() + " and " + self.user3.getName())
            lcd.writeLcd(self.user.getName() + " fight with " + self.user2.getName() + " and " + self.user3.getName())
            sleep(3)
            # Let everyone get a fight
            self.user.fightWith(self.user2)
            self.user.fightWith(self.user3)
            self.user2.fightWith(self.user3)

            # If there is a problem in the future, first consider here
            if self.user.blood == self.user2.blood and self.user.blood == self.user3.blood:
                # Everyone have the same blood
                choose = random.randint(1, 3)
                if choose == 1:
                    self.user2.moveBack()
                    self.user3.moveBack()
                    return self.user.getName()
                elif choose == 2:
                    self.user.moveBack()
                    self.user3.moveBack()
                    return self.user2.getName()
                elif choose == 3:
                    self.user.moveBack()
                    self.user2.moveBack()
                    return self.user3.getName()
            elif self.user.blood >= self.user2.blood and self.user.blood >= self.user3.blood:
                # Player1 have the highest blood
                self.user2.moveBack()
                self.user3.moveBack()
                return self.user.getName()
            elif self.user2.blood >= self.user.blood and self.user2.blood >= self.user3.blood:
                # Player2 have the highest blood
                self.user.moveBack()
                self.user3.moveBack()
                return self.user2.getName()
            elif self.user3.blood >= self.user.blood and self.user3.blood >= self.user2.blood:
                # Player3 have the highest blood
                self.user.moveBack()
                self.user2.moveBack()
                return self.user3.getName()
        else:
            loser = self.user.fightWith(self.user2)
            loser.moveBack()
            print(self.user.getName() + " fight with " + self.user2.getName())
            lcd.writeLcd(self.user.getName() + " fight with " + self.user2.getName())
            sleep(3)
            if self.user.getName() == loser.getName():
                return self.user2.getName()
            else:
                return self.user.getName()


class GetItemEvent(Event):
    def __init__(self, user: player, gameMap:GameMap):
        super().__init__(user)
        self.priority = 5
        self.gameMap = gameMap

    def eventHandle(self, lcd):
        item = self.gameMap.moveOn(self.user)
        if item != "":
            print(self.user.getName() + " get item")
            lcd.writeLcd(self.user.getName() + " get item", item)
            sleep(3)
        print(self.user.items)
        if item == items[2]:
            rifle(self.user)
        elif item == items[3]:
            armor(self.user)
        


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
