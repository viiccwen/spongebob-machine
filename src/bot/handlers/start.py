"""Handler for /start command."""

from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards import get_main_keyboard


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    welcome_message = (
        "歡迎使用派星機！\n\n"
        "你可以：\n"
        "• 直接輸入你的心情，我會幫你找適合的梗圖\n"
        "• 使用下方按鈕快速選擇\n"
        "• 輸入 /random 隨機獲得一張梗圖"
    )

    await update.message.reply_text(welcome_message, reply_markup=get_main_keyboard())
