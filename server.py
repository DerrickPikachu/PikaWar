from flask import Flask, render_template,request,session
import os
from Player.player import player

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

playerpool = dict()


@app.route('/')
def index():
    if  session.get('username') == None:
        if "player1" not in playerpool:
            session["username"] = "player1"
            playerpool["player1"] = player("player1")
            print("born player1")
            print("pn:",playerpool["player1"].getName())
            return render_template("index.html",user=playerpool["player1"])
        elif "player2" not in playerpool:
            session["username"] = "player2"
            playerpool["player2"] = player("player2")
            print("born player2")
            return render_template("index.html",user=playerpool["player2"])
        elif "player3" not in playerpool:
            session["username"] = "player3"
            playerpool["player3"] = player("player3")
            print("born player3")
            return render_template("index.html",user=playerpool["player3"])
    else:
        username = session["username"]
        print("use",username)
        print(playerpool[username].getName())
        return render_template("index.html",user=playerpool[username])
    

@app.route('/',methods = ["POST"])
def formHandle():
    username = session["username"]
    name = request.values.get('direction')
    print("Action" + name)
    return render_template("index.html",user=playerpool[username])

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
