from cryptography.fernet import Fernet


class Qrypt:
    def __init__(self):
        pass

    def generate_key(self, key_path):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)

    def split_key(self):
        pass

    def recombine_key(self):
        pass

    def encypt(self):
        pass

    def decrypt(self):
        pass

