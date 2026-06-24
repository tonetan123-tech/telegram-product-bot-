import os
import random
import json
from telegram import Bot
from telegram.ext import Application, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
YOUR_USER_ID = int(os.getenv("YOUR_USER_ID"))
PRODUCTS_FILE = "products.json"

bot = Bot(token=BOT_TOKEN)

def load_products():
    try:
        with open(PRODUCTS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_products(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f)

def addproduct(update, context):
    if not update.message.photo:
        update.message.reply_text("Please send a photo with the caption.")
        return

    caption = update.message.caption or "No caption"
    photo_file_id = update.message.photo[-1].file_id

    products = load_products()
    products.append({
        "caption": caption,
        "photo_file_id": photo_file_id
    })
    save_products(products)

    update.message.reply_text("Saved.")

def pick(update, context):
    products = load_products()
    if len(products) < 2:
        update.message.reply_text("Need at least 2 products saved.")
        return

    selected = random.sample(products, 2)
    for p in selected:
        bot.send_photo(
            chat_id=YOUR_USER_ID,
            photo=p["photo_file_id"],
            caption=p["caption"]
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("addproduct", addproduct))
    app.add_handler(CommandHandler("pick", pick))
    app.run_polling()

if __name__ == "__main__":
    main()
