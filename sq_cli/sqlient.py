from sq_cli.key_store_manager import KeyStoreManager
from sq_cli.mount10 import Mount10
from sq_cli.qrypt import Qrypt
import logging

logger = logging.getLogger(__name__)


class SQlient:
    def __init__(self, name, server_ip, server_access_key, server_secret_key, key_stores):
        self.name = name
        self.buckets = [f"bucket-1-{name}"]
        self.mount10 = Mount10(self.name, server_ip, server_access_key, server_secret_key)
        self.key_store_manager = KeyStoreManager(key_stores)
        self.key = None
        try:
            logger.debug("Trying to fetch key shares...")
            shares = self.key_store_manager.retrieve_shares(self.name)
            logger.debug(f"Fetched the following key shares: {shares}")
            logger.debug(f"Generating user's key from key shares...")
            self.key = Qrypt.recombine_key(shares)
            logger.debug(f"User's Master Key {self.key}")
        except Exception as err:
            logging.debug(f"Could not find user {self.name}'s key on the key stores.")
            logging.error(err)
            logging.debug(f"Generating new key for user {self.name}")
            self.key = Qrypt.generate_key()
            logging.debug(f"Splitting key into key shares")
            shares = Qrypt.split_key(self.key)
            logging.debug(f"Uploading the following key shares to the key stores: {shares}")
            self.key_store_manager.send_shares(self.name, shares)

        # if not os.path.exists(Constants.SQ_CLIENT_KEY):
        #     self.key = Qrypt.generate_key()
        #     Qrypt.save_key(self.key, Constants.SQ_CLIENT_KEY)
        # else:
        #     self.key = Qrypt.load_key(Constants.SQ_CLIENT_KEY)

        for bucket in self.buckets:
            try:
                logging.debug(f"Checking if bucket {self.buckets[0]} exists on Mount10")
                self.mount10.create_bucket(bucket)
                logging.debug(f"Bucket {self.buckets[0]} created for {self.name} on Mount10")
            except Exception as err:
                logging.debug(f"Bucket {self.buckets[0]} already exists on Mount10")
                logging.error(err)
