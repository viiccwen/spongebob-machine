"""Handler for text messages."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from nlp.intent import analyze_intent_emotion
from meme.selector import select_meme
from bot.keyboards import get_main_keyboard

logger = logging.getLogger(__name__)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages."""
    user_text = update.message.text

    try:
        # Analyze user input for intent and emotion
        analysis = analyze_intent_emotion(user_text)
        logger.info(f"User input: {user_text}, Analysis: {analysis}")

        # Select appropriate meme
        meme_result = select_meme(user_text, analysis)

        if meme_result:
            # Send meme image with caption
            caption = meme_result.get("response_text", "這張給你！")
            image_path = meme_result["file_path"]

            with open(image_path, "rb") as photo:
                await update.message.reply_photo(
                    photo=photo, caption=caption, reply_markup=get_main_keyboard()
                )
        else:
            # Fallback if no meme found
            await update.message.reply_text(
                "找不到適合的梗圖，試試看用按鈕選擇吧！",
                reply_markup=get_main_keyboard(),
            )

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        await update.message.reply_text(
            "發生錯誤，請稍後再試！", reply_markup=get_main_keyboard()
        )
