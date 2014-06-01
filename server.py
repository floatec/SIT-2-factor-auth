__author__ = 'floatec'
import socket
import sys
from thread import *

import uuid
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
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
        data = self.server.private.decrypt(conn.recv(2048))
        key_info = data.split('delim')
        print "key_info:" + str(key_info)
        if len(key_info) == 2:
            key_val = key_info[0]
            iv = key_info[1]
        else:
            print "incomplete key info!"
            conn.close()
            return
        self.session_key = AES.new(key_val, AES.MODE_CFB, iv)
        self.username = self.session_key.decrypt(conn.recv(1024))
        self.pwd = self.session_key.decrypt(conn.recv(1024))
        db_return = db.get_user_pw(self.username)
        if db_return != hashlib.sha1(self.pwd).hexdigest():
            conn.send(self.session_key.encrypt(Server.BAD_REQUEST))
        else:
            print "password accepted!"
            # answer with a challenge to prevent replay attacks
            challenge = str(uuid.uuid4())
            cypher_text = self.session_key.encrypt(challenge)

            conn.send(cypher_text)
            # check if user beat the challenge
            data = self.session_key.decrypt(conn.recv(1024))
            if data == hashlib.sha1(challenge+self.username).digest():
                conn.sendall(self.session_key.encrypt("OK"))
                # user beat challenge. Seems to be no attack... So create random number for second factor
                temp_pwd = self.session_key.decrypt(conn.recv(1024))  # accept temporary password for entering second factor
                print "temp pwd: " + temp_pwd
                temp_rand = hashlib.md5(str(uuid.uuid4())).hexdigest()[:5]
                conn.sendall(self.session_key.encrypt(temp_rand))
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
                        conn.send(self.session_key.encrypt('OK' + temp_rand))
                        return

                conn.send(self.session_key.encrypt(Server.BAD_REQUEST))
            else:
                conn.send(self.session_key.encrypt(Server.BAD_REQUEST))

        conn.close()


class Server:
    BAD_REQUEST = 'Bad Request'

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