from sq_cli.__version__ import __version__
from pathlib import Path


class Constants:
    def __init__(self):
        pass

    ASCII_VERSION_ART = f"""
        
  / ____|                                   / __ \                  | |                  
 | (___  _   _ _ __   ___ _ __ __ _ _   _  | |  | |_   _  __ _ _ __ | |_ _   _ _ __ ___  
  \___ \| | | | '_ \ / _ \ '__/ _` | | | | | |  | | | | |/ _` | '_ \| __| | | | '_ ` _ \ 
  ____) | |_| | | | |  __/ | | (_| | |_| | | |__| | |_| | (_| | | | | |_| |_| | | | | | |
 |_____/ \__, |_| |_|\___|_|  \__, |\__, |  \___\_\\__,_|\__,_|_| |_|\__|\__,_|_| |_| |_|
          __/ |                __/ | __/ |                                               
         |___/                |___/ |___/                                                

                                                                  version: {__version__}
    """

    USER_HOME_DIR = str(Path.home())
    SQ_CONFIG_DIR = str(Path(f"{USER_HOME_DIR}", ".synerguquantum"))
    SQ_CONFIG_FILE = str(Path(SQ_CONFIG_DIR, "config"))
    SQ_CONFIG_FILE_TEMPLATE_DICT = {
        "username": "maany",
        "server": "0.0.0.0:9000",
        "access_key": "minioadmin",
        "secret_key": "minioadmin",
        "key_stores": [
            {
                "host": "0.0.0.0",
                "port": "6379",
                "password": "redisadmin"
            },
            {
                "host": "0.0.0.0",
                "port": "6380",
                "password": "redisadmin"
            },
            {
                "host": "0.0.0.0",
                "port": "6381",
                "password": "redisadmin"
            }
        ],
        "aws_cognito_user_pool_url": "",
        "aws_cognito_client_id": "",
        "aws_cognito_client_secret": "",
        "aws_cognito_user_pool_id": "",
        "aws_cognito_user_pool_arn": "",

    }
    SQ_CLIENT_KEY = str(Path(f"{SQ_CONFIG_DIR}/sq.key"))
    SQ_CLIENT_SECURE_DATA_DIR = str(Path(f"{SQ_CONFIG_DIR}/mount10"))
    CQC_TEST_SANDBOX_CERT = '/Users/mayanksharma/Downloads/CQC_testing_cert.pfx'
    CQC_TEST_SANDBOX_CERT_PASS = '$Friday345'
