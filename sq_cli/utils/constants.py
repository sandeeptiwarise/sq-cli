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
    SQ_CONFIG_DIR = Path(f"{USER_HOME_DIR}/.synerguquantum").name
    SQ_CONFIG_FILE = Path(f"{SQ_CONFIG_DIR}/config").name
    SQ_CONFIG_FILE_TEMPLATE_DICT = {
        "username": "",
        "server": "IP_ADDRESS:PORT",
        "access_key": "replace with access key",
        "secret_key": "replace with secret key",
        "key_stores": [
            {
                "host": "",
                "port": "",
                "password": ""
            },
            {
                "host": "",
                "port": "",
                "password": ""
            },
            {
                "host": "",
                "port": "",
                "password": ""
            }
        ]
    }
    SQ_CLIENT_KEY = Path(f"{SQ_CONFIG_DIR}/sq.key").name
    SQ_CLIENT_SECURE_DATA_DIR = Path(f"{SQ_CONFIG_DIR}/mount10").name
