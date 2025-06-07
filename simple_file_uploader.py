import os
import io
from tqdm import tqdm
import zstandard as zstd
from cryptography.fernet import Fernet
import traceback


CHUNK_SIZE = 4096
MB_RATE = 1_000_000
UPLOAD_DESTINATION = "Uploads"
DOWNLOAD_DESTINATION = "Downloads"

def main():
    print("Welcome to the FileVault!")
    operation = input("Please choose the operation:\n1. Upload\n2. Download\n")
    try:
        if int(operation) == 1:
            input_file = input("Please enter the file path: ")
            final_size = upload_chunks("Samples", input_file)
            print("\033[92m" + f"Successfully uploaded and compressed and encrypted, final file size: {final_size:.2f} MB" + "\033[0m")
        if int(operation) == 2:
            file_name = input("Enter the file name to download and decrypt: ")
            decrypted_file_path = download_file(DOWNLOAD_DESTINATION, file_name)
            print("\033[92m" + f"Successfully downloaded, file path: {DOWNLOAD_DESTINATION}/{decrypted_file_path}" + "\033[0m")
    except Exception as e:
        tb = traceback.TracebackException.from_exception(e)
        print("\033[91m" + f"Fatal error: {e}" + "\033[0m")
        for line in tb.format():
            print("\033[91m" + line.strip() + "\033[0m")

def upload_chunks(directory, file):
    upload_destination = f"{UPLOAD_DESTINATION}/{file}.zst.maz"
    cctx = zstd.ZstdCompressor(level=22)
    with io.BytesIO() as memory_buffer:
        
        with open(f"{directory}/{file}", "rb") as uploaded_file:
            size = os.path.getsize(filename=f"{directory}/{file}")
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
            with open(f"{upload_destination}", "wb") as encrypted_result:
                encrypted_result.write(encrypted_file)
    return (os.path.getsize(f"{upload_destination}") / MB_RATE)

# TODO: Make the Upload and download directories selectable by the user.
def download_file(directory, file): 
    decrypted_file_path = f"{DOWNLOAD_DESTINATION}/{file}".replace(".maz", "").replace(".zst", "")
    dctx = zstd.ZstdDecompressor()
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

if __name__ == '__main__':
    try:
        encryption_key = open("encryption_key.enc").read()
        fernet = Fernet(encryption_key)
    except OSError as e:
        print(f"Encryption key error: {e}")
    try:
        main()
    except KeyboardInterrupt:
        print("Bye!")




# import hashlib
# def md5(fname):
#     hash_md5 = hashlib.md5()
#     with open(fname, "rb") as f:
#         for chunk in iter(lambda: f.read(4096), b""):
#             hash_md5.update(chunk)
#     return hash_md5.hexdigest()