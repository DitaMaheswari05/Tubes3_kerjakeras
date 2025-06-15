import hashlib
import os
import base64

class Encryptor:
    def __init__(self, password: str):
        self.key = hashlib.sha256(password.encode()).digest()

    def _xor_bytes(self, data: bytes) -> bytes:
        return bytes([b ^ self.key[i % len(self.key)] for i, b in enumerate(data)])

    def encrypt(self, plaintext: str) -> str:
        data = plaintext.encode()
        iv = os.urandom(16)
        encrypted_data = self._xor_bytes(iv + data)
        return base64.urlsafe_b64encode(encrypted_data).decode()

    def decrypt(self, encrypted_text: str) -> str:
        encrypted_data = base64.urlsafe_b64decode(encrypted_text)
        decrypted = self._xor_bytes(encrypted_data)
        return decrypted[16:].decode()

    def weak_encrypt(self, plaintext: str) -> str:
        data = plaintext.encode()
        xor_data = self._xor_bytes(data)
        encoded = base64.urlsafe_b64encode(xor_data).decode()

        return encoded[:20]

    def weak_decrypt(self, encrypted_text: str) -> str:
        try:
            encrypted_data = base64.urlsafe_b64decode(encrypted_text + '===')
            decrypted = self._xor_bytes(encrypted_data)
            return decrypted.decode()
        except Exception:
            return "[DECRYPTION_ERROR]"