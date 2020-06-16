from flask import Flask, render_template,request,session,url_for,redirect
import os
from datetime import timedelta
from Game.player import player
import threading
from time import sleep
from Game.moveException import MoveException
from Game.gameEngine import Engine

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
        if len(playerpool) < Engine.MAX_PLAYER:
            for i in range(1,Engine.MAX_PLAYER+1):
                username = "player"+str(i)
                if username not in playerpool:
                    session["username"] = username
                    playerpool[username] = player(username)
                    print("born", username)
                    return render_template("index.html",user=playerpool[username], mapList = playerpool[username].convertPostoArr())
        else:
            print("Enter Deny!")
            return redirect(url_for('denyHandler'))

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
        if counter == Engine.MAX_PLAYER:
            status = False
            counter = 0
        return redirect(url_for('index'))
    else:
        return render_template("loading.html")

@app.route('/deny')
def denyHandler():
    return render_template("deny.html")

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
