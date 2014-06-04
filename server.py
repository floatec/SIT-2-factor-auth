__author__ = 'floatec'
import socket
import sys
from thread import *

import uuid
import hashlib
from Crypto.PublicKey import RSA
from AESCipher import *
import dbConnection as db
import time


class ServerInstance:

    def __init__(self, server):
        self.username = ""
        self.pwd = ""
        self.session_key = ""
        self.server = server
        self.ttl = 30

    #Function for handling connections. This will be used to create threads
    def client_thread(self, conn):
        #Receive authentication from client: a new session key, the username and password
        self.session_key = AESCipher(self.server.private.decrypt(conn.recv(2048)))

        user_data = self.session_key.decrypt(conn.recv(1024))
        user_data = user_data.split(Server.DELIMITER)

        if len(user_data) != 2:
            print "incomplete user data!"
            conn.close()
            return

        self.username = user_data[0]
        self.pwd = user_data[1]

        #db_return = db.get_user_pw(self.username)
        if not db.validate_login(self.username, self.pwd):  # db_return != hashlib.sha1(self.pwd).hexdigest():
            conn.send(self.session_key.encrypt(Server.BAD_REQUEST))
        else:
            # answer with a challenge to prevent replay attacks
            challenge = str(uuid.uuid4())
            conn.send(self.session_key.encrypt(challenge))

            # check if user beat the challenge
            challenge_response = self.session_key.decrypt(conn.recv(1024))
            if challenge_response == hashlib.sha1(challenge+self.username).digest():
                conn.sendall(self.session_key.encrypt("OK, I almost trust that you are " + self.username))
                # user beat challenge. Seems to be no attack. So ...
                # 1. accept temporary password for entering second factor
                temp_pwd = self.session_key.decrypt(conn.recv(1024))
                # 2. generate a second factor and send it to the user
                temp_rand = hashlib.md5(str(uuid.uuid4())).hexdigest()[:5]
                conn.sendall(self.session_key.encrypt(temp_rand))
                # 3. create a time-limited session in the database
                temp_hash = hashlib.sha1(temp_pwd + temp_rand).hexdigest()
                db.insert_session(self.username, temp_hash)
                ttl = self.ttl
                while ttl > 0:
                    print "ttl: " + str(ttl)
                    ttl -= 1
                    time.sleep(1)
                    if db.session_is_valid(self.username, temp_hash):
                        conn.send(self.session_key.encrypt('OK' + temp_rand))
                        return

                conn.send(self.session_key.encrypt(Server.BAD_REQUEST))
            else:
                conn.send(self.session_key.encrypt(Server.BAD_REQUEST))

        conn.close()


class Server:
    BAD_REQUEST = 'Bad Request'
    DELIMITER = 'Delimiter'

    def __init__(self):
        try:
            with open('id_rsa', 'r') as key_file:
                key = key_file.read()
            self.private = RSA.importKey(key)
        except IOError:
            print "Unable to read key!"

        self.host = ''   # Symbolic name meaning all available interfaces
        self.port = 8888  # Arbitrary non-privileged port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created'

    def open_socket(self):
        #Bind socket to local host and port
        try:
            self.socket.bind((self.host, self.port))
        except socket.error, msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

        print 'Socket bind complete'

        #Start listening on socket
        self.socket.listen(10)
        print 'Socket now listening'

    def handle_clients(self):
        #now keep talking with the client
        while True:
            #wait to accept a connection - blocking call
            conn, address = self.socket.accept()
            print 'Connected with ' + address[0] + ':' + str(address[1])

            #start new thread takes 1st argument as a function name to be run,
            # second is the tuple of arguments to the function.
            server_instance = ServerInstance(self)
            start_new_thread(server_instance.client_thread, (conn,))

        ServerInstance.socket.close()