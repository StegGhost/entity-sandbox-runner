import hashlib

class CryptoProvider:
    @staticmethod
    def hash(data: bytes):
        return hashlib.sha3_512(data).hexdigest()

    @staticmethod
    def sign(data: bytes, key=None):
        return CryptoProvider.hash(data)

    @staticmethod
    def verify(data: bytes, signature: str, key=None):
        return CryptoProvider.hash(data) == signature