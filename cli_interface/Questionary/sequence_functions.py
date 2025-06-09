import sys
import shlex
from pathlib import Path

from questionary import Question

from app.config import manual_config
from app import settings
from app.vault_app import FileVaultApp


def trigger_upload_sequence(question_bank: dict[str, Question], vault: FileVaultApp):
    choice = question_bank["select_file_upload"].ask()
    if choice is None: # choice being none means a KeyboardInterrupt occured, a limitation of questionary.
        return # Return to main menu
    selected_file = shlex.split(choice)[0]
    selected_file = Path(selected_file)
    final_size = vault.upload(file=selected_file)
    print("\033[92m" + f"Successfully uploaded and compressed and encrypted, final file size: {final_size:.2f} MB" + "\033[0m")

def trigger_download_sequence(question_bank: dict[str, Question], vault: FileVaultApp):
    config = settings.get_config()
    choice = question_bank["select_file_download"].ask()
    if choice == "Go Back ⬅":
        return # Return to main menu
    decrypted_file_path = vault.download(directory=config.download_destination, file=choice)
    print("\033[92m" + f"Successfully downloaded, file path: {vault.config.download_destination}/{decrypted_file_path}" + "\033[0m")

def trigger_config_change_sequence(question_bank: dict[str, Question], vault: FileVaultApp):
    config_path = settings.get_config_path()
    manual_config(config_path)

def trigger_exit_sequence(question_bank: dict[str, Question], vault: FileVaultApp):
    print("Bye!")
    sys.exit(0)
