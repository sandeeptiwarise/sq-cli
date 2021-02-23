import json
import logging
import base64
import traceback

import requests
from sq_cli.utils.config import get_config, save_config

logger = logging.getLogger(__name__)


class SQAuth:

    @classmethod
    def generate_authorization_header(cls, app_id, app_secret):
        authorization_string = f"{app_id}:{app_secret}"
        authorization_string_bytes = authorization_string.encode('ascii')
        base64_bytes = base64.b64encode(authorization_string_bytes)
        base64_header = base64_bytes.decode('ascii')
        authorization_header = f"Basic {base64_header}"
        logger.info(f"Generating authorization header: {authorization_header}")
        return authorization_header

    @classmethod
    def generate_authorization_endpoint_url(cls, url, client_id, redirect_uri):
        return f"https://{url}/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"

    @classmethod
    def generate_token_endpoint_url(cls, url):
        return f"https://{url}/oauth2/token"

    @classmethod
    def generate_auth_key_url(cls):
        logger.info("Generating AWS Cognito URL for /authorize endpoint")
        APP_ID = get_config('aws_cognito_client_id')
        URL = get_config('aws_cognito_user_pool_url')
        REDIRECT_URI = get_config('aws_cognito_redirect_url')
        authorization_url = SQAuth.generate_authorization_endpoint_url(URL, APP_ID, REDIRECT_URI)
        print(
            "Please open the following url in your browser. You will be asked to login with your SynergyQuantum account. "
            "After a successful login, you will be redirected to a local web page. Please copy the url of the local web page "
            "and run:"
            "\nsq auth redirected_at {paste your redirect url here}. Merci!"
        )
        print(f"{authorization_url}")

    @classmethod
    def fetch_token(cls, auth_code):
        APP_ID = get_config('aws_cognito_client_id')
        APP_SECRET = get_config('aws_cognito_client_secret')
        URL = get_config('aws_cognito_user_pool_url')
        REDIRECT_URI = get_config('aws_cognito_redirect_url')
        url = SQAuth.generate_token_endpoint_url(URL)
        authorization_header = SQAuth.generate_authorization_header(APP_ID, APP_SECRET)
        token_request = requests.post(url,
                                      data={
                                          "grant_type": "authorization_code",
                                          "client_id": APP_ID,
                                          "code": auth_code,
                                          "redirect_uri": REDIRECT_URI
                                      },
                                      headers={
                                          "Content-Type": "application/x-www-form-urlencoded",
                                          "Authorization": f"{authorization_header}"
                                      })
        res = token_request.text
        logger.info(f"Tokens Received: {res}")
        tokens = json.loads(res)
        access_token = ''
        try:
            access_token = tokens['access_token']
            logger.info('Saving access token to configuration file....')
            save_config('aws_cognito_access_token', access_token)

            refresh_token = tokens['refresh_token']
            logger.info('Saving Refresh token to configuration file....')
            save_config('aws_cognito_refresh_token', refresh_token)
        except Exception as e:
            logger.error('Auth Code expired. Re-run sq auth fetch-auth-code')
            exit()

        print(f"Access Token: {access_token}")
        return access_token
    @classmethod
    def verify_token(cls, access_token):
        SQ_API_GAETEWAY_URL = get_config('sq_api_gateway_url')
        # send request to SQ API Gateway using API endpoint
        response = requests.get(f"{SQ_API_GAETEWAY_URL}/validate", headers={
            "Authorization": f"Bearer {access_token}"
        })
        print(response.text)
