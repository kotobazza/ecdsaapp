from modules.Cryptrography.Keys.ECDSAkeys import ECDSAPublicKey
import hashlib

class Unit:
    def __init__(self, number):
        self.number = number
    
    def set_keypair(self, key):
        self._private_key = key
        self._public_key = key.publickey
        self._curve = key.generation_point.curve 
        self._subgroup_order = key.q
    
    @property
    def public_key(self):
        return self._public_key.public_key_point
    
    @property
    def private_key(self):
        return self._private_key.private_key
    
    @property
    def generation_curve(self):
        return self._curve


#
        # вот здеся
        # #
    def sign_message(self, message):
        m = hashlib.sha224()
        m.update(message.encode())
        t = int(m.hexdigest(), 16)
        assert(t < self._subgroup_order)
        return self._private_key.sing_number(t)

    

    def check_signature(self, signature, public_key:ECDSAPublicKey):
        return public_key.check_signature(signature)