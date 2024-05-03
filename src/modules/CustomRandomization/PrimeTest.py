from .RandomGeneration import generate_random_number
from ..FastPower import fast_power
import math

def fermat_test(p, k=5):
    if p == 2:
        return True
    if not p & 1:
        return False

    def check(a, n, x, s):
        result = fast_power(a, x, n)
        if result == 1 or result == n - 1:
            return True
        for _ in range(s - 1):
            result = fast_power(result, 2, n)
            if result == n - 1:
                return True
            if result == 1:
                return False
        return False

    for _ in range(k):
        a = generate_random_number(2, p - 1)
        x = p - 1
        s = 0
        while x % 2 == 0:
            x //= 2
            s += 1
        if not check(a, p, x, s):
            return False
    return True


def miller_rabin(n, k):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    
    # разложение n-1 на 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    for _ in range(k):
        a = generate_random_number(2, n - 2)
        x = fast_power(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = fast_power(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def double_prime_test_adaptive(number: int):
    '''
    Проверяет число на простоту *математически* достаточным количеством 
    тестов (фактически, тестов делается слишком много)
    '''
    fermat_iterations = math.ceil(math.log(number))
    rabin_iterations = math.ceil(fermat_iterations/2)
    return dpuble_prime_test_sized(number 
                                    ,fermat_iterations=fermat_iterations 
                                    ,rabin_iterations=rabin_iterations)
    
def double_prime_test_fixed(number: int):
    '''
    Проверяет число на простоту 50-ю тестами ферма и 30 тестами Миллера-Рабина
    '''
    fermat_iterations = 50
    rabin_iterations = 30
    return dpuble_prime_test_sized(number 
                                    ,fermat_iterations=fermat_iterations 
                                    ,rabin_iterations=rabin_iterations)


def dpuble_prime_test_sized(number: int, fermat_iterations: int, rabin_iterations: int):
    if fermat_test(number, fermat_iterations):
        if miller_rabin(number, rabin_iterations):
            return True
    return False

