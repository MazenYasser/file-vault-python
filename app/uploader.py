import io
import os
from zstandard import ZstdCompressor
from tqdm import tqdm
from pathlib import Path
from .config import CHUNK_SIZE, MB_RATE

def upload_file(vault, fernet, file: Path):
    cctx = ZstdCompressor(level=22)
    with io.BytesIO() as memory_buffer:
        
        with open(file, "rb") as uploaded_file:
            size = os.path.getsize(filename=f"{file}")
            print(f"File size before compression: {(size / MB_RATE)} MB")
            
            with cctx.stream_writer(memory_buffer, closefd=False) as compressor:
                with tqdm(total=size, unit='B', unit_scale=True, desc="Compressing") as progress_bar:
                    while chunk := uploaded_file.read(CHUNK_SIZE):
                        compressor.write(chunk)
                        progress_bar.update(len(chunk)) # Update progress bar manually
                
            memory_buffer.flush()
            memory_buffer.seek(0)
            compressed_file = memory_buffer.read()
            encrypted_file = fernet.encrypt(compressed_file)
            with open(f"{vault.config.upload_destination}/{file.name}.zst.maz", "wb") as encrypted_result:
                encrypted_result.write(encrypted_file)
    return (os.path.getsize(f"{vault.config.upload_destination}") / MB_RATE)