from cryptography.fernet import Fernet


class Qrypt:
    def __init__(self):
        pass

    def generate_key(self):
        key = Fernet.generate_key()
        return key

    def save_key(self, key, key_path):
        with open(f"{key_path}", "wb") as key_file:
            key_file.write(key)

    def load_key(self, key_path):
        with open(f"{key_path}", "r") as key_file:
            return key_file.read()

    def split_key(self):
        pass

    def recombine_key(self):
        pass

    def encypt(self):
        pass

    def decrypt(self):
        pass

