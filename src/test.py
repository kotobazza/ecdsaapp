from modules.Cryptrography.Math.EllipticCurveMath import Point, EllipticCurve
from modules.Cryptrography.Keys import ECDSAPrivateKey
from bestconfig import Config

config = Config()

gp = Point(
            int(config.generation_point.x),
            int(config.generation_point.y),
            EllipticCurve(
                int(config.curve.a),
                int(config.curve.b),
                int(config.curve.p)
            )
        )

q = int(config.subgroup_order)

private_key = ECDSAPrivateKey(q, gp)

public_key = private_key.public_key

sign = private_key.sign("Hello World")




