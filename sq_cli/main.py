import shutil
import sys

import click
import logging
import os

from sq_cli.qrypt import Qrypt
from sq_cli.utils import config_root_logger, generate_configuration_template, get_client
from sq_cli.utils.constants import Constants

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
def config(ctx):
    """
    Configure Synergy Quantum CLI
    """
    # check if SQ_CONFIG_DIR exists, create if not
    if os.path.exists(Constants.SQ_CONFIG_DIR):
        logger.debug(f"SQ configuration directory exists: {Constants.SQ_CONFIG_DIR}")
    else:
        logger.debug(f"SQ configuration directory NOT FOUND: {Constants.SQ_CONFIG_DIR}")
        logger.debug(f"Creating SQ configuration directory: {Constants.SQ_CONFIG_DIR}")
        os.mkdir(Constants.SQ_CONFIG_DIR)

    # check if user's key exists, generate new one otherwise
    if os.path.exists(Constants.SQ_CLIENT_KEY):
        logger.debug(f"SQ Key found: {Constants.SQ_CONFIG_DIR}")
    else:
        logger.debug(f"Generating new SQ Key and saving to {Constants.SQ_CONFIG_DIR}")
        key = Qrypt.generate_key()
        Qrypt.save_key(key, Constants.SQ_CLIENT_KEY)

    # check if client config file exists, generate template otherwise
    if os.path.exists(Constants.SQ_CONFIG_FILE):
        logger.debug(f"Found Mount10 Configuration in the config file: {Constants.SQ_CONFIG_DIR}")
    else:
        logger.debug(f"Mount10 Configuration Not FOUND: {Constants.SQ_CONFIG_DIR}")
        generate_configuration_template()
        click.echo(f"Generated template of Mount10 configuration file {Constants.SQ_CONFIG_FILE}")
        click.echo("Please fill out the configuration pararmeters in the template")
        return
    click.echo(Constants.ASCII_VERSION_ART)
    click.echo("SQ CLI is properly configured")
    ctx.obj.is_configured = True


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
    :return:
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
    :return:
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


# @cli.command()
# @click.pass_context
# def encrypt(ctx):
#     is_valid = validate_config()
#     if not is_valid:
#         return
#
#
# @cli.command()
# @click.pass_context
# def decrypt(ctx):
#     is_valid = validate_config()
#     if not is_valid:
#         return


# if __name__ == '__main__':
#     client_michal = SQlient("michal", "3.121.232.99:9000", "minioadmin", "minioadmin")
#     #TODO do the enc while uploading
#     client_michal.qrypt.encrypt_file("data/file1.txt")
#
#     client_michal.mount10.put_object(client_michal.buckets[0], "file1", "data/file1.txt")
#     client_michal.mount10.get_object(client_michal.buckets[0], "file1", "data/file2")
#
#     client_michal.qrypt.decrypt_file("data/file2")
#     print("*******************")
#     data = client_michal.qrypt.decrypt_file("data/file1.txt")
#     print(open("data/file2").read().encode())
#     assert data == open("data/file2").read().encode()
#


"""
-> Clean up interfaces 
-> decouple encryption decryption and agree on expose hooks
-> 
"""
