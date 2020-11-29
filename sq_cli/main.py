import sys

import click

from sq_cli.__version__ import __version__
import logging

from sq_cli.utils import config_root_logger

logger = logging.getLogger(__name__)


class Session:
    def __init__(self):
        self.config = {}
        self.verbose = False
        self.ascii_art = f"""
        
  / ____|                                   / __ \                  | |                  
 | (___  _   _ _ __   ___ _ __ __ _ _   _  | |  | |_   _  __ _ _ __ | |_ _   _ _ __ ___  
  \___ \| | | | '_ \ / _ \ '__/ _` | | | | | |  | | | | |/ _` | '_ \| __| | | | '_ ` _ \ 
  ____) | |_| | | | |  __/ | | (_| | |_| | | |__| | |_| | (_| | | | | |_| |_| | | | | | |
 |_____/ \__, |_| |_|\___|_|  \__, |\__, |  \___\_\\__,_|\__,_|_| |_|\__|\__,_|_| |_| |_|
          __/ |                __/ | __/ |                                               
         |___/                |___/ |___/                                                

                                                                  version: {__version__}
    """

    def set_config(self, key, value):
        self.config[key] = value
        if self.verbose:
            logger.debug('  config[%s] = %s' % (key, value), file=sys.stderr)


pass_session = click.make_pass_decorator(Session)


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
    print(ctx.obj.ascii_art)


@cli.command()
def upload():
    pass


@cli.command()
def download():
    pass


@cli.command()
def encrypt():
    pass


@cli.command()
def decrypt():
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
