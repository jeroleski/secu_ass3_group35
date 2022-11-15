import base64, requests, random, time

# "https://github.com/jeroleski/secu-ass3-g35/blob/main/Nudes/AntonNudes.txt"
# 'https://api.github.com/repos/{user}/{repo_name}/contents/{path_to_file}'

def getRandomNude(name=""):
    if name == "":
        nudeNames = ["Anton", "BALTAZAAR", "DILF", "HjelGaard", "Jackey", "Mads", "Sebastian", "Slas"]
        r = random.randint(0, len(nudeNames)-1)
        name = nudeNames[r]
    fileName = name + "Nude.txt"

    print("fetching: " + fileName)
    url = "https://api.github.com/repos/g35repo/secu_group35_nudes/contents/" + fileName
    req = requests.get(url)

    if req.status_code == requests.codes.ok:
        req = req.json()  # the response is a JSON
        # req is now a dict with keys: name, encoding, url, size ...
        # and content. But it is encoded with base64.
        content = str(base64.b64decode(req['content']))
        nude = content.replace("\\n", "\n").removeprefix("b'").removesuffix("'").removesuffix("\n")

        meta = "WELCOMING NUDE DOWNLOADED FROM: %s\n\n" % url
        note = incejtStringOnLines(nude, meta)
        #note = meta + nude
        print(note)
        return note
    else:
        if name != "BALTAZAAR":
            print('Content was not found. Fetching BALTAZAAR!')
            return getRandomNude("BALTAZAAR")
        else:
            print('Content was not found.')
            return ""


def incejtStringOnLines(text, s):
    textList = text.split("\n")
    result = ""

    for i in range(len(textList)):
        result += "\n" + s[i] + " " + textList[i] + " "
    
    for i in range(len(textList), len(s)):
        result += s[i]

    return result


def insertRandomNude(c, username):
    nude = getRandomNude()
    if nude == "":
        return

    statement = "SELECT id FROM users WHERE username = :username;"
    c.execute(statement, {'username': username})
    assocUser = c.fetchone()[0]

    statement = """INSERT INTO notes(id, assocUser, dateWritten, note, publicID) VALUES(null, '%s', '%s', '%s', '%s');""" % (assocUser, time.strftime('%Y-%m-%d %H:%M:%S'), nude, random.randrange(1000000000, 9999999999))
    print(statement)
    c.executescript(statement)

getRandomNude()