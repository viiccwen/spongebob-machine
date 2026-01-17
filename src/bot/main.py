"""Main entry point for the Telegram bot."""

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
from bot.logger import get_logger, setup_logging

# Load environment variables
load_dotenv()

# Setup logging (must be called before importing other modules that use logging)
setup_logging()

logger = get_logger(__name__)


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
