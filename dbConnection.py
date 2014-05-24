import MySQLdb
import time

db = MySQLdb.connect(host="localhost", user="root", passwd="mytienmagsit", db="database")

cur = db.cursor()
cur.execute()


def get_user_pw(username):
    userpw = cur.execute("SELECT password FROM user where Username ="+username+";")
    return userpw


def insert_session(username, hash_val):
    cur.execute("INSERT INTO session(Timestamp,hash) VALUES ("+time.time()+","+hash_val+") WHERE Username='"+username+"';")


def validate(username, hash_val):
    db_timestamp = cur.execute("SELECT Timestamp FROM Session WHERE Username='"+username+"'AND hash='"+hash_val+"';")
    if db_timestamp - time.time() < 30:
        return True
    else:
        return False


def is_valid(username, hash_val):
    isValid = cur.execute("SELECT valid FROM Session WHERE Username='"+username+"'AND hash='"+hash_val+"';")
    return isValid