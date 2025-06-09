import sys
import traceback

from cryptography.fernet import Fernet

from app import settings
from app.config import get_or_create_config, initialize_config
from app.vault_app import FileVaultApp
from cli_interface.Questionary.questionary_tui import QuestionaryTUI
from encryption_key_generator import get_or_create_key


def main(fernet, config):
    vault = FileVaultApp(fernet, config)
    print("🔒 Welcome to the FileVault! ")
    try:
        ui = QuestionaryTUI(vault=vault)
        while True:
            ui.run()
    except KeyboardInterrupt:
        print("Bye!")
        sys.exit(0)
    except Exception as e:
        tb = traceback.TracebackException.from_exception(e)
        print("\033[91m" + f"Fatal error: {e}" + "\033[0m")
        for line in tb.format():
            print("\033[91m" + line.strip() + "\033[0m")

if __name__ == '__main__':
    try:
        # Load the encryption key
        encryption_key = get_or_create_key()
        fernet = Fernet(encryption_key)
        # Setup the config paths and create files if not existing
        config_path, default_config_path = initialize_config()
        # Prompt user to use default or input manual config
        config = get_or_create_config(config_path, default_config_path)
        # Make config class and path global for access through the settings module
        settings.configure(config, str(config_path))
        main(fernet, config)
    except OSError as e:
        print(f"App startup error: {e}")
        tb = traceback.TracebackException.from_exception(e)
        for line in tb.format():
            print("\033[91m" + line.strip() + "\033[0m")
