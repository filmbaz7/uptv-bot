import requests
from bs4 import BeautifulSoup
import json
from telegram import Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8245533941:AAGZR2MPSn38ehCBlvO6VUmWDizmIbIKYAk"

# ---------------------------
# دانلود HTML
# ---------------------------
def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0)"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print("خطا در دریافت صفحه:", e)
        return None

# ---------------------------
# پردازش فیلم‌ها
# ---------------------------
def parse_movies(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("a.top-choices-item")
    results = []

    for it in items:
        title = it.get_text(strip=True)
        link = it.get("href")
        img_tag = it.find("img")
        image = img_tag.get("src") if img_tag else None

        results.append({
            "title": title,
            "link": link,
            "image": image
        })

    return results


# ---------------------------
# ذخیره JSON
# ---------------------------
def save_json(data, filename="movies.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---------------------------
# فرمان تلگرام: /movies
# ---------------------------
async def movies_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ در حال دریافت فیلم‌ها...")

    url = "https://uptvs.com/category/moviesz"
    html = fetch_html(url)

    if not html:
        await update.message.reply_text("❌ خطا در دریافت صفحه")
        return

    movies = parse_movies(html)
    save_json(movies)

    if not movies:
        await update.message.reply_text("هیچ فیلمی پیدا نشد.")
        return

    for m in movies[:20]:   # فقط ۲۰ فیلم اول
        text = f"🎬 *{m['title']}*\n🔗 {m['link']}"
        if m["image"]:
            await update.message.reply_photo(photo=m["image"], caption=text, parse_mode="Markdown")
        else:
            await update.message.reply_text(text, parse_mode="Markdown")


# ---------------------------
# شروع ربات
# ---------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("movies", movies_command))

    print("ربات اجرا شد...")
    app.run_polling()


if __name__ == "__main__":
    main()
