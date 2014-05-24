__author__ = 'floatec'
#Socket client example in python

from Crypto.PublicKey import RSA
import socket
import sys  # for exit
import time
import hashlib
import AESCipher

import uuid


class Client:
    def __init__(self):
        self.host = 'localhost'
        self.port = 8888
        self.temp_pwd = 'temp1234'
        self.session_key = ''

        try:
            with open('id_rsa.pub', 'r') as key_file:
                self.server_key = RSA.importKey(key_file.read())
        except IOError:
            print 'Unable to open key file!'

        #create an INET, STREAMing socket
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print 'Failed to create socket'
            sys.exit()

    def open_socket(self):
        try:
            remote_ip = socket.gethostbyname(self.host)
            #Connect to remote server
            self.socket.connect((remote_ip, self.port))
        except socket.gaierror:
            #could not resolve
            print 'Hostname could not be resolved. Exiting'
            sys.exit()

    def login(self, username, password):
        session_key_value = hashlib.sha256(str(uuid.uuid4())).digest()
        self.session_key = AESCipher.AESCipher(session_key_value)
        try:
            #Send new session key and login data (first factor)
            session_key_crypt = self.server_key.encrypt(session_key_value, "hallo")
            self.socket.sendall(session_key_crypt[0])
            self.socket.sendall(self.session_key.encrypt(username))
            time.sleep(1)  # TODO: this is a nasty hack for sending username and password separately! Find a clean way..
            self.socket.sendall(self.session_key.encrypt(password))
        except socket.error:
            print 'Send failed'
            sys.exit()

        # now receive challenge data that prevents replay attacks
        cipher = self.socket.recv(4096)
        print cipher + "\n"
        reply = self.session_key.decrypt(cipher)

        print reply + "\n"

        challenge = hashlib.sha1(reply + username).digest()
        self.socket.sendall(self.session_key.encrypt(challenge))
        self.socket.sendall(self.session_key.encrypt(self.temp_pwd))

        # if challenge is beat, receive the second factor. Otherwise an error reply is received
        msg = self.session_key.decrypt(self.socket.recv(4096))
        print "\n" + msg

client = Client()
client.open_socket()
client.login('test', '1234')