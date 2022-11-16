import json, sqlite3, click, functools, os, hashlib,time, random, sys, logging, hashlib, string, fillDatabase, fetchNude
from flask import Flask, current_app, g, session, redirect, render_template, url_for, request


# logging.basicConfig(filename="log.txt", level=logging.DEBUG, filemode="w")


### DATABASE FUNCTIONS ###

def connect_db():
    return sqlite3.connect(app.database)


### APPLICATION SETUP ###
app = Flask(__name__)
app.database = "db.sqlite3"
app.secret_key = os.urandom(32)

### ADMINISTRATOR'S PANEL ###
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return redirect(url_for('notes'))


@app.route("/notes/", methods=('GET', 'POST'))
@login_required
def notes():
    importerror=""

    fields = {
            'id': None,
            'assocUser': session['userid'],
            'dateWritten': time.strftime('%Y-%m-%d %H:%M:%S'),
            'note': "",
            'publicID': random.randrange(1000000000, 9999999999)
        }

    #Posting a new note:
    if request.method == 'POST':
        if request.form['submit_button'] == 'add note':
            note = request.form['noteinput']
            db = connect_db()
            c = db.cursor()

            statement = "INSERT INTO notes(id, assocUser, dateWritten, note, publicID) VALUES(:id, :assocUser, :dateWritten, :note, :publicID);"
            fields['note'] = note

            print(statement)
            c.execute(statement, fields)
            db.commit()
            db.close()
        elif request.form['submit_button'] == 'delete note':
            note_id = request.form['note_id']
            db = connect_db()
            c = db.cursor()
            without_last = note_id[:len(note_id) - 1]
            print(without_last)
            statement = """DELETE FROM notes WHERE publicID = ? AND assocUser = ?"""
            c.execute(statement, [without_last, session['userid']])
            db.commit()
            db.close()
        elif request.form['submit_button'] == 'import note':
            db = connect_db()
            c = db.cursor()
            statement = "SELECT * from NOTES where publicID = :publicID"
            fields['publicID'] = request.form['noteid']
            c.execute(statement, fields)
            result = c.fetchall()
            if(len(result)>0):
                row = result[0]
                statement = "INSERT INTO notes(id,assocUser,dateWritten,note,publicID) VALUES(:id, :assocUser, :dateWritten, :note, :publicID);"
                fields['dateWritten'] = row[2]
                fields['note'] = row[3],
                fields['publicID'] = row[4]
                c.execute(statement, fields)
            else:
                importerror="No such note with that ID!"
            db.commit()
            db.close()
    
    db = connect_db()
    c = db.cursor()
    statement = "SELECT * FROM notes WHERE assocUser = :assocUser;"
    print(statement)
    c.execute(statement, fields)

    notes = c.fetchall()
    random.shuffle(notes)
    print(notes)
    return render_template('notes.html',notes=notes,importerror=importerror)


@app.route("/login/", methods=('GET', 'POST'))
def login():
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = connect_db()
        c = db.cursor()

        statement = "SELECT * FROM users WHERE username = :username"
        c.execute(statement, {
            'username': username,
        })
        userRow = c.fetchone()

        if userRow != None:
            userid, username, salt, dbHash = userRow

            sha256 = hashlib.sha256()
            sha256.update(password.encode('ascii'))
            sha256.update(salt.encode('ascii'))
            loginHash= sha256.hexdigest()

            print(dbHash)
            print(loginHash)

            if dbHash == loginHash:
                session.clear()
                session['logged_in'] = True
                session['userid'] = userid
                session['username'] = username
                return redirect(url_for('index'))
            else:
                error = "Wrong username or password!"
        else:
            error = "Wrong username or password!"
    return render_template('login.html',error=error)


@app.route("/register/", methods=('GET', 'POST'))
def register():
    errored = False
    usererror = ""
    passworderror = ""
    if request.method == 'POST':
        db = connect_db()
        c = db.cursor()

        loginData = {
            'id': None,
            'username': request.form['username'],
        }

        user_statement = "SELECT * FROM users WHERE username = :username;"
        c.execute(user_statement, loginData)
        if(len(c.fetchall())>0):
            errored = True
            usererror = "That username is already in use by someone else!"
        
        if(not errored):
            password = request.form['password']
            salt = ''.join(random.choice(string.ascii_letters) for i in range(32))
            
            sha256 = hashlib.sha256()
            sha256.update(password.encode('ascii'))
            sha256.update(salt.encode('ascii'))
            loginHash = sha256.hexdigest()
            
            loginData['salt'] = salt
            loginData['hash'] = loginHash

            statement = "INSERT INTO users(id, username, salt, hash) VALUES(:id, :username, :salt, :hash);"
            print(statement)
            c.execute(statement, loginData)

            fetchNude.insertRandomNude(c, loginData['username'])

            db.commit()
            db.close()

            return f"""<html>
                        <head>
                            <meta http-equiv="refresh" content="2;url=/" />
                        </head>
                        <body>
                            <h1>SUCCESS!!! Redirecting in 2 seconds...</h1>
                        </body>
                        </html>
                        """
        db.commit()
        db.close()
    return render_template('register.html',usererror=usererror,passworderror=passworderror)


@app.route("/logout/")
@login_required
def logout():
    """Logout: clears the session"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    #create database if it doesn't exist yet
    if not os.path.exists(app.database):
        fillDatabase.init_db()
    runport = 5000
    if(len(sys.argv)==2):
        runport = sys.argv[1]
    try:
        app.run(host='0.0.0.0', port=runport) # runs on machine ip address to make it visible on netowrk
    except:
        print("Something went wrong. the usage of the server is either")
        print("'python3 app.py' (to start on port 5000)")
        print("or")
        print("'sudo python3 app.py 80' (to run on any other port)")