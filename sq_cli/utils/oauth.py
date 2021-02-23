from urllib import parse
import logging

logger = logging.getLogger(__name__)


def extract_auth_code(redirect_uri):
    query_string = parse.urlsplit(redirect_uri).query
    auth_code = dict(parse.parse_qsl(query_string))['code']
    logger.info(f"Authorization code: {auth_code} extracted from url {redirect_uri}")
    return auth_code
