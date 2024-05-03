class KeyScheme:
    @property
    def publicKey(self):
        pass

    @property
    def privateKey(self):
        pass

    def encrypt(self, message:int) -> int:
        pass

    def decrypt(self, message:int) -> int:
        pass