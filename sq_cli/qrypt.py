from cryptography.fernet import Fernet
import logging

logger = logging.getLogger(__name__)

class Qrypt:
    def __init__(self, key):
        self.key = Fernet(key)

    @classmethod
    def generate_key(cls):
        key = Fernet.generate_key()
        return key

    @classmethod
    def save_key(cls, key, key_path):
        with open(f"{key_path}", "wb") as key_file:
            key_file.write(key)

    @classmethod
    def load_key(cls, key_path):
        with open(f"{key_path}", "r") as key_file:
            return key_file.read()

    @classmethod
    def split_key(cls, key):
        pass

    @classmethod
    def recombine_key(cls):
        pass

    @classmethod
    def encrypt_file(cls, key, local_file, encrypted_local_file):
        print('Reading File')

        with open(local_file, "rb") as fp:
            file_data = fp.read()
            encrypted_data = key.encrypt(file_data)

        print('Saving encrypted file')

        with open(encrypted_local_file, "wb") as fp:
            fp.write(encrypted_data)

    @classmethod
    def decrypt_file(cls, key, encrypted_local_file, decrypted_local_file):
        """
            Given a filename (str) and key (bytes), it decrypts the file and write it
        """
        print(f"Reading Encrypted File {encrypted_local_file}")
        with open(encrypted_local_file, "rb") as file:
            # read the encrypted data
            encrypted_data = file.read()
        print(f"Decrypting File {encrypted_local_file}")

        # decrypt data
        decrypted_data = key.decrypt(encrypted_data)

        print(f"Saving decrypted file {decrypted_local_file}")
        # write the original files
        with open(decrypted_local_file, "wb") as fp:
            fp.write(decrypted_data)

    @classmethod
    def encrypt_message(cls, key, message):
        print(f"Encrypting {message}")
        return key.encypt(message)

    @classmethod
    def decrypt_message(cls, key, encrypted_message):
        decrypted = key.decrypt(encrypted_message)
        print(f"Decrypted Message: {decrypted}")
        return decrypted
