import logging
import logging.config
import sys

from src.env import ENV

logging.config.dictConfig(dict(version=1, disable_existing_loggers=True))


def getLogger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    logger = logging.getLogger(name)
    logger.setLevel(ENV().LOG_LEVEL)
    stream_handler = logging.StreamHandler(sys.stdout)
    log_formatter = logging.Formatter("%(levelname)s :: %(name)s :: %(message)s")
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)
    return logger
