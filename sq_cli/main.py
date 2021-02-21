import shutil
import sys
from urllib import parse

import click
import logging
import os

from sq_cli.cqc import CQCAdapter
from sq_cli.qrypt import Qrypt
from sq_cli.utils import config_root_logger, generate_configuration_template, get_client
from sq_cli.utils.config import get_config
from sq_cli.utils.constants import Constants
from sq_cli.sqauth import SQAuth
from sq_cli.keymanager import KeyManager
from sq_cli.utils.oauth import extract_auth_code

logger = logging.getLogger(__name__)


class Session:
    def __init__(self):
        self.config = {}
        self.verbose = False
        self.ascii_art = Constants.ASCII_VERSION_ART
        self.is_configured = False

    def set_config(self, key, value):
        self.config[key] = value
        if self.verbose:
            logger.debug('  config[%s] = %s' % (key, value), file=sys.stderr)


pass_session = click.make_pass_decorator(Session)


def validate_config():
    if not os.path.exists(Constants.SQ_CONFIG_DIR) or not os.path.exists(Constants.SQ_CLIENT_KEY) or not os.path.exists(
            Constants.SQ_CONFIG_FILE):
        click.echo("SQ CLI is not configured. Please run $> sq config")
        logger.error("Client Configuration FAILED!")
        return False
    else:
        logging.debug("SQ CLI is properly configured")
        return True


@click.group()
@click.option('--verbose', '-v',
              count=True,
              help="Set verbosity level. Select between -v, -vv or -vvv.")
@click.option('--mode', '-m',
              type=click.Choice(['api', 'standalone'], case_sensitive=False),
              help="In API mode, output is JSON encoded. Default is standalone",
              default='standalone')
@click.pass_context
def cli(ctx, verbose, mode):
    ctx.obj = Session()
    config_root_logger(verbose, mode)


@cli.command()
@click.pass_context
def version(ctx):
    click.echo(ctx.obj.ascii_art)


@cli.command()
@click.pass_context
def init(ctx):
    """
    Initialize the SQ CLI for a new user
    """
    # Check if SQ Config Dir exists
    if os.path.exists(Constants.SQ_CONFIG_DIR):
        logger.info(f"SQ configuration directory exists: {Constants.SQ_CONFIG_DIR}")
    else:
        logger.error(f"SQ configuration directory NOT FOUND: {Constants.SQ_CONFIG_DIR}")
        logger.debug(f"Creating SQ configuration directory: {Constants.SQ_CONFIG_DIR}")
        os.mkdir(Constants.SQ_CONFIG_DIR)

    # Check if SQ config exists
    if os.path.exists(Constants.SQ_CONFIG_FILE):
        logger.debug(f"Found SQ Configuration in the config file: {Constants.SQ_CONFIG_DIR}")
    else:
        logger.error(f"SQ Configuration Not FOUND: {Constants.SQ_CONFIG_DIR}")
        generate_configuration_template()
        click.echo(f"Generated template of SQ configuration file {Constants.SQ_CONFIG_FILE}")
        click.echo("Please fill out the configuration parameters in the template carefully and re-run `sq init`")
        return

    user = get_config('username')
    click.echo(Constants.ASCII_VERSION_ART)
    click.echo(f"SQ CLI is properly initialized for user {user}. Please run `sq config` to configure the CLI.")
    ctx.obj.is_configured = True


@cli.command()
def config():
    """
    Configure Synergy Quantum CLI.
    """
    # Get token
    oauth_token = get_config('aws_cognito_access_token')
    if oauth_token is '' or oauth_token is None:
        SQAuth.generate_auth_key_url()
        redirect_uri = click.prompt("Paste your redirection uri here: ")
        auth_code = extract_auth_code(redirect_uri)
        logger.info(f"Fetching access_token for auth_code: {auth_code}")
        SQAuth.fetch_token(auth_code)
    else:
        logger.info("OAuth Token found!")

    # Get Key
    # check if user's key exists remotely via SQ API Gateway
    access_token = get_config('aws_cognito_access_token')
    print(f"8888 {access_token}")
    keyshares = KeyManager.fetch_keyshares(access_token=access_token)
    if keyshares is None:
        if os.path.exists(Constants.SQ_CLIENT_KEY):
            logger.info(f"SQ Key found: {Constants.SQ_CLIENT_KEY}")
        else:
            logger.info(f"Generating new SQ Key and saving to {Constants.SQ_CLIENT_KEY}")
            key = Qrypt.generate_key()
            Qrypt.save_key(key, Constants.SQ_CLIENT_KEY)

        logger.info("Loading local copy of user's key")
        key_as_text = Qrypt.load_key_as_text(Constants.SQ_CLIENT_KEY)
        shares = Qrypt.split_key(key_as_text)
        # upload shares via sq-api-gateway

    # click.echo(Constants.ASCII_VERSION_ART)
    # click.echo("SQ CLI is properly configured")
    # ctx.obj.is_configured = True


