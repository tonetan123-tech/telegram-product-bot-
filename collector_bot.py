import os
import json
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
PRODUCTS_FILE = "products.json"

def load_products():
    try:
        with open(PRODUCTS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_products(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send a photo with the product name as the caption.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.caption:
        await update.message.reply_text("Please add the product name in the caption.")
        return

    name = update.message.caption.strip()
    photo_file_id = update.message.photo[-1].file_id

    products = load_products()
    products.append({
        "category": "Unknown",
        "caption": name,
        "photo_file_id": photo_file_id
    })
    save_products(products)

    await update.message.reply_text(f"Saved: {name}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()

if __name__ == "__main__":
    main()
