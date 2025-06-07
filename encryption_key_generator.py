import os
from cryptography.fernet import Fernet

def generate_encryption_key():
    key = Fernet.generate_key()
    decrypted_key = key.decode()

    with open("encryption_key.enc", "w+") as encryption_key:
        encryption_key.write(decrypted_key)

if __name__ == '__main__':
    generate_encryption_key()