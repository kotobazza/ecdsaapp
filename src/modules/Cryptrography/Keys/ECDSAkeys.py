from ...CustomRandomization import generate_random_number, generate_random_prime_number
from ..Math import extended_euclidean_algorithm
from ...FastPower import fast_power
from ..Math import EclipticCurve
import hashlib

class ECDSASignature:
    def __init__(self, type, r, s, message_hash, message):
        self.r = r
        self.s = s
        self.message_hash = message_hash
        self.message = message
        self.type = type
    
    def __repr__(self):
        return f"ECDSASignature: {self.r}, {self.s}, {self.message_hash}, {self.message}"

class ECDSAPublicKey:
    def __init__(self, q, public_key_point, generation_point):
        self.generation_point = generation_point
        self.subgroup_order = q
        self.public_key_point = public_key_point
    
    def check_signature(self, sign: Signature) -> bool:
        assert(0 < sign.r and sign.r < self.subgroup_order)
        assert(0 < sign.s and sign.s < self.subgroup_order)

        e = sign.message % self.subgroup_order
        _, v, _ = extended_euclidean_algorithm(e, self.subgroup_order)

        z1 = sign.s*v%self.subgroup_order
        z2 = -sign.r*v%self.subgroup_order

        C = z1*self.generation_point + z2*self.public_key_point

        return C.x == sign.r




class ECDSAPrivateKey:

    def __init__(self, q, gp:EclipticCurve.Point):
        self.q = q
        
        self.generation_point = gp 

        self.private_key = generate_random_number(3, self.q)
        self.public_key = self.private_key * self.generation_point

    def sing_string(self, string:str):
        m = hashlib.sha224()
        m.update(string.encode())
        t = int(m.hexdigest(), 16)
        assert(t < self.q)
        assert(0==1) # метод нерабочий
        
    
    def sing_number(self, number:int):
        assert(number < self.q)
        e = number % self.q
        s = 0
        while s == 0:

            k = generate_random_number(0, self.q)
            C = k*self.generation_point

            r = C.x % self.q
            s = (r*self.private_key + k*e) % self.q

        return ECDSASignature(r, s, number, number)

    @property
    def publickey(self):
        return ECDSAPublicKey(self.q, self.public_key, self.generation_point)
        

