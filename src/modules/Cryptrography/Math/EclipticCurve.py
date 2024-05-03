from ..Math import extended_euclidean_algorithm

class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def __eq__(self, other):
        return (self.a, self.b, self.p) == (other.a, other.b, other.p)
    
    def __repr__(self):
        return f"EllipticCurve(a={self.a}, b={self.b}, p={self.p})"

class Point:
    def __init__(self, x, y, curve:EllipticCurve):
        self.x = x
        self.y = y
        self.curve = curve
    
    def __neg__(self):
        return Point(self.x, -self.y % self.curve.p, self.curve)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y) and self.curve == other.curve

    def __add__(self, other):
        if self == other:
            return __rmul__(2)

        _, d, _ = extended_euclidean_algorithm((other.x - self.x),self.curve.p)
        print(d)
        d = (d+self.curve.p)%self.curve.p
        

        slope = (other.y - self.y) * d % self.curve.p

        cx = (slope**2-self.x-other.x) % self.curve.p
        cy = (slope - (self.x-cx) - self.y)%self.curve.p
        return Point(cx, cy, self.curve)
        
        
        

    def __rmul__(self, k:int):
        pass



    def __repr__(self):
        return f"Point({self.x}, {self.y})"



