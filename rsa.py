__author__ = 'Tieni'

from Crypto.PublicKey import RSA as rsa


class RSA:
    def __init__(self):
        self.private = rsa.generate(2048)

    def encrypt(self, msg):
        return self.private.encrypt(msg)

    def decrypt(self, msg):
        return self.private.decrypt(msg)

    def show_keys(self):
        public = self.private.publickey()
        print self.private.exportKey()
        print public.exportKey()

rsa_obj = RSA()
rsa_obj.show_keys()
