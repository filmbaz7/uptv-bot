# bot.py
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8245533941:AAGZR2MPSn38ehCBlvO6VUmWDizmIbIKYAk"
PORT = int(os.environ.get("PORT", 8443))
WEBHOOK_URL = f"https://uptv-bot-1.onrender.com/{TOKEN}"

# ------------------------------
# Handlers
# ------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات شما آماده است 🚀")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("دستورات موجود:\n/start\n/help")

# ------------------------------
# Main
# ------------------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Start webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=WEBHOOK_URL
    )
