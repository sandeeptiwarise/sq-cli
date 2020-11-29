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
    SQ_CONFIG_DIR = f"{USER_HOME_DIR}/.synerguquantum"
    SQ_CONFIG_FILE = f"{SQ_CONFIG_DIR}/config"
    SQ_CLIENT_KEY = f"{SQ_CONFIG_DIR}/sq.key"
    SQ_CLIENT_SECURE_DATA_DIR = f"{SQ_CONFIG_DIR}/mount10"
