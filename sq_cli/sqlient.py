from cryptography.fernet import Fernet

from sq_cli.key_store_manager import KeyStoreManager
from sq_cli.mount10 import Mount10
from sq_cli.qrypt import Qrypt
import os
import logging

from sq_cli.utils import Constants

logger = logging.getLogger(__name__)


class SQlient:
    def __init__(self, name, server_ip, server_access_key, server_secret_key, key_stores):
        self.name = name
        self.buckets = [f"bucket-1-{name}"]
        self.mount10 = Mount10(self.name, server_ip, server_access_key, server_secret_key)
        self.key_store_manager = KeyStoreManager(key_stores)

        if not os.path.exists(Constants.SQ_CLIENT_KEY):
            self.key = Qrypt.generate_key()
            Qrypt.save_key(self.key, Constants.SQ_CLIENT_KEY)
        else:
            self.key = Qrypt.load_key(Constants.SQ_CLIENT_KEY)

        for bucket in self.buckets:
            try:
                self.mount10.create_bucket(bucket)
            except Exception as err:
                logging.error(err)
