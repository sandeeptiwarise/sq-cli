from mount10 import Mount10


class Client:
    def __init__(self, name):
        self.name = name
        self.mount10 = Mount10(self.name)

