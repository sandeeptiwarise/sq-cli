import sys

import click

from sq_cli.__version__ import __version__
import logging

logger = logging.getLogger(__name__)


class Session:
    def __init__(self):
        self.config = {}
        self.verbose = False

    def set_config(self, key, value):
        self.config[key] = value
        if self.verbose:
            logger.debug('  config[%s] = %s' % (key, value), file=sys.stderr)


pass_session = click.make_pass_decorator(Session)


@click.group()
@click.version_option(__version__)
@click.pass_context
def cli(ctx):
    ctx.obj = Session()


@cli.command()
def config():
    pass


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
