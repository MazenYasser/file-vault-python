import getpass
import json
import os
import sys
from base64 import urlsafe_b64decode, urlsafe_b64encode
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_key_from_password(password: str, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    hashed_key = kdf.derive(password.encode())
    return hashed_key

def encrypt_fernet_key(password: str):
    salt = os.urandom(16)
    key = generate_key_from_password(password, salt)
    fernet = Fernet(urlsafe_b64encode(key))
    fernet_key = Fernet.generate_key()
    encrypted_key = fernet.encrypt(fernet_key)
    with open(".filevault_config/secrets.json", "w+") as secrets:
        data = json.dumps({
            "salt": urlsafe_b64encode(salt).decode(),
            "key": encrypted_key.decode()  # because Fernet returns base64-encoded bytes
        })
        secrets.write(data)

def decrypt_fernet_key(password: str):
    with open(".filevault_config/secrets.json", "r") as secrets_file:
        try:
            secrets = json.loads(secrets_file.read())
            salt = urlsafe_b64decode(secrets["salt"])
            derived_key = generate_key_from_password(password, salt)
            fernet = Fernet(urlsafe_b64encode(derived_key))
            decrypted_key = fernet.decrypt(secrets["key"])
            return decrypted_key
        except InvalidToken:
            print("Invalid password, Exiting...")
            sys.exit(0)

def set_password():
    print("NOTE: If you lose your password, you will never be able to decrypt your files!")
    password = getpass.getpass("Create password to protect your FileVault: ")
    encrypt_fernet_key(password)
    return password


def get_or_create_key():
    key_path = Path(".filevault_config/secrets.json")
    if key_path.exists():
        password = getpass.getpass("Enter your password to access your FileVault: ")
        return decrypt_fernet_key(password)
    else:
        password = set_password()
        return decrypt_fernet_key(password)
