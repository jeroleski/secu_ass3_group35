import sqlite3, hashlib, random, string, time

def init_db():
    # Initializes the database with our great SQL schema
    conn = sqlite3.connect("db.sqlite3")
    db = conn.cursor()
    db.executescript("""
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS notes;

CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assocUser INTEGER NOT NULL,
    dateWritten DATETIME NOT NULL,
    note TEXT NOT NULL,
    publicID INTEGER NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    salt TEXT NOT NULL,
    hash TEXT NOT NULL
);
""")

    # insert burner users
    addUser(db, "admin", "password") # 1
    addUser(db, "bernardo", "omgMPC") # 2
    addUser(db, "anton", "qWeRtY0987") # 3
    addUser(db, "baltazaar", "dinkleberg") # 4
    addUser(db, "dilf", "lord.vincent") # 5
    addUser(db, "hjemgaard", "who-let-the-dogs-out") # 6
    addUser(db, "jackey", "SuperSecretPassphrase4321.") # 7
    addUser(db, "mads", "bajer") # 8
    addUser(db, "sebastian", "MilleMus") # 9
    addUser(db, "slas", "1234") # 10
    
    #insert burner notes
    addNote(db, 1, "THE FOLLOWING USERNAMES ARE INITIALIZED IN THE DATABASE:\nadmin\nbernardo\nanton\nbaltazaar\ndilf\nhjemgaard\njackey\nmads\nsebastian\nslas\n")
    addNote(db, 2, "hello my friend")
    addNote(db, 2, "i want lunch pls")
    addNote(db, 3, "skaldet indianer i en sovepose")
    addNote(db, 4, "hashtag get trolled")
    addNote(db, 4, "hashtag red herring")
    addNote(db, 4, "hashtag tak sam")
    addNote(db, 5, "husk at klippe barnet den 12. december!")
    addNote(db, 5, "ive fucked ip boyz... i killed the server")
    addNote(db, 5, "jeg ved ikke hvad der er værst.... at lugte til nossesved i metroen eller lugte til KU'ere på turen fra islandsbrygge")
    addNote(db, 6, "Did you ever hear the tragedy of Darth Plagueis The Wise? I thought not. It’s not a story the Jedi would tell you. It’s a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life… He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful… the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. Ironic. He could save others from death, but not himself.")
    addNote(db, 7, "hey friis, btw vi har leaket credentials til hjemmesiden til en fra gruppe 36... kh jackey <3")
    addNote(db, 7, "Jackeys to do:\n-Vask bilen (X)\n-Spil brætspil med mads ( )\n-Lav nye credentials til serveren (X)\n-Fetch BALTAZAARNude.txt hvis ingen af de andre findes (X)\n-Giv nyt username til serveren til sebastian (X)\n-Giv nyt password til serveren til hjemgaard (X)\n-Aflever perflab ( )")
    addNote(db, 8, "HUSK spil brætspil med jackey, tirsdag kl. 14 i analog")
    addNote(db, 8, "jeg kan drikke baltazaar s vægt i øl")
    addNote(db, 8, "It takes only one drink to get me drunk. The trouble is, I can’t remember if it’s the thirteenth or the fourteenth.")
    addNote(db, 8, "A man knows less as he drinks more, and loses more and more of his wisdom.")
    addNote(db, 8, "I am not an alcoholic. I am a drunk, and there is a vast difference.")
    addNote(db, 8, "Promise me one thing: don’t take me home until I’m drunk… Very drunk indeed.")
    addNote(db, 8, "To alcohol! The cause of – and solution – to all of life’s problems.")
    addNote(db, 8, "When the beer goes in the wits go out.")
    addNote(db, 8, "When your companions get drunk and fight, Take up your hat, and wish them good night.")
    addNote(db, 9, "gib beer plox")
    addNote(db, 10,"hvis i køber øl til os gir vi et hint")
    addNote(db, 10,"Salatslynger er køkkenudstyrets gbi'er. Overflødig og spild af plads.")

    # insert burner credentials
    addNote(db, 1, "login til @secu35.itu.dk:\nusername: server\npassword: BilligBajer49")
    addNote(db, 2, "login til @secu35.itu.dk:\nusername: admin\npassword: DrinkingBeerAllDay17")
    addNote(db, 3, "login til @secu35.itu.dk:\nusername: beer\npassword: NarMenDeGraderErDetAltidMedEnBajerIHaanden")
    addNote(db, 4, "login til @secu35.itu.dk:\nusername: bajz\npassword: WillCode4Beer")
    addNote(db, 5, "login til @secu35.itu.dk:\nusername: baltazaar\npassword: BeerAndBlowjob69")
    addNote(db, 6, "login til @secu35.itu.dk:\nusername: dogs\npassword: ChugSomeBeer3")
    addNote(db, 7, "login til @secu35.itu.dk:\nusername: sweeden\npassword: RockAndBajzBaby1234")
    addNote(db, 8, "login til @secu35.itu.dk:\nusername: client\npassword: WhoLetTheBajzOut22222")
    addNote(db, 9, "login til @secu35.itu.dk:\nusername: user\npassword: GimmiGimmiGimmiABeerAfter24")
    addNote(db, 10,"login til @secu35.itu.dk:\nusername: sudo\npassword: Beers1Badminton")

    conn.commit()
    conn.close()


def addUser(db, username, password):
    salt, loginHash = hashPassword(password)
    loginData = {
        'id': None,
        'username': username,
        'salt': salt,
        'hash': loginHash
    }
    db.execute("INSERT INTO users(id, username, salt, hash) VALUES(:id, :username, :salt, :hash);", loginData)


def addNote(db, assocUser, note):
    fields = {
            'id': None,
            'assocUser': assocUser,
            'dateWritten': time.strftime('%Y-%m-%d %H:%M:%S'),
            'note': note,
            'publicID': random.randrange(1000000000, 9999999999)
        }
    db.execute("INSERT INTO notes(id, assocUser, dateWritten, note, publicID) VALUES(:id, :assocUser, :dateWritten, :note, :publicID);", fields)


def hashPassword(password) -> (str, str):
    salt = ''.join(random.choice(string.ascii_letters) for i in range(32))

    sha256 = hashlib.sha256()
    sha256.update(password.encode('ascii'))
    sha256.update(salt.encode('ascii'))
    loginHash= sha256.hexdigest()

    return salt, loginHash

    
init_db()
