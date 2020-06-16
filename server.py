from flask import Flask, render_template,request,session,url_for,redirect
import os
from datetime import timedelta
from Game.player import player
import threading
from time import sleep
from Game.moveException import MoveException

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

playerpool = dict()

status = False
counter = 0


@app.route('/')
def index():
    global status
    if  session.get('username') == None:
        if "player1" not in playerpool:
            session["username"] = "player1"
            playerpool["player1"] = player("player1")
            print("born player1")
            print("pn:",playerpool["player1"].getName())
            return render_template("index.html",user=playerpool["player1"], mapList = playerpool["player1"].convertPostoArr())
        elif "player2" not in playerpool:
            session["username"] = "player2"
            playerpool["player2"] = player("player2")
            print("born player2")
            #for test signal
            # status = True
            return render_template("index.html",user=playerpool["player2"], mapList = playerpool["player2"].convertPostoArr())
        elif "player3" not in playerpool:
            session["username"] = "player3"
            playerpool["player3"] = player("player3")
            print("born player3")
            return render_template("index.html",user=playerpool["player3"], mapList = playerpool["player3"].convertPostoArr())
    else:
        username = session["username"]
        print("use", username)
        print(playerpool[username].getName())
        return render_template("index.html",user=playerpool[username],mapList = playerpool[username].convertPostoArr())
    

@app.route('/', methods = ["POST"])
def formHandle():
    username = session["username"]
    action = request.values.get('direction')
    print("Action " + action)
    #suppose it will be valid
    try:
        playerpool[username].move(action=action)
        playerpool[username].ready = True
        if checkAllPlayerReady():
            thread = threading.Thread(target=gameProcess)
            thread.start()
        return redirect(url_for('loadingTimeHandler'))
    except MoveException:
        return render_template("index.html", user=playerpool[username], mapList=playerpool[username].convertPostoArr())

@app.route('/loading')
def loadingTimeHandler():
    global status, counter
    if status:
        counter += 1
        #TODO need to decide the number
        if counter == 2:
            status = False
            counter = 0
        return redirect(url_for('index'))
    else:
        return render_template("loading.html")


def gameProcess():
    global status
    sleep(5)
    status = True
    for key in playerpool:
        playerpool[key].ready = False 


def checkAllPlayerReady():
    for key, user in playerpool.items():
        if not user.ready:
            return False
    return True


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
