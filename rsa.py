__author__ = 'Tieni'

from Crypto.PublicKey import RSA as rsa


class RSA:

    def __init__(self):
        try:
            with open('id_rsa', 'r') as key_file:
                key = key_file.read()

            self.private = rsa.importKey(key)

        except IOError:
            print "Unable to read key!"

    def encrypt(self, msg):
        return self.private.encrypt(msg)

    def decrypt(self, msg):
        return self.private.decrypt(msg)

    def show_keys(self):
        public = self.private.publickey()
        print self.private.exportKey()
        print public.exportKey()

private = rsa.generate(2048)
rsa_obj = RSA()
rsa_obj.show_keys()
