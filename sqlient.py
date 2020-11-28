from mount10 import Mount10
from qrypt import Qrypt
import os


class SQlient:
    def __init__(self, name):
        self.name = name
        self.buckets = []
        self.mount10 = Mount10(self.name)
        self.qrypt = Qrypt()

        home_dir = os.getenv("HOME")
        self.local_dir_path = f"{home_dir}/synergy-quantum/{self.name}/"
        try:
            os.mkdir(self.local_dir_path)
        except Exception as err:
            print(err)

        self.key_path = f"{self.local_dir_path}/key"
        self.key = self.qrypt.generate_key(key_path=self.key_path)

        for bucket in self.buckets:
            try:
                self.mount10.create_bucket(bucket)
            except Exception as err:
                print(err)
