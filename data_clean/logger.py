import logging

def setup_logger(verbosity: int) -> None:
    logger = logging.getLogger(__name__)
    format = '%(levelname)s-%(message)s'
    print(verbosity)
    if verbosity == 0:
        logging.basicConfig(format=format, level=logging.ERROR)
    elif verbosity == 1:
        logging.basicConfig(format=format, level=logging.INFO)
    elif verbosity == 2:
        logging.basicConfig(format=format, level=logging.INFO)
    elif verbosity == 3:
        logging.basicConfig(format=format, level=logging.DEBUG)
        