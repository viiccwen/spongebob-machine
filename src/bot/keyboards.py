"""Inline keyboard definitions for the bot."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_keyboard():
    """Get the main inline keyboard with emotion/intent buttons."""
    keyboard = [
        [
            InlineKeyboardButton("😫 好累", callback_data="tired"),
            InlineKeyboardButton("😡 生氣", callback_data="angry"),
        ],
        [
            InlineKeyboardButton("😆 爽啦", callback_data="happy"),
            InlineKeyboardButton("😢 難過", callback_data="sad"),
        ],
        [
            InlineKeyboardButton("🤪 瘋了", callback_data="crazy"),
            InlineKeyboardButton("🎲 隨機", callback_data="random"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
