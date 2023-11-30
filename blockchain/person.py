import hashlib
from ecdsa import SigningKey

sk = SigningKey.generate()

class person:  # class name
    def __init__(self, name):  # constructor
        self.name = name
        self.sk = SigningKey.generate('password')
        self.pk = sk.get_verifying_key()

    def get_has_name(self):  # method
        # return the hash of the name
        return hashlib.sha256(self.name.encode()).hexdigest()

def get_pk(self):
    return self.pk

# get the public key of the person
def get_sk(self):
    return self.sk


# sign a message
def sign(self, message):
    return self.sk.sign(message)


# verify a message
def verify(self, message, signature):
    return self.pk.verify(signature, message)


# get the hash of the public key
def get_hash_pk(self):
    return hashlib.sha256(self.pk.to_string()).hexdigest()

    #
