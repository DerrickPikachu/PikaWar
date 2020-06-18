from flask import Flask, render_template, request, session, url_for, redirect
import os
from datetime import timedelta

from Game.item import items
from Game.player import player
import threading
from time import sleep
from Game.moveException import MoveException
from Game.gameEngine import Engine

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

playerpool = dict()
engine = Engine()

status = False
counter = 0

position={"player1":[0, 0], "player2":[0, 2], "player3":[1, 1]}

@app.route('/')
def index():
    global status, engine

    if  session.get('username') == None:
        if len(playerpool) < Engine.MAX_PLAYER:
            for i in range(1, Engine.MAX_PLAYER+1):
                username = "player"+str(i)

                if username not in playerpool:
                    session["username"] = username
                    playerpool[username] = player(username,position[username])
                    engine.addPlayer(playerpool[username])
                    print("born", username)
                    return render_template("index.html", user=playerpool[username], mapList = playerpool[username].convertPostArr())
        else:
            print("Enter Deny!")
            return redirect(url_for('denyHandler'))

    else:
        username = session["username"]
        print("use", username)
        return render_template("index.html", user=playerpool[username], mapList = playerpool[username].convertPostArr())
    

@app.route('/', methods = ["POST"])
def formHandle():
    global engine
    username = session["username"]
    action = request.values.get('direction')
    print("Action " + action)

    #suppose it will be valid
    try:
        engine.moveAction(username=username, action=action)
        # playerpool[username].move(action=action)
        playerpool[username].ready = True

        if request.values.get('tool'):
            tool = request.values.get('tool')
            if tool == '特殊技能':
                # engine.lcd.writeLcd("please sense",  "your card!")
                # rfid = RFIDResovler()
                # id = rfid.readRFID()
                # print("Get card id")
                # engine.lcd.writeLcd("Get card id","id: "+ str(id))
                # sleep(3)
                engine.useSkill(username)
            elif tool == items[1]:
                engine.chooseItem(username=username, item=request.values.get('tool'))
            elif tool == items[0]:
                shootLoc = int(request.values.get('bulletLoc'))
                pos = [(shootLoc - 1) // 3, (shootLoc - 1) % 3]
                engine.chooseItem(username=username, item=request.values.get('tool'), pos=pos)

        if checkAllPlayerReady():
            thread = threading.Thread(target=gameProcess)
            thread.start()

        return redirect(url_for('loadingTimeHandler'))
    except MoveException:
        return render_template("index.html", user=playerpool[username], mapList=playerpool[username].convertPostArr())


@app.route('/loading')
def loadingTimeHandler():
    username = session.get('username')
    global status, counter

    if not playerpool[username].alive:
        del playerpool[username]
        return redirect(url_for("deathHandler"))

    if status:
        counter += 1
        #TODO need to decide the number
        if counter == Engine.MAX_PLAYER:
            status = False
            counter = 0

        if Engine.MAX_PLAYER == 1:
            return redirect(url_for('winnerHandler'))
        return redirect(url_for('index'))
    else:
        return render_template("loading.html")


@app.route('/deny')
def denyHandler():
    return render_template("deny.html")


@app.route('/death')
def deathHandler():
    global counter
    session.clear()
    # When draw
    if Engine.MAX_PLAYER == 0:
        counter = 0
        Engine.MAX_PLAYER = 3
    return render_template("death.html")


@app.route('/winner')
def winnerHandler():
    global counter
    username = session.get('username')
    del playerpool[username]
    session.clear()
    # Let the server can start a new game
    counter = 0
    Engine.MAX_PLAYER = 3
    return render_template("winner.html")


def gameProcess():
    # TODO: Engine
    global status, engine
    sleep(2)
    engine.run()
    status = True
    for key in playerpool:
        playerpool[key].ready = False


def checkAllPlayerReady():
    if len(playerpool) != Engine.MAX_PLAYER:
        return False
    for key, user in playerpool.items():
        if not user.ready:
            return False
    return True


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
