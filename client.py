__author__ = 'floatec'
#Socket client example in python

from Crypto import Random
from Crypto.PublicKey import RSA
import socket  # for sockets
import sys  # for exit
import hashlib
import base64
import AESCipher

import uuid

host = 'localhost'
port = 8888
user = 'test'
pwd = '1234'
temp_pwd = 'temp1234'
import rsa

try:
    with open('id_rsa.pub', 'r') as key_file:
        keyString = key_file.read()
        server_key = RSA.importKey(keyString)
except IOError:
    print 'Unable to open key file!'


#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()





try:
    remote_ip = socket.gethostbyname(host)

except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

key = hashlib.sha256(str(uuid.uuid4())).digest()
aes=AESCipher.AESCipher(key)

#Connect to remote server
s.connect((remote_ip, port))




try :
    #Set the whole string
    s.sendall(key)
    s.sendall(aes.encrypt(user))
    s.sendall(aes.encrypt(pwd))
except socket.error:
    #Send failed
    print 'Send failed'
    sys.exit()


#Now receive data
cipher = s.recv(4096)
print(cipher)
reply = aes.decrypt(cipher)

print reply

chalange = hashlib.sha1(reply+user).digest()
s.sendall(aes.encrypt(chalange))
s.sendall(aes.encrypt(temp_pwd))


temp_rand = aes.decrypt(s.recv(4096))
print "\n"+temp_rand
