from Game.player import player
items = ["狙擊槍", "醫療箱", "步槍", "防彈衣"]


def sniperRifle(user1:player, user2:player, user3:player, userIndex:int,location:list):
    users = [user1, user2, user3]
    print("sniperRifle Active!")
    if user1.getPosition() == location:
        print("sniperRifle user1 is attacked!")
        user1.setBlood(user1.getBlood()//2)
    elif user2.getPosition() == location:
        print("sniperRifle user2 is attacked!")
        user2.setBlood(user2.getBlood()//2)
    elif user3.getPosition() == location:
        print("sniperRifle user3 is attacked!")
        user3.setBlood(user3.getBlood()//2)
    else:
        print("nobody will be hurt!")
    users[userIndex].items.remove(0)


def medical(user:player): 
    totalBlood = user.getBlood() + 5
    if totalBlood >= 10:
        user.setBlood(10)
    else:
        user.setBlood(totalBlood)
    user.items.remove(1)


def rifle(user:player):
    totalPower = user.getPower() + 2
    if totalPower >= 10:
        user.setPower(10)
    else:
        user.setPower(totalPower)
    


def armor(user:player):
    totalDefense = user.getDefense() + 2
    if totalDefense >= 7:
        user.setDefense(7)
    else:
        user.setDefense(totalDefense)
    
    