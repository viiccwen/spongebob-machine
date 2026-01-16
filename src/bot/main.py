"""Main entry point for the Telegram bot."""

import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from bot.handlers.start import start_handler
from bot.handlers.message import message_handler
from bot.handlers.random import random_handler
from bot.handlers.callback import callback_handler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=(
        logging.INFO if os.getenv("DEBUG", "false").lower() != "true" else logging.DEBUG
    ),
)

# Suppress logs from external packages
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)
logging.getLogger("telegram.ext").setLevel(logging.WARNING)
logging.getLogger("telegram.bot").setLevel(logging.WARNING)
logging.getLogger("telegram.client").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def main():
    """Initialize and start the bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")

    # Create application
    application = Application.builder().token(token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("random", random_handler))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
    )
    application.add_handler(CallbackQueryHandler(callback_handler))

    # Start the bot
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
