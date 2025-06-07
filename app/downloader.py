from zstandard import ZstdDecompressor
from .config import UPLOAD_DESTINATION, CHUNK_SIZE


# TODO: Make the Upload and download directories selectable by the user.
def download_file(fernet, directory, file): 
    decrypted_file_path = f"{directory}/{file}".replace(".maz", "").replace(".zst", "")
    dctx = ZstdDecompressor()
    with open(decrypted_file_path, "wb") as decrypted_output:
        with open(f"{UPLOAD_DESTINATION}/{file}", "rb") as encrypted_file:
            content = encrypted_file.read()
            decrypted_file = fernet.decrypt(content)
        
        reader = dctx.stream_reader(decrypted_file)
        while True:
            chunk = reader.read(CHUNK_SIZE)
            if not chunk:
                break
            decrypted_output.write(chunk)
   
    return decrypted_file_path
