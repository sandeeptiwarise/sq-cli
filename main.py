from minio import Minio
from minio.error import ResponseError


# Initialize minioClient with an endpoint and access/secret keys.
minioClient = Minio('3.121.232.99:9000',
                  access_key='minioadmin',
                  secret_key='minioadmin',
                  secure=False)
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)



# Make a bucket with the make_bucket API call.
try:
       minioClient.make_bucket("sq-test-bucket", location="us-east-1")
except BucketAlreadyOwnedByYou as err:
       pass
except BucketAlreadyExists as err:
       pass
except ResponseError as err:
       raise

# Put an object 'pumaserver_debug.log' with contents from 'pumaserver_debug.log'.
try:
       minioClient.fput_object('sq-test-bucket', 'file1.txt', 'data/file1.txt')
except ResponseError as err:
       print(err)
