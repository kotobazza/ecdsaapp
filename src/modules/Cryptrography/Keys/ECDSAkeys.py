from ...CustomRandomization import generate_random_number, generate_random_prime_number
from ..Math import extended_euclidean_algorithm
from ...FastPower import fast_power
from ..Math import EllipticCurveMath
import hashlib
import json


class Signature:
    def __init__(self, r, s, hashed):
        self.r = r
        self.s = s
        self.hash = hashed
    
    def __repr__(self):
        return f"ECDSA_Signature: {self.r}, {self.s}, {self.hash}"

    def json(self):
        return "{"+ f"message_hash: {self.hash}," + f"signature_r: {self.r}" + f"signature_s: {self.s}" + "}"

    @staticmethod
    def load_from_json(string):
        data = json.loads(string)
        signature_r = int(data['signature_r'])
        signature_s = int(data['signature_s'])
        message_hash = int(data['message_hash'])
        return Signature(signature_r, signature_s, message_hash)


class SignedMessage:
    def __init__(self, message, signature:Signature):
        self.message = message
        self.signature = signature

    def __repr__(self):
        return f"ECDSA_SignedMessage: {self.message}, {self.signature.__repr__()}"
    
    def json(self):
        return "{" + f"message: {self.message}," + f"signature: {self.signature.json}"+ "}"

    @staticmethod
    def load_from_json(string):
        data = json.loads(string)
        message = data['message']
        signature = Signature.load_from_json(data['signature'])
        return SignedMessage(message, signature)
        



        


class ECDSAPublicKey:
    def __init__(self, q, public_key_point, generation_point):
        self.generation_point = generation_point
        self.subgroup_order = q
        self.public_key_point = public_key_point
    
    def check_signature(self, signed_message: SignedMessage) -> bool:
        sign = signed_message.signature
        
        assert(0 < sign.r and sign.r < self.subgroup_order)
        assert(0 < sign.s and sign.s < self.subgroup_order)

        e = sign.message % self.subgroup_order
        _, v, _ = extended_euclidean_algorithm(e, self.subgroup_order)

        z1 = sign.s*v%self.subgroup_order
        z2 = -sign.r*v%self.subgroup_order

        C = z1*self.generation_point + z2*self.public_key_point

        return C.x == sign.r

    def __repr__(self):
        return f"ECDSA_PublicKey: {self.generation_point}, {self.subgroup_order}, {self.public_key_point}" 

    def json(self):
        return "{"+ f"subgroup_order: {self.subgroup_order}, generation_point: {self.generation_point.json()}, public_key_point: {self.public_key_point.json()}" +"}"

    @staticmethod
    def load_from_json(string):
        data = json.loads(string)
        subgroup_order = int(data['subgroup_order'])
        generation_point = EllipticCurveMath.Point.load_from_json(data['generation_point'])
        public_key_point = EllipticCurveMath.Point.load_from_json(data['public_key_point'])

        return ECDSAPublicKey(send_pubkey_button, public_key_point, generation_point)



class ECDSAPrivateKey:

    def __init__(self, q, gp: EllipticCurveMath.Point):
        self.q = q
        
        self.generation_point = gp 

        self.private_key = generate_random_number(3, self.q)
        self.public_key = self.private_key * self.generation_point

    def sign(self, signable:str):
        m = hashlib.sha224()
        m.update(string.encode("utf-8"))
        hashed = int(m.hexdigest(), 16)

        signature = self.__sing_sha224hash(hashed)

        return SignedMessage(signable, signautre)

        
    
    def __sing_sha224hash(self, hashed:int):
        assert(hashed < self.q)
        e = hashed % self.q
        s = 0
        while s == 0:

            k = generate_random_number(0, self.q)
            C = k*self.generation_point

            r = C.x % self.q
            s = (r*self.private_key + k*e) % self.q

        return Signature(r, s, hashed)

    @property
    def publickey(self):
        return ECDSAPublicKey(self.q, self.public_key, self.generation_point)
        

