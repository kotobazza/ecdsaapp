from modules.Cryptrography import ECDSAPrivateKey
from modules.Cryptrography.Math.EclipticCurve import Point, EllipticCurve


privatekey = ECDSAPrivateKey()
publickey = privatekey.publickey


a = privatekey.sing_number(10000)
print(publickey.check_signature(a))

