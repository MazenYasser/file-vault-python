import traceback
from cryptography.fernet import Fernet
from app.config import *
from cli_interface.Questionary.questionary_tui import QuestionaryTUI
from app.vault_app import FileVaultApp


def main(fernet):
    vault = FileVaultApp(fernet)
    print("🔒 Welcome to the FileVault! ")
    try:
        ui = QuestionaryTUI(vault=vault)
        while True:
            ui.run()
    except Exception as e:
        tb = traceback.TracebackException.from_exception(e)
        print("\033[91m" + f"Fatal error: {e}" + "\033[0m")
        for line in tb.format():
            print("\033[91m" + line.strip() + "\033[0m")

if __name__ == '__main__':
    try:
        encryption_key = open("keys/encryption_key.enc").read()
        fernet = Fernet(encryption_key)
        main(fernet)
    except OSError as e:
        print(f"Encryption key error: {e}")
    except KeyboardInterrupt:
        print("Bye!")




# import hashlib
# def md5(fname):
#     hash_md5 = hashlib.md5()
#     with open(fname, "rb") as f:
#         for chunk in iter(lambda: f.read(4096), b""):
#             hash_md5.update(chunk)
#     return hash_md5.hexdigest()
