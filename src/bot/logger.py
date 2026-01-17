"""Logging configuration for the bot."""

import logging
import os
import sys
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def setup_logging(log_level: Optional[str] = None) -> None:
    # Determine log level
    if log_level:
        level = getattr(logging, log_level.upper(), logging.INFO)
    else:
        # Production: WARNING, Development: DEBUG
        is_debug = os.getenv("DEBUG", "false").lower() == "true"
        level = logging.DEBUG if is_debug else logging.WARNING

    # Configure root logger
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=level,
        stream=sys.stdout,
    )

    # Suppress logs from external packages (always WARNING or above)
    external_loggers = [
        "asyncio",
        "httpcore",
        "httpx",
        "telegram",
        "telegram.ext",
        "telegram.bot",
        "telegram.client",
        "urllib3",
        "boto3",
        "botocore",
        "sqlalchemy.engine",
        "sqlalchemy.pool",
    ]

    for logger_name in external_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    # Log the configuration
    logger = logging.getLogger(__name__)
    env_name = "development" if level == logging.DEBUG else "production"
    logger.info(
        f"Logging configured for {env_name} environment (level: {logging.getLevelName(level)})"
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
