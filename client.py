__author__ = 'floatec'
#Socket client example in python

from Crypto.PublicKey import RSA
import socket
import sys  # for exit
import time
import hashlib
import AESCipher
from server import Server
import uuid


class Client:
    def __init__(self):
        self.host = 'localhost'
        self.port = 8888
        self.temp_rand = ''
        self.session_key = None

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
        except socket.error, msg:
            print 'Sending authentication failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            return False

        # now receive challenge data that prevents replay attacks
        response = self.session_key.decrypt(self.socket.recv(4096))
        if response == Server.BAD_REQUEST:
            return False

        reply = response

        print reply + "\n"

        challenge = hashlib.sha1(reply + username).digest()
        self.socket.sendall(self.session_key.encrypt(challenge))
        msg = self.session_key.decrypt(self.socket.recv(4096))
        if msg == 'OK':
            return True
        return False

    def send_tmp_pwd(self, tmp_pwd):
        self.socket.sendall(self.session_key.encrypt(tmp_pwd))
        msg = self.session_key.decrypt(self.socket.recv(4096))
        print "after send tmp " + msg
        if msg == Server.BAD_REQUEST:
            return False
        self.temp_rand = msg
        return msg

    def wait_for_authentication(self):
        msg = self.session_key.decrypt(self.socket.recv(4096))
        print "FINAL RESPONSE: " + msg
        if msg == 'OK'+self.temp_rand:
            return True
        return False