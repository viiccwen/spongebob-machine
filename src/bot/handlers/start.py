"""Handler for /start command."""

from telegram import Update
from telegram.ext import ContextTypes


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    welcome_message = (
        "歡迎使用派星機！\n\n"
        "你可以：\n"
        "• 直接輸入你的心情，我會幫你找適合的梗圖\n"
        "• 輸入 /random 隨機獲得一張梗圖"
    )

    await update.message.reply_text(welcome_message)
