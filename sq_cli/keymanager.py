import json
import logging
import base64
import requests
import jwt

logger = logging.getLogger(__name__)


class KeyManager:
    APP_ID = "5ds1u73jqstrjkjivge8e3cb3q"
    APP_SECRET = "11ntmbq08pl40433hkq5oa6t9tdqmp55qd0ij9pp4anmkmivlikc"
    URL = "auth-synergyquantum.auth.us-east-2.amazoncognito.com"
    REDIRECT_URI = "https://localhost/test"
    SQ_API_GAETEWAY_URL = "http://0.0.0.0:8000/api"

    def __init__(self):
        pass


    @classmethod
    def recieve_keys(cls, access_token):
        
        #send request to SQ API Gateway using API endpoint
        response = requests.get(f"{KeyManager.SQ_API_GAETEWAY_URL}/key",headers={
            "Authorization": f"Bearer {access_token}" 
        } )
        print(response.text)

  