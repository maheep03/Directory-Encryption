from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import MD5
import hashlib

from encrypt import protect_private_key
from decrypt import unprotect_private_key


def sign_aes_keys(secret_code: str) -> None:
    unprotect_private_key(secret_code=secret_code)

    # Load the private key
    with open('private.pem', 'rb') as f:
        private_key = RSA.import_key(f.read())

    # Calculate the MD5 hash of the encrypted AES keys file
    with open('aes_keys_chain.bin', 'rb') as f:
        data = f.read()
        md5_hash = hashlib.md5(data).digest()

    # Sign the hash with the private key
    signature = pkcs1_15.new(private_key).sign(MD5.new(md5_hash))
    with open('signature.bin', 'wb') as f:
        f.write(signature)


def verify_aes_keys(secret_code: str) -> None:
    # Load the public key
    with open('public.pem', 'rb') as f:  # will deny with publicFake.pem
        public_key = RSA.import_key(f.read())

    # Load the signature and the encrypted AES keys file
    with open('signature.bin', 'rb') as f:
        signature = f.read()
    with open('aes_keys_chain.bin', 'rb') as f:
        data = f.read()

    # Calculate the MD5 hash of the encrypted AES keys file
    md5_hash = hashlib.md5(data).digest()

    # Verify the signature
    try:
        pkcs1_15.new(public_key).verify(MD5.new(md5_hash), signature)
        print("The signature is valid.")
    except (ValueError, TypeError):
        print("The signature is not valid.")

    protect_private_key(secret_code=secret_code)
