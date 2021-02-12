import logging
import base64

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
        authorization_string = base64.b64decode(f"{app_id}:{app_secret}")
        authorization_header = f"Basic {authorization_string}"
        logger.info(f"Generating authorization header: {authorization_header}")
        return authorization_header

    @classmethod
    def generate_authorization_url(cls, url, client_id, redirect_uri):
        return f"https://{url}/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"

    @classmethod
    def generate_auth_key_url(cls):
        logger.info("Generating AWS Cognito URL for /authorize endpoint")
        authorization_url = SQAuth.generate_authorization_url(SQAuth.URL, SQAuth.APP_ID, SQAuth.REDIRECT_URI)
        print(
            "Please open the following url in your browser. You will be asked to login with your SynergyQuantum account. "
            "After a successful login, you will be redirected to a local web page. Please copy the url of the local web page "
            "and run:"
            "\nsq auth redirected_at {paste your redirect url here}. Merci!"
        )
        print(f"{authorization_url}")

    @classmethod
    def fetch_token(cls):
        pass

    @classmethod
    def verify_token(cls):
        pass
