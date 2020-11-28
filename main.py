from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)


class SQrypt:
    def __init__(self):
        self.minioClient = self.connect(
            '3.121.232.99:9000',
            access_key='minioadmin',
            secret_key='minioadmin'
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
            self.minioClient.make_bucket(bucket, location="us-east-1")
        except BucketAlreadyOwnedByYou as err:
            pass
        except BucketAlreadyExists as err:
            pass
        except ResponseError as err:
            raise
        return bucket

    def encrypt_file(self):
        pass

    def decrypt_file(self):
        pass

    def upload_file(self, bucket, remote_file, local_file):
        try:
            self.minioClient.fput_object(bucket, remote_file, local_file)
        except ResponseError as err:
            print(err)

    def download_file(self):
        pass


if __name__ == '__main__':
    sqrypt = SQrypt()
    bucket = sqrypt.create_bucket("another-bucket")
    sqrypt.upload_file(bucket, "file1.txt", "data/file1.txt")
