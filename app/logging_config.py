"""
Centralized logging configuration.

The production system will use logging for:
- application events
- camera events
- inspection errors
- PLC communication
- system faults
- performance monitoring
"""

import logging
import sys
from pathlib import Path

from loguru import logger


def setup_logging(log_path: str, log_level: str = "INFO") -> None:
    """
    Configure application logging.

    Logs are written both to the console and to a rotating file.
    """

    Path(log_path).mkdir(parents=True, exist_ok=True)

    logger.remove()

    logger.add(
        sys.stderr,
        level=log_level,
        enqueue=True,
        backtrace=True,
        diagnose=False,
    )

    logger.add(
        Path(log_path) / "pharma_vision.log",
        level=log_level,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        enqueue=True,
        backtrace=True,
        diagnose=False,
    )

    logging.basicConfig(
        handlers=[InterceptHandler()],
        level=0,
    )


class InterceptHandler(logging.Handler):
    """Forward standard Python logging into Loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        level = logger.level(record.levelname).name

        logger.opt(
            exception=record.exc_info,
            depth=6,
        ).log(level, record.getMessage())