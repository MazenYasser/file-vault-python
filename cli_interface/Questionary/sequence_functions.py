import sys
from app.vault_app import FileVaultApp

def trigger_upload_sequence(question_bank, vault: FileVaultApp):
    selected_file = question_bank["select_file_upload"].ask()
    
    final_size = vault.upload(directory=vault.config.samples_path, file=selected_file)
    print("\033[92m" + f"Successfully uploaded and compressed and encrypted, final file size: {final_size:.2f} MB" + "\033[0m")

def trigger_download_sequence(question_bank, vault: FileVaultApp):
    file_name = question_bank["select_file_download"].ask()
    decrypted_file_path = vault.download(directory=vault.config.download_destination, file=file_name)
    print("\033[92m" + f"Successfully downloaded, file path: {vault.config.download_destination}/{decrypted_file_path}" + "\033[0m")

def trigger_exit_sequence(question_bank, vault: FileVaultApp):
    print("Bye!")
    sys.exit(0)