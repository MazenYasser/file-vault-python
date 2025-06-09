from zstandard import ZstdDecompressor
from tqdm import tqdm
from app import settings

from .config import CHUNK_SIZE

def download_file(fernet, directory, file): 
    config = settings.get_config()
    decrypted_file_path = f"{directory}/{file}".replace(".maz", "").replace(".zst", "")
    dctx = ZstdDecompressor()

    with open(decrypted_file_path, "wb") as decrypted_output:
        with open(f"{config.upload_destination}/{file}", "rb") as encrypted_file:
            content = encrypted_file.read()
            decrypted_file = fernet.decrypt(content)

        total_size = len(decrypted_file)
        reader = dctx.stream_reader(decrypted_file)

        with tqdm(total=total_size, desc="Decompressing", unit="B", unit_scale=True) as progress:
            while True:
                chunk = reader.read(CHUNK_SIZE)
                if not chunk:
                    break
                decrypted_output.write(chunk)
                progress.update(len(chunk))

    return decrypted_file_path