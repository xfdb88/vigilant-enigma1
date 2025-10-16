import logging
import os
import sys
from typing import Optional

def init_logger(name: str = "igscraper", level: Optional[str] = None) -> logging.Logger:
    lvl = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
    logger = logging.getLogger(name)
    logger.setLevel(lvl)
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        handler = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    logger.propagate = False
    return logger
