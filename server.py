__author__ = 'floatec'
import socket
import sys
from thread import *
import AESCipher
import uuid
import hashlib
from Crypto.PublicKey import RSA


class ServerInstance:

    def __init__(self, server):
        self.username = ""
        self.pwd = ""
        self.session_key = ""
        self.server = server

    #Function for handling connections. This will be used to create threads
    def client_thread(self, conn):
        #Sending message to connected client
        #conn.send('Welcome to the server. Type something and hit enter\n')  # send only takes string

        #infinite loop so that function do not terminate and thread do not end.


        #Receiving from client
        data = server.private.decrypt(conn.recv(2048))
        self.session_key = AESCipher.AESCipher(data)
        self.username = self.session_key.decrypt(conn.recv(1024))
        self.pwd = self.session_key.decrypt(conn.recv(1024))
        # answer
        challenge = str(uuid.uuid4())
        cypher_text = self.session_key.encrypt(challenge)

        if not data:
            print "no data!"
            return

        conn.send(cypher_text)
        data = self.session_key.decrypt(conn.recv(1024))
        if data == hashlib.sha1(challenge+self.username).digest():
            temp_pwd = self.session_key.decrypt(conn.recv(1024))
            temp_rand = hashlib.md5(str(uuid.uuid4())).hexdigest()[:5]
            #TODO add database parts here
            conn.send(self.session_key.encrypt(temp_rand))
        else:
            conn.send(self.session_key.encrypt("__ERROR"))
        #came out of loop
        conn.close()


class Server:
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

server = Server()
server.open_socket()
server.handle_clients()