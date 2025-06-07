from .uploader import upload_chunks
from .downloader import download_file

class FileVaultApp:
    def __init__(self, fernet):
        self.fernet = fernet
        # self.config = config
    
    def upload(self, directory, file):
        """
        Uploads the file to the vault

        Args:
            directory (str): Path to the folder that contains the file
            file (str): The file name to upload
        """
        return upload_chunks(fernet=self.fernet, directory=directory, file=file)
        
    
    def download(self, directory, file):
        """
        Downloads the file from the vault to select destination

        Args:
            directory (str): Download destination
            file (str): The file name to download
        """
        return download_file(fernet=self.fernet, directory=directory, file=file)
