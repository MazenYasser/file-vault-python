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
    """
    Derives a cryptographic key from a password and salt using PBKDF2-HMAC-SHA256.

    Args:
        password (str): The input password from which to derive the key.
        salt (bytes): A cryptographically secure random salt.

    Returns:
        bytes: The derived 32-byte cryptographic key.

    Raises:
        TypeError: If the password is not a string or the salt is not bytes.
        Exception: If key derivation fails for any reason.
    """
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
    """
    Encrypts a newly generated Fernet key using a password-derived key and stores the encrypted key and salt in a JSON file.

    Args:
        password (str): The password used to derive the encryption key.

    Side Effects:
        - Generates a random salt and Fernet key.
        - Encrypts the Fernet key with a key derived from the provided password.
        - Writes the salt and encrypted Fernet key to '.filevault_config/secrets.json' in JSON format.

    Raises:
        Any exceptions raised by file I/O, key generation, or encryption operations.
    """
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
    """
    Decrypts and returns the Fernet encryption key using a password.

    This function reads the encrypted Fernet key and salt from the secrets.json file,
    derives a key from the provided password and salt, and attempts to decrypt the Fernet key.
    If the password is invalid, the function prints an error message and exits the program.

    Args:
        password (str): The password used to derive the decryption key.

    Returns:
        bytes: The decrypted Fernet key.

    Raises:
        SystemExit: If the provided password is invalid and decryption fails.
    """
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
    """
    Prompts the user to create a password for protecting their FileVault, warns about the importance of remembering the password,
    and uses the provided password to encrypt the Fernet key.

    Returns:
        str: The password entered by the user.
    """
    print("NOTE: If you lose your password, you will never be able to decrypt your files!")
    password = getpass.getpass("Create password to protect your FileVault: ")
    encrypt_fernet_key(password)
    return password


def get_or_create_key():
    """
    Retrieves or creates an encryption key for the FileVault.

    If the secrets file exists, prompts the user for their password and returns the decrypted Fernet key.
    If the secrets file does not exist, prompts the user to set a new password and returns the decrypted Fernet key.

    Returns:
        bytes: The decrypted Fernet encryption key.

    Raises:
        Exception: If password verification or decryption fails.
    """
    key_path = Path(".filevault_config/secrets.json")
    if key_path.exists():
        password = getpass.getpass("Enter your password to access your FileVault: ")
        return decrypt_fernet_key(password)
    else:
        key_path.parent.mkdir(parents=True, exist_ok=True)
        password = set_password()
        return decrypt_fernet_key(password)
