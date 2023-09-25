import yaml

from key_generation import generate_keys_aes, generate_rsa_key
from encrypt import encrypt_files, encrypt_aes_keys, protect_private_key
from sign_and_verify import sign_aes_keys, verify_aes_keys


def start_service():
    # Read config file
    try:
        with open('config.yml') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError:
        print('YAML read error')
        print('Encryption service stopped')
        exit(1)

    # Generate AES keys and RSA keys
    key_dict = generate_keys_aes(config['key_size'], config['files'])
    generate_rsa_key(config['public_key'], config['private_key'])
    print('Keys generated')

    # store AES keys in aes_keys_chain.bin and encrypt it with RSA
    encrypt_aes_keys(key_dict)
    print('AES keys encrypted')

    # protect private key with a secret code
    code = input('Enter secret code: ')
    protect_private_key(secret_code=code)
    print('Private key protected')

    # sign aes_keys_chain.bin with private key
    # sign_aes_keys() temporarily removes private key protection to make the signature
    sign_aes_keys(secret_code=code)
    print('AES keys signed')

    # verify signature with public key and restore private key protection
    verify_aes_keys(secret_code=code)

    # encrypt files with AES keys
    encrypt_files(key_dict, config['directories'])
    print('Files encrypted')

    print('Encryption service stopped')


if __name__ == '__main__':
    start_service()
