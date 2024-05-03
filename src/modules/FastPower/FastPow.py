def fast_power(base, power, modulus):
    result = 1
    base = base % modulus
    while power > 0:
        if power & 1:
            result = (result * base) % modulus
        power >>= 1
        base = (base * base) % modulus
    return result