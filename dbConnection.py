import MySQLdb
import time

db = MySQLdb.connect(host="localhost", user="root", passwd="mytienmagsit", db="database")

cur = db.cursor()


def get_user_pw(username):
    cur.execute("SELECT password FROM user WHERE Username =%s;", (username,))
    result = cur.fetchone()
    if result is not None:
        return result[0]
    else:
        return None


def insert_session(username, hash_val):
    print str(time.time())
    cur.execute("INSERT INTO session(actualtime,hash,username,valid) VALUES (%s,%s,%s,FALSE)",
                (float(time.time()), hash_val, username))
    db.commit()


def validate(username, hash_val):
    cur.execute("SELECT actualtime FROM Session WHERE Username=%s AND hash=%s;", (username, hash_val))
    db_timestamp = cur.fetchone()
    print db_timestamp[0]
    print time.time()
    diff = (time.time() - db_timestamp[0])
    print diff
    if float(diff) < 100.0*1000 and float(db_timestamp[0]) > 0.0:
        print "setting SESSION TO VALID. username " + username + "  hash: " + hash_val
        cur.execute("UPDATE session SET valid=1 WHERE Username=%s AND hash=%s",
                    (username, hash_val))
        db.commit()
        return True
    else:
        return False


def is_valid(username, hash_val):
    print "username: " + username + " hash: " + hash_val
    db = MySQLdb.connect(host="localhost", user="root", passwd="mytienmagsit", db="database")
    newcur = db.cursor()
    newcur.execute("SELECT valid FROM Session WHERE Username=%s AND hash=%s;", (username, hash_val))
    valid = newcur.fetchone()
    print valid
    print valid[0]
    if valid[0] == 1:
        return True
    else:
        return False
