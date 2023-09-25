from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


def generate_keys_aes(key_size: int, file: list) -> 'dict[str, bytes]':
    key_dict = {}
    byte_size = key_size // 8

    # Generate AES keys for each file extension
    for ext in file:
        key_dict[ext] = get_random_bytes(byte_size)

    return key_dict


def generate_rsa_key(public: str, private: str) -> None:
    # Generate private key pair for 2048 bits
    key_pair = RSA.generate(2048)

    # Save private key
    with open(private, 'wb') as f:
        f.write(key_pair.export_key())

    # Save public key
    with open(public, 'wb') as f:
        f.write(key_pair.publickey().export_key())
