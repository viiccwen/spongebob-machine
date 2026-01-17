"""Handler for callback queries (button clicks)."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from db.user_queries import update_user_query_selection
from bot.utils import send_selected_meme

logger = logging.getLogger(__name__)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline keyboard buttons."""
    query = update.callback_query

    if not query or not query.data:
        return

    try:
        # Parse callback data: "select_meme:{meme_id}" or "select_meme:{meme_id}:{user_query_id}"
        if query.data.startswith("select_meme:"):
            parts = query.data.split(":", 2)
            meme_id = parts[1]
            user_query_id = int(parts[2]) if len(parts) > 2 else None

            telegram_user_id = (
                update.effective_user.id if update.effective_user else None
            )
            if telegram_user_id:
                update_user_query_selection(
                    telegram_user_id, meme_id, user_query_id=user_query_id
                )
            await send_selected_meme(update, meme_id)
        else:
            logger.warning(f"Unknown callback data: {query.data}")
            await query.answer("未知的操作", show_alert=True)
    except Exception as e:
        logger.error(f"Error handling callback: {e}", exc_info=True)
        await query.answer("發生錯誤，請稍後再試！", show_alert=True)
