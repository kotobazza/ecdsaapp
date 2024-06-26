import json

class EllipticCurve:
    """ Класс для элиптической кривой в форме y^2 = x^3 + ax + b над полем F_p. """
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def __eq__(self, other):
        return (self.a, self.b, self.p) == (other.a, other.b, other.p)

    def __repr__(self):
        return f"EllipticCurve(a={self.a}, b={self.b}, p={self.p})"

    def json(self):
        return "{" + f"curve.a: {self.a}, curve.b: {self.b}, curve.p: {self.p}" +"}"

    @staticmethod
    def load_from_json(string):
        data = json.loads(string)
        a = int(data['curve.a'])
        b = int(data['curve.b'])
        p = int(data['curve.p'])
        return EllipticCurve(a, b, p)


class Point:
    """ Класс для представления точек на элиптической кривой. """
    def __init__(self, x, y, curve:EllipticCurve):
        self.x = x
        self.y = y
        self.curve = curve

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y) and self.curve == other.curve

    def __neg__(self):
        return Point(self.x, -self.y % self.curve.p, self.curve)

    def __add__(self, other):
        if self.x is None or self.y is None:
            return other
        if other.x is None or other.y is None:
            return self

        assert self.curve == other.curve

        # Случай, когда точки равны
        if self == other:
            if self.y == 0:
                return Point(None, None, self.curve)
            # Удвоение точки
            s = (3 * self.x**2 + self.curve.a) * pow(2 * self.y, -1, self.curve.p)
            
        else:
            if self.x == other.x:
                return Point(None, None, self.curve)
            # Сложение различных точек
            s = (other.y - self.y) * pow(other.x - self.x, -1, self.curve.p)

        x_r = (s**2 - self.x - other.x) % self.curve.p
        y_r = (s * (self.x - x_r) - self.y) % self.curve.p

        return Point(x_r, y_r, self.curve)

    def __rmul__(self, k):
        result = Point(None, None, self.curve)
        addend = self

        while k:
            if k & 1:
                result += addend
            addend += addend
            k >>= 1

        return result

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


    def json(self):
        return "{"+ f"x: {self.x}, y: {self.y}, curve: {self.curve.json()}" +"}"

    @staticmethod
    def load_from_json(string):
        data = json.loads(string)
        x = int(data['x'])
        y = int(data['y'])
        curve = EllipticCurve.load_from_json(data['curve'])
        return Point(x, y, curve)


