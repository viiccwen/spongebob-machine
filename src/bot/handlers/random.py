"""Handler for random meme command."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from db.user_queries import create_user_query
from meme.selector import select_meme_by_random
from bot.utils import send_meme_selection

logger = logging.getLogger(__name__)


async def random_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /random command for random meme."""
    telegram_user_id = update.effective_user.id if update.effective_user else None

    try:
        user_query_id: int | None = None
        if telegram_user_id:
            user_query = create_user_query(telegram_user_id, query_text=None)
            if user_query:
                user_query_id = user_query.id
        memes = select_meme_by_random("random", count=3)
        await send_meme_selection(
            update,
            memes,
            user_query_id=user_query_id,
            not_found_message="目前沒有可用的梗圖，請稍後再試！",
        )
    except Exception as e:
        logger.error(f"Error in random handler: {e}", exc_info=True)
        await update.message.reply_text("發生錯誤，請稍後再試！")
