from minio import Minio
from minio.error import ResponseError


# Initialize minioClient with an endpoint and access/secret keys.
minioClient = Minio('play.min.io',
                  access_key='minioadmin',
                  secret_key='minioadmin',
                  secure=True)
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)



# Make a bucket with the make_bucket API call.
try:
       minioClient.make_bucket("sq_mk_test_bucket", location="us-east-1")
except BucketAlreadyOwnedByYou as err:
       pass
except BucketAlreadyExists as err:
       pass
except ResponseError as err:
       raise

# Put an object 'pumaserver_debug.log' with contents from 'pumaserver_debug.log'.
try:
       minioClient.fput_object('maylogs', 'pumaserver_debug.log', '/tmp/pumaserver_debug.log')
except ResponseError as err:
       print(err)
