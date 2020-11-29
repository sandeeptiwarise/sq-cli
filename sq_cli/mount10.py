from minio import ResponseError, Minio
from minio.error import BucketAlreadyOwnedByYou, BucketAlreadyExists
import logging

logger = logging.getLogger(__name__)


class Mount10:
    def __init__(self, client_name, server_ip, server_access_key, server_secret_key):
        self.buckets = [f"{client_name}-bucket-01"]
        self.server_info = {
            "ip": server_ip,
            "access_key": server_access_key,
            "secret_key": server_secret_key
        }

        self.minio = self.connect(
            self.server_info["ip"],
            self.server_info["access_key"],
            self.server_info["secret_key"]
        )

    def connect(self, server, access_key, secret_key):
        """
        :param server IP:Port of the Minio Server
        :param access_key of the server
        :param secret_key of the server
        :return: MinioClient object connected to our server
        """
        minioClient = Minio(server,
                            access_key,
                            secret_key,
                            secure=False)
        return minioClient

    def create_bucket(self, bucket):
        # Make a bucket with the make_bucket API call.
        try:
            self.minio.make_bucket(bucket, location="us-east-1")
        except BucketAlreadyOwnedByYou as err:
            pass
        except BucketAlreadyExists as err:
            pass
        except ResponseError as err:
            raise
        return bucket

    def put_object(self, bucket, remote_object_name, local_object_path):
        try:
            self.minio.fput_object(bucket, remote_object_name, local_object_path)
        except ResponseError as err:
            logging.error(err)

    def get_object(self, bucket, remote_object_name, local_object_path):
        try:
            self.minio.fget_object(bucket, remote_object_name, local_object_path)
        except ResponseError as err:
            logging.error(err)