@click.command()
def clean():
    """
    Remove all configuration and data locally
    """
    logging.debug(f"Removing {Constants.SQ_CONFIG_DIR}")
    try:
        shutil.rmtree(Constants.SQ_CONFIG_DIR)
    except:
        click.echo(f"Error while deleting directory f{Constants.SQ_CONFIG_DIR}")


@cli.command()
@click.argument('local-file',
                type=click.Path(exists=True),
                )
def upload(local_file):
    """
    Encrypt and Upload a local file to Mount10
    """
    is_valid = validate_config()
    if not is_valid:
        return
    # get client
    client = get_client()
    # encrypt file
    logger.debug(f"Encrypting {local_file}")
    key = client.key
    filename = os.path.split(local_file)[-1]
    encrypted_local_file = f"{local_file}.encrypted"
    Qrypt.encrypt_file(key, local_file, encrypted_local_file)
    # upload file
    logger.debug(f"Uploading {local_file} as {filename}")
    client.mount10.put_object(client.buckets[0], filename, encrypted_local_file)


@cli.command()
@click.argument('remote-file')
def download(remote_file):
    """
    Download a file from Mount10 and save the decrypted copy locally
    """
    is_valid = validate_config()
    if not is_valid:
        return
    client = get_client()

    # download encrypted file
    encrypted_local_file = f"{Constants.SQ_CLIENT_SECURE_DATA_DIR}/{remote_file}.encrypted"
    decrypted_local_file = f"{Constants.SQ_CLIENT_SECURE_DATA_DIR}/{remote_file}"
    logger.debug(f"Downloading encrypted file {remote_file} to {encrypted_local_file}")
    client.mount10.get_object(client.buckets[0], remote_file, encrypted_local_file)

    # decrypt file
    logger.debug(f"Decrypting {encrypted_local_file} to {decrypted_local_file}")
    key = client.key
    Qrypt.decrypt_file(key, encrypted_local_file, decrypted_local_file)


@cli.command()
def ls():
    """
    List remote directory structure
    """
    is_valid = validate_config()
    if not is_valid:
        return
    client = get_client()
    bucket = client.buckets[0]
    objects = client.mount10.list_object(bucket)
    for obj in objects:
        click.echo(f"- filename: {obj.object_name}, size: {obj.size}")


@cli.command()
@click.argument('remote-file')
def delete(remote_file):
    """
    Delete remote file
    """
    is_valid = validate_config()
    if not is_valid:
        return
    client = get_client()
    bucket = client.buckets[0]

    client.mount10.delete_object(bucket, remote_file)


@cli.command()
def cleanup():
    """
    Removes local configuration for SQ CLI
    """
    logger.info(f"Removing {Constants.SQ_CONFIG_DIR}")
    shutil.rmtree(Constants.SQ_CONFIG_DIR)


@cli.group()
def auth():
    """
    Generate Access Token for communicating with SQ API Gateway
    """
    pass


@auth.command()
def fetch_auth_code():
    """
    Generate the Authorization Endpoint URL
    """
    SQAuth.generate_auth_key_url()


@auth.command()
@click.option('--redirect-uri', prompt='Paste your redirection uri here',
              help='The redirection url after running sq auth request-auth-code.')
def fetch_token(redirect_uri):
    """
    Swap auth_code for token
    """
    auth_code = extract_auth_code(redirect_uri)
    SQAuth.fetch_token(auth_code)


@auth.command()
@click.option('--access-token', prompt='Paste your access token here',
              help='The access token after running sq auth fetch-token')
def verify_token(access_token):
    """
    Access Token Vericfication Using API Gateway
    """
    # print(access_token)
    # call sq auth validate function
    SQAuth.verify_token(access_token)


@auth.command()
@click.option('--access-token', prompt='Paste your access token here',
              help='The key after running sq auth get-key')
def get_key(access_token):
    """
    Key Share Generation Using Key Store API Gateway For Active Access Token
    """
    # print(access_token)
    # call sq auth validate function
    KeyManager.recieve_keys(access_token)


@cli.group()
def cqc():
    """
    Adapter for exploring CQC functionality
    """
    pass


@cqc.command()
def test_connection():
    """
    Test Connection to ironbridge api sandbox
    """
    CQCAdapter.testConnection()


@cqc.command()
def get_info():
    """
    Get endpoint info
    """
    CQCAdapter.getInfo()


@cqc.command()
def setup_client():
    """
    Check certificate
    """
    CQCAdapter.setupClient()
