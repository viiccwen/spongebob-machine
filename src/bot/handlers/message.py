"""Handler for text messages."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from meme.selector import select_meme
from bot.utils import send_meme_selection

logger = logging.getLogger(__name__)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages."""
    user_text = update.message.text

    try:
        logger.info(f"User input: {user_text}")
        memes = select_meme(user_text, count=3)
        await send_meme_selection(
            update, memes, not_found_message="找不到適合的梗圖，請再試試看！"
        )
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        await update.message.reply_text("發生錯誤，請稍後再試！")
