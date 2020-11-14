

import flask
import sqlite3

app = flask.Flask(__name__, static_folder="styles/")

@app.route("/login", methods=["GET", "POST"])
def login():
    return flask.render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    return flask.render_template("register.html")

if __name__ == "__main__":
    app.run(port=5001, host='127.0.0.1', debug=True, use_evalex=False)