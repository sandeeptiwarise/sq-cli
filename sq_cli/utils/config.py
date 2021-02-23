import json

from sq_cli.utils.constants import Constants


def get_config(key):
    with open(Constants.SQ_CONFIG_FILE, 'r') as f:
        config = json.load(f)
        value = config.get(key, None)
        return value


def save_config(key, value):
    with open(Constants.SQ_CONFIG_FILE, 'r+') as f:
        config = json.load(f)
        config[key] = value
        f.seek(0)
        f.write(json.dumps(config, indent=4))
        return config
