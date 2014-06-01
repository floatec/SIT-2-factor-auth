__author__ = 'floatec'
#Socket client example in python

from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES
import socket
import sys  # for exit
import hashlib
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
        self.session_key = hashlib.sha256(str(uuid.uuid4())).digest()

        try:
            #Send new session key and login data (first factor)
            session_key_crypt = self.server_key.encrypt(self.session_key, "hallo")
            self.socket.sendall(session_key_crypt[0])
            self.socket.sendall(self.encrypt_msg(username + Server.DELIMITER + password))
        except socket.error, msg:
            print 'Sending authentication failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            return False

        # now receive challenge data that prevents replay attacks
        message = self.decrypt_msg(self.socket.recv(4096))
        if message == Server.BAD_REQUEST:
            return False

        print message

        challenge = hashlib.sha1(message + username).digest()
        self.socket.sendall(self.encrypt_msg(challenge))
        msg = self.decrypt_msg(self.socket.recv(4096))
        if msg == 'OK':
            return True
        return False

    def send_tmp_pwd(self, tmp_pwd):
        self.socket.sendall(self.encrypt_msg(tmp_pwd))
        msg = self.decrypt_msg(self.socket.recv(4096))
        print "after send tmp " + msg
        if msg == Server.BAD_REQUEST:
            return False
        self.temp_rand = msg
        return msg

    def wait_for_authentication(self):
        msg = self.decrypt_msg(self.socket.recv(4096))
        print "FINAL RESPONSE: " + msg
        if msg == 'OK'+self.temp_rand:
            return True
        return False

    def decrypt_msg(self, msg):
        iv = msg[0:AES.block_size]
        key = AES.new(self.session_key, AES.MODE_CFB, iv)
        return key.decrypt(msg[AES.block_size:])

    def encrypt_msg(self, msg):
        iv = Random.new().read(AES.block_size)
        key = AES.new(self.session_key, AES.MODE_CFB, iv)
        return iv+key.encrypt(msg)