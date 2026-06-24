import os
import random
import json
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
YOUR_USER_ID = int(os.getenv("YOUR_USER_ID"))
PRODUCTS_FILE = "products.json"

def load_products():
    try:
        with open(PRODUCTS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def main():
    bot = Bot(token=BOT_TOKEN)
    products = load_products()

    if len(products) < 2:
        bot.send_message(chat_id=YOUR_USER_ID, text="Need at least 2 products saved.")
        return

    selected = random.sample(products, 2)

    for p in selected:
        bot.send_photo(
            chat_id=YOUR_USER_ID,
            photo=p["photo_file_id"],
            caption=p["caption"]
        )

if __name__ == "__main__":
    main()
