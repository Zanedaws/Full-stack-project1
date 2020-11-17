

import flask
import sqlite3
import datetime
import hashlib

app = flask.Flask(__name__, static_folder="styles/")

@app.route("/login", methods=["GET"])
def login_get():
    return flask.render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    user = flask.request.form['user']
    pswd = flask.request.form['pass']
    iden = int(hashlib.shake_256(user.encode('utf-8')+pswd.encode('utf-8')).hexdigest(4), 16)
    return flask.redirect(flask.url_for(hash=iden, endpoint='feed_get'))

@app.route("/<hash>/profile", methods=["GET"])
def profile_get(hash):
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE userHash=?",(hash,))
    posts = c.fetchall()
    c.execute("SELECT * FROM users WHERE hash=?",(hash,))
    name = c.fetchall()
    posts.reverse()
    posts.insert(0,name[0][0])
    conn.close()
    posts.insert(0, hash)
    print(posts)
    return flask.render_template("profile.html", data=posts)

@app.route("/<user>/profile", methods=["POST"])
def profile_post(user):
    pass

@app.route("/<hash>/feed", methods=["GET"])
def feed_get(hash):
    user = hash;
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE userHash!=?",(user,))
    posts = c.fetchall()
    posts.reverse()
    c.execute("SELECT * FROM users WHERE hash=?",(user,))
    userInfo = c.fetchall()
    conn.close()
    posts.insert(0,userInfo[0][0])
    return flask.render_template("feed.html", data = posts)

@app.route("/<hash>/create",methods=["GET"])
def create_get(hash):
    return flask.render_template("create.html", data=hash)

@app.route("/<user>/create",methods=["POST"])
def create_post(user):
    content = flask.request.form['cont']
    title = flask.request.form['title']
    conn = sqlite3.connect("data/database.db")
    c = conn.cursor()
    postHash = int(hashlib.shake_256(content.encode('utf-8')+title.encode('utf-8')+str(datetime.datetime.now()).encode('utf-8')).hexdigest(4),16)
    data=(int(user),postHash,0,content,title)
    print(data)
    try:
        c.execute("INSERT INTO posts (userHash, postHash, likes, content, title) VALUES (?,?,?,?,?)",data)
    except:
        pass
    conn.commit()
    conn.close()
    return flask.redirect(flask.url_for(hash=user, endpoint="profile_get"))

@app.route("/register", methods=["GET"])
def register_get():
    return flask.render_template("register.html")

@app.route("/register", methods=["POST"])
def register_post():
    user = flask.request.form['user']
    pswd = flask.request.form['pass']
    iden = int(hashlib.shake_256(user.encode('utf-8')+pswd.encode('utf-8')).hexdigest(4),16)
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