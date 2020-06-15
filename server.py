from flask import Flask, render_template,request,session
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

playerpool = set()

@app.route('/')
def index():
    if  session.get('username') == None:
        if "player1" not in playerpool:
            session["username"] = "player1"
            playerpool.add("player1")
            print("born player1")
            return render_template("index.html",username="player1")
        elif "player2" not in playerpool:
            session["username"] = "player2"
            playerpool.add("player2")
            print("born player2")
            return render_template("index.html",username="player2")
        elif "player3" not in playerpool:
            session["username"] = "player3"
            playerpool.add("player3")
            print("born player3")
            return render_template("index.html",username="player3")
    else:
        username = session["username"]
        print("use",username)
        return render_template("index.html",username=username)
    

@app.route('/',methods = ["POST"])
def formHandle():
    name = request.values.get('direction')
    print("Hello" + name)
    return name

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
