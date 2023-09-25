import os
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES


def decrypt_files(key_dict: 'dict[str, bytes]', directories: list) -> None:
    # decrypt each file in each directory with the corresponding AES key
    for key in key_dict:
        for dir_path in directories:
            for file_name in os.listdir(dir_path):
                if file_name.endswith('.' + key + '.encrypted'):
                    current_file_path = os.path.join(dir_path, file_name)
                    enc_file_path = os.path.join(dir_path, file_name[:-10])
                    decrypt_file_aes(key_dict[key], current_file_path, enc_file_path)

                    print('File decrypted: ' + file_name[:-10])
                    time.sleep(1)
                    os.remove(current_file_path)


def decrypt_file_aes(key: bytes, current_file: str, decrypted_file: str):
    with open(current_file, 'rb') as cf, open(decrypted_file, 'wb') as df:
        # Read IV(initialization vector)
        iv = cf.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, iv)

        while True:
            # Read file in chunks
            chunk = cf.read(64 * 1024)
            if len(chunk) == 0:
                break

            # Write decrypted chunk to output file
            df.write(decryptor.decrypt(chunk))

        # Remove padding from the last chunk
        df.truncate(os.path.getsize(decrypted_file) - df.tell())


def unprotect_private_key(secret_code: str) -> None:

    # Read and decrypt encrypted private key
    encoded_key = open("private.pem", "rb").read()
    key = RSA.import_key(encoded_key, passphrase=secret_code)

    with open('private.pem', 'wb') as f:
        f.write(key.export_key())
