from telegram.ext import Application, CommandHandler, MessageHandler, Filters
import random
import json
import schedule
from telegram import Bot

# Replace these with your values:
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
YOUR_USER_ID = 123456789
CHANNEL_ID = "@yourproductslisting"

# File to store product list
PRODUCTS_FILE = "products.json"

# Initialize bot
bot = Bot(token=BOT_TOKEN)

def load_products():
    try:
        with open(PRODUCTS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

async def save_product_command(update, context):
    product_name = context.args[0] if context.args else "Unknown"
    
    if update.message and update.message.photo:
        photo_file_id = update.message.photo[-1].file_id
        caption = update.message.caption or ""
        
        products = load_products()
        products.append({
            "name": product_name,
            "photo_file_id": photo_file_id,
            "caption": caption
        })
        
        with open(PRODUCTS_FILE, "w") as f:
            json.dump(products, f)
        
        await update.message.reply_text(f"✅ Saved: {product_name}")
    
    else:
        await update.message.reply_text("❌ Please attach a picture!")

def send_random_2():
    products = load_products()
    
    if len(products) < 2:
        bot.send_message(
            chat_id=YOUR_USER_ID,
            text="❌ You need at least 2 products saved! Use /addproduct to add more."
        )
        return
    
    selected = random.sample(products, 2)
    
    for product in selected:
        formatted_caption = f"""
🛒 **{product['name']}**

{product['caption']}

━━━━━━━━━━━━━━━━
📩 Vet & forward to target channel
"""
        
        bot.send_photo(
            chat_id=YOUR_USER_ID,
            photo=product['photo_file_id'],
            caption=formatted_caption
        )

async def daily_pick(update, context):
    send_random_2()

schedule.every().day.at("10:00").do(send_random_2)
schedule.every().day.at("18:00").do(send_random_2)

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("addproduct", save_product_command))
app.add_handler(CommandHandler("daily-pick", daily_pick))
app.run_polling()
