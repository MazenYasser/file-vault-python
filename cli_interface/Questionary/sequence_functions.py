import sys
from pathlib import Path
from app.vault_app import FileVaultApp
from app.config import manual_config

def trigger_upload_sequence(question_bank, vault: FileVaultApp):
    selected_file = question_bank["select_file_upload"].ask()
    selected_file = selected_file.replace("'", "")
    selected_file = Path(selected_file)
    final_size = vault.upload(file=selected_file)
    print("\033[92m" + f"Successfully uploaded and compressed and encrypted, final file size: {final_size:.2f} MB" + "\033[0m")

def trigger_download_sequence(question_bank, vault: FileVaultApp):
    file_name = question_bank["select_file_download"].ask()
    decrypted_file_path = vault.download(directory=vault.config.download_destination, file=file_name)
    print("\033[92m" + f"Successfully downloaded, file path: {vault.config.download_destination}/{decrypted_file_path}" + "\033[0m")

def trigger_config_change_sequence(question_bank, vault: FileVaultApp):
    manual_config(vault.config_path)

def trigger_exit_sequence(question_bank, vault: FileVaultApp):
    print("Bye!")
    sys.exit(0)
