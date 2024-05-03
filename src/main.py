from modules.Cryptrography.Keys import ECDSAkeys
from modules.Cryptrography.Math.EclipticCurve import Point, EllipticCurve


curve = EllipticCurve(a=2, b=6, p=7)
G = Point(x=2, y=5, curve=curve)
P = Point(x=1, y=3, curve=curve)

print(G+P)

