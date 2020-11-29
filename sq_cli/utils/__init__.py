import logging

import sq_cli

class APIFilter(logging.Filter):
    """
    Filters API log level messages
    """
    def filter(self, record):
        return record.levelno == logging.API


def config_root_logger(verbosity, mode):
    """
    Configure application logger based on verbosity level received from CLI
    Verbosity values of 0, 1, 2 correspond to log level of Warning, Info, Debug respectively
    :param verbosity: integer: 0, 1, 2
    """
    root_logger = logging.getLogger(sq_cli.__name__)
    console_handler = logging.StreamHandler()
    api_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt='%d/%m/%Y %I:%M:%S %p')
    console_handler.setFormatter(formatter)

    if mode == 'standalone':
        if verbosity == 0:
            root_logger.setLevel(logging.WARNING)
        elif verbosity == 1:
            root_logger.setLevel(logging.INFO)
        elif verbosity >= 2:
            root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(console_handler)
    elif mode == 'api':
        root_logger.setLevel(logging.API)
        api_handler.addFilter(APIFilter())
        root_logger.addHandler(api_handler)
