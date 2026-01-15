"""Handler for random meme command."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from meme.selector import select_meme_by_random
from bot.utils import get_image_from_r2

logger = logging.getLogger(__name__)


async def random_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /random command for random meme."""
    try:
        meme_result = select_meme_by_random("random")

        if meme_result:
            caption = meme_result.get("response_text", "這張給你！")
            meme = meme_result.get("meme", {})
            meme_id = meme.get("meme_id", "")

            if meme_id:
                # Get image from R2
                image_data = await get_image_from_r2(meme_id)
                if image_data:
                    image_data.seek(0)  # Reset file pointer
                    await update.message.reply_photo(
                        photo=image_data,
                        caption=caption,
                    )
                else:
                    logger.warning(
                        f"Failed to get image from R2 for meme_id: {meme_id}"
                    )
                    await update.message.reply_text("找不到圖片，請稍後再試！")
            else:
                logger.warning("No meme_id found in meme result")
                await update.message.reply_text("找不到圖片，請稍後再試！")
        else:
            await update.message.reply_text("目前沒有可用的梗圖，請稍後再試！")
    except Exception as e:
        logger.error(f"Error in random handler: {e}", exc_info=True)
        await update.message.reply_text("發生錯誤，請稍後再試！")
