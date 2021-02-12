import logging
import base64
import requests


logger = logging.getLogger(__name__)


class SQAuth:
    APP_ID = "5ds1u73jqstrjkjivge8e3cb3q"
    APP_SECRET = "11ntmbq08pl40433hkq5oa6t9tdqmp55qd0ij9pp4anmkmivlikc"
    URL = "auth-synergyquantum.auth.us-east-2.amazoncognito.com"
    REDIRECT_URI = "https://localhost/test"

    def __init__(self):
        pass

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
        authorization_url = SQAuth.generate_authorization_endpoint_url(SQAuth.URL, SQAuth.APP_ID, SQAuth.REDIRECT_URI)
        print(
            "Please open the following url in your browser. You will be asked to login with your SynergyQuantum account. "
            "After a successful login, you will be redirected to a local web page. Please copy the url of the local web page "
            "and run:"
            "\nsq auth redirected_at {paste your redirect url here}. Merci!"
        )
        print(f"{authorization_url}")

    @classmethod
    def fetch_token(cls, auth_code):
        url = SQAuth.generate_token_endpoint_url(SQAuth.URL)
        authorization_header = SQAuth.generate_authorization_header(SQAuth.APP_ID, SQAuth.APP_SECRET)
        token_request = requests.post(url,
                                      data={
                                          "grant_type": "authorization_code",
                                          "client_id": SQAuth.APP_ID,
                                          "code": auth_code,
                                          "redirect_uri": SQAuth.REDIRECT_URI
                                      },
                                      headers={
                                          "Content-Type": "application/x-www-form-urlencoded",
                                          "Authorization": f"{authorization_header}"
                                      })
        print(token_request.text)

    @classmethod
    def verify_token(cls):
        pass
