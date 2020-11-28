from cryptography.fernet import Fernet


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

    def split_key(self):
        pass

    def recombine_key(self):
        pass

    def encrypt_file(self, file):
        print('Reading File')

        with open(file, "rb") as fp:
            file_data = fp.read()
            encrypted_data = self.key.encrypt(file_data)

        print('Saving encrypted file')

        with open(file, "wb") as fp:
            fp.write(encrypted_data)

    def decrypt_file(self, encrypted_file):
        """
            Given a filename (str) and key (bytes), it decrypts the file and write it
        """
        print(f"Reading Encrypted File {encrypted_file}")
        with open(encrypted_file, "rb") as file:
            # read the encrypted data
            encrypted_data = file.read()
        print(f"Decrypting File {encrypted_file}")

        # decrypt data
        decrypted_data = self.key.decrypt(encrypted_data)

        print(f"Saving decrypted file {encrypted_file}")
        # write the original files
        with open(encrypted_file, "wb") as fp:
            fp.write(decrypted_data)

    def encrypt_message(self, message):
        print(f"Encrypting {message}")
        return self.key.encypt(message)

    def decrypt_message(self, encrypted_message):
        decrypted = self.key.decrypt(encrypted_message)
        print(f"Decrypted Message: {decrypted}")
        return decrypted
