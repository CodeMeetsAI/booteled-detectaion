"""
Main application entry point.

This module initializes configuration and logging.
Actual camera, inspection, AI, PLC, database, and UI
components will be connected here progressively.
"""

from loguru import logger

from app.config import settings
from app.logging_config import setup_logging


def main() -> None:
    """Start the Pharma Bottle Vision application."""

    setup_logging(
        log_path=settings.log_path,
        log_level=settings.log_level,
    )

    logger.info("Starting {}", settings.app_name)
    logger.info("Environment: {}", settings.app_env)
    logger.info(
        "Target production speed: {} bottles/minute",
        settings.target_bottles_per_minute,
    )

    logger.info("Application foundation initialized.")


if __name__ == "__main__":
    main()