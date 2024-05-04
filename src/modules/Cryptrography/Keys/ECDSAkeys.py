from ...CustomRandomization import generate_random_number, generate_random_prime_number
from ..Math import extended_euclidean_algorithm
from ...FastPower import fast_power
from ..Math import EclipticCurve

from bestconfig import Config

"""
Модуль сам по себе будет использовать кривую curve25519. Это значит, что все параметры будут захардкожены внутрь ECDSAKeys в виде cистемного объекта
"""

config = Config()

class _Signature:
    def __init__(self, r, s, message):
        self.r = r
        self.s = s
        self.message = message

def convert_string_to_hashable_format(string, bits):
    pass

class ECDSAPrivateKey:

    def __init__(self):
        self.q = int(config.subgroup_order)
        
        self.generation_point = EclipticCurve.Point(
            int(config.generation_point.x),
            int(config.generation_point.y),
            EclipticCurve.EllipticCurve(
                int(config.curve.a),
                int(config.curve.b),
                int(config.curve.p)
            )
        ) 

        self.d = generate_random_number(3, self.q)
        self.public_key = self.d * self.generation_point

    
    def sing_number(self, number:int):
        assert(number < self.q)
        e = number % self.q
        s = 0
        while s == 0:

            k = generate_random_number(0, self.q)
            C = k*self.generation_point

            r = C.x % self.q
            s = (r*self.d + k*e) % self.q

        return _Signature(r, s, number)


    class _ECDSAPublicKey:
        def __init__(self, q, public_key, generation_point):
            self.generation_point = generation_point
            self.q = q
            self.public_key = public_key
        
        def check_signature(self, sign: _Signature) -> bool:
            assert(0 < sign.r and sign.r < self.q)
            assert(0 < sign.s and sign.s < self.q)

            e = sign.message % self.q
            _, v, _ = extended_euclidean_algorithm(e, self.q)

            z1 = sign.s*v%self.q
            z2 = -sign.r*v%self.q

            C = z1*self.generation_point + z2*self.public_key

            return C.x == sign.r
        

        
    @property
    def publickey(self):
        return self._ECDSAPublicKey(self.q, self.public_key, self.generation_point)
        

