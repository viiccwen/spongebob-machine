"""Handler for random meme command."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from meme.selector import select_meme_by_intent
from bot.keyboards import get_main_keyboard

logger = logging.getLogger(__name__)


async def random_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /random command for random meme."""
    try:
        meme_result = select_meme_by_intent("random")

        if meme_result:
            caption = meme_result.get("response_text", "這張給你！")
            image_path = meme_result["file_path"]

            with open(image_path, "rb") as photo:
                await update.message.reply_photo(
                    photo=photo, caption=caption, reply_markup=get_main_keyboard()
                )
        else:
            await update.message.reply_text(
                "目前沒有可用的梗圖，請稍後再試！", reply_markup=get_main_keyboard()
            )
    except Exception as e:
        logger.error(f"Error in random handler: {e}", exc_info=True)
        await update.message.reply_text(
            "發生錯誤，請稍後再試！", reply_markup=get_main_keyboard()
        )
