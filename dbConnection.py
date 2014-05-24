import MySQLdb, time

db = MySQLdb.connect(host="localhost", user="root", passwd="mytienmagsit", db="database")

cur = db.cursor()
cur.execute()

def GetUserPw(username):
    userpw = cur.execute("SELECT password FROM user where Username ='%s';", (username))
    return userpw

def InsertSession(username, hash):
    cur.execute("INSERT INTO session(Timestamp,hash) VALUES ("+time.time()+",%s) WHERE Username='%s';", (hash, username))

def Validate(username, hash):
    dbTimestamp = cur.execute("SELECT Timestamp FROM Session WHERE Username='%s' AND hash='%s';", (username, hash))
    if dbTimestamp - time.time() < 30:
        return True
    else:
        return False

def IsValid(username, hash):
    isValid = cur.execute("SELECT valid FROM Session WHERE Username='%s'AND hash='%s';", (username, hash))
    return isValid