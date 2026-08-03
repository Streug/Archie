"""
This module provides uniform logging for all Foto modules.
"""

import logging
from logging.handlers import RotatingFileHandler


def setup_logging(lvl, file, fmt, mb, bu):  # ? mb en bu?????????
    logger = logging.getLogger()
    if logger.handlers:
        return logger
    logger.setLevel(lvl)
    handler = RotatingFileHandler(file)
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    return logger


# VOORBEELD GEBRUIK: logging.info("Start Section 2 *********")
