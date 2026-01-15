"""Handler for callback queries from inline keyboards."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from meme.selector import select_meme_by_intent
from bot.keyboards import get_main_keyboard

logger = logging.getLogger(__name__)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline buttons."""
    query = update.callback_query
    await query.answer()

    intent = query.data  # e.g., "tired", "angry", "happy", "random"

    try:
        # Select meme by intent (direct mapping, no NLP needed)
        meme_result = select_meme_by_intent(intent)

        if meme_result:
            caption = meme_result.get("response_text", "這張給你！")
            image_path = meme_result["file_path"]

            with open(image_path, "rb") as photo:
                await query.message.reply_photo(
                    photo=photo, caption=caption, reply_markup=get_main_keyboard()
                )
        else:
            await query.message.reply_text(
                f"找不到 {intent} 相關的梗圖，試試看其他選項吧！",
                reply_markup=get_main_keyboard(),
            )

    except Exception as e:
        logger.error(f"Error processing callback: {e}", exc_info=True)
        await query.message.reply_text(
            "發生錯誤，請稍後再試！", reply_markup=get_main_keyboard()
        )
