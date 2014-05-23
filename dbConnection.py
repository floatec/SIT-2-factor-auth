import MySQLdb, time

db = MySQLdb.connect(host="localhost",user="root",passwd="mytienmagsit",db="database")

cur = db.cursor()
cur.execute()

def GetUserPw(username):
    userpw = cur.execute("SELECT password FROM user where Username ="+username+";")
    return userpw

def InsertSession(username,hash):
    cur.execute("INSERT INTO session(Timestamp,hash) VALUES ("+time.time()+","+hash+") WHERE Username='"+username+"';")

def Validate(username,hash):
    dbTimestamp = cur.execute("SELECT Timestamp FROM Session WHERE Username='"+username+"'AND hash='"+hash+"';")
    if dbTimestamp - time.time() < 30:
        return True
    else:
        return False