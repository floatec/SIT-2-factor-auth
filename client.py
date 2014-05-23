__author__ = 'floatec'
#Socket client example in python

from Crypto import Random
import socket  # for sockets
import sys  # for exit
import hashlib
import base64
import AESCipher


#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

print 'Socket Created'

host = 'localhost'
port = 8889

try:
    remote_ip = socket.gethostbyname(host)

except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
key = hashlib.sha256("notsosecure").digest()
aes=AESCipher.AESCipher(key)
#Connect to remote server
s.connect((remote_ip, port))



message = key

try :
    #Set the whole string
    s.sendall(message)
except socket.error:
    #Send failed
    print 'Send failed'
    sys.exit()


#Now receive data
cipher = s.recv(4096)
print(cipher)
reply = aes.decrypt(cipher)

print reply