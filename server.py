__author__ = 'floatec'
import socket
import sys
from thread import *
import base64
import AESCipher
import uuid
import hashlib

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8889  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'


#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    #conn.send('Welcome to the server. Type something and hit enter\n')  # send only takes string

    #infinite loop so that function do not terminate and thread do not end.
    while True:

        #Receiving from client
        data = conn.recv(1024)
        key = data
        aes = AESCipher.AESCipher(key)
        user = aes.decrypt(conn.recv(1024))
        pwd = aes.decrypt(conn.recv(1024))
        print user
        #antwort
        chalange = str(uuid.uuid4())
        cyphertext = aes.encrypt(chalange)

        if not data:
            break

        conn.send(cyphertext)
        data = aes.decrypt(conn.recv(1024))
        if data == hashlib.sha1(chalange+user).digest():
            temp_pwd = aes.decrypt(conn.recv(1024))
            temp_rand = hashlib.md5(str(uuid.uuid4())).digest()
            #TODO add database parts here
            conn.send(aes.encrypt(temp_rand))

            print("fuck")
        else:
             conn.send(aes.encrypt("__ERROR"))
    #came out of loop
    conn.close()

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread, (conn,))

s.close()