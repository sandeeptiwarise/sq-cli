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
        elif response.status_code == 200:
            logger.info(f"Keyshares retrieved: {response.text}")
            return json.loads(response.text)
        else:
            logger.error(f"Unexpected error occurred while fetching keyshares: Response Code {response.status_code}")
            return None
