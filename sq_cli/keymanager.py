import json
import logging
import requests
from sq_cli.utils.config import get_config

logger = logging.getLogger(__name__)


class KeyManager:

    @classmethod
    def fetch_keyshares(cls, access_token):
        SQ_API_GATEWAY_URL = get_config('sq_api_gateway_url')
        response = requests.get(f"{SQ_API_GATEWAY_URL}/key", headers={
            "Authorization": f"Bearer {access_token}"
        })

        if response.status_code == 404:
            logger.error("Keyshares not found")
            return None
        elif response.status_code == 403:
            logger.error("Invalid Access Token. Please run `sq auth fetch-auth-code`")
        elif response.status_code == 200:
            logger.info(f"Keyshares retrieved: {response.text}")
            return json.loads(response.text)
        else:
            logger.error(f"Unexpected error occurred while fetching keyshares: Response Code {response.status_code}")
            return None

    @classmethod
    def upload_keyshares(cls, access_token, keyshares):
        SQ_API_GATEWAY_URL = get_config('sq_api_gateway_url')
        response = requests.post(f"{SQ_API_GATEWAY_URL}/key", headers={
            "Authorization": f"Bearer {access_token}"
        }, data=json.dumps(keyshares))
        status = response.status_code
        # 403, 400, 206, 500, 200
        if status == 403:
            logger.error("Invalid Access Token. Please use `sq auth fetch-auth-code`")
            return False
        elif status == 200:
            logger.info("Keyshares successfully uploaded")
            return True
        elif status in [206, 400, 500]:
            logger.error(response.text)
            return False
