__author__ = 'floatec'
import socket
import sys
from thread import *

import uuid
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
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
        self.session_key = self.server.private.decrypt(conn.recv(2048))

        user_data = self.decrypt_msg(conn.recv(1024))
        user_data = user_data.split(Server.DELIMITER)
        print user_data
        if len(user_data) != 2:
            print "incomplete user data!"
            conn.close()
            return

        self.username = user_data[0]
        self.pwd = user_data[1]

        db_return = db.get_user_pw(self.username)
        if db_return != hashlib.sha1(self.pwd).hexdigest():
            conn.send(self.encrypt_msg(Server.BAD_REQUEST))
        else:
            print "password accepted!"
            # answer with a challenge to prevent replay attacks
            challenge = str(uuid.uuid4())
            conn.send(self.encrypt_msg(challenge))

            # check if user beat the challenge
            challenge_response = self.decrypt_msg(conn.recv(1024))
            if challenge_response == hashlib.sha1(challenge+self.username).digest():
                conn.sendall(self.encrypt_msg("OK, I almost trust that you are " + self.username))
                # user beat challenge. Seems to be no attack... So create random number for second factor
                temp_pwd = self.decrypt_msg(conn.recv(1024))  # accept temporary password for entering second factor
                print "temp pwd: " + temp_pwd
                temp_rand = hashlib.md5(str(uuid.uuid4())).hexdigest()[:5]
                conn.sendall(self.encrypt_msg(temp_rand))
                temp_hash = hashlib.sha1(temp_pwd + temp_rand).hexdigest()
                print "temp hash: " + temp_hash
                db.insert_session(self.username, temp_hash)
                ttl = self.ttl
                while ttl > 0:
                    print "ttl: " + str(ttl)
                    ttl -= 1
                    time.sleep(1)
                    if db.is_valid(self.username, temp_hash):
                        print "I SEND: " + 'OK' + temp_rand
                        conn.send(self.encrypt_msg('OK' + temp_rand))
                        return

                conn.send(self.encrypt_msg(Server.BAD_REQUEST))
            else:
                conn.send(self.encrypt_msg(Server.BAD_REQUEST))

        conn.close()

    def decrypt_msg(self, msg):
        iv = msg[0:AES.block_size]
        key = AES.new(self.session_key, AES.MODE_CFB, iv)
        return key.decrypt(msg[AES.block_size:])

    def encrypt_msg(self, msg):
        iv = Random.new().read(AES.block_size)
        key = AES.new(self.session_key, AES.MODE_CFB, iv)
        return iv+key.encrypt(msg)


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