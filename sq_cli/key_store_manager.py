import redis
import logging

logger = logging.getLogger(__name__)


class KeyStoreManager:

    def __init__(self, key_stores):
        self.stores = []
        for store in key_stores:
            host = store['host']
            port = store['port']
            password = store['password']
            logger.debug(f"Connecting to KeyStore {host}:{port}")
            store = KeyStoreManager.connect(host, port, password)
            self.stores.append(store)

    @classmethod
    def connect(cls, host, port, password):
        return redis.Redis(host=host, port=port, password=password)

    def send_shares(self, db_key, shares):
        mapped_shares = list(zip(self.stores, shares))
        for store, share in mapped_shares:
            store.lpush(db_key, share)

    def retrieve_shares(self, db_key):
        shares = []
        for store in self.stores:
            shares.append(store.lpop(db_key).decode())
        self.send_shares(db_key, shares)
        return shares
