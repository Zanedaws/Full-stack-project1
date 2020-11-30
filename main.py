import flask
import sqlite3
import datetime
import hashlib
import math

app = flask.Flask(__name__, static_folder="")

@app.route("/login", methods=["GET"])
def login_get():
    return flask.render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    user = flask.request.form['user']
    pswd = flask.request.form['pass']
    iden = int(hashlib.shake_256(user.encode('utf-8')+pswd.encode('utf-8')).hexdigest(4), 16)
    conn = sqlite3.connect("data/database.db")
    c = conn.cursor()

    if (c.execute("SELECT * FROM users WHERE hash=?", (iden,)).fetchall() != []): #login success
        print(c.fetchall())
        #return flask.redirect(flask.url_for(hash=iden, endpoint='profile_get'))
        return flask.redirect(flask.url_for(hash=iden, endpoint='feed_get'))
    else:
        return flask.render_template('login.html') #login fail


@app.route("/<hash>/<numPages>/<page>", methods=["GET"])
def page_get(hash, numPages, page):
    print(page)
    page = int(page)
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE userHash=?", (hash,))
    posts = c.fetchall()
    posts.reverse()
    if page > 0:
        start = (page) * 5
    else:
        start = 0
    print(start)
    print(start+6)
    posts = posts[start:start + 6]
    c.execute("SELECT * FROM users WHERE hash=?", (hash,))
    name = c.fetchall()
    posts.insert(0, name[0][0])
    conn.close()
    posts.insert(0,numPages)
    posts.insert(0,hash)
    print(posts)
    return flask.render_template("profilecards.html", data=posts)

@app.route("/<hash>/profile", methods=["GET"])
def profile_get(hash):
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE userHash=?", (hash,))
    posts = c.fetchall()
    c.execute("SELECT * FROM users WHERE hash=?", (hash,))
    name = c.fetchall()
    posts.reverse() #reverse chronological order ( may need to adjust for pagination)
    posts.insert(0, name[0][0])
    conn.close()

    numPages = math.ceil((len(posts)-1)/5)

    posts.insert(0, numPages)
    posts.insert(0, hash)
    #print(posts)
    return flask.render_template("profilecards.html", data=posts)

@app.route("/<user>/profile", methods=["POST"]) #need to implement post deletion (phase 2)
def profile_post(user):
    pass

@app.route("/<posthash>/delete", methods=["POST"]) #this is currently where the delete button goes
def post_delete(posthash):
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE postHash=?", (posthash,))
    conn.commit()
    conn.close()
    return '', 204

@app.route("/<hash>/feed", methods=["GET"])
def feed_get(hash):
    user = hash
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE userHash!=?", (user, ))
    posts = c.fetchall()
    posts.reverse() #reverse chronological order ( may need to adjust for pagination)
    c.execute("SELECT * FROM users WHERE hash=?", (user, ))
    userInfo = c.fetchall()
    print(userInfo)
    conn.close()
    numPages = math.ceil((len(posts)-1)/5)
    posts.insert(0, userInfo[0][0])
    posts.insert(1, userInfo[0][2])
    posts.insert(0, numPages)
    print(posts)
    return flask.render_template("feed.html", data=posts)

@app.route("/<userhash>/posts/<posthash>", methods=["GET"]) #added userhash for voting tracking
def post_get(userhash, posthash):
    post = posthash
    user = userhash
    print(posthash)
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE postHash=?", (post, )) #finds post with given postHash
    posts = c.fetchall()
    posts.reverse()
    conn.close()
    #print("\n\n\nPost\n\n\n")
    posts.insert(0, user)
    return flask.render_template("posts.html", data=posts)

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

    print(postHash)
    data = (int(user), postHash, 0, content, title)

    print(data)
    try:
        c.execute("INSERT INTO posts (userHash, postHash, likes, content, title) VALUES (?,?,?,?,?)", data)
        #creates post
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
    print(iden)
    if c.execute("SELECT * FROM users WHERE hash=?", (iden,)).fetchall() == []:
        c.execute("INSERT INTO users VALUES (?,?,?)", (user, pswd, iden))
        conn.commit()
        conn.close()
        return flask.redirect(flask.url_for(hash=iden, endpoint='feed_get'))
        #return flask.redirect(flask.url_for(hash=iden, endpoint='profile_get')) #remove phase 2

    else:
        conn.close()
        return flask.redirect(flask.url_for(hash=iden, endpoint='feed_get'))
        #return flask.redirect(flask.url_for(hash=iden, endpoint='profile_get')) #remove phase 2


if __name__ == "__main__":
    app.run(port=5001, host='127.0.0.1', debug=True, use_evalex=False)