"""
Deze code zorgt voor een uniforme logging voor alle Foto modules.
Voorbeeld: logging.info("Start Section 2 *********")
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(lvl, file, fmt, mb, bu):
    logger = logging.getLogger()

    if logger.handlers:
        return logger

    logger.setLevel(lvl)

    logpad = Path(file)
    logpad.parent.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        logpad,
        maxBytes=mb,
        backupCount=bu,
        encoding="utf-8",
    )

    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)

    return logger
