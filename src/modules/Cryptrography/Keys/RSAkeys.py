from ...CustomRandomization import generate_random_number, generate_random_prime_number
from ..Math import extended_euclidean_algorithm
from ...FastPower import fast_power

'''
Приватный ключ генерируется на основе публичного, публичный - на основе приватного...
ммм
'''

class RSAPrivateKey:
    bits: int
    modulus: int
    public_part: int
    private_part: int

    # must be removed
    p: int
    q: int
    phi: int



    def __init__(self, bits):
        self.bits = bits
        min_number_size = 2<<int(bits/2-1)
        max_number_size = 2<<int(bits/2)

        self.p = generate_random_prime_number(min_number_size, max_number_size)
        self.q = generate_random_prime_number(min_number_size, max_number_size)

        self.modulus = self.p*self.q
        
        self.phi = (self.p - 1) * (self.q - 1)
        self.public_part = generate_random_number(2, self.phi)

        while True:
            gcd, d, _ = extended_euclidean_algorithm(self.public_part, self.phi)
            if gcd != 1: 
                self.public_part = generate_random_number(2, self.phi)
            else:
                self.private_part = (self.phi + d) % self.phi
                assert(self.private_part>0)
                break
    

    @property
    def publickey(self):
        return self._RSAPublicKey(self.public_part, self.modulus)

    def decrypt_number(self, message: int):
        return fast_power(abs(message), self.private_part, self.modulus)

    def decrypt_string_sample(self, message: str):
        '''
            Является sample-методом. Ужасно работает
            Для переработки надо построить хеш-функцию
        '''
        symbols = message.split(" ")
        string = ""
        for symbol in symbols:
            try:
                string += chr(self.decrypt_number(int(symbol)))
            except ValueError:
                raise Exception(f"Can't decrypt. Message has wrong symbols: {symbol}")
        return string

    class _RSAPublicKey:
        public_part: int
        modulus: int

        def __init__(self, public_part, modulus):
            self.public_part = public_part
            self.modulus = modulus
            

        def encrypt_number(self, message: int):
            return fast_power(abs(message), self.public_part, self.modulus)


        def encrypt_string_sample(self, message: str):
            '''
                Является sample-методом. Ужасно работает
                Для переработки надо построить хеш-функцию
            '''
            symbols = []
            for symbol in message:
                symbol_order = ord(symbol)
                symbols.append(str(self.encrypt_number(symbol_order)))
            return " ".join(symbols)


