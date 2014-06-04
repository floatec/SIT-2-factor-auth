import MySQLdb
import time
import hashlib

db = MySQLdb.connect(host="localhost", user="root", passwd="mytienmagsit", db="database")

cur = db.cursor()


def get_user_pw(username):
    cur.execute("SELECT password FROM user WHERE Username =%s;", (username,))
    result = cur.fetchone()
    if result is not None:
        return result[0]
    else:
        return None


def validate_login(username, send_pw):
    cur.execute("SELECT salt, password FROM user WHERE username=%s", username)
    result = cur.fetchone()
    if result is not None:
        return hashlib.sha1(send_pw+result[0]).hexdigest() == result[1]
    return False


def insert_session(username, hash_val):
    cur.execute("INSERT INTO session(actualtime,hash,username,valid) VALUES (%s,%s,%s,FALSE)",
                (float(time.time()), hash_val, username))
    db.commit()


def validate_session(username, hash_val):
    cur.execute("SELECT actualtime FROM Session WHERE Username=%s AND hash=%s;", (username, hash_val))
    db_timestamp = cur.fetchone()
    if db_timestamp is None:
        return False

    diff = (time.time() - db_timestamp[0])
    if float(diff) < 100.0*1000 and float(db_timestamp[0]) > 0.0:
        cur.execute("UPDATE session SET valid=1 WHERE Username=%s AND hash=%s",
                    (username, hash_val))
        db.commit()
        return True
    else:
        return False


def session_is_valid(username, hash_val):
    db_handle = MySQLdb.connect(host="localhost", user="root", passwd="mytienmagsit", db="database")
    new_cur = db_handle.cursor()
    new_cur.execute("SELECT valid FROM Session WHERE Username=%s AND hash=%s;", (username, hash_val))
    valid = new_cur.fetchone()
    if valid is None:
        return False
    if valid[0] == 1:
        new_cur.execute("DELETE FROM Session WHERE Username=%s AND hash=%s;", (username, hash_val))
        db_handle.commit()
        return True
    else:
        return False
