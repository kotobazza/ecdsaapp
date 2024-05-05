from modules.Cryptrography.Keys.ECDSAkeys import ECDSAPublicKey
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

    def sign_message(self, message:int):
        assert(message < self._subgroup_order)
        return self._private_key.sing_number(message)

    # нужно создать новый формат сигнатуры вовне, чтобы объект сигнатуры мог быть создан на основе строки

    def check_signature(self, signature, public_key:ECDSAPublicKey):
        return public_key.check_signature(signature)