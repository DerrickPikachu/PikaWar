from flask import Flask, render_template


app = Flask(__name__)


@app.route('/<name>')
def index(name):
    testDic = {1:"a",2:"b"}
    return render_template("index.html",name=testDic)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
