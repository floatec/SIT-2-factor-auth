import MySQLdb, time


db = MySQLdb.connect(host="localhost", user="root", passwd="mytienmagsit", db="database")

cur = db.cursor()


def GetUserPw(username):
    cur.execute("SELECT password FROM user WHERE Username =%s;", (username,))
    return cur.fetchone()

def InsertSession(username, hash):
    print str(time.time())
    cur.execute("INSERT INTO session(actualtime,hash,username) VALUES (%s,%s,%s)", (float(time.time()),hash, username))
    db.commit()

def Validate(username, hash):
    cur.execute("SELECT actualtime FROM Session WHERE Username=%s AND hash=%s;", (username, hash))
    dbTimestamp = cur.fetchone()
    print dbTimestamp[0]
    print time.time()
    diff = (time.time() - dbTimestamp[0])
    print diff
    valid=False
    if float(diff) < 30.0 and float(dbTimestamp[0]) > 0.0:
        cur.execute("UPDATE session SET valid=1 WHERE Username=%s AND hash=%s AND actualtime=%s",(username,hash,dbTimestamp[0]))
        return True
    else:
        return False

def IsValid(username, hash):
    isValid = cur.execute("SELECT valid FROM Session WHERE Username=%s AND hash=%s;", (username, hash))
    if isValid == 1:
        return True
    else:
        return False
