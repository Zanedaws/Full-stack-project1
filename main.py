

import flask
import sqlite3
import safe_serialization

app = flask.Flask(__name__, static_folder="styles/")

@app.route("/login", methods=["GET"])
def login_get():
    return flask.render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    user = flask.request.form['user']
    pswd = flask.request.form['pass']
    iden = hash((user,pswd))
    return flask.redirect(flask.url_for(hash=iden, endpoint='feed_get'))

@app.route("/<hash>/feed", methods=["GET"])
def feed_get(hash):
    user = hash;
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE userHash!=?",(user,))
    posts = c.fetchall()
    c.execute("SELECT * FROM users WHERE hash=?",(user,))
    userInfo = c.fetchall()
    posts.insert(0,userInfo[0][0])
    print(posts)
    return flask.render_template("feed.html", data = posts)

@app.route("/register", methods=["GET"])
def register_get():
    return flask.render_template("register.html")

@app.route("/register", methods=["POST"])
def register_post():
    user = flask.request.form['user']
    pswd = flask.request.form['pass']
    iden = hash((user,pswd))
    conn = sqlite3.connect("data/database.db")
    c = conn.cursor()
    if(c.execute("SELECT * FROM users WHERE hash=?",(iden,)).fetchall() == []):
        c.execute("INSERT INTO users VALUES (?,?,?)", (user, pswd, iden))
        conn.commit()
        conn.close()
        return flask.redirect(flask.url_for(hash=iden, endpoint='feed_get'))
    else:
        conn.close()
        return flask.redirect(flask.url_for(hash=iden, endpoint='feed_get'))

if __name__ == "__main__":
    app.run(port=5001, host='127.0.0.1', debug=True, use_evalex=False)