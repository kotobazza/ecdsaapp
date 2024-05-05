from modules.Cryptrography.Math import Point, EllipticCurve
from modules.CustomRandomization.PrimeTest import double_prime_test_adaptive
from modules.Cryptrography.Keys import ECDSAPrivateKey
from .Units import Unit

class Cryptosystem:
    def __init__(self, config):
        self.config = config
        self.unit1 = -1
        self.unit2 = -1
        self.gp = Point(
            int(self.config.generation_point.x),
            int(self.config.generation_point.y),
            EllipticCurve(
                int(self.config.curve.a),
                int(self.config.curve.b),
                int(self.config.curve.p)
            )
        )
        self.q = int(self.config.subgroup_order)

    @property
    def generation_point(self):
        return Point(
            self.gp.x, 
            self.gp.y,
            self.gp.curve
        )
    
    @property
    def subgroup_order(self):
        return self.q
    
    @property
    def curve(self):
        return EllipticCurve(
            self.gp.curve.a, 
            self.gp.curve.b, 
            self.gp.curve.p
        )
    
    
    def check_p(self):
        return double_prime_test_adaptive(self.gp.curve.p)
    
    def check_subgroup_order(self):
        return double_prime_test_adaptive(self.subgroup_order)

    def check_generation_point(self):
        zero_point = Point(None, None, self.gp.curve)
        return self.subgroup_order * self.gp == zero_point
    
    def get_first_unit(self):
        if self.unit1 == -1:
            self.unit1 = Unit(1)
            return self.unit1
        return self.unit1
    
    def get_second_unit(self):
        if self.unit2 == -1:
            self.unit2 = Unit(2)
            return self.unit2
        return self.unit2

    
    def generate_keypair(self):
        privatekey = ECDSAPrivateKey(self.subgroup_order, self.gp)
        return privatekey




    