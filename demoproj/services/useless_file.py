import logging

logger = logging.getLogger(__name__)


def useless_function(id_: str = None) -> bool:
    """
    Useless function to demonstrate a function log message.
    :return: True
    """
    logger.warning('Some warning in a function %s', id_)
    return True
