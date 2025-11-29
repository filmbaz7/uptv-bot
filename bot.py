import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8245533941:AAGZR2MPSn38ehCBlvO6VUmWDizmIbIKYAk"

# -----------------------------
# فرمان شروع
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! ربات آماده است ✅\n"
        "برای دیدن 20 فیلم اول، دستور /movies را بزنید."
    )

# -----------------------------
# فرمان نمایش فیلم‌ها
# -----------------------------
async def movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://www.uptvs.com/"  # صفحه اصلی فیلم‌ها
    try:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        
        films = soup.select("a.top-choices-item")[:20]  # 20 فیلم اول
        msg = ""
        for film in films:
            title = film.get("title", "بدون عنوان")
            link = film.get("href", "#")
            msg += f"🎬 {title}\n🔗 {link}\n\n"
        
        await update.message.reply_text(msg or "هیچ فیلمی پیدا نشد.")
    except Exception as e:
        await update.message.reply_text(f"خطا در دریافت فیلم‌ها:\n{e}")

# -----------------------------
# برنامه اصلی
# -----------------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    # اضافه کردن Handlerها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("movies", movies))

    # پورت و URL برای Render
    PORT = int(os.environ.get("PORT", 5000))
    URL = f"https://your-render-service.onrender.com/{TOKEN}"  # <- اینو عوض کن

    print(f"🚀 ربات با Webhook روی {URL} در حال اجراست")

    # اجرای Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=URL
    )
