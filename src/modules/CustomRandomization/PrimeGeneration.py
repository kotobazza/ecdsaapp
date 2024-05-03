from .PrimeTest import double_prime_test_fixed
from .RandomGeneration import generate_random_number

def generate_random_prime_number(minimal: int, maximal: int):
    a = generate_random_number(minimal, maximal)
    while not double_prime_test_fixed(a):
        a = generate_random_number(minimal, maximal)
    return a